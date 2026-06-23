---
layout: pipeline
title: "Eco-Flow/nanoporemetabarcoding"
nav_order: 4
status: In development
summary: "Process and annotate nanopore metabarcoding data across taxonomic levels."
redirect_from:
  - /pipelines/nanoporemetabarcoding.html
---

**Eco-Flow/nanoporemetabarcoding** is a **Nextflow pipeline** -written using the **[nf-core standards](https://nf-co.re/)**- for processing -quality control, demultiplexing, and clustering- and annotate **nanopore metabarcoding data**. Annotation is performed at different taxonomic levels on the consensus sequences, using the **BLASTnt database** and **taxonomizr**.

### Overview

Overall, the pipeline performs the following steps:

- Performs read filtering, trimming, and quality control on both raw and processed sequencing reads.
- Demultiplexes reads based on tag–primer combinations
- Groups amplicon reads into 'species' consensus sequences
- Annotates consensus sequences based on the best matching reference hit against BLAST database
- Assigns taxonomy to annotated sequences using NCBI taxonomy identifiers

For additional details, usage instructions, and examples, please refer to the [Eco-Flow/nanoporemetabarcding GitHub repository](https://github.com/Eco-Flow/nanoporemetabarcoding).