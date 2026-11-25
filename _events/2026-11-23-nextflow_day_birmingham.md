---
title: 'Nextflow and nf-core training day, University of Birmingham'
date: 2026-11-23
description: 'A full day of Nextflow and nf-core training for MSc Bioinformatics students at the University of Birmingham: a morning lecture on pipeline languages and writing Nextflow, then an afternoon practical in GitHub Codespaces with Hello Nextflow and nf-core/rnaseq.'
author: 'Christopher Wyatt'
host: birmingham
role: delivering
location: Birmingham, UK
type: [training]
tags: ["nextflow", "nf-core", "training", "rnaseq", "codespaces", "genomics"]
---

<img src="{{ '/img/birmingham-great-hall.webp' | relative_url }}" alt="The red-brick Great Hall of the University of Birmingham, with the Old Joe clock tower rising behind it">
<p style="text-align:center; font-size:.82rem; color:#8a9890; margin-top:-.9rem;">The Great Hall and Old Joe, University of Birmingham. <em>Photo: <a href="https://commons.wikimedia.org/wiki/File:Great_Hall_seen_in_line_with_the_clock_tower.jpg">Tom Axford</a>, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC&nbsp;BY-SA&nbsp;4.0</a> (Wikimedia&nbsp;Commons).</em></p>

On **Monday 23 November 2026**, Chris Wyatt from Eco-Flow and **[Yunjia Zhang](https://www.linkedin.com/in/yunjiazhang/)**, a Nextflow Ambassador from the **Wellcome Sanger Institute**, delivered a full day of Nextflow and nf-core training for MSc Bioinformatics students at the **University of Birmingham**. Organised by **[Deena Mohamad Gendoo](https://www.linkedin.com/in/deena-mohamad-gendoo-b4979b50/)**, the training brought together practical introductions to workflow development, the nf-core community and running production-ready bioinformatics pipelines.

### Who it was for

38 first-semester MSc Bioinformatics students, already comfortable with R, the Linux shell and core genomics. Five teaching assistants supported the afternoon practical.

### Built into the Genomics module

Deena scheduled the day at the end of the course's Genomics module and told us beforehand exactly what the students had covered, which made it easy to build on. In that module they had built a variant-calling pipeline by hand, running and checking every step from FASTQ to BAM to VCF themselves.

We started by revisiting the commands the students had used to process a single sample, from FASTQ files through quality control (FastQC), alignment (minimap2), and variant calling (samtools and DeepVariant). We then demonstrated how these individual commands could be organised into Nextflow processes and connected together into a reproducible workflow.

### How the sessions fit together

Yunjia and Chris took turns through the morning, and each session picked up where the last one left off:

- **Working with a pipeline language** (Yunjia): Introducing the concept of workflow languages using a Lego analogy to explain how individual components fit together.
- **Introduction to Nextflow** (Chris): Introducing how processes do the work and channels move the data, shown on the same QC, alignment and variant-calling steps. And why reproducibility is key!
- **Coding in Nextflow** (Yunjia): Putting the building blocks together by recreating the students' variant-calling workflow in Nextflow.
- **What's nf-core?** (Chris): Introducing the nf-core community, its pipelines, reusable modules and best-practice approaches to developing bioinformatics workflows.

In the afternoon the students met the same ideas from both sides: first writing their own pipeline in Hello Nextflow, then running a large community pipeline, nf-core/rnaseq.

### The programme

A two-hour lecture in the morning, then a three-hour hands-on practical in a computer cluster.

| Time | Session |
|---|---|
| 10:00 | Welcome and training goals |
| 10:15 | Working with a pipeline language |
| 10:30 | Introduction to Nextflow |
| 10:50 | Q&A |
| 11:00 | Coding in Nextflow |
| 11:45 | What's nf-core? |
| 12:00 | Lunch |
| 13:00 | Codespace setup |
| 13:10 | Command line basics |
| 13:20 | Hello Nextflow: writing a first pipeline |
| 14:20 | Coffee break |
| 14:30 | Running [nf-core/rnaseq](https://nf-co.re/rnaseq) |
| 15:30 | Advanced tools by Seqera |
| 15:40 | Running pipelines on HPC |
| 15:50 | Wrap-up and questions |

Everything ran in the browser through **GitHub Codespaces**, so students had nothing to install.

### Keep learning

- **[Hello Nextflow](https://training.nextflow.io/)**, the course behind the afternoon's first practical, is free online. *Nextflow for Genomics*, on the same site, is the natural next step after a genomics module.
- **[Run an nf-core RNA-Seq pipeline]({{ '/training/nfcore-rnaseq/' | relative_url }})** is the Eco-Flow lesson we used for the nf-core/rnaseq run. The **[full Eco-Flow training course]({{ '/training/' | relative_url }})** goes further, with HPC, differential expression in R and amplicon analysis.

It was great teaching alongside Yunjia for the first time. Thank you to Deena for inviting us and for making the day so interactive and motivating the students, to the TAs for their help, and to all the students who took part.
