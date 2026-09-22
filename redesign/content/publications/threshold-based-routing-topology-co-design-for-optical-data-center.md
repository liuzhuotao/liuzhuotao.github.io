---
title: "Threshold-Based Routing-Topology Co-Design for Optical Data Center"
authors: ["Peirui Cao","Shizhen Zhao","Dai Zhang","Zhuotao Liu","Mingwei Xu","Min Yee Teh","Yunzhuo Liu","Xinbing Wang","Chenghu Zou"]
venue: "IEEE/ACM ToN"
year: 2023
paper: "https://ieeexplore.ieee.org/abstract/document/10102400"
topics: ["Networking Infrastructure for AI","Datacenter Networking"]
aliases: ["/publications/networking_infrastructure_for_ai/datacenter_networking/3-1-3/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:70eg2SAEIzsC"
---

Despite the bandwidth scaling limit of electrical switching and the high cost of building Clos data center networks (DCNs), the adoption of optical DCNs is still limited. There are two reasons. First, existing optical DCN designs usually face high deployment complexity. Second, these designs are not full-optical and the performance benefit over the non-blocking Clos DCN is not clear. After exploring the design tradeoffs of the existing optical DCN designs, we propose TROD (Threshold Routing based Optical Datacenter), a low-complexity optical DCN with superior performance than other optical DCNs. There are two novel designs in TROD that contribute to its success. First, TROD performs robust topology optimization based on the recurring traffic patterns and thus does not need to react to every traffic change, which lowers deployment and management complexity. Second, TROD introduces tVLB (threshold-based Valiant Load Balance), which can avoid network congestion as much as possible even under unexpected traffic bursts. We conduct simulation based on both Facebook’s real DCN traces and our synthesized highly bursty DCN traces. TROD reduces flow completion time (FCT) by about 1.15- 2.16× compared to Google’s Jupiter DCN, at least 2× compared to other optical DCN designs, and about 2.4- 3.2× compared to expander graph DCN. Compared with the non-blocking Clos, TROD reduces the hop count of the majority packets by one, and could even outperform the non-blocking Clos with proper bandwidth over-provision at the optical layer. Note that TROD can be built with commercially available hardware and does not require host modifications.
