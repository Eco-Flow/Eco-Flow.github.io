---
layout: default
title: "Eco-Flow/excon"
nav_order: 2
---

## Eco-Flow/excon

**Eco-Flow/excon** is a **Nextflow pipeline** -written using the **[nf-core standards](https://nf-co.re/)**- that runs **gene family expansion and contraction analysis** (via CAFE). This pipeline automates the analysis to run the basic steps in EXpansion and CONtraction of gene families, as well as running GO enrichment analysis on the output.

### Overview

Roughly, the pipeline performs the following steps:

- Describes the genome assembly and annotation: completness, contiguity and general gene stats (e.g., number of genes, exons, introns).
- Identifies orthologous genes across assemblies.
- Detects gene family expansion and contraction based on orthologous gene groups.
- Performs Gene Ontology annotation on orthologous genes.

For additional details, usage instructions, and examples, please refer to the [Eco-Flow/excon GitHub repository](https://github.com/Eco-Flow/excon).
