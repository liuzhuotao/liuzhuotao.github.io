---
title: "A Hard Label Black-box Adversarial Attack Against Graph Neural Networks"
authors: ["Jiaming Mu","Binghui Wang","Qi Li","Kun Sun","Mingwei Xu","Zhuotao Liu"]
venue: "ACM CCS"
year: 2021
paper: "https://dl.acm.org/doi/abs/10.1145/3460120.3484796"
code: "https://github.com/mujm/CCS21_GNNattack/tree/master"
pdf: "https://arxiv.org/pdf/2108.09513.pdf"
conference: "https://www.sigsac.org/ccs/CCS2021/"
topics: ["AI and Data Security (with Applied Cryptography)","AI Security"]
aliases: ["/publications/ai_and_data_security/ai_security/2-3-3/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:isC4tDSrTZIC"
---

Graph Neural Networks (GNNs) have achieved state-of-the-art performance in various graph structure related tasks such as node classification and graph classification. However, GNNs are vulnerable to adversarial attacks. Existing works mainly focus on attacking GNNs for node classification; nevertheless, the attacks against GNNs for graph classification have not been well explored. In this work, we conduct a systematic study on adversarial attacks against GNNs for graph classification via perturbing the graph structure. In particular, we focus on the most challenging attack, i.e., hard label black-box attack, where an attacker has no knowledge about the target GNN model and can only obtain predicted labels through querying the target model. To achieve this goal, we formulate our attack as an optimization problem, whose objective is to minimize the number of edges to be perturbed in a graph while maintaining the high attack success rate. The original optimization problem is intractable to solve, and we relax the optimization problem to be a tractable one, which is solved with theoretical convergence guarantee. We also design a coarse-grained searching algorithm and a query-efficient gradient computation algorithm to decrease the number of queries to the target GNN model. Our experimental results on three real-world datasets demonstrate that our attack can effectively attack representative GNNs for graph classification with less queries and perturbations. We also evaluate the effectiveness of our attack under two defenses: one is well-designed adversarial graph detector and the other is that the target GNN model itself is equipped with a defense to prevent adversarial graph generation. Our experimental results show that such defenses are not effective enough, which highlights more advanced defenses.
