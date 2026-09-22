---
title: "Managing Recurrent Virtual Network Updates in Multi-Tenant Datacenters: A System Perspective"
authors: ["Zhuotao Liu","Yuan Cao","Xuewu Zhang","Changping Zhu","Fan Zhang"]
venue: "IEEE TPDS"
year: 2019
paper: "https://ieeexplore.ieee.org/abstract/document/8613794"
topics: ["Networking Infrastructure for AI","Datacenter Networking"]
aliases: ["/publications/networking_infrastructure_for_ai/datacenter_networking/3-1-6/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:3fE2CSJIrl8C"
---

With the advent of software-defined networking, network configuration through programmable interfaces becomes practical, leading to various on-demand opportunities for network routing update in multi-tenant datacenters, where tenants have diverse requirements on network routings such as short latency, low path inflation, large bandwidth, high reliability, etc. Conventional solutions that rely on topology search coupled with an objective function to find desired routings have at least two shortcomings: (i)(i) they run into scalability issues when handling consistent and frequent routing updates and (ii)(ii) they restrict the flexibility and capability to satisfy various routing requirements. To address these issues, this paper proposes a novel search and optimization decoupled design, which not only saves considerable topology search costs via search result reuse, but also avoids possible sub-optimality in greedy routing search algorithms by making decisions based on the global view of all possible routings. We implement a prototype of our proposed system, OpReduce, and perform extensive evaluations to validate its design goals.
