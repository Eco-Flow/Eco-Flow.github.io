---
title: 'nf-core hackathon Barcelona'
date: 2025-10-31
description: 'Blog post related to the nf-core hackathon in Barcelona in October 2025.'
author: 'Fernando Duarte'
tags: ["nextflow", "hackathon", "nf-core", "nfcore"]
---

<img align="top" width="" src="/img/hackathon-barcelona-2025.jpg" />

<br>

Last October, I had the opportunity to attend this year’s **nf-core hackathon** in the beautiful city of Barcelona. This marked my third in-person hackathon within the span of a single year - without even considering the online Hackathon we hosted at University College London East Campus in March.

I was pleasantly surprised by the number of nf-core and Nextflow enthusiasts attending the event, specially considering there was no **Nextflow Summit**. In previous editions, in-person nf-core hackathons and the Nextflow Summit were typically held together (as was the case during this year’s hackathon in Boston), but this October they decided to split them in two standalone events. It was exciting to see the nf-core community continuing to grow and amazing to witness so many people eager to contribute and help make scientists’ lives a little easier.

During the main event, I joined forces with some memebers of the **MGnify team**, alongside other nf-core contributors, to work on their new project: the **[nf-core/seqsubmit]( https://nf-co.re/seqsubmit/dev/)** pipeline. Our group was led by both [Ekaterina Sakharova](https://github.com/KateSakharova) and [Sofia Ochkalova](https://github.com/ochkalova), who did a great job at guiding us through, and helping us with the troubleshoot. The goal of this pipeline is to simplify the **submission of genomic data** to public repositories such as ENA and NCBI. Having previously dealt with uploading metagenomic data to ENA, I am aware of how tedious and complicated this process can be, which makes a tool like this particularly valuable. At present, the pipeline is still **under development** and is primarily focused on metagenomic data, including the submission of assemblies, bins, and metagenome-assembled genomes (MAGs).

While we already rely on helper tools such as the Webin-CLI Submission, the idea behind this pipeline is to provide a **comprehensive and unified platform** for submitting data to the most well-known genomic repositories. During the hackathon, I mainly focused on developing and refining the assembly and genome submission workflows, as well as working on the input validation.

On a side note, it was great to reconnect with former colleagues from the Centre for Genomic Regulation (CRG), who were contributing to other projects at the event. Overall, it was a fantastic experience, and I was delighted to have attended again. I’m already looking forward to the next hackathon.
