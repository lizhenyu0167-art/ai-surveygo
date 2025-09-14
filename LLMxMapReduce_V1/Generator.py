# LLMxMapReduce V1核心生成器类
# 负责文本处理、模型调用和MapReduce各阶段实现
import os
import json
import time
import asyncio
import aiohttp
import tiktoken
import requests
import numpy as np
from tqdm import tqdm
from openai import OpenAI
from typing import List, Dict, Any, Optional, Union
from transformers import AutoTokenizer


class Generator:
    """
    LLMxMapReduce的核心生成器类
    
    该类负责实现MapReduce框架的各个阶段，包括：
    - 文档分块
    - Map阶段并行处理
    - 中间结果合并
    - Reduce阶段生成最终答案
    
    同时支持OpenAI API和本地部署模型两种调用方式
    
    Args:
        config: 配置字典，包含模型参数、提示词模板等
        print_intermediate_path: 中间结果输出路径
        doc_id: 文档标识符
    """
    def __init__(self, config, print_intermediate_path=None, doc_id=None):
        """
        初始化生成器
        
        Args:
            config: 配置字典
            print_intermediate_path: 中间结果输出路径
            doc_id: 文档标识符
        """
        # 获取Map阶段的提示词模板
        self.first_prompt = config['map_prompt']
        # 获取生成参数（温度、最大token等）
        self.gen_args = config.get('gen_args', {})
        
        self.config = config
        # 最大并行工作数量
        self.max_work_count = config.get('max_work_count', 4)
        
        # 判断是否使用OpenAI API
        self.use_openai_api = config.get('use_openai_api', False)
        if self.use_openai_api:
            # 配置OpenAI API相关参数
            self.openai_key = config.get('openai_api', {}).get('api_key', None)
            self.openai_base_url = config.get('openai_api', {}).get(
                'base_url', 'https://api.openai.com/v1')
            self.openai_client = OpenAI(
                api_key=self.openai_key, base_url=self.openai_base_url)
            self.openai_model = config.get('openai_api', {}).get('model', 'text-davinci-003')
            
            # 判断是否为vLLM服务器
            self.is_vllm_sever = config.get('openai_api', {}).get('is_vllm_sever', False)
            if self.is_vllm_sever:
                # 使用HuggingFace分词器
                self.tokenizer = AutoTokenizer.from_pretrained(
                    config['openai_api']['name_or_path'])
            else:
                # 使用tiktoken分词器
                self.tokenizer = tiktoken.encoding_for_model(self.openai_model)
        else:
            # 使用本地部署的模型
            self.url = config.get('llm', {}).get('url', 'http://localhost:5002/infer')
            self.tokenizer = AutoTokenizer.from_pretrained(
            config['llm']['name_or_path'])
        
        # 中间结果输出相关配置
        self.print_intermediate_path = print_intermediate_path
        self.doc_id = doc_id

    def build_message(self, prompt, input_dict):
        """
        构建聊天消息格式
        
        将提示词和输入参数格式化为模型可接受的消息格式
        
        Args:
            prompt: 提示词模板
            input_dict: 输入参数字典
            
        Returns:
            str: 格式化后的消息字符串
        """
        message = [{'role': 'user', 'content': prompt.format(**input_dict)}]
        message_str = self.tokenizer.apply_chat_template(
            conversation=message, tokenize=False, add_generation_prompt=True)
        return message_str

    def split_list_to_chunks(self, lst: list, chunk_num):
        """
        将列表分割成指定数量的块
        
        用于并行处理时将任务列表分配给多个工作进程
        
        Args:
            lst: 待分割的列表
            chunk_num: 分割块数
            
        Returns:
            list: 分割后的块列表
        """
        length = len(lst)
        if len(lst) <= chunk_num:
            return lst

        chunk_size = length // chunk_num
        result = [lst[i * chunk_size:(i + 1) * chunk_size]
                  for i in range(chunk_num - 1)]
        # 最后一块包含所有剩余元素
        result.append(lst[(chunk_num - 1) * chunk_size:])
        assert len(result) == chunk_num
        assert sum([len(i) for i in result]) == length
        return result

    def mr_map(self, context: list[str], question) -> list[str]:
        """
        MapReduce的Map阶段实现
        
        并行处理所有文档块，从每个块中提取与问题相关的信息
        
        Args:
            context: 文档块列表
            question: 查询问题
            
        Returns:
            list[str]: Map阶段的处理结果列表
        """
        prompt = self.config['map_prompt']