---
layout: pipeline
title: "Eco-Flow/synteny"
nav_order: 3
status: Released
summary: "Compare gene macrosynteny between chromosome-level genome assemblies."
redirect_from:
  - /pipelines/synteny.html
---

**Eco-Flow/synteny** is a **Nextflow pipeline** -written using the **[nf-core standards](https://nf-co.re/)**- for comparing **gene synteny** between chromosome level genome assemblies. It takes genomes and annotations files as inputs and assesses **macrosynteny** using a suit of tools.

### Overview

At a high level, the workflow performs the following steps:

- Downloads chromosome-level genome assemblies and annotations.
- Identifies orthologous genes across species.
- Detects syntenyc blocks and structural rearrangements.
- Produces synteny visualizations and summary tables.

<!-- Synteny is the study of chromosome arrangement and gene order. Over evolutionary time, two species diverge from the state of the common ancestor, due to a variety of structural changes. These include indels, inversions, translocations, fusions and fissions. This pipeline aims to produce common synteny plots, as well as tables documenting the types of syntenic changes. -->

<img src="/img/synteny.png" />

For additional details, usage instructions, and examples, please refer to the [Eco-Flow/synteny GitHub repository](https://github.com/Eco-Flow/synteny).
