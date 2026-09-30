---
title: 'Nextflow: Reproducible Scientific Workflows at Scale'
date: 2026-09-30
description: 'An online Nextflow workshop for the Young Zoologist Group (Université de Namur, Belgium), covering amplicon data analysis with nf-core/ampliseq and running pipelines on an HPC.'
author: 'Christopher Wyatt'
host: yzg
role: delivering
location: Online
type: [training]
tags: ["nextflow", "nf-core", "training", "hpc", "ampliseq", "amplicon", "online"]
video: pending   # swap for the embed URL (e.g. https://www.youtube.com/embed/<id>) once the recording is ready
---

<br>

On **Wednesday 30 September 2026, 15:00–17:00 CEST**, we ran **Nextflow: Reproducible Scientific Workflows at Scale**, a live online workshop over Microsoft Teams for the **Young Zoologist Group** in Belgium. It was organised by Maxence and Mario, members of the group, with the **Université de Namur**.

### What it was about

The workshop introduced **[Nextflow](https://www.nextflow.io)** and **[nf-core](https://nf-co.re)**. We explained why pipelines matter for reproducible science and showed how the same analysis can run on a laptop or scale up to an HPC cluster.

Attendees worked through our hands-on exercises from the **[Eco-Flow training course]({{ '/training/' | relative_url }})**, which runs in the browser through GitHub Codespaces:

- **[Amplicon data analysis]({{ '/training/nfcore_ampliseq/' | relative_url }})**: running the [nf-core/ampliseq](https://nf-co.re/ampliseq) pipeline on 16S data from river and soil samples, from raw reads to taxonomic classification, diversity statistics and a QC report. We made this lesson especially for this course.
- **[Running a pipeline on an HPC]({{ '/training/hpc/' | relative_url }})**: running an nf-core pipeline on a Slurm or SGE cluster, including getting the pipeline, submitting and monitoring jobs, keeping Nextflow running, and avoiding common mistakes. Attendees practised on a mini Slurm cluster inside Codespaces.

The session finished with a Q&A.

### Who it was for

Students, early-career researchers and anyone curious about building reproducible analyses. No prior Nextflow experience was needed.

### The poster

<a href="{{ '/img/yzg-workshop-poster-2026.webp' | relative_url }}"><img src="{{ '/img/yzg-workshop-poster-2026.webp' | relative_url }}" alt="Workshop poster: Nextflow, Reproducible Scientific Workflows at Scale. Speakers Chris Wyatt and Fernando Duarte Frutos (University College London); organised by Maxence and Mario of the Young Zoologist Group; 30/09/2026, 15:00–17:00 CEST, online." style="width:100%;max-width:460px;"></a>

### Keep learning

All of the workshop material stays online, so you can work through it at your own pace. The **[full training course]({{ '/training/' | relative_url }})** goes further, with a command-line primer, an RNA-Seq practical, differential expression in R, nanopore metabarcoding and monitoring runs with Seqera Platform.

Thank you to Maxence, Mario and the Young Zoologist Group for inviting us, and to everyone who joined. For questions, contact us at ecoflow.ucl@gmail.com.
