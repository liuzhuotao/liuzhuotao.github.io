---
title: "LLMs can understand encrypted prompt: Towards privacy-computing friendly transformers"
authors: ["Xuanqi Liu", "Zhuotao Liu"]
venue: "arXiv preprint"
year: 2023
paper: "https://arxiv.org/abs/2305.18396"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:SeFeTyx0c_EC"
# Metadata source: https://arxiv.org/abs/2305.18396
preprint: "https://arxiv.org/abs/2305.18396"
auto_enrich: true
---

<!-- Abstract source: https://arxiv.org/abs/2305.18396 -->
The community explored to build private inference frameworks for transformer-based large language models (LLMs) in a server-client setting, where the server holds the model parameters and the client inputs its private data (or prompt) for inference. However, these frameworks impose significant overhead when the private inputs are forward propagated through the original LLMs. In this paper, we show that substituting the computation- and communication-heavy operators in the transformer architecture with privacy-computing friendly approximations can greatly reduce the private inference costs while incurring very minor impact on model performance. Compared to state-of-the-art Iron (NeurIPS 2022), our privacy-computing friendly model inference pipeline achieves a $5\\times$ acceleration in computation and an 80% reduction in communication overhead, while retaining nearly identical accuracy.
