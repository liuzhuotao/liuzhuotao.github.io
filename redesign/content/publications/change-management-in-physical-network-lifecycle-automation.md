---
title: "Change Management in Physical Network Lifecycle Automation"
authors: ["Mohammad Al-Fares","Virginia Beauregard","Kevin Grant","Angus Griffith","Quan Leng","Alexander Lin","Zhuotao Liu","Bill Martinusen","Nikil Mehta","Jeffrey Mogul","Andrew Narver","Anshul Nigham","Sean Smith","Amin Vahdat"]
venue: "USENIX ATC"
year: 2023
paper: "https://www.usenix.org/conference/atc23/presentation/al-fares"
conference: "https://www.usenix.org/conference/atc23"
topics: ["Networking Infrastructure for AI","Datacenter Networking"]
aliases: ["/publications/networking_infrastructure_for_ai/datacenter_networking/3-1-2/"]
---

Automated management of a physical network's lifecycle is critical for large networks. At Google, we manage network design, construction, evolution, and management via multiple automated systems. In our experience, one of the primary challenges is to reliably and efficiently manage change in this domain -- additions of new hardware and connectivity, planning and sequencing of topology mutations, introduction of new architectures, new software systems and fixes to old ones, etc.
We especially have learned the importance of supporting multiple kinds of change in parallel without conflicts or mistakes (which cause outages) while also maintaining parallelism between different teams and between different processes. We now know that this requires automated support.
This paper describes some of our network lifecycle goals, the automation we have developed to meet those goals, and the change-management challenges we encountered. We then discuss in detail our approaches to several specific kinds of change management: (1) managing conflicts between multiple operations on the same network; (2) managing conflicts between operations spanning the boundaries between networks; (3) managing representational changes in the models that drive our automated systems. These approaches combine both novel software systems and software-engineering practices.
