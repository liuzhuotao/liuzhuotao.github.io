---
title: "Stable byzantine fault tolerance in wide area networks with unreliable links"
authors: ["Sitong Ling", "Zhuotao Liu", "Qi Li", "Xinle Du", "Jing Chen", "Ke Xu"]
venue: "IEEE/ACM ToN"
year: 2024
paper: "https://ieeexplore.ieee.org/abstract/document/10695774/"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:WbkHhVStYXYC"
# Metadata source: https://openalex.org/W4402892212
auto_enrich: true
---

<!-- Abstract source: https://openalex.org/W4402892212 -->
With the increasing demand for blockchain technology in various industry sectors, there has been a growing interest in the Byzantine Fault Tolerance (BFT) consensus that is the backbone of most of these blockchains. However, many state-of-the-art algorithms that require reliable connections can only offer limited throughput in wide-area networks (WANs), where participants are connected over long distances and may experience unpredictable network failures. The partially-connected BFTs are designed for unreliable and highly dynamic networks yet impose exponential communication complexity. This paper proposes Stable Byzantine Fault Tolerance (SBFT), a BFT communication abstraction that can sustain high throughput and low latency in WAN. SBFT separates the leader from consensus in pipelined BFT consensus and uses an adaptive consensus mechanism to resist dynamic faulty links, maintaining consensus efficiency when network connectivity is high while adapting to dynamic networks with low connectivity. We implemented a prototype of SBFT and tested it on the WAN. The results demonstrate that SBFT has a throughput similar to HotStuff in a fault-free environment but can reduce about 80% of consensus latency. Besides, SBFT retains 40% of the original throughput when the link failure probability is 0.4, while the baseline HotStuff retains less than 40% when the link failure probability is only 0.1.
