---
title: "A Hard-Label Black-Box Evasion Attack against ML-based Malicious Traffic Detection Systems"
authors: ["Zixuan Liu","Yi Zhao","Zhuotao Liu","Qi Li","Chuanpu Fu","Guangmeng Zhou","Ke Xu"]
venue: "NDSS"
year: 2026
conference: "https://www.ndss-symposium.org/ndss2026/"
topics: ["Secure Networking and Systems Infrastructure","AI-Driven Traffic Analysis","Encrypted Traffic Analysis"]
aliases: ["/publications/secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-11/"]
paper: "https://arxiv.org/abs/2510.14906"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:1qzjygNMrQYC"
# Metadata source: https://arxiv.org/abs/2510.14906
preprint: "https://arxiv.org/abs/2510.14906"
auto_enrich: true
---

<!-- Abstract source: https://arxiv.org/abs/2510.14906 -->
Machine Learning (ML)-based malicious traffic detection is a promising security paradigm. It outperforms rule-based traditional detection by identifying various advanced attacks. However, the robustness of these ML models is largely unexplored, thereby allowing attackers to craft adversarial traffic examples that evade detection. Existing evasion attacks typically rely on overly restrictive conditions (e.g., encrypted protocols, Tor, or specialized setups), or require detailed prior knowledge of the target (e.g., training data and model parameters), which is impractical in realistic black-box scenarios. The feasibility of a hard-label black-box evasion attack (i.e., applicable across diverse tasks and protocols without internal target insights) thus remains an open challenge. To this end, we develop NetMasquerade, which leverages reinforcement learning (RL) to manipulate attack flows to mimic benign traffic and evade detection. Specifically, we establish a tailored pre-trained model called Traffic-BERT, utilizing a network-specialized tokenizer and an attention mechanism to extract diverse benign traffic patterns. Subsequently, we integrate Traffic-BERT into the RL framework, allowing NetMasquerade to effectively manipulate malicious packet sequences based on benign traffic patterns with minimal modifications. Experimental results demonstrate that NetMasquerade enables both brute-force and stealthy attacks to evade 6 existing detection methods under 80 attack scenarios, achieving over 96.65% attack success rate. Notably, it can evade the methods that are either empirically or certifiably robust against existing evasion attacks. Finally, NetMasquerade achieves low-latency adversarial traffic generation, demonstrating its practicality in real-world scenarios.
