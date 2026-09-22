---
title: "Enabling Work-Conserving Bandwidth Guarantees for Multi-Tenant Datacenters via Dynamic Tenant-Queue Binding"
authors: ["Zhuotao Liu","Kai Chen","Haitao Wu","Shuihai Hu","Yih-Chun Hu","Yi Wang","Gong Zhang"]
venue: "IEEE INFOCOM"
year: 2018
paper: "https://ieeexplore.ieee.org/document/8486219"
pdf: "https://arxiv.org/abs/1712.06766"
conference: "https://infocom2018.ieee-infocom.org/index.html"
topics: ["Networking Infrastructure for AI","Datacenter Networking"]
aliases: ["/publications/networking_infrastructure_for_ai/datacenter_networking/3-1-4/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:roLk4NBRz8UC"
---

Today's cloud networks are shared among many tenants. Bandwidth guarantees and work conservation are two key properties to ensure predictable performance for tenant applications and high network utilization for providers. Despite significant efforts, very little prior work can really achieve both properties simultaneously even some of them claimed so. In this paper, we present QShare, a comprehensive in-network solution to achieve bandwidth guarantees and work conservation simultaneously. QShare leverages weighted fair queuing on commodity switches to slice network bandwidth for tenants, and solves the challenge of queue scarcity through balanced tenant placement and dynamic tenant-queue binding. We have implemented a QShare prototype and evaluated it extensively via both testbed experiments and simulations. Our results show that QShare ensures bandwidth guarantees while driving network utilization to over 91% even under unpredictable traffic demands.
