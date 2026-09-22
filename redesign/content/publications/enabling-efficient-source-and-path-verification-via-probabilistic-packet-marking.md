---
title: "Enabling Efficient Source and Path Verification via Probabilistic Packet Marking"
authors: ["Bo Wu","Ke Xu","Qi Li","Zhuotao Liu","Yih-Chun Hu","Martin J. Reed","Meng Shen","Fan Yang"]
venue: "IEEE/ACM IWQoS"
year: 2018
paper: "https://ieeexplore.ieee.org/abstract/document/8624169"
conference: "https://iwqos2018.ieee-iwqos.org/index.html"
topics: ["Secure Networking and Systems Infrastructure","Secure Internet Routing"]
aliases: ["/publications/secure_networking_and_systems_infrastructure/secure_internet_routing/1-1-3/"]
---

The Internet lacks verification of source authenticity and path compliance between the planned packet delivery paths and the real delivery paths, which allows attackers to construct attacks like source spoofing and traffic hijacking attacks. Thus, it is essential to enable source and path verification in networks to detect forwarding anomalies and ensure correct packet delivery. However, most of the existing security mechanisms can only capture anomalies but are unable to locate the detected anomalies. Besides, they incur significant computation and communication overhead, which exacerbates the packet delivery performance. In this paper, we propose a high-efficient packet forwarding verification mechanism called PPV for networks, which verifies packet source and their forwarding paths in real time. PPV enables probabilistic packet marking in routers instead of verifying all packets. Thus, it can efficiently identify forwarding anomalies by verifying markings. Moreover, it localizes packet forwarding anomalies, e.g., malicious routers, by reconstructing packet forwarding paths based on the packet markings. We implement PPV prototype in Click routers and commodity servers, and conducts real experiments in a real testbed built upon the prototype. The experimental results demonstrate the efficiency and performance of PPV. In particular, PPV significantly improves the throughput and the goodput of forwarding verification, and achieves around 2 times and 3 times improvement compared with the-state-of-art OPT scheme, respectively.
