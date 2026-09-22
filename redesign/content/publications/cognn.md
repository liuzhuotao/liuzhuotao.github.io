---
title: "CoGNN: Towards Secure and Efficient Collaborative Graph Learning"
authors: ["Zhenhua Zou","Zhuotao Liu","Jinyong Shan","Qi Li","Ke Xu","Mingwei Xu"]
venue: "ACM CCS"
year: 2024
paper: "https://eprint.iacr.org/2024/987"
code: "https://github.com/InspiringGroup-Lab/CoGNN"
conference: "https://www.sigsac.org/ccs/CCS2024/"
corresponding: ["Zhuotao Liu"]
selected: true
group_authors: [1]
topics: ["AI and Data Security (with Applied Cryptography)","Privacy-Preserving Machine Learning","Data Security"]
aliases: ["/publications/ai_and_data_security/privacy-preserving_machinelearning/2-1-2/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:SP6oXDckpogC"
---

Collaborative graph learning represents a learning paradigm where multiple parties jointly train a graph neural network (GNN) using their own proprietary graph data. To honor the data privacy of all parties, existing solutions for collaborative graph learning are either based on federated learning (FL) or secure machine learning (SML). Although promising in terms of efficiency and scalability due to their distributed training scheme, FL-based approaches fall short in providing provable security guarantees and achieving good model performance. Conversely, SML-based solutions, while offering provable privacy guarantees, are hindered by their high computational and communication overhead, as well as poor scalability as more parties participate.
To address the above problem, we propose CoGNN, a novel framework that simultaneously reaps the benefits of both FL-based and SML-based approaches. At a high level, CoGNN is enabled by (i) a novel message passing mechanism that can obliviously and efficiently express the vertex data propagation/aggregation required in GNN training and inference and (ii) a two-stage Dispatch-Collect execution scheme to securely decompose and distribute the GNN computation workload for concurrent and scalable executions. We further instantiate the CoGNN framework, together with customized optimizations, to train Graph Convolutional Network (GCN) models. Extensive evaluations on three graph datasets demonstrate that compared with the state-of-the-art (SOTA) SML-based approach, CoGNN reduces up to x running time and up to x communication cost per party. Meanwhile, the GCN models trained using CoGNN have nearly identical accuracies as the plaintext global-graph training, yielding up to accuracy improvement over the GCN models trained via federated learning.
