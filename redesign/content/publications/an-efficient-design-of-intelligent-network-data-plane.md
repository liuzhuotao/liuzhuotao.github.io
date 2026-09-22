---
title: "An Efficient Design of Intelligent Network Data Plane"
authors: ["Guangmeng Zhou","Zhuotao Liu","Chuanpu Fu","Qi Li","Ke Xu"]
venue: "USENIX Security"
year: 2023
paper: "https://www.usenix.org/conference/usenixsecurity23/presentation/zhou-guangmeng"
conference: "https://www.usenix.org/conference/usenixsecurity23"
award: ["Distinguished Paper Award"]
selected: true
topics: ["Networking Infrastructure for AI","Intelligent Network Architecture"]
aliases: ["/publications/networking_infrastructure_for_ai/intelligent_network_architecture/3-2-2/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:ns9cj8rnVeAC"
---

Deploying machine learning models directly on the network data plane enables intelligent traffic analysis at line-speed using data-driven models rather than predefined protocols. Such a capability, referred to as Intelligent Data Plane (IDP), may potentially transform a wide range of networking designs. The emerging programmable switches provide crucial hardware support to realize IDP. Prior art in this regard is divided into two major categories: (i) focusing on extract useful flow information from the data plane, while placing the learning-based traffic analysis on the control plane; and (ii) taking a step further to embed learning models into the data plane, while failing to use flow-level features that are critical to achieve high learning accuracies. In this paper, we propose NetBeacon to advance the state-of-the-art in both model accuracy and model deployment efficiency. In particular, NetBeacon proposes a multi-phase sequential model architecture to perform dynamic packet analysis at different phases of a flow as it proceeds, by incorporating flow-level features that are computable at line-speed to boost learning accuracies. Further, NetBeacon designs efficient model representation mechanisms to address the table entry explosion problem when deploying tree-based models on the network data plane. Finally, NetBeacon hardens its scalability for handling concurrent flows via multiple tightly-coupled designs for managing stateful storage used to store per-flow state. We implement a prototype of NetBeacon and extensively evaluate its performance over multiple traffic analysis tasks.
