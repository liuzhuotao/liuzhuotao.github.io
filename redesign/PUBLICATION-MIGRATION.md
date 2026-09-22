# Publication archive migration

The redesign contains **58 unique publication records**, all imported from the
legacy `content/publications/` archive at repository commit
`0b680aedcfeaabbe8c19fe0a7adc69c9e5051ed5`. No source publications were removed,
merged, or rewritten. Euston, RingSG, and PRED remain selected for the homepage,
with `selected_order: 1`, `2`, and `3` respectively. The other 55 records appear
only in the complete list by default.

## One collection to maintain

Edit the files in `redesign/content/publications/`. Each publication has one file
used by both the complete list and, when `selected: true`, the homepage.
The required fields remain only `title`, `authors`, `venue`, and `year`.
`selected` and `selected_order` are optional. All other migrated metadata is
optional too; a new entry never needs to copy a large form.

The migration script is a historical import helper, not the updating workflow.
It uses Ruby's standard library and accepts only an empty staging directory:

```sh
ruby redesign/scripts/migrate-publications.rb --output /tmp/publication-import
```

It never writes into the maintained collection automatically. Do not copy a fresh
legacy import over subsequent manual edits. Day-to-day updates use the Markdown
files directly.

## Completeness and preservation

- **58 source files → 58 records**; **58 distinct titles** after case/whitespace
  normalization. There were no duplicates to deduplicate. A count of 57 can result
  from counting the `publication` field: 57 files have that field, including three
  empty values; the fourth Agent Security preprint has no `publication` field.
- Every original title and author position is retained. Author identifiers with
  an existing profile are expanded to that profile's display name. Literal author
  names are not corrected, reordered, removed, or merged.
- **54 abstracts** are copied from source front matter into each file's Markdown
  body. YAML line folding is decoded; the wording is retained. Four source records
  have no abstract and keep an empty body.
- **49 paper links**, **13 code links**, **10 PDF links**, and **39 conference links**
  retain their exact original URLs. Four explicitly identified arXiv preprints
  become `paper: https://arxiv.org/abs/<source-id>`, including each version suffix.
- **Four awards on three papers** are preserved as award lists, including both
  awards for *Learning with Semantics*.
- **16 corresponding-author annotations** and **one equal-contribution pair**
  retain their original author association using `corresponding` and
  `equal_contribution` lists.
- Group-member underlines from existing author profiles are preserved on **12
  papers** through `group_authors`, a list of **one-based author positions**.
  Positions distinguish different people who share the same displayed name.
- `topics` preserves the legacy broad section, subsection, and `Subtype` labels
  (identical labels are included once). Interoperability has no legacy section
  index, so its human-readable label comes from its existing directory name.
- Every record preserves its legacy publication URL as a Hugo `aliases` entry.
  The old mixed-case `ddoS_attack_prevention` directory is lowercased to match
  Hugo's canonical generated URLs. These aliases are routing metadata, optional
  when adding a brand-new publication.
- The publication year comes from the source `date`. Venue fields are condensed
  into a single familiar label, such as ACM CCS or USENIX Security; all four
  Agent Security papers are explicitly labelled arXiv preprint based on their
  existing arXiv link records. The legacy FC-BGP preprint retains its preprint
  status. Layout-only sequence numbers and duplicated venue/year fields are
  removed.

Year totals: 2026 **9**, 2025 **11**, 2024 **9**, 2023 **10**, 2022 **8**,
2021 **2**, 2019 **4**, 2018 **3**, 2017 **1**, 2016 **1**.

## Source issues retained for review

The migration does not silently invent missing bibliography information:

- *Blind Gods and Broken Screens* lists author ID `guosheng`, for which the
  source has no author profile. That exact identifier remains in `authors` until
  the correct display name is confirmed.
- *martFL* contains both profile ID `liqi` (displayed as Qi Li) and a separate
  literal `Qi Li`. Both author positions remain. Only the first carries the
  original group-member annotation. This is not treated as a duplicate author.
- Literal source spellings remain, including `Hanling Huang` in *Revisiting
  Random Early Detection* and `Li Qi` in *Defending Against Data Reconstruction
  Attacks*. These are not changed based on similarity to other names.
- The title *Training Robust Classifiers for Classfiying Encrypted Traffic under
  Dynamic Network Conditions* retains the source spelling `Classfiying`.
- Four NDSS 2026 records lack both an abstract and a paper URL in the source:
  *Achieving Interpretable DL-based Web Attack Detection through Malicious Payload
  Localization*; *Enhancing Website Fingerprinting Attacks against Traffic Drift*;
  *A Universal Black-Box Evasion Attack against ML-based Malicious Traffic Detection
  Systems*; and *Understanding the Stealthy BGP Hijacking Risk in the ROV Era*.
  Their existing conference URLs are retained. Missing abstracts and paper URLs
  have not been fabricated.
