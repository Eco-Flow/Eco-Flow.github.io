---
layout: pipeline
title: "nf-core/genomeqc"
nav_order: 6
status: In development
summary: "Assess genome assembly and annotation quality with an ensuite of tools, plus phylogeny."
---

<img src="/img/genomeqc-logo.png" />

**nf-core/genomeqc** is an **[nf-core pipeline](https://github.com/nf-core/genomeqc)** written in Nextflow designed to assess the quality of genome assemblies and their respective annotations using an ensuite of tools and custom scripts.

### Overview

**nf-core/genomeqc** assessess the assembly quality based on:

- **Contiguity:**
  - Metrics such as the N50.
- **Completeness:**
  - Presence of telomeric repeats Benchmarking Universal Single-Copy Orthologs, and k-amers.
- **Contamination:**
  - Genome contamination screening.
  - Sequence clasiffication (Archaea, Bacteria, Prokarya, Eukaryota, organelles or unknown).
- **Other**:
  - Presence and number of Transposable Elements.
  - Gene stats (gene number, overlapping genes, mean gene length, etc.).

Additionally, the pipeline runs OrthoFinder for phylogenetic orthology inference and plots the results in an easy-to-visualize and comparable way.

<img src="/img/genomeqc-tree-plot.png" />

For additional details, usage instructions, and examples, please refer to the [nf-core/genomeqc GitHub repository](https://github.com/nf-core/genomeqc).