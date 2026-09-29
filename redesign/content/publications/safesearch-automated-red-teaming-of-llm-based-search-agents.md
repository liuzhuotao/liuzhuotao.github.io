---
title: "SafeSearch: Automated Red-Teaming of LLM-Based Search Agents"
authors: ["Jianshuo Dong", "Sheng Guo", "Hao Wang", "Xun Chen", "Zhuotao Liu", "Tianwei Zhang", "Ke Xu", "Minlie Huang", "Han Qiu"]
venue: "ICML"
year: 2026
paper: "https://arxiv.org/abs/2509.23694"
scholar: "https://scholar.google.com/citations?view_op=view_citation&user=F8gi4rcAAAAJ&citation_for_view=F8gi4rcAAAAJ:eq2jaN3J8jMC"
# Metadata source: https://arxiv.org/abs/2509.23694
preprint: "https://arxiv.org/abs/2509.23694"
auto_enrich: true
---

<!-- Abstract source: https://arxiv.org/abs/2509.23694 -->
Search agents connect LLMs to the Internet, enabling them to access broader and more up-to-date information. However, this also introduces a new threat surface: unreliable search results can mislead agents into producing unsafe outputs. Real-world incidents and our two in-the-wild observations show that such failures can occur in practice. To study this threat systematically, we propose SafeSearch, an automated red-teaming framework that is scalable, cost-efficient, and lightweight, enabling sandboxed safety evaluation of search agents. Using this, we generate 300 test cases spanning five risk categories (e.g., misinformation and prompt injection) and evaluate three search agent scaffolds across 17 representative LLMs. Our results reveal substantial vulnerabilities in LLM-based search agents, with the highest ASR reaching 90.5% for GPT-4.1-mini in a search-workflow setting. Moreover, we find that common defenses, such as reminder prompting, offer limited protection. Overall, SafeSearch provides a practical way to measure and improve the safety of LLM-based search agents.
