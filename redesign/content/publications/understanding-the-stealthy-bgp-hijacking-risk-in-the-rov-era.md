---
title: "Understanding the Stealthy BGP Hijacking Risk in the ROV Era"
authors: ["Yihao Chen","Qi Li","Ke Xu","Zhuotao Liu","Jianping Wu"]
venue: "NDSS"
year: 2026
conference: "https://www.ndss-symposium.org/ndss2026/"
topics: ["Secure Networking and Systems Infrastructure","Secure Internet Routing"]
aliases: ["/publications/secure_networking_and_systems_infrastructure/secure_internet_routing/1-1-4/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:dTyEYWd-f8wC"
# Metadata source: https://doi.org/10.14722/ndss.2026.230097
paper: "https://doi.org/10.14722/ndss.2026.230097"
auto_enrich: true
# Metadata source: https://openalex.org/W7161062882
preprint: "https://arxiv.org/abs/2606.23071"
---

<!-- Abstract source: https://openalex.org/W7161062882 -->
The partial deployment of Route Origin Validation (ROV) poses an unexpected security threat known as stealthy BGP hijacking, i.e., a particularly elusive form of BGP hijacking where malicious routes divert traffic without reaching (and thus alerting) the victims. This risk remains largely unexplored, with neither documented real-world incidents nor systematic characterization available. To bridge this gap, we formalize stealthy BGP hijacking and propose heuristics to discover potential instances through routing table discrepancies. We conduct the first empirical study to track and profile stealthy BGP hijacking in the wild, contributing a curated real-world incident dataset and a long-term monitoring service. Inspired by the empirical insights, we further conduct an analytical study to exhaustively assess the risk. This requires accurate ROV deployment data, complete Internet-wide routes, and tailored analytical models. To address these challenges, we develop SHAMAN, a BGP route inference framework dedicated to assessing stealthy BGP hijacking risk. SHAMAN consolidates multiple sources to construct an accurate view of ROV deployment, infers complete Internet-wide routes through a highly efficient matrix-based approach, and facilitates statistical risk analysis via a "victim-target-hijacker" 3-tuple model. By reducing the time for generating Internet-scale routes from over three months to just 5.22 hours, SHAMAN enables systematic risk assessment across 8.3 billion generated routes under real-world ROV deployment. Our findings reveal a 14.1% overall success probability for stealthy BGP hijacking, with targeted attacks reaching 99.5% success in specific cases. Validation against our real-world dataset shows up to 95.9% incident-level accuracy, demonstrating the fidelity of our analytical results.
