---
title: "Towards Practical Few-shot Multi-tab Website Fingerprinting"
authors: ["Lin Liu","Ziling Wei","Zhuotao Liu","Xinhao Deng","Zixuan Dong","Shuhui Chen"]
venue: "USENIX Security"
year: 2026
corresponding: ["Zhuotao Liu"]
paper: "https://www.usenix.org/conference/usenixsecurity26/presentation/liu-lin"
conference: "https://www.usenix.org/conference/usenixsecurity26/"
topics: ["Secure Networking and Systems Infrastructure","AI-Driven Traffic Analysis","Encrypted Traffic Analysis"]
aliases: ["/publications/secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-13/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:SdhP9T11ey4C"
---

Website fingerprinting (WF) attacks can infer the visited websites to deanonymize Tor networks by analyzing encrypted traffic patterns. Recent few-shot WF methods reduce reliance on large-scale data collection, yet they predominantly formulate WF as a single-label classification task and rely on meta-learning episodes that assume disjoint label sets and stable embedding spaces. These assumptions break down in the realistic multi-tab browsing, where traffic from multiple websites interleaves within a single observation window and the number of concurrent tabs is unknown. Meanwhile, the label space grows exponentially as the monitored set expands, making existing multi-tab WF methods costly to update. To address these challenges, we propose MMF, a novel framework for few-shot multi-tab WF. MMF shifts the meta-learning objective from single-label classification to support-guided presence detection. In each episode, we pair a mixed multi-tab query trace with a small set of single-tab support traces for each monitored website, and generate class-specific features by feature reweighting to decide which websites are present. This detection-centric formulation yields well-defined few-shot tasks in multi-tab scenarios and enables MMF to detect previously unseen websites from limited traces. We evaluate MMF on established public datasets and a new real-world dataset collected under varied browsing conditions. Results demonstrate that MMF consistently outperforms state-of-the-art multi-tab WF attacks across all settings. Notably, in the 5-shot scenario, MMF achieves improvements of up to 300% in Novel Precision@k, highlighting its strong capability for few-shot detection in dynamically growing website sets.
