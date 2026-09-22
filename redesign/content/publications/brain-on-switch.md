---
title: "Brain-on-Switch: Towards Advanced Intelligent Network Dataplane via NN-Driven Traffic Analysis at Line-Speed"
authors: ["Jinzhu Yan","Haotian Xu","Zhuotao Liu","Qi Li","Ke Xu","Mingwei Xu","Jianping Wu"]
venue: "USENIX NSDI"
year: 2024
paper: "https://www.usenix.org/conference/nsdi24/presentation/yan"
code: "https://github.com/InspiringGroup-Lab/Brain-on-Switch"
pdf: "https://arxiv.org/pdf/2403.11090"
conference: "https://www.usenix.org/conference/nsdi24"
equal_contribution: ["Jinzhu Yan","Haotian Xu"]
corresponding: ["Zhuotao Liu"]
group_authors: [1,2]
topics: ["Networking Infrastructure for AI","Intelligent Network Architecture"]
aliases: ["/publications/networking_infrastructure_for_ai/intelligent_network_architecture/3-2-1/"]
---

The emerging programmable networks sparked significant research on Intelligent Network Data Plane (INDP), which achieves learning-based traffic analysis at line-speed. Prior art in INDP focus on deploying tree/forest models on the data plane. We observe a fundamental limitation in tree-based INDP approaches: although it is possible to represent even larger tree/forest tables on the data plane, the flow features that are computable on the data plane are fundamentally limited by hardware constraints. In this paper, we present BoS to push the boundaries of INDP by enabling Neural Network (NN) driven traffic analysis at line-speed. Many types of NNs (such as Recurrent Neural Network (RNN), and transformers) that are designed to work with sequential data have advantages over tree-based models, because they can take raw network data as input without complex feature computations on the fly. However, the challenge is significant: the recurrent computation scheme used in RNN inference is fundamentally different from the match-action paradigm used on the network data plane. BoS addresses this challenge by (i) designing a novel data plane friendly RNN architecture that can execute unlimited RNN time steps with limited data plane stages, effectively achieving line-speed RNN inference; and (ii) complementing the on-switch RNN model with an off-switch transformer-based traffic analysis module to further boost the overall performance. We implement a prototype of BoS using a P4 programmable switch as our data plane, and extensively evaluate it over multiple traffic analysis tasks. The results show that BoS outperforms state-of-the-art in both analysis accuracy and scalability.