- Some links originally labelled `pdf` lead to an arXiv abstract page. Their exact
  original destinations are retained.

## Source-to-file mapping

Source paths below are relative to legacy `content/publications/`; maintained
files are relative to `redesign/content/publications/`.

| Legacy source | Maintained file | Year |
| --- | --- | --- |
| `ai_and_data_security/agent_security/2-4-1.md` | `blocka2a.md` | 2025 |
| `ai_and_data_security/agent_security/2-4-2.md` | `agentic-privacy-preserving-machine-learning.md` | 2025 |
| `ai_and_data_security/agent_security/2-4-3.md` | `anonymization-enhanced-privacy-protection-for-mobile-gui-agents-available-but-invisible.md` | 2026 |
| `ai_and_data_security/agent_security/2-4-4.md` | `blind-gods-and-broken-screens-architecting-a-secure-intent-centric-mobile-agent-operating-system.md` | 2026 |
| `ai_and_data_security/ai_security/2-3-1.md` | `provenance-of-training-without-training-data-towards-privacy-preserving-dnn-model-ownership-verification.md` | 2023 |
| `ai_and_data_security/ai_security/2-3-2.md` | `good-learning-bad-performance-a-novel-attack-against-rl-based-congestion-control-systems.md` | 2022 |
| `ai_and_data_security/ai_security/2-3-3.md` | `a-hard-label-black-box-adversarial-attack-against-graph-neural-networks.md` | 2021 |
| `ai_and_data_security/ai_security/2-3-4.md` | `detection-of-adversarial-attacks-via-disentangling-natural-images-and-perturbations.md` | 2024 |
| `ai_and_data_security/federated_learning/2-2-2.md` | `defending-against-data-reconstruction-attacks-in-federated-learning-an-information-theory-approach.md` | 2024 |
| `ai_and_data_security/privacy-preserving_machinelearning/2-1-1.md` | `pencil.md` | 2024 |
| `ai_and_data_security/privacy-preserving_machinelearning/2-1-2.md` | `cognn.md` | 2024 |
| `ai_and_data_security/privacy-preserving_machinelearning/2-1-3.md` | `ringsg.md` | 2025 |
| `ai_and_data_security/privacy-preserving_machinelearning/2-1-4.md` | `euston.md` | 2026 |
| `networking_infrastructure_for_ai/datacenter_networking/3-1-1.md` | `pred.md` | 2025 |
| `networking_infrastructure_for_ai/datacenter_networking/3-1-2.md` | `change-management-in-physical-network-lifecycle-automation.md` | 2023 |
| `networking_infrastructure_for_ai/datacenter_networking/3-1-3.md` | `threshold-based-routing-topology-co-design-for-optical-data-center.md` | 2023 |
| `networking_infrastructure_for_ai/datacenter_networking/3-1-4.md` | `enabling-work-conserving-bandwidth-guarantees-for-multi-tenant-datacenters-via-dynamic-tenant-queue-binding.md` | 2018 |
| `networking_infrastructure_for_ai/datacenter_networking/3-1-5.md` | `efficient-forwarding-anomaly-detection-in-software-defined-networks.md` | 2021 |
| `networking_infrastructure_for_ai/datacenter_networking/3-1-6.md` | `managing-recurrent-virtual-network-updates-in-multi-tenant-datacenters-a-system-perspective.md` | 2019 |
| `networking_infrastructure_for_ai/datacenter_networking/3-1-7.md` | `diffecn.md` | 2025 |
| `networking_infrastructure_for_ai/datacenter_networking/3-1-8.md` | `revisiting-random-early-detection-tuning-for-high-performance-datacenter-networks.md` | 2025 |
| `networking_infrastructure_for_ai/intelligent_network_architecture/3-2-1.md` | `brain-on-switch.md` | 2024 |
| `networking_infrastructure_for_ai/intelligent_network_architecture/3-2-2.md` | `an-efficient-design-of-intelligent-network-data-plane.md` | 2023 |
| `networking_infrastructure_for_ai/intelligent_network_architecture/3-2-3.md` | `flowtele.md` | 2022 |
| `networking_infrastructure_for_ai/intelligent_network_architecture/3-2-4.md` | `pegasus.md` | 2025 |
| `networking_infrastructure_for_ai/intelligent_network_architecture/3-2-5.md` | `achieving-interpretable-dl-based-web-attack-detection-through-malicious-payload-localization.md` | 2026 |
| `secure_networking_and_systems_infrastructure/ddoS_attack_prevention/1-3-1.md` | `middlepolice.md` | 2016 |
| `secure_networking_and_systems_infrastructure/ddoS_attack_prevention/1-3-2.md` | `practical-proactive-ddos-attack-mitigation-via-endpoint-driven-in-network-traffic-control.md` | 2018 |
| `secure_networking_and_systems_infrastructure/ddoS_attack_prevention/1-3-3.md` | `effective-ddos-mitigation-via-ml-driven-in-network-traffic-shaping.md` | 2024 |
| `secure_networking_and_systems_infrastructure/ddoS_attack_prevention/1-3-4.md` | `umbrella.md` | 2019 |
| `secure_networking_and_systems_infrastructure/ddoS_attack_prevention/1-3-5.md` | `dynamic-network-security-function-enforcement-via-joint-flow-and-function-scheduling.md` | 2022 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-1.md` | `robust-multi-tab-website-fingerprinting-attacks-in-the-wild.md` | 2023 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-10.md` | `enhancing-website-fingerprinting-attacks-against-traffic-drift.md` | 2026 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-11.md` | `a-universal-black-box-evasion-attack-against-ml-based-malicious-traffic-detection-systems.md` | 2026 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-12.md` | `learning-flow-semantics-for-encrypted-traffic-analysis-a-contrastive-pre-training-approach.md` | 2026 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-13.md` | `towards-practical-few-shot-multi-tab-website-fingerprinting.md` | 2026 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-2.md` | `learning-from-limited-heterogeneous-training-data-meta-learning-for-unsupervised-zero-day-web-attack-detection-across-web-domains.md` | 2023 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-3.md` | `low-quality-training-data-only-a-robust-framework-for-detecting-encrypted-malicious-network-traffic.md` | 2024 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-4.md` | `towards-fine-grained-webpage-fingerprinting-at-scale.md` | 2024 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-5.md` | `automated-multi-tab-website-fingerprinting-attack.md` | 2022 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-6.md` | `mm4flow.md` | 2025 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-7.md` | `trafficformer.md` | 2025 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-8.md` | `certta.md` | 2025 |
| `secure_networking_and_systems_infrastructure/encrypted_traffic_analysis/1-2-9.md` | `training-robust-classifiers-for-classfiying-encrypted-traffic-under-dynamic-network-conditions.md` | 2025 |
| `secure_networking_and_systems_infrastructure/secure_internet_routing/1-1-1.md` | `learning-with-semantics-towards-a-semantics-aware-routing-anomaly-detection-system.md` | 2024 |
| `secure_networking_and_systems_infrastructure/secure_internet_routing/1-1-2.md` | `secure-inter-domain-routing-and-forwarding-via-verifiable-forwarding-commitments.md` | 2023 |
| `secure_networking_and_systems_infrastructure/secure_internet_routing/1-1-3.md` | `enabling-efficient-source-and-path-verification-via-probabilistic-packet-marking.md` | 2018 |
| `secure_networking_and_systems_infrastructure/secure_internet_routing/1-1-4.md` | `understanding-the-stealthy-bgp-hijacking-risk-in-the-rov-era.md` | 2026 |
| `secure_networking_and_systems_infrastructure/systems_security/1-4-1.md` | `back-propagating-system-dependency-impact-for-attack-investigation.md` | 2022 |
| `secure_networking_and_systems_infrastructure/systems_security/1-4-2.md` | `rapidpatch.md` | 2022 |
| `secure_networking_and_systems_infrastructure/systems_security/1-4-3.md` | `cross-container-attacks-the-bewildered-ebpf-on-clouds.md` | 2023 |
| `secure_networking_and_systems_infrastructure/systems_security/1-4-4.md` | `unsupervised-contextual-anomaly-detection-for-database-systems.md` | 2022 |
| `secure_networking_and_systems_infrastructure/systems_security/1-4-5.md` | `deepintent.md` | 2019 |
| `secure_networking_and_systems_infrastructure/systems_security/1-4-6.md` | `torpolice.md` | 2017 |
| `web3_and_block_chain/interoperability/4-1-1.md` | `hyperservice.md` | 2019 |
| `web3_and_block_chain/web3_infra_and_application/4-2-1.md` | `make-web3-0-connected.md` | 2022 |
| `web3_and_block_chain/web3_infra_and_application/4-2-2.md` | `isyn.md` | 2023 |
| `web3_and_block_chain/zero_knowledge_proof/4-3-1.md` | `martfl.md` | 2023 |
