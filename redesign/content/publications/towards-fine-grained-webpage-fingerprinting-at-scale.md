---
title: "Towards Fine-Grained Webpage Fingerprinting at Scale"
authors: ["Xiyuan Zhao","Xinhao Deng","Qi Li","Yunpeng Liu","Zhuotao Liu","Kun Sun","Ke Xu"]
venue: "ACM CCS"
year: 2024
paper: "https://dl.acm.org/doi/10.1145/3658644.3690211"
pdf: "https://arxiv.org/abs/2409.04341"
conference: "https://www.sigsac.org/ccs/CCS2024/"
topics: ["Secure Networking and Systems Infrastructure","AI-Driven Traffic Analysis","Encrypted Traffic Analysis"]
aliases: ["/publications/secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-4/"]
---

Website Fingerprinting (WF) attacks can effectively identify the websites visited by Tor clients via analyzing encrypted traffic patterns. Existing attacks focus on identifying different websites, but their accuracy dramatically decreases when applied to identify fine-grained webpages, especially when distinguishing among different subpages of the same website. WebPage Fingerprinting (WPF) attacks face the challenges of highly similar traffic patterns and a much larger scale of webpages. Furthermore, clients often visit multiple webpages concurrently, increasing the difficulty of extracting the traffic patterns of each webpage from the obfuscated traffic. In this paper, we propose Oscar, a WPF attack based on multi-label metric learning that identifies different webpages from obfuscated traffic by transforming the feature space. Oscar can extract the subtle differences among various webpages, even those with similar traffic patterns. In particular, Oscar combines proxy-based and sample-based metric learning losses to extract webpage features from obfuscated traffic and identify multiple webpages. We prototype Oscar and evaluate its performance using traffic collected from 1,000 monitored webpages and over 9,000 unmonitored webpages in the real world. Oscar demonstrates an 88.6% improvement in the multi-label metric Recall@5 compared to the state-of-the-art attacks.
