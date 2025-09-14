# LLMxMapReduce V1版本的主要处理流水线
# 实现了基于MapReduce思想的长文档处理框架
from Generator import Generator


class BasePipeline:
    """
    基础处理流水线类
    
    该类实现了LLMxMapReduce-V1的核心处理逻辑，采用分治策略处理长文档：
    1. Map阶段：将长文档分块并行处理
    2. Collapse阶段：合并中间结果
    3. Reduce阶段：生成最终答案
    
    Args:
        config: 配置字典，包含模型参数和提示词模板
        print_intermediate_path: 中间结果输出路径（可选）
        doc_id: 文档ID标识符（可选）
    """
    def __init__(self, config, print_intermediate_path=None, doc_id=None):
        # 初始化生成器，负责具体的文本处理和模型调用
        self.generator = Generator(
            config, print_intermediate_path=print_intermediate_path, doc_id=doc_id)
        
    def remove_chunk(self, chunks: list, irrelevant_note=['[NOT MENTIONED]'], question=''):
        """
        移除不相关的文档块
        
        该方法用于过滤掉不包含有用信息的文档块，提高处理效率和结果质量。
        
        Args:
            chunks: 文档块列表
            irrelevant_note: 标识不相关信息的标记列表
            question: 查询问题
            
        Returns:
            list: 过滤后的文档块列表
        """
        # 移除chunks中对应索引的元素
        new_chunks = []
        
        # 如果问题本身就提到了不相关标记，直接返回原chunks
        for q in question:
            for note in irrelevant_note:
                if note.upper() in q.upper():
                    return chunks

        # 过滤掉包含不相关标记的文档块
        for chunk in chunks:
            flag = False
            for note in irrelevant_note:
                if note.upper() in chunk.upper():
                    flag = True
                    break
            if not flag:
                new_chunks.append(chunk)
        
        # 如果过滤后为空，返回原chunks
        if len(new_chunks) == 0:
            return chunks
        return new_chunks

    def process(self, document, question):
        """
        处理文档并回答问题
        
        实现完整的MapReduce流程：
        1. 将文档分块
        2. 对每个块执行Map操作
        3. 合并中间结果
        4. 执行Reduce操作生成最终答案
        
        Args:
            document: 输入文档内容
            question: 查询问题
            
        Returns:
            str: 生成的回答
        """
        # 执行MapReduce流程
        chunks = self.generator.split_document(document)
        map_results = self.generator.map_chunks(chunks, question)
        map_results = self.remove_chunk(map_results, question=question)
        reduce_result = self.generator.reduce(map_results, question)
        return reduce_result