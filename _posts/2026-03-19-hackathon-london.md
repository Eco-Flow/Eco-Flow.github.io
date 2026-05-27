---
title: 'nf-core hackathon London'
date: 2026-03-19
description: 'Blog post related to the nf-core hackathon we hosted in London in 2026.'
author: 'Fernando Duarte'
tags: ["nextflow", "hackathon", "nf-core", "nfcore"]
---

<img align="top" width="" src="/img/hackathon-london-2026.jpg" />

<br>

Just like we did last year, we organised a local site for the **[2026 nf-core Hackathon](https://nf-co.re/events/2025/hackathon-march-2026)** at the UCL East campus. Over the course of 3 dayss, we welcomed 25 Nextflow and nf-core enthusiasts from a range of backgrounds, spanning both academia and industry.

During the hackathon, people focused on different tasks. Some attendees worked on building **nf-core modules** (these are modules of popular bioinformatic tools, such as Blast, samtools, BUSCO, etc.). For example, one contributor tried to build an nf-core module based on [earlgrey](https://github.com/TobyBaril/EarlGrey), which is a tool for transposable elements annotation. Others worked on updating existing modules, by bumping up tool versions or adapting them to the new Nextflow syntax and channels (such as migrating to the [topic channels](https://nf-co.re/docs/developing/migration-guides/update-pipelines)).

Besides nf-core modules, we also had hackers working on their own projects. For example, the **Fungarium team from Kew Gardens** were continuing their **FSP Assembly Pipeline** development, a Nextflow and nf-core based workflow for the assembly of genomes for short-read sequencing data. The pipeline itself covers pre-processing, assembly, and quality control.

The [nf-core/gwas](https://github.com/nf-core/gwas) pipeline, which we started over a year ago, performs genome-wide association studies using [plink](https://www.cog-genomics.org/plink/). After a period of inactivity, we took this hackathon as an opportunity to bring it up to date with the latest tool versions, Nextflow syntax, and nf-core template, before handing it off to new contributors to take forward.

We also worked on [nf-core/genomeqc](https://github.com/nf-core/genomeqc), a pipeline for assessing genome assembly quality, by updating several of its nf-core modules, along with adding a repeat annotation subworkflow.

As some social highlights, we had free pizza on the first day and enjoyed a nature walk around the Queen Elizabeth Park. It was rewarding to see people engaging, making connections, and contributing to the nf-core community. **Looks like the London nf-core community is thriving!**
