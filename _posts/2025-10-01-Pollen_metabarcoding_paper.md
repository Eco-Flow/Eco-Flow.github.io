---
title: 'New Publication: Pollen Metabarcoding Reveals Plant-Pollinator Networks'
date: 2025-10-01
description: 'Our pollen metabarcoding pipeline enables large-scale analysis of plant-pollinator interactions'
author: 'Christopher Wyatt'
tags: ["publication", "nextflow", "metabarcoding", "pollinators"]
event_type: 'past'
---

We're excited to share a recent publication in the *Journal of Animal Ecology* that we were a part of: [DNA metabarcoding of pollen reveals highly diverse and spatially structured plant-pollinator interactions](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70126).

## The Challenge

Understanding plant-pollinator interactions is crucial for conservation, but traditional observation methods are time-consuming and can miss cryptic interactions. DNA metabarcoding of pollen collected from pollinators offers a powerful alternative, but analyzing these data at scale requires robust bioinformatics workflows.

## Our Solution

We developed [pollen-metabarcoding](https://github.com/Eco-Flow/pollen-metabarcoding), a Nextflow pipeline that automates the analysis of pollen DNA metabarcoding data. We followed the analysis structure shown in Suchan 2018 (Suchan, T., Talavera, G., Sáez, L., Ronikier, M., & Vila, R. (2018). Pollen metabarcoding as a tool for tracking long-distance insect migrations. Molecular Ecology Resources, 19(1), 149–162. https://doi.org/10.1111/1755-0998.12948), and built the steps they used into a replicable/scalable pipeline. 

The pipeline handles:

- Quality control and filtering of sequencing reads
- Taxonomic assignment of pollen samples
- Statistical analysis of plant-pollinator interactions

## Key Findings

Using our pipeline, the study revealed:

- Highly diverse plant-pollinator networks across agricultural landscapes
- Spatial structuring of interactions at local scales
- Previously undocumented plant-pollinator associations

## Open Science in Action

Both the pipeline and the data are freely available, enabling researchers to reproduce our analyses and apply these methods to their own pollinator communities. This work demonstrates the power of combining reproducible bioinformatics workflows with ecological research.

## Who

Chris Wyatt and former Eco-flow member Simon Murray worked on this project over the last year (from the Eco-flow side), its great to see the work out in the wild. Working mostly with Toby and Eva (the first two authors of the paper), we had a really enjoyable time building out this pipeline and working with this group.

**Links:**
- [Read the paper](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70126)
- [Explore the pipeline](https://github.com/Eco-Flow/pollen-metabarcoding)

---