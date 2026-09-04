---
title: 'DIETS Symposium nanometabarcoding workshop'
date: 2026-07-21
description: 'A recap of our nf-core nanometabarcoding workshop, run with Jordan Cuff at the DIETS Symposium in Durham.'
author: 'Fernando Duarte'
event: /events/2026-07-21-nanometabarcoding-newcastle/
tags: ["nextflow", "nf-core", "workshop", "metabarcoding", "nanopore"]
---

<img align="top" width="" src="/img/diets.jpeg" />

<br>

As part of the [DIETS Symposium](https://foragingecology.com/diets/) in Durham, we ran a hands-on bioinformatics workshop covering running Nextflow and nf-core pipelines using the command line interface.

The **DIETS Symposium** (Dietary Interactions in Ecology Through Sequencing) is a symposium focused on molecular analysis of trophic interactions, bringing together researchers who use **DNA sequencing** and related molecular methods to study **diets and ecosystem food webs**.

We were invited by [Jordan Cuff](https://www.ncl.ac.uk/nes/people/profile/jordancuff.html) from Newcastle University, with whom we have been collaborating on the **Eco-Flow [nanoporemetabarcoding](https://github.com/Eco-Flow/nanoporemetabarcoding)** pipeline. The pipeline takes raw nanopore reads through filtering and QC, groups reads into consensus sequences, and finally annotates them against a custom BLAST database with taxonomy assigned using the NCBI taxonomy database. It's not an official pipeline, but it was developed using the nf-core framework. We built it primarily in collaboration with other researchers interested in using DNA sequencing - and nanopore sequencing in particular - for diet profiling, with Jordan Cuff being the main brain behind the pipeline and we the developers.

Attendees of different levels of expertise with bioinformatics tools signed up for the workshop. We did a walkthrough of the basics of the **UNIX command line** and collaborative environments such as GitHub. We quickly moved on to running nf-core pipelines locally using the **[nf-core/rnaseq](https://nf-co.re/rnaseq)** pipeline as an example. Once we made sure attendees were comfortable with the command line and had an understanding of the inputs and outputs of nf-core pipelines, we showed them how to run the **nanoporemetabarcoding** pipeline, which was the main interest for attendees given the nature of the symposium.

Overall, we were satisfied with how the workshop went. We had kind words from attendees, which always motivate us to keep building open tools like this for the community. This was also a great opportunity to advertise the work we do and potentially get new collaborators.