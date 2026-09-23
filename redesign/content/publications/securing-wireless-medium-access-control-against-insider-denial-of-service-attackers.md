---
title: "Securing wireless medium access control against insider denial-of-service attackers"
authors: ["Sang-Yoon Chang", "Yih-Chun Hu", "Zhuotao Liu"]
venue: "IEEE CNS"
year: 2015
paper: "https://ieeexplore.ieee.org/abstract/document/7346848/"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:IjCSPb-OGe4C"
# Metadata source: https://openalex.org/W2186488678
auto_enrich: true
---

<!-- Abstract source: https://openalex.org/W2186488678 -->
In a wireless network, users share a limited resource in bandwidth. To improve spectral efficiency, the network dynamically allocates channel resources and, to avoid collisions, has its users cooperate with each other using a medium access control (MAC) protocol. In a MAC protocol, the users exchange control messages to establish more efficient data communication, but such MAC assumes user compliance and can be detrimental when a user misbehaves. An attacker who compromised the network can launch a two-pronged denial-of-service (DoS) attack that is more devastating than an outsider attack: first, it can send excessive reservation requests to waste bandwidth, and second, it can focus its power on jamming those channels that it has not reserved. Furthermore, the attacker can falsify information to skew the network control decisions to its favor. To defend against such insider threats, we propose a resource-based channel access scheme that holds the attacker accountable for its channel reservation. Building on the randomization technology of spread spectrum to thwart outsider jamming, our solution comprises of a bandwidth allocation component to nullify excessive reservations, bandwidth coordination to resolve over-reserved and under-reserved spectrum, and power attribution to determine each node's contribution to the received power. We analyze our scheme theoretically and validate it with WARP-based testbed implementation and MATLAB simulations. Our results demonstrate superior performance over the typical solutions that bypass MAC control when faced against insider adversary, and our scheme effectively nullifies the insider attacker threats while retaining the MAC benefits between the collaborative users.
