---
title: "UAV-enabled federated learning in dynamic environments: Efficiency and security trade-off"
authors: ["Xiaokun Fan", "Yali Chen", "Min Liu", "Sheng Sun", "Zhuotao Liu", "Ke Xu", "Zhongcheng Li"]
venue: "IEEE TVT"
year: 2023
paper: "https://ieeexplore.ieee.org/abstract/document/10375744/"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:bFI3QPDXJZMC"
# Metadata source: https://openalex.org/W4390357346
auto_enrich: true
---

<!-- Abstract source: https://openalex.org/W4390357346 -->
Unmanned aerial vehicles (UAVs) can be deployed as flying base stations to provide wireless communication and machine learning (ML) training services for ground user equipments (UEs). Due to privacy concerns, many UEs are not willing to send their raw data to the UAV for model training. Fortunately, federated learning (FL) has emerged as an effective solution to privacy-preserving ML. To balance efficiency and wireless security, this paper proposes a novel secure and efficient FL framework in UAV-enabled networks. Specifically, we design a secure UE selection scheme based on the secrecy outage probability to prevent uploaded model parameters from being wiretapped by a malicious eavesdropper. Then, we formulate a joint UAV placement and resource allocation problem for minimizing training time and UE energy consumption while maximizing the number of secure UEs under the UAV's energy constraint. Considering the random movement of the eavesdropper and UEs as well as online task generation on UEs in practical application scenarios, we present the long short-term memory (LSTM)-based deep deterministic policy gradient (DDPG) algorithm (LSTM-DDPG) to facilitate real-time decision making for the formulated problem. Finally, simulation results show that the proposed LSTM-DDPG algorithm outperforms the state-of-arts in terms of efficiency and security of FL.
