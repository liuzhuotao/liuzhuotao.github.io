---
title: "TrustedARI: Towards Trust-Native Agentic Routing Infrastructure for Agentic AI"
authors: ["Qi Li", "Zhenhua Zou", "Shuo Li", "Mingwei Xu", "Zhuotao Liu"]
venue: "arXiv preprint"
year: 2026
paper: "https://arxiv.org/abs/2606.15822"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:9vf0nzSNQJEC"
# Metadata source: https://openalex.org/W7164897612
preprint: "https://arxiv.org/abs/2606.15822"
auto_enrich: true
---

<!-- Abstract source: https://openalex.org/W7164897612 -->
AI agents increasingly access external models, tools, and services through Agentic Routing Infrastructure (ARI) to manage the overhead of heterogeneous interfaces and fragmented subscriptions. Yet, the architecture of ARI introduces fundamental trust risks: it obtains plaintext access to agent queries and service responses, while leaving agents unable to verify that their queries are routed to intended service providers or that requests and responses remain untampered. To address this problem, we present TrustedARI, the first trust-native agentic routing infrastructure for agentic AI. Architecturally, TrustedARI is built upon three core innovations: (i) an ARI-adapted three-party TLS handshake that enables the agent and ARI to jointly authenticate the service provider through role-specific distribution of TLS key materials; (ii) a privacy-preserving query-construction protocol that allows the agent and ARI to collaboratively construct well-formed queries without exposing their respective private inputs; and (iii) a verifiable billing protocol that supports fair usage-based settlement while preserving the integrity and confidentiality of service responses. We implemented and extensively evaluated a prototype of TrustedARI to validate its performance. Experiments confirm that TrustedARI is highly efficient: our ARI-adapted handshake protocol reduces communication overhead by 39.34% compared to the existing three-party TLS handshake. Furthermore, the privacy-preserving query-construction protocol imposes negligible overhead-averaging 0.19 seconds in computation time and 0.58 MB in communication costs-while the verifiable billing protocol speeds up proof generation by 28.20x. Crucially, TrustedARI is readily deployable without any modification to the service providers.
