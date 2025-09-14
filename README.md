# LLMxMapReduce: Simplified Long-Sequence Processing using Large Language Models

<a href='https://surveygo.modelbest.cn/'><img src='https://img.shields.io/badge/Demo-Page-pink'></a> <a href='https://arxiv.org/abs/2410.09342'><img src='https://img.shields.io/badge/V1-Paper-Green'></a> <a href='https://arxiv.org/abs/2504.05732'><img src='https://img.shields.io/badge/V2-Paper-blue'></a> <a href='https://huggingface.co/datasets/R0k1e/SurveyEval'><img src='https://img.shields.io/badge/SurveyEval-Benchmark-yellow'></a> <a href='README_zh.md'><img src='https://img.shields.io/badge/Chinese-Readme-red'></a>

# 🎉 News
- [x] **`2025.04.22`** Release [SurveyGO](https://surveygo.modelbest.cn/), an online writting system driven by LLMxMapReduce-V2.
- [x] **`2025.04.09`** Release the paper of LLMxMapReduce-V2 in [arXiv](https://arxiv.org/abs/2504.05732).
- [x] **`2025.02.21`** Add support for both OpenAI API and OpenAI-compatible APIs (e.g., vLLM).
- [x] **`2024.10.12`** Release the paper of LLMxMapReduce-V1 in [arXiv](https://arxiv.org/abs/2410.09342).
- [x] **`2024.09.12`** Release the code for LLMxMapReduce-V1.

# 📚 Overview
**LLMxMapReduce** is a divide-and-conquer framework designed to enhance modern large language models (LLMs) in understanding and generating long sequences. Developed collaboratively by **AI9STARS**, **OpenBMB**, and **THUNLP**, this framework draws inspiration from the classic MapReduce algorithm introduced in the field of big data. Our goal is to build an LLM-driven distributed computing system capable of efficiently processing long sequences. Here are the main versions of LLMxMapReduce:

* [**LLMxMapReduce-V1**](https://github.com/thunlp/LLMxMapReduce/blob/main/LLMxMapReduce_V1): Utilizes a structured information protocol and in-context confidence calibration to enhance long-sequence understanding, enabling [MiniCPM3-4B](https://github.com/OpenBMB/MiniCPM) to outperform 70B-scale models in long-context evaluations.
* [**LLMxMapReduce-V2**](https://github.com/thunlp/LLMxMapReduce/tree/main/LLMxMapReduce_V2): Introduces an entropy-driven convolutional test-time scaling mechanism to improve the integration of extremely large volumes of information, powering the online [SurveyGO](https://surveygo.modelbest.cn/) system.

# 📖 Introduction


Long-form generation is crucial for a wide range of practical applications, typically categorized into short-to-long and long-to-long generation. While short-to-long generations have received considerable attention, generating long texts from extremely long resources remains relatively underexplored. The primary challenge in long-to-long generation lies in effectively integrating and analyzing relevant information from extensive inputs, which remains difficult for current large language models (LLMs). In this paper, we propose LLMxMapReduce-V2, a novel test-time scaling strategy designed to enhance the ability of LLMs to process extremely long inputs. Drawing inspiration from convolutional neural networks, which iteratively integrate local features into higher-level global representations, LLMxMapReduce-V2 utilizes stacked convolutional scaling layers to progressively expand the understanding of input materials. Both quantitative and qualitative experimental results demonstrate that our approach substantially enhances the ability of LLMs to process long inputs and generate coherent, informative long-form articles, outperforming several representative baselines.

<div align="center">
  <img src="assets/main_pic.jpg" alt="$\text{LLM}\times \text{MapReduce}$-V2 framework">
</div>

# ⚡️ Getting Started
The following steps are about LLMxMapReduce-V2. If you want to use LLMxMapReduce-V1, you need to refer to [here](LLMxMapReduce_V1/README.md).

To get started, ensure all dependencies listed in requirements.txt are installed. You can do this by running: