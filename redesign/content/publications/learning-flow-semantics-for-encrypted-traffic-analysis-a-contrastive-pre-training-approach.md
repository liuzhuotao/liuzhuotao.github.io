---
title: "Learning Flow Semantics for Encrypted Traffic Analysis: A Contrastive Pre-Training Approach"
authors: ["Ruijie Zhao","Mingwei Zhan","Qi Li","Zhuotao Liu","Xianwen Deng","Yanhao Wang","Guang Cheng","Zhi Xue","Ke Xu"]
venue: "IEEE TDSC"
year: 2026
paper: "https://ieeexplore.ieee.org/abstract/document/11456104"
topics: ["Secure Networking and Systems Infrastructure","AI-Driven Traffic Analysis","Encrypted Traffic Analysis"]
aliases: ["/publications/secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-12/"]
---

Encrypted traffic analysis is crucial for cyberspace security. Self-supervised learning shows great promise to enhance traffic analysis with the pre-trained traffic encoder, which is constructed using large-scale, readily available unlabeled traffic data. However, existing approaches struggle to handle the increasingly prevalent encrypted traffic, as their generative reconstruction tasks cannot process encrypted content. To this end, we propose TaCo, a robust and flexible encrypted traffic analysis system based on flow semantics learning. Specifically, we first design several feasible traffic data augmentation strategies to prepare flow semantics knowledge from the unlabeled traffic. Then, our traffic encoder with a traffic partition module learns the semantics knowledge based on the contrastive pre-training paradigm. It serves as a traffic foundation encoder that can comprehend flow semantics and extract effective semantic representations. Finally, we fine-tune the traffic encoder to leverage flow semantics for various downstream encrypted traffic analysis tasks. The experimental results illustrate that TaCo outperforms the optimal baseline by 7.49% in average F1 score on four traffic classification datasets and 9.61% in average F1 score on the three transfer tasks, while indicating superior efficiency.
