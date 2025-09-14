# $\text{LLM}\times\text{MapReduce}$: Simplified Long-Sequence Processing using Large Language Models

<p align="center">•
 <a href="#-introduction"> 📖Introduction </a> •
 <a href="#-news">🎉News</a> •
 <a href="#-features">✨Features</a> •
 <a href="#%EF%B8%8F-getting-started">⚡️Getting Started</a> 
</p>
<p align="center">•
 <a href="#-evaluation">📃 Evaluation</a> •
 <a href="#-experiment-results">📊Experiment Results</a> •
 <a href="#-citation">📝 Citation</a>•
 <a href="https://arxiv.org/abs/2410.09342">📃Paper</a>


</p>
</div>

# 📖 Introduction
Enlarging the context window of large language models (LLMs) has become a crucial research area, particularly for applications involving extremely long sequences. We introduce $\text{LLM}\times\text{MapReduce}$, a novel training-free framework for processing long sequences, utilizing a divide-and-conquer strategy to achieve comprehensive document understanding. The proposed $\text{LLM}\times\text{MapReduce}$ framework splits the entire document into several chunks for LLMs to read and then aggregates the intermediate answers to produce the final output. The main challenge for divide-and-conquer long-sequence processing frameworks lies in the risk of losing essential long-range information when splitting the document, which can lead the model to produce incomplete or incorrect answers based on the segmented texts. Disrupted long-range information can be classified into two categories: **inter-chunk dependency** and **inter-chunk conflict**.
We design **a structured information protocol** to better cope with inter-chunk dependency and **an in-context confidence calibration mechanism** to resolve inter-chunk conflicts. Experimental results demonstrate that $\text{LLM}\times\text{MapReduce}$ can outperform representative open-source and commercial long-context LLMs, and is applicable to several different models.

# ✨ Features

1. **Divide-and-Conquer Strategy**: The entire document is divided into chunks, which are processed individually by LLMs.
2. **Structured Information Protocol**: a structured information protocol ensures that crucial information flows between the map and reduce stages, preventing information loss when documents are split into chunks and enabling coherent answers for complex questions.

3. **In-Context Confidence Calibration Mechanism**: a dynamic mechanism that resolves conflicts between outputs from different chunks, ensuring the final result is accurate, consistent, and contextually aligned across the entire document.