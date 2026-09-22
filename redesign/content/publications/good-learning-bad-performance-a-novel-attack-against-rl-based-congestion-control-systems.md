---
title: "Good Learning, Bad Performance: A Novel Attack Against RL-Based Congestion Control Systems"
authors: ["Zijie Yang","Jiahao Cao","Zhuotao Liu","Xiaoli Zhang","Kun Sun","Qi Li"]
venue: "IEEE TIFS"
year: 2022
paper: "https://ieeexplore.ieee.org/abstract/document/9722881"
corresponding: ["Zhuotao Liu"]
topics: ["AI and Data Security (with Applied Cryptography)","AI Security"]
aliases: ["/publications/ai_and_data_security/ai_security/2-3-2/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:NMxIlDl6LWMC"
---

Reinforcement Learning (RL) has been applied to solve decision-making problems in computer network designs, especially in TCP congestion control. As RL-based congestion control methods enable powerful learning abilities, it achieves competitive performance and adaptiveness advantages over the traditional methods. However, RL-based systems suffer from adversarial attacks that generate perturbations to significantly degrade the performance. In this paper, we conduct a comprehensive study of adversarial attacks against RL-based congestion control systems. Unlike the state-of-the-art adversarial attacks on images where an attacker can easily obtain the input states to introduce perturbations, the attacker cannot directly obtain the input states in congestion control settings that are only available to the agents. It is challenging to add effective perturbations without knowing the input states for RL-based congestion control models. To solve the challenge, we develop an adversarial attack to estimate states of the target agent, craft adversarial perturbations, and apply the generated perturbations in an automated fashion. We evaluate how our adversarial attack affects the target agent’s decision-making process. Our experiments illustrate that our attack can effectively reduce about 50% average throughput while increasing more than 36x latency and 45% packet loss rate.
