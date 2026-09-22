---
title: "Anonymization-Enhanced Privacy Protection for Mobile GUI Agents: Available but Invisible"
authors: ["Lepeng Zhao","Zhenhua Zou","Shuo Li","Zhuotao Liu"]
venue: "arXiv preprint"
year: 2026
paper: "https://arxiv.org/abs/2602.10139v3"
corresponding: ["Zhuotao Liu"]
group_authors: [2]
topics: ["AI and Data Security (with Applied Cryptography)","Agent Security"]
aliases: ["/publications/ai_and_data_security/agent_security/2-4-3/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:t6usbXjVLHcC"
---

Mobile Graphical User Interface (GUI) agents have demonstrated strong capabilities in automating complex smartphone tasks by leveraging multimodal large language models (MLLMs) and system-level control interfaces. However, this paradigm introduces significant privacy risks, as agents typically capture and process entire screen contents, thereby exposing sensitive personal data such as phone numbers, addresses, messages, and financial information. Existing defenses either reduce UI exposure, obfuscate only task-irrelevant content, or rely on user authorization, but none can protect task-critical sensitive information while preserving seamless agent usability. We propose an anonymization-based privacy protection framework that enforces the principle of available-but-invisible access to sensitive data: sensitive information remains usable for task execution but is never directly visible to the cloud-based agent. Our system detects sensitive UI content using a PII-aware recognition model and replaces it with deterministic, type-preserving placeholders (e.g., PHONE_NUMBER#a1b2c) that retain semantic categories while removing identifying details. A layered architecture comprising a PII Detector, UI Transformer, Secure Interaction Proxy, and Privacy Gatekeeper ensures consistent anonymization across user instructions, XML hierarchies, and screenshots, mediates all agent actions over anonymized interfaces, and supports narrowly scoped local computations when reasoning over raw values is necessary. Extensive experiments on the AndroidLab and PrivScreen benchmarks show that our framework substantially reduces privacy leakage across multiple models while incurring only modest utility degradation, achieving the best observed privacy-utility trade-off among existing methods. Code available at: https://github.com/one-step-beh1nd/gui_privacy_protection
