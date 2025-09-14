# LLMxMapReduce V1版本的核心生成器类
# 负责具体的文本处理、模型调用和MapReduce各阶段的实现

from calendar import c
import copy
from pyexpat import model
from typing import List, Optional, Tuple, Any
import json
from unittest import result
from openai import OpenAI
import tiktoken
from vllm import SamplingParams
from transformers import AutoTokenizer

import os
import re
import random
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential, stop_after_delay,
)
from utils import get_openai_batch_reply, print_intermediate_output, run_thread_pool_sub, split_list_of_docs, thread_function


class Generator:
    """
    LLMxMapReduce的核心生成器类
    
    该类负责实现MapReduce框架的所有核心功能：
    - 文档分块和预处理
    - Map阶段的并行处理
    - Collapse阶段的层次化合并
    - Reduce阶段的最终归约
    - 支持多种LLM后端（OpenAI API、本地部署等）
    """
    def __init__(
        self,
        config: dict, 
        tokenizer=None,
        print_intermediate_path=None,
        doc_id=None
    ):
        """
        初始化生成器
        
        Args:
            config: 配置字典，包含模型设置、提示词模板等
            tokenizer: 分词器（可选）
            print_intermediate_path: 中间结果保存路径
            doc_id: 文档ID
        """
        self.config = config
        self.print_intermediate_path = print_intermediate_path
        self.doc_id = doc_id
        
        # 设置模型和分词器
        self.model_name = config.get("model_name", "gpt-3.5-turbo")
        self.tokenizer = tokenizer
        if self.tokenizer is None:
            if "gpt" in self.model_name:
                self.tokenizer = tiktoken.encoding_for_model(self.model_name)
            else:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # 设置API类型和端点
        self.api_type = config.get("api_type", "openai")
        self.api_base = config.get("api_base", None)
        self.api_key = config.get("api_key", None)
        
        # 设置生成参数
        self.temperature = config.get("temperature", 0.0)
        self.max_tokens = config.get("max_tokens", 4096)
        self.top_p = config.get("top_p", 1.0)
        
        # 设置MapReduce参数
        self.chunk_size = config.get("chunk_size", 4000)
        self.chunk_overlap = config.get("chunk_overlap", 0)
        self.max_chunks = config.get("max_chunks", 20)
        
        # 设置提示词模板
        self.system_prompt = config.get("system_prompt", "")
        self.map_prompt = config.get("map_prompt", "")
        self.reduce_prompt = config.get("reduce_prompt", "")
        
        # 初始化客户端
        if self.api_type == "openai":
            self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)
        
        # 设置并行处理参数
        self.parallel = config.get("parallel", True)
        self.max_workers = config.get("max_workers", 10)