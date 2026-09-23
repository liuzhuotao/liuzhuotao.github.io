---
title: "Understanding the Security Boundary of Obfuscation-based On-Device LLM Protection"
authors: ["Hanyi Zhou", "Chenyang Li", "Yuanzhe Pang", "Ke Xu", "Mingwei Xu", "Zhuotao Liu"]
venue: "ACM CCS"
year: 2026
corresponding: ["Zhuotao Liu"]
selected: true
paper: "https://arxiv.org/abs/2609.10117"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:N5tVd3kTz84C"
# Metadata source: https://openalex.org/W7212136445
preprint: "https://arxiv.org/abs/2609.10117"
auto_enrich: true
---

<!-- Abstract source: https://openalex.org/W7212136445 -->
Trusted Execution Environments (TEEs) offer a promising mechanism for safeguarding the intellectual property of on-device Large Language Models (LLMs). To overcome the inherent computational bottlenecks of TEEs, existing TEE-Shielded LLM Partition (TSLP) methods apply efficient obfuscation schemes to computationally intensive layers, offloading them to external GPUs while retaining only lightweight operations within the TEE. Although a growing body of TSLP-based approaches has emerged, these defense mechanisms remain largely heuristic. Consequently, some methods are proven vulnerable to certain specialized adversarial attacks designed to exploit their specific architectural implementations. To overcome the limitations of these heuristic designs, this paper addresses a fundamental research question: can we establish common primitives to unify representative prior methodologies, characterize the security boundary of their compositions, and systematically extend them? To this end, we formalize a set of obfuscation primitives, defined as dual-tuples of linear computations satisfying specific algebraic properties. We demonstrate that the matrix-level weight transformations of several representative efficient TSLP frameworks can be expressed as compositions of these primitives; consequently, the canonical form of these primitive compositions, denoted as \\priorboundary, defines the security boundary of this primitive family. We then expose the vulnerabilities of \\priorboundary through a novel primitive-guided attack methodology, \\sysattack, demonstrating a shared vulnerability in several prominent TSLP methods published in top-tier venues, such as ArrowCloak (Security'25), TSQP (S\\&amp;P'25), and LoRO (NeurIPS'25). Finally, we introduce two novel obfuscation primitives and integrate them with existing constructs to formulate \\sysdefense, extending the prior security boundary \\priorboundary.
