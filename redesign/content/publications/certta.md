---
title: "CertTA: Certified Robustness Made Practical for Learning-Based Traffic Analysis"
authors: ["Jinzhu Yan","Zhuotao Liu","Yuyang Xie","Shiyu Liang","Lin Liu","Ke Xu"]
venue: "USENIX Security"
year: 2025
paper: "https://www.usenix.org/conference/usenixsecurity25/presentation/yan-jinzhu"
code: "https://github.com/InspiringGroup-NeoLab/CertTA"
conference: "https://www.usenix.org/conference/usenixsecurity25"
corresponding: ["Zhuotao Liu"]
group_authors: [1,3]
topics: ["Secure Networking and Systems Infrastructure","AI-Driven Traffic Analysis","Encrypted Traffic Analysis"]
aliases: ["/publications/secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-8/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:D_sINldO8mEC"
---

Learning-based traffic analysis models exhibit significant vulnerabilities to adversarial attacks. Attackers can compromise these models by generating adversarial network flows with precisely optimized perturbations. These perturbations typically take two forms: additive modifications, which include packet length padding and timing delays, and discrete alterations, such as dummy packet insertion. In response to these threats, certified robustness has emerged as a promising methodology for ensuring reliable model performance in the presence of adversarially manipulated network traffic. However, current approaches inadequately address the multi-modal nature of adversarial perturbations in network traffic, resulting in limited robustness guarantees against sophisticated attacks. To overcome this limitation, we introduce CertTA, the first solution providing certifiable robustness against multi-modal adversarial attacks in traffic analysis models. CertTA incorporates a novel multi-modal smoothing mechanism that explicitly accounts for attack-induced perturbations during the generation of smoothing samples, based on which CertTA rigorously derives robustness regions that are meaningful against these attacks. We implement a prototype of CertTA and extensively evaluate it against three categories of multi-modal adversarial attacks across six traffic analysis models and two datasets. Our experimental results demonstrate that CertTA provides significantly stronger robustness guarantees than the state-of-the-art approaches when confronting adversarial attacks. Further, CertTA is universally applicable across diverse model architectures and flow representations.
