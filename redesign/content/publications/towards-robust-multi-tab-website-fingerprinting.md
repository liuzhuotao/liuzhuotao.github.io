---
title: "Towards robust multi-tab website fingerprinting"
authors: ["Xinhao Deng", "Xiyuan Zhao", "Qilei Yin", "Zhuotao Liu", "Qi Li", "Mingwei Xu", "Ke Xu", "Jianping Wu"]
venue: "IEEE ToN"
year: 2026
paper: "https://ieeexplore.ieee.org/abstract/document/11406189/"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:sSrBHYA8nusC"
# Metadata source: https://arxiv.org/abs/2501.12622
preprint: "https://arxiv.org/abs/2501.12622"
auto_enrich: true
---

<!-- Abstract source: https://arxiv.org/abs/2501.12622 -->
Website fingerprinting enables an eavesdropper to determine which websites a user is visiting over an encrypted connection. State-of-the-art website fingerprinting (WF) attacks have demonstrated effectiveness even against Tor-protected network traffic. However, existing WF attacks have critical limitations on accurately identifying websites in multi-tab browsing sessions, where the holistic pattern of individual websites is no longer preserved, and the number of tabs opened by a client is unknown a priori. In this paper, we propose ARES, a novel WF framework natively designed for multi-tab WF attacks. ARES formulates the multi-tab attack as a multi-label classification problem and solves it using the novel Transformer-based models. Specifically, ARES extracts local patterns based on multi-level traffic aggregation features and utilizes the improved self-attention mechanism to analyze the correlations between these local patterns, effectively identifying websites. We implement a prototype of ARES and extensively evaluate its effectiveness using our large-scale datasets collected over multiple months. The experimental results illustrate that ARES achieves optimal performance in several realistic scenarios. Further, ARES remains robust even against various WF defenses.
