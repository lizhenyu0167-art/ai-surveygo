# -*- coding: utf-8 -*-
"""
LLMxMapReduce V2 主流水线启动模块

该模块实现了LLMxMapReduce V2版本的完整流水线系统，包括：
- 编码流水线（EncodePipeline）：数据预处理和结构化
- 隐藏流水线（HiddenPipeline）：核心信息提取和处理
- 解码流水线（DecodePipeline）：结果生成和输出
- 自动网络检索和爬取功能
- 流水线监控和分析

作者：AI9STARS, OpenBMB, THUNLP
"""

import os
import json
import logging
import gevent
from args import parse_args
import asyncio
from datetime import datetime

from async_d import Monitor, PipelineAnalyser
from async_d import Pipeline
from src.decode.decode_pipeline import DecodePipeline
from src.encode.encode_pipeline import EncodePipeline
from src.hidden.hidden_pipeline import HiddenPipeline
from src.LLM_search import LLM_search
from src.async_crawl import AsyncCrawler

logger = logging.getLogger(__name__)


class EntirePipeline(Pipeline):
    """
    完整的LLMxMapReduce V2流水线系统
    
    该类整合了编码、隐藏和解码三个子流水线，实现端到端的长文本处理。
    相比V1版本，V2采用了更加模块化的设计，支持异步处理和实时监控。
    
    主要特性：
    - 三阶段流水线架构：Encode -> Hidden -> Decode
    - 异步并发处理，提高处理效率
    - 实时监控和分析功能
    - 支持多种输入格式和输出选项
    - 集成网络检索和内容爬取
    
    Attributes:
        encode_pipeline: 编码流水线，负责数据预处理
        hidden_pipeline: 隐藏流水线，负责核心信息处理
        decode_pipeline: 解码流水线，负责结果生成
        monitor: 流水线监控器
        analyser: 流水线分析器
    """
    def __init__(self, args):
        """
        初始化完整流水线
        
        Args:
            args: 命令行参数对象
        """
        super().__init__()
        self.args = args
        
        # 创建三个子流水线
        self.encode_pipeline = EncodePipeline(args)
        self.hidden_pipeline = HiddenPipeline(args)
        self.decode_pipeline = DecodePipeline(args)
        
        # 连接流水线
        self.encode_pipeline.connect(self.hidden_pipeline)
        self.hidden_pipeline.connect(self.decode_pipeline)
        
        # 设置监控和分析器
        self.monitor = Monitor()
        self.analyser = PipelineAnalyser()
        
        # 注册流水线到监控器
        self.monitor.register(self.encode_pipeline)
        self.monitor.register(self.hidden_pipeline)
        self.monitor.register(self.decode_pipeline)
        
        # 设置分析器
        self.analyser.set_pipeline(self)
        
    async def run(self, input_data, question):
        """
        运行完整流水线
        
        Args:
            input_data: 输入数据（文档内容）
            question: 查询问题
            
        Returns:
            dict: 包含处理结果和分析信息的字典
        """
        # 启动监控器
        self.monitor.start()
        
        # 准备输入数据
        input_dict = {
            'document': input_data,
            'question': question
        }
        
        # 启动流水线处理
        start_time = datetime.now()
        result = await self.encode_pipeline.process(input_dict)
        end_time = datetime.now()
        
        # 停止监控器
        self.monitor.stop()
        
        # 获取分析结果
        analysis = self.analyser.analyse()
        
        # 构建返回结果
        output = {
            'result': result,
            'analysis': analysis,
            'time_cost': (end_time - start_time).total_seconds()
        }
        
        return output


async def process_document(args, document, question):
    """
    处理文档并回答问题
    
    Args:
        args: 命令行参数对象
        document: 文档内容
        question: 查询问题
        
    Returns:
        dict: 处理结果
    """
    # 创建并运行流水线
    pipeline = EntirePipeline(args)
    result = await pipeline.run(document, question)
    return result


async def process_url(args, url, question):
    """
    处理URL指向的内容并回答问题
    
    Args:
        args: 命令行参数对象
        url: 目标URL
        question: 查询问题
        
    Returns:
        dict: 处理结果
    """
    # 创建爬虫并获取内容
    crawler = AsyncCrawler()
    content = await crawler.crawl(url)
    
    # 处理获取的内容
    return await process_document(args, content, question)


async def process_search(args, query, question):
    """
    基于搜索结果回答问题
    
    Args:
        args: 命令行参数对象
        query: 搜索查询
        question: 查询问题
        
    Returns:
        dict: 处理结果
    """
    # 执行搜索
    searcher = LLM_search(args)
    search_results = await searcher.search(query)
    
    # 处理搜索结果
    return await process_document(args, search_results, question)


async def main():
    """
    主函数，处理命令行参数并启动相应的处理流程
    """
    # 解析命令行参数
    args = parse_args()
    
    # 根据输入类型选择处理方式
    if args.input_type == 'document':
        # 读取文档内容
        with open(args.input_path, 'r', encoding='utf-8') as f:
            document = f.read()
        result = await process_document(args, document, args.question)
    
    elif args.input_type == 'url':
        result = await process_url(args, args.input_path, args.question)
    
    elif args.input_type == 'search':
        result = await process_search(args, args.input_path, args.question)
    
    else:
        raise ValueError(f"不支持的输入类型: {args.input_type}")
    
    # 输出结果
    if args.output_path:
        with open(args.output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    # 设置日志级别
    logging.basicConfig(level=logging.INFO)
    
    # 运行主函数
    asyncio.run(main())