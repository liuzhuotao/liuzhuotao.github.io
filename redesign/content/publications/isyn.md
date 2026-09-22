---
title: "iSyn: Semi-Automated Smart Contract Synthesis from Legal Financial Agreements"
authors: ["Pengcheng Fang","Zhenhua Zou","Xusheng Xiao","Zhuotao Liu"]
venue: "ACM ISSTA"
year: 2023
paper: "https://dl.acm.org/doi/abs/10.1145/3597926.3598091"
conference: "https://conf.researchr.org/home/issta-2023"
corresponding: ["Zhuotao Liu"]
selected: true
group_authors: [2]
topics: ["Web3.0 and Blockchain","Web3.0 Infra and Application","Web3 & Block Chain"]
aliases: ["/publications/web3_and_block_chain/web3_infra_and_application/4-2-2/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:3s1wT3WcHBgC"
---

Embracing software-driven smart contracts to fulfill legal agreements is a promising direction for digital transformation in the legal sector. Existing solutions mostly consider smart contracts as simple add-ons, without leveraging the programmability of smart contracts to realize complex semantics of legal agreements. In this paper, we propose iSyn, the first end-to-end system that synthesizes smart contracts to fulfill the semantics of financial legal agreements, with minimal human interventions. The design of iSyn centers around a novel intermediate representation (SmartIR) that closes the gap between the natural language sentences and smart contract statements. Specifically, iSyn includes a synergistic pipeline that unifies multiple NLP-techniques to accurately construct SmartIR instances given legal agreements, and performs template-based synthesis based on the SmartIR instances to synthesize smart contracts. We also design a validation framework to verify the correctness and detect known vulnerabilities of the synthesized smart contracts. We evaluate iSyn using legal agreements centering around financial transactions. The results show that iSyn-synthesized smart contracts are syntactically similar and semantically correct (or within a few edits), compared with the "ground truth" smart contracts manually developed by inspecting the legal agreements.
