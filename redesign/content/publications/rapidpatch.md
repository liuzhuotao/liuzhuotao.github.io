---
title: "RapidPatch: Firmware Hotpatching for Real-Time Embedded Devices"
authors: ["Yi He","Zhenhua Zou","Kun Sun","Zhuotao Liu","Ke Xu","Qian Wang","Chao Shen","Zhi Wang","Qi Li"]
venue: "USENIX Security"
year: 2022
paper: "https://www.usenix.org/conference/usenixsecurity22/presentation/he-yi"
conference: "https://www.usenix.org/conference/usenixsecurity22"
group_authors: [2]
topics: ["Secure Networking and Systems Infrastructure","Systems Security","System Security"]
aliases: ["/publications/secure_networking_and_systems_infrastructure/systems_security/1-4-2/"]
---

Nowadays real-time embedded devices are becoming one main target of cyber attacks. A huge number of embedded devices equipped with outdated firmware are subject to various vulnerabilities, but they cannot be timely patched due to two main reasons. First, it is difficult for vendors who have various types of fragmented devices to generate patches for each type of device. Second, it is challenging to deploy patches on many embedded devices without restarting or halting real-time tasks, hindering the patch installation on devices (e.g., industrial control devices) that have high availability requirements. In this paper, we present RapidPatch, a new hotpatching framework to facilitate patch propagation by installing generic patches without disrupting other tasks running on heterogeneous embedded devices. RapidPatch allows RTOS developers to directly release common patches for all downstream devices so that device maintainers can easily generate device-specific patches for different firmware. We utilize eBPF virtual machines to execute patches on resource-constrained embedded devices and develop three hotpatching strategies to support hotpatching for all major microcontroller (MCU) architectures. In particular, we propose two types of eBPF patches for different types of vulnerabilities and develop an eBPF patch verifier to ensure patch safety. We evaluate RapidPatch with major CVEs on four major RTOSes running on different embedded devices. We find that over 90% vulnerabilities can be hotpatched via RapidPatch. Our system can work on devices with 64 KB or more memory and 64 MHz MCU frequency. The average patch delay is less than 8 µs and the overall latency overhead is less than 0.6%.
