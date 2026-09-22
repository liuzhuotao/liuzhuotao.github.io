---
title: "RingSG: Optimal Secure Vertex-Centric Computation for Collaborative Graph Processing"
authors: ["Zhenhua Zou","Zhuotao Liu","Jinyong Shan","Qi Li","Ke Xu","Mingwei Xu"]
venue: "ACM CCS"
year: 2025
paper: "https://dl.acm.org/doi/10.1145/3719027.3744824"
conference: "https://www.sigsac.org/ccs/CCS2025/"
award: ["Distinguished Paper Award"]
corresponding: ["Zhuotao Liu"]
group_authors: [1]
topics: ["AI and Data Security (with Applied Cryptography)","Privacy-Preserving Machine Learning","Data Security"]
selected: true
selected_order: 2
aliases: ["/publications/ai_and_data_security/privacy-preserving_machinelearning/2-1-3/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:fQNAKQ3IYiAC"
---

Collaborative graph processing refers to the joint analysis of inter-connected graphs held by multiple graph owners. To honor data privacy and support various graph processing algorithms, existing approaches employ secure multi-party computation (MPC) protocols to express the vertex-centric abstraction. Yet, due to certain computation-intensive cryptography constructions, state-of-the-art (SOTA) approaches are asymptotically suboptimal, imposing significant overheads in terms of computation and communication. In this paper, we present RingSG, the first system to attain optimal communication/computation complexity within the MPC-based vertex-centric abstraction for collaborative graph processing. This optimal complexity is attributed to Ring-ScatterGather, a novel computation paradigm that can avoid exceedingly expensive cryptography operations (e.g., oblivious sort), and simultaneously ensure the overall workload can be optimally decomposed into parallelizable and mutually exclusive MPC tasks. Within Ring-ScatterGather, RingSG improves the concrete runtime efficiency by incorporating 3-party secure computation via share conversion, and optimizing the most cost-heavy part using a novel oblivious group aggregation protocol. Finally, unlike prior approaches, we instantiate RingSG into two end-to-end applications to effectively obtain application-specific results from the protocol outputs in a privacy-preserving manner. We developed a prototype of RingSG and extensively evaluated it across various graph collaboration settings, including different graph sizes, numbers of parties, and average vertex degrees. The results show RingSG reduces the system running time of SOTA approaches by up to 15.34× and per-party communication by up to 10.36×. Notably, RingSG excels in processing sparse global graphs collectively held by more parties, consistent with our theoretical cost analysis.
