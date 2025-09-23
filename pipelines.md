## Pipelines

Here are a list of our main Eco-flow contributed pipelines. 

Those hosted on https://github.com/Eco-Flow were built using a basic nextflow/nf-core framework for specific research projects, whereas those hosted at https://github.com/nf-core are part of the bigger nf-core community, and follow strict nf-core guidelines and practise and are more application to a wider scientific community.

Not all our current pipelines are mentioned here, as some end-users prefer to keep them in private repositories until the paper is published. We encourage our users to publish as quick as possible, and be open with their code, but in some circumstances we cannot acheive that.

### Released pipelines

These are pipelines that have passed the initial development stage and are now ready for publication or release:

* [Eco-Flow/synteny](https://github.com/Eco-Flow/synteny) - A pipeline that compares gene synteny between chromosome level genome assemblies. It takes genomes and gff (annotation) files and compares the macrosynteny using a variety of programs.

* [Eco-Flow/excon](https://github.com/Eco-Flow/excon) - A pipeline that runs gene family expansion and contraction analysis (via CAFE). This pipeline automates the analysis to run the basic steps in EXpansion and CONtraction of gene families, as well as running GO enrichment analysis on the output.

* [Eco-Flow/pollen-metabarcoding](https://github.com/Eco-Flow/pollen-metabarcoding) - A pipeline to process meta barcoding data and assign species and produce tables/figures appropriate for this analysis. Paper: https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.70126?af=R

### Pipelines in Development

Pipelines that are still in development but are already functional and close to be released:

* [Eco-Flow/nanoporemetabarcoding](https://github.com/Eco-Flow/nanoporemetabarcoding) - A pipeline for processing - quality control, demultiplexing, and clustering - and annotate nanopore metabarcoding data. Annotation is performed at different taxonomic levels on the consensus sequences, using the BLASTnt database and [taxonomizr](https://github.com/sherrillmix/taxonomizr).

* [nf-core/genomeqc](https://github.com/nf-core/genomeqc) - A pipeline to for the quality control of genome assemblies and their respective annotations using common tools such as Quast, BUSCO, AGAT, FCS-GX, etc. It also runs orthofinder for quick phylogeny, and it presents the results as a tree plot with the different statistics.

Pipelines that are still in early stages of development:

* [nf-core/gwas](https://github.com/nf-core/gwas) - A pipeline to conduct genome-wide association studies (GWAS).

### Custom config files

* [Eco-Flow/configs](https://github.com/Eco-Flow/configs/tree/main) - A repository to store custom configuration files we develop for our community.

### Request a Pipeline

If you would like to request a pipeline then open a new GitHub Issue on our [pipeline discussions](https://github.com/Eco-Flow/pipeline-discussions) repository. Or email us at: ecoflow.ucl @ gmail.com

### Request a Feature
If you would like to request an additional feature to a published pipeline then please open a new issue on that pipeline's GitHub repository.
