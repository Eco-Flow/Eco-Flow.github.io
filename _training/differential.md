---
layout: "training"
title: "Differential gene expression"
num: "4"
type: "Practical"
order: 4
---

🧭 [◀️ Part 3 · nf-core RNA-Seq](/training/nfcore-rnaseq/) &nbsp;|&nbsp; [🏠 Course menu](/training/)

🚀 **Start now:** [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Eco-Flow/training) — *first launch takes a couple of minutes to build.*

---

Now that we have run the nf-core RNA-Seq pipeline, we have the raw counts needed to run differential expression using DESeq2.

## Prerequisites

Before we start this section, we assume you know basic `R`. 
If not I would recommend [swirl](https://swirlstats.com/)

We also would recommend reading the full docs for DESeq2 [here](https://www.bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)

## Our data

Following on from the previous section, we have 3 wild type and 3 manipulated cell samples. 

We want to normalise the effects of gene size and of total number of counts in each samples, in order to determin if there is a consistent difference in expression leves of all the genes in the genome.

We need to normalise:

* Gene size , as larger genes will be more likely to have mapped reads.
* Total counts, as some samples (n=6) could have more RNA-Seq reads than other others.

## Load DESeq2

If you have DESeq2 downloaded you simply need to call the library:

```R
library(DESeq2)
```

IF that doesn't work you need to install it, the easiest way is with the bioc manager:

```R
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("DESeq2")
```

-> Write `yes` when prompted to agree to download.

## How to get the data into `R`

To get the data into R from nf-core RNA-Seq, we can use either the `load` function in R or `read.csv`.


### Load from the raw counts

The raw counts that DESeq2 requires are here: `<outdir_name>/star_salmon/salmon.merged.gene_counts.tsv`. If you used the default settings in nf-core rnaseq, if you chose a different aligner (e.g. `--aligner star_rsem`), then you would look in `star_rsem/rsem.merged.gene_counts.tsv` .

`cts <- read.csv("salmon.merged.gene_counts.tsv", h=T, row.names=1, sep="\t")`
#Read in the tab separated file, with first line as header, and first row as row names.

Next you need to make a coldata sheet, this tells DESeq2 which samples are different or part of a group. For our data we would want this:

```
,condition,type
CONTROL_REP1,wild,paired-end
CONTROL_REP2,wild,paired-end
CONTROL_REP3,wild,paired-end
MANIPULATED_REP1,kd,single-read
MANIPULATED_REP2,kd,single-read
MANIPULATED_REP3,kd,single-read
```

!Warning, you must make the names in column 1 exactly the same as what you chose when you wrote the samplesheet for nf-core rnaseq!

Save this to a R variable called `coldata`.


```R
coldata<-read.csv("condition.tsv", h=T, row.names=1)
```

Now you can load DESeq2 and create the `dds` (**D**ESeq **D**ata **S**et)


```R
#Load the data into a DESeq data object, including the counts, column data (groups) and experimental design.
dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design = ~ condition)
```

## Running differential expression

To run DESeq2, I would again point to the great documentation, as there are many variants you may want to consider.

For now we will do the "quick start" options:


```R
# Run DEseq
dds <- DESeq(dds)
resultsNames(dds) # lists the coefficients
res <- results(dds)
write.table(res, "Deseq_results_table.csv", sep="\t", quote=F)
```

Now in the R variable `res`, we should have our results, which we save to a file called "Deseq_results_table.csv".

---

🧭 [◀️ Part 3 · nf-core RNA-Seq](/training/nfcore-rnaseq/) &nbsp;|&nbsp; [🏠 Course menu](/training/)
