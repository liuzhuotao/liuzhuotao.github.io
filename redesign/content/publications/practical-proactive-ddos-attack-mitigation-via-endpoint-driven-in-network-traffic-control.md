---
title: "Practical Proactive DDoS-Attack Mitigation via Endpoint-Driven In-Network Traffic Control"
authors: ["Zhuotao Liu","Hao Jin","Yih-Chun Hu","Michael Bailey"]
venue: "IEEE/ACM ToN"
year: 2018
paper: "https://ieeexplore.ieee.org/document/8418343"
code: "https://github.com/zliuInspire/MiddlePolice"
topics: ["Secure Networking and Systems Infrastructure","DDoS Attack Prevention","DDoS Prevention"]
aliases: ["/publications/secure_networking_and_systems_infrastructure/ddos_attack_prevention/1-3-2/"]
---

Volumetric attacks, which overwhelm the bandwidth of a destination, are among the most common distributed denial-of-service (DDoS) attacks today. Despite considerable effort made by both research and industry, our recent interviews with over 100 potential DDoS victims in over 10 industry segments indicate that today's DDoS prevention is far from perfect. On one hand, few academical proposals have ever been deployed in the Internet; on the other hand, solutions offered by existing DDoS prevention vendors are not silver bullet to defend against the entire attack spectrum. Guided by such large-scale study of today's DDoS defense, in this paper, we present MiddlePolice, the first readily deployable and proactive DDoS prevention mechanism. We carefully architect MiddlePolice such that it requires no changes from both the Internet core and the network stack of clients, yielding instant deployability in the current Internet architecture. Further, relying on our novel capability feedback mechanism, MiddlePolice is able to enforce destination-driven traffic control so that it guarantees to deliver victim-desired traffic regardless of the attacker strategies. We implement a prototype of MiddlePolice and demonstrate its feasibility via extensive evaluations in the Internet, hardware testbed, and large-scale simulations.
