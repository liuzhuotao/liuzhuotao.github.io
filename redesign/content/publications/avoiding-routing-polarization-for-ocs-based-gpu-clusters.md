---
title: "Avoiding routing polarization for OCS-based GPU clusters"
authors: ["Xinchi Han", "Weihao Jiang", "Yingming Mao", "Yike Liu", "Zhuoran Liu", "Yongxi Lv", "Peirui Cao", "Zhuotao Liu", "Ximeng Liu", "Xinbing Wang", "Changbo Wu", "Zihan Zhu", "Dongchao Wu", "Jian Yang", "Zhanbang Zhang", "Yuansen Cheng", "Shizhen Zhao"]
venue: "Journal of Optical Communications and Networking"
year: 2026
paper: "https://opg.optica.org/abstract.cfm?uri=jocn-18-9-900"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:LjlpjdlvIbIC"
versions: [{"label": "Preprint", "url": "https://arxiv.org/abs/2603.28168"}, {"label": "Author PDF", "url": "https://jhc.sjtu.edu.cn/~shizhenzhao/JOCN2026_tech.pdf"}]
# Metadata source: https://doi.org/10.1364/jocn.590440
auto_enrich: true
---

<!-- Abstract source: https://doi.org/10.1364/jocn.590440 -->
Recent years have witnessed the growing deployment of optical circuit switches (OCSes) in commercial GPU clusters (e.g., Google’s A3 GPU cluster) optimized for machine learning (ML) workloads. Such clusters adopt a three-tier leaf–spine–OCS topology: servers attach to leaf-layer electronic packet switches (EPSes), these leaf switches aggregate into spine-layer EPSes to form a pod, and multiple pods are interconnected via core-layer OCSes. Unlike EPSes, OCSes only support circuit-based paths between directly connected spine switches, potentially inducing a phenomenon termed routing polarization, which refers to the scenario where the bandwidth requirements between specific pairs of pods are unevenly fulfilled through links among different spine switches. The resulting imbalance induces traffic contention and bottlenecks on specific leaf-to-spine links, ultimately reducing ML training throughput. To mitigate this issue, we introduce a leaf-centric paradigm to ensure traffic originating from the same leaf switch is evenly distributed across multiple spine switches with balanced loads. Through rigorous theoretical analysis, we establish a sufficient condition for avoiding routing polarization and propose a corresponding logical topology design algorithm with polynomial-time complexity. Evaluations on a 128-NPU testbed show up to 23.7% higher training throughput than state-of-the-art pod-centric approaches, while large-scale simulations validate up to 19.27% throughput improvement and a 99.16% reduction in logical topology computation overhead compared to mixed integer programming (MIP)-based methods.
