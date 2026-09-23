---
title: "A middle path for on-premises llm deployment: Preserving privacy without sacrificing model confidentiality"
authors: ["Hanbo Huang", "Yihan Li", "Bowen Jiang", "Bo Jiang", "Lin Liu", "Zhuotao Liu", "Ruoyu Sun", "Shiyu Liang"]
venue: "EMNLP"
year: 2025
paper: "https://aclanthology.org/2025.emnlp-main.420/"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:J-pR_7NvFogC"
versions: [{"label": "Preprint", "url": "https://arxiv.org/abs/2410.11182"}, {"label": "Workshop version", "url": "https://openreview.net/forum?id=u61yT9ZkEZ"}]
# Metadata source: https://openalex.org/W4416036720
pdf: "https://aclanthology.org/2025.emnlp-main.420.pdf"
auto_enrich: true
---

<!-- Abstract source: https://openalex.org/W4416036720 -->
Privacy-sensitive users require deploying large language models (LLMs) within their own infrastructure (on-premises) to safeguard private data and enable customization.However, vulnerabilities in local environments can lead to unauthorized access and potential model theft.To address this, prior research on small models has explored securing only the output layer within hardware-secured devices to balance model confidentiality and customization.Yet this approach fails to protect LLMs effectively.In this paper, we discover that (1) query-based distillation attacks targeting the secured top layer can produce a functionally equivalent replica of the victim model; (2) securing the same number of layers, bottom layers before a transition layer provide stronger protection against distillation attacks than top layers, with comparable effects on customization performance; and (3) the number of secured layers creates a trade-off between protection and customization flexibility.Based on these insights, we propose SOLID, a novel deployment framework that secures a few bottom layers in a secure environment and introduces an efficient metric to optimize the trade-off by determining the ideal number of hidden layers.Extensive experiments on five models (1.3B to 70B parameters) demonstrate that SOLID outperforms baselines, achieving a better balance between protection and downstream customization.Our code can be found at: https://github.com/ OTTO-OTO/SOLID-OnPremiseDeployment.
