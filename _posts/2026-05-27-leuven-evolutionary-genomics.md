---
title: 'Nextflow, nf-core and synteny in Leuven'
date: 2026-05-27
description: "Sharing Nextflow, nf-core and our synteny pipeline at the Mini-Symposium on Evolutionary Genomics at KU Leuven."
author: 'Chris Wyatt'
tags: ["nextflow", "nf-core", "synteny", "talk", "genomics"]
---

<img src="/img/leuven-grote-markt.jpg" alt="The Grote Markt square in Leuven, with the Gothic town hall and St Peter's Church">
<p style="text-align:center; font-size:.82rem; color:#8a9890; margin-top:-.9rem;">Leuven's Grote Markt. <em>Photo: Snowdog, public domain (Wikimedia&nbsp;Commons).</em></p>

I was delighted to visit **KU Leuven** to take part in the [Mini-Symposium on Evolutionary Genomics](https://bio.kuleuven.be/news/mini-symposium-on-evolutionary-genomics), hosted by the Department of Biology. It was a great excuse to talk about two of my favourite things — **reproducible pipelines** and **genome evolution** — with a room full of evolutionary genomicists.

### The talk

My talk, *"Extensive genome rearrangements in the haplodiploids: a novel pipeline for syntenic break"*, looked at how chromosomes have been reshuffled across the haplodiploid insects, and how we can detect and quantify those rearrangements at scale.

The engine behind that work is **[Eco-Flow/synteny](/pipelines/synteny/)** — a Nextflow pipeline, built to nf-core standards, that compares gene macrosynteny between chromosome-level genome assemblies. Give it genomes and their annotations and it handles the rest, producing comparable, publication-ready synteny analyses across many species.

### Spreading the Nextflow word

Alongside the science, a big part of the visit was introducing **Nextflow** and the **nf-core** community to researchers who hadn't used them before. Pipelines like our synteny workflow are a great way to show *why* reproducible, portable workflows matter: the same analysis runs on a laptop, an HPC, or the cloud, and anyone can reproduce your results. Conversations like these are exactly how we grow the community.

### The rest of the programme

The symposium also featured two talks I was sorry to miss: **Emilia Santos** (University of Cambridge) on the genomic and developmental basis of colour-pattern evolution, and **Sozos Michaelides** (Concordia University) on lake trout adaptations in a large postglacial lake. Both sounded fascinating — a real shame our schedules didn't line up, but a good excuse to catch them another time.

Huge thanks to **Tom Wenseleers** for the invitation and the warm welcome to KU Leuven.

---

Curious about the synteny pipeline? Take a look at **[Eco-Flow/synteny](/pipelines/synteny/)**, or [get in touch](mailto:ecoflow.ucl@gmail.com) if you'd like help running it on your own genomes.
