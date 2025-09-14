# LLMxMapReduce: 使用大语言模型简化长序列处理

<a href='https://surveygo.modelbest.cn/'><img src='https://img.shields.io/badge/Demo-Page-pink'></a> <a href='https://arxiv.org/abs/2410.09342'><img src='https://img.shields.io/badge/V1-Paper-Green'></a> <a href='https://arxiv.org/abs/2504.05732'><img src='https://img.shields.io/badge/V2-Paper-blue'></a> <a href='https://huggingface.co/datasets/R0k1e/SurveyEval'><img src='https://img.shields.io/badge/SurveyEval-Benchmark-yellow'></a> <a href='README.md'><img src='https://img.shields.io/badge/English-Readme-red'></a>

# 🎉 新闻
- [x] **`2025.04.22`** 发布 [SurveyGO](https://surveygo.modelbest.cn/)，一个由 LLMxMapReduce-V2 驱动的在线写作系统。
- [x] **`2025.04.09`** 在 [arXiv](https://arxiv.org/abs/2504.05732) 上发布 LLMxMapReduce-V2 论文。
- [x] **`2025.02.21`** 添加对 OpenAI API 和 OpenAI 兼容 API（例如 vLLM）的支持。
- [x] **`2024.10.12`** 在 [arXiv](https://arxiv.org/abs/2410.09342) 上发布 LLMxMapReduce-V1 论文。
- [x] **`2024.09.12`** 发布 LLMxMapReduce-V1 的代码。

# 📚 概述
**LLMxMapReduce** 是一个分而治之的框架，旨在增强现代大型语言模型（LLMs）理解和生成长序列的能力。该框架由 **AI9STARS**、**OpenBMB** 和 **THUNLP** 合作开发，灵感来源于大数据领域的经典 MapReduce 算法。我们的目标是构建一个由 LLM 驱动的分布式计算系统，能够高效处理长序列。以下是 LLMxMapReduce 的主要版本：

* [**LLMxMapReduce-V1**](https://github.com/thunlp/LLMxMapReduce/blob/main/LLMxMapReduce_V1)：利用结构化信息协议和上下文置信度校准来增强长序列理解，使 [MiniCPM3-4B](https://github.com/OpenBMB/MiniCPM) 在长上下文评估中超越 70B 规模的模型。
* [**LLMxMapReduce-V2**](https://github.com/thunlp/LLMxMapReduce/tree/main/LLMxMapReduce_V2)：引入熵驱动的卷积测试时间缩放机制，以改善极大量信息的整合，为在线 [SurveyGO](https://surveygo.modelbest.cn/) 系统提供支持。

# 📖 介绍

长篇生成对于广泛的实际应用至关重要，通常分为短到长和长到长生成。虽然短到长生成已经受到相当多的关注，但从极长资源生成长文本仍然相对未被探索。长到长生成的主要挑战在于有效整合和分析来自广泛输入的相关信息，这对当前的大型语言模型（LLMs）仍然很困难。在本文中，我们提出了 LLMxMapReduce-V2，这是一种新颖的测试时间缩放策略，旨在增强 LLMs 处理极长输入的能力。受卷积神经网络的启发，它通过迭代地将局部特征整合为更高级别的全局表示，LLMxMapReduce-V2 利用堆叠的卷积缩放层逐步扩展对输入材料的理解。定量和定性实验结果都表明，我们的方法大大增强了 LLMs 处理长输入和生成连贯、信息丰富的长篇文章的能力，优于几个代表性的基线。

<div align="center">
  <img src="assets/main_pic.jpg" alt="$\text{LLM}\times \text{MapReduce}$-V2 框架">
</div>

# ⚡️ 快速开始
以下步骤是关于 LLMxMapReduce-V2 的。如果你想使用 LLMxMapReduce-V1，你需要参考[这里](LLMxMapReduce_V1/README.md)。

要开始使用，请确保安装了 requirements.txt 中列出的所有依赖项。你可以通过运行以下命令来实现：

```bash
pip install -r requirements.txt
```