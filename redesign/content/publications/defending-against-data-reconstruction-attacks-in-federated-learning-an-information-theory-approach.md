---
title: "Defending Against Data Reconstruction Attacks in Federated Learning: An Information Theory Approach"
authors: ["Qi Tan","Li Qi","Yi Zhao","Zhuotao Liu","Xiaobing Guo","Ke Xu"]
venue: "USENIX Security"
year: 2024
paper: "https://www.usenix.org/conference/usenixsecurity24/presentation/tan"
conference: "https://www.usenix.org/conference/usenixsecurity24"
topics: ["AI and Data Security (with Applied Cryptography)","Federated Learning","Data Security"]
aliases: ["/publications/ai_and_data_security/federated_learning/2-2-2/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:KxtntwgDAa4C"
---

Federated Learning (FL) trains a black-box and high-dimensional model among different clients by exchanging parameters instead of direct data sharing, which mitigates the privacy leak incurred by machine learning. However, FL still suffers from membership inference attacks (MIA) or data reconstruction attacks (DRA). In particular, an attacker can extract the information from local datasets by constructing DRA, which cannot be effectively throttled by existing techniques, e.g., Differential Privacy (DP).
In this paper, we aim to ensure a strong privacy guarantee for FL under DRA. We prove that econstruction errors under DRA are constrained by the information acquired by an attacker, which means that constraining the transmitted information can effectively throttle DRA. To quantify the information leakage incurred by FL, we establish a channel model, which depends on the upper bound of joint mutual information between the local dataset and multiple transmitted parameters. Moreover, the channel model indicates that the transmitted information can be constrained through data space operation, which can improve training efficiency and the model accuracy under constrained information. According to the channel model, we propose algorithms to constrain the information transmitted in a single round of local training. With a limited number of training rounds, the algorithms ensure that the total amount of transmitted information is limited. Furthermore, our channel model can be applied to various privacy-enhancing techniques (such as DP) to enhance privacy guarantees against DRA. Extensive experiments with real-world datasets validate the effectiveness of our methods.
