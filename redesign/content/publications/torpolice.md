---
title: "TorPolice: Towards enforcing service-defined access policies for anonymous communication in the Tor network"
authors: ["Zhuotao Liu","Yushan Liu","Philipp Winter","Prateek Mittal","Yih-Chun Hu"]
venue: "IEEE ICNP"
year: 2017
paper: "https://ieeexplore.ieee.org/abstract/document/8117564"
conference: "https://iqua.ece.toronto.edu/icnp17/"
topics: ["Secure Networking and Systems Infrastructure","Systems Security","System Security"]
aliases: ["/publications/secure_networking_and_systems_infrastructure/systems_security/1-4-6/"]
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:_FxGoFyzp5QC"
---

Tor is the most widely used anonymity network, currently serving millions of users each day. However, there is no access control in place for all these users, leaving the network vulnerable to botnet abuse and attacks. For example, criminals frequently use exit relays as stepping stones for attacks, causing service providers to serve CAPTCHAs to exit relay IP addresses or blacklisting them altogether, which leads to severe usability issues for legitimate Tor users. To address this problem, we propose TorPolice, the first privacy-preserving access control framework for Tor. TorPolice enables abuse-plagued service providers such as Yelp to enforce access rules to police and throttle malicious requests coming from Tor while still providing service to legitimate Tor users. Further, TorPolice equips Tor with global access control for relays, enhancing Tor's resilience to botnet abuse. We show that TorPolice preserves the privacy of Tor users, implement a prototype of TorPolice, and perform extensive evaluations to validate our design goals.
