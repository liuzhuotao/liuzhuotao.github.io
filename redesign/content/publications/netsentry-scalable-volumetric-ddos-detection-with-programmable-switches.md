---
title: "NetSentry: Scalable volumetric DDoS detection with programmable switches"
authors: ["Junchen Pan", "Kunpeng He", "Lei Zhang", "Zhuotao Liu", "Xinggong Zhang", "Yong Cui"]
venue: "2024 IEEE/ACM 32nd International Symposium on Quality of Service (IWQoS)"
year: 2024
paper: "https://ieeexplore.ieee.org/abstract/document/10682912/"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:738O_yMBCRsC"
# Metadata source: https://openalex.org/W4402897266
auto_enrich: true
---

<!-- Abstract source: https://openalex.org/W4402897266 -->
Distributed Denial of Service (DDoS) attack is a critical and persistent threat to the Internet. Recent DDoS detection schemes based on emerging programmable switches can achieve higher processing throughput and improve detection accuracy. However, with limited data plane memory, such schemes are not suitable for handling a large number of concurrent flows. Prior arts that attempt to increase memory efficiency have failed to do so without the expense of cost and accuracy. In this paper, we propose NetSentry, the first programmable switch based dynamic pooled testing DDoS detector. NetSentry detects DDoS in a pooled testing manner, where multiple flows are grouped to share the same storage unit on the data plane. NetSentry designs an elastic flow aggregation mechanism to dynamically adjust the detection granularity. Further, to achieve accurate DDoS detection for aggregated flows, NetSentry implements frequency domain DDoS detection on programmable switches. Evaluations of NetSentry’s hardware prototype show that NetSentry can achieve better accuracy while saving up to 91% of the data plane memory required to store flow features compared to the state-of-the-art programmable switch-based flow classification scheme.
