---
title: "Umbrella: Enabling ISPs to Offer Readily Deployable and Privacy-Preserving DDoS Prevention Services"
authors: ["Zhuotao Liu","Yuan Cao","Min Zhu","Wei Ge"]
venue: "IEEE TIFS"
year: 2019
paper: "https://ieeexplore.ieee.org/document/8466917"
pdf: "https://arxiv.org/abs/1903.07796"
code: "https://github.com/zliuInspire/MiddlePolice"
topics: ["Secure Networking and Systems Infrastructure","DDoS Attack Prevention","DDoS Prevention"]
aliases: ["/publications/secure_networking_and_systems_infrastructure/ddos_attack_prevention/1-3-4/"]
---

Defending against distributed denial of service (DDoS) attacks on the Internet is a fundamental problem. However, recent industrial interviews with over 100 security experts from more than ten industry segments indicate that DDoS problems have not been fully addressed. The reasons are twofold. On one hand, many academic proposals that are provably secure witness little real-world deployment. On the other hand, the operation model for existing DDoS-prevention service providers (e.g., Cloudflare, Akamai) is privacy invasive for large organizations (e.g., government). In this paper, we present Umbrella, a new DDoS defense mechanism enabling Internet service providers to offer readily deployable and privacy-preserving DDoS prevention services to their customers. At its core, Umbrella develops a multi-layered defense architecture to defend against a wide spectrum of DDoS attacks. In particular, the flood throttling layer stops amplification-based DDoS attacks; the congestion resolving layer, aiming to prevent sophisticated attacks that cannot be easily filtered, enforces congestion accountability to ensure that legitimate flows are guaranteed to receive their fair shares regardless of attackers' strategies; and finally the user-specific layer allows DDoS victims to enforce self-desired traffic control policies that best satisfy their business requirements. Based on Linux implementation, we demonstrate that Umbrella is capable to deal with large-scale attacks involving millions of attack flows, meanwhile imposing negligible packet processing overhead. Further, our physical test bed experiments and large-scale simulations prove that Umbrella is effective to mitigate various DDoS attacks.
