---
title: "FlowTele: Remotely Shaping Traffic on Internet-Scale Networks"
authors: ["Bo-Rong Chen","Zhuotao Liu","Fanhui Zeng","Zhoushi Zhu","Siva Phani Keshav Bachu","Yih-Chun Hu"]
venue: "ACM CoNEXT"
year: 2022
paper: "https://dl.acm.org/doi/abs/10.1145/3555050.3569139"
conference: "https://conferences.sigcomm.org/co-next/2022"
corresponding: ["Zhuotao Liu"]
topics: ["Networking Infrastructure for AI","Intelligent Network Architecture"]
aliases: ["/publications/networking_infrastructure_for_ai/intelligent_network_architecture/3-2-3/"]
---

Internet content providers often deliver content through bandwidth bottlenecks that are out of their control. Thus, despite often having massively over-provisioned upstream servers, the content providers still cannot control the end-to-end user experience. This paper explores remote traffic shaping, allowing the content provider to allocate its share of a remote bottleneck link across its users using a metric other than TCP fairness, while remaining TCP-friendly to cross traffic on the bottleneck link. To evaluate this approach, we designed FlowTele, the first system that shapes outbound traffic on an Internet-scale network to optimize provider-selected metrics, using source control with neither in-network support nor special client support. Our extensive evaluations over the Internet show that by strategically reallocating bandwidth among provider-owned co-bottlenecked flows, FlowTele improves the provider's total revenue by roughly 20%--30% in various network settings, compared with both (i) status quo TCP fairshare and (ii) recent practice by content providers that proactively throttles video quality during the COVID-19 pandemic, while being TCP-friendly to cross-traffic. Besides revenue, we also study other metrics, such as QoE fairness, that a content provider may wish to optimize using FlowTele.
