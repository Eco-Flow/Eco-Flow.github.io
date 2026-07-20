---
layout: "training"
title: "Differential gene expression"
num: "4"
type: "Practical"
order: 4
---

🚀 **Start now:** [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Eco-Flow/training) — *first launch takes a couple of minutes to build.*

---

Now that we have run the nf-core RNA-Seq pipeline, we have the raw counts needed to run differential expression using DESeq2.

## Prerequisites

Before we start this section, we assume you know basic `R`. 
If not I would recommend [swirl](https://swirlstats.com/)

We also would recommend reading the full docs for DESeq2 [here](https://www.bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html). 

## Our data

Following on from the previous section, we have 3 wild type and 3 manipulated cell samples. 

We want to account for technical differences between samples, in order to determine if there is a consistent difference in expression levels of the genes across our two conditions.

We need to account for:

* **Total counts (library size)**, as some samples could have more RNA-Seq reads than others.
* **RNA composition**, as a few very highly expressed genes in one condition can make everything else look relatively lower.

> 💡 **A common misconception:** DESeq2 does **not** correct for gene length. Its median-of-ratios method normalises for library size and composition *between samples*, which is what you need for differential expression (you are comparing the *same* gene across samples, so its length cancels out). Gene length only matters when you compare *different* genes within one sample (e.g. TPM/FPKM). Keep that distinction in mind.

> 🧪 **About this test dataset — read this first.** This is the nf-core test data: *Saccharomyces cerevisiae* (budding yeast), and to keep it small and fast **it contains only chromosome I**. Every gene you see in your counts is on chr I — there are no genes from the other 15 chromosomes here. That has two consequences:
> 1. The counts are largely synthetic, so there is no guarantee of a strong "true" differentially expressed gene. The goal is to learn the **workflow and how to read the output**, not to make a discovery.
> 2. A real gene of interest might not even be on the chromosome we have. Always check your target gene is present in the annotation before drawing conclusions.
>
> Our "manipulated" samples represent a **Rap1 knockdown**. Rap1 is a yeast transcription factor that *activates* many glycolytic and ribosomal-protein genes (see [PMID 30576656](https://pubmed.ncbi.nlm.nih.gov/30576656/)). Rap1 itself (`YNL216W`) is on chromosome XIV, so it is **not** in our chr I data — but one of its well-known target genes is.
>
> 🔎 **Your turn — predict, then hunt.** Before running anything, write down:
> 1. If Rap1 *activates* its targets, which direction (up or down) should a Rap1 target gene move when Rap1 is knocked **down**?
> 2. **The challenge:** among the genes on chromosome I, one is a classic, textbook Rap1-activated **glycolytic** gene. Can you work out which one it is? (Hint: it encodes pyruvate kinase and is essential for growth on glucose.) Write down your guess — we'll return to it at the very end.

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

> ✍️ **Your turn — check your object.** Don't just move on. Run `dds` on its own line and read the summary it prints. How many genes (rows) and how many samples (columns) does it report? Do those numbers match what you expect from your samplesheet? If the sample count is wrong, your `coldata` names probably don't match your count columns — fix it now before continuing.

## Prepare the data before running

### Pre-filter low-count genes

Many genes will have almost no reads across all samples. They carry no useful signal, slow things down, and cost us statistical power during multiple-testing correction. We can drop genes with very few counts:

```R
# Keep only genes with a total of at least 10 reads across all samples
keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep, ]
```

> ✍️ **Your turn.** Run `nrow(dds)` before and after the filtering step. How many genes did you remove? Is that a small fraction or a large one? Jot the number down.

### Set the reference level

DESeq2 needs to know which group is the "baseline" so that a **positive** log2 fold change means "higher in the manipulated samples". By default R picks the alphabetically-first level, which may not be what you want. Set it explicitly:

```R
# Make "wild" the reference/baseline condition
dds$condition <- relevel(dds$condition, ref = "wild")
```

> ⚠️ This is one of the most common ways to misread a result. If you skip it, a gene that is genuinely *up* in the knockdown might show a *negative* fold change simply because the comparison was flipped. Always set your reference deliberately.

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

## Quality control — do you trust the experiment?

Before interpreting a single gene, we should check the experiment as a whole. If the biological groups don't separate, or a sample is an outlier, no gene-level result is trustworthy.

First transform the counts so the variance is roughly constant across the range of expression (raw counts are heavily skewed by highly-expressed genes):

```R
# Variance-stabilising transform, good for visualisation/QC
vsd <- vst(dds, blind = TRUE)
```

Now make a PCA plot:

```R
plotPCA(vsd, intgroup = "condition")
```

> ✍️ **Your turn — interpret, don't just generate.** Look at your PCA plot and answer:
> 1. Do the three wild-type samples cluster together, separate from the three knockdown samples?
> 2. Which axis (PC1 or PC2) captures the condition difference, and what % of variance does it explain?
> 3. Is any single sample sitting far away from its group (a possible outlier)?
>
> Only continue once you're happy the groups separate. If they don't, that's a real result too — it tells you the manipulation may not have had a strong genome-wide effect.

We can also check that the model fit the data well by looking at the dispersion estimates:

```R
plotDispEsts(dds)
```

You should see the fitted red line running through a cloud of points that shrink toward it — that's the model borrowing information across genes. If it looks wildly off, revisit your design.

## Interpreting the results table

Take a proper look at the table before making any plots:

```R
summary(res)
head(res[order(res$padj), ])   # top genes by adjusted p-value
```

Each row is a gene. The columns mean:

| Column | Meaning |
| --- | --- |
| `baseMean` | Average normalised count across all samples |
| `log2FoldChange` | Effect size — log2(knockdown / wild). +1 = doubled, −1 = halved |
| `lfcSE` | Standard error of that fold change |
| `stat` | Wald test statistic |
| `pvalue` | Raw p-value |
| `padj` | **p-value adjusted for multiple testing (use this one!)** |

> ⚠️ **Always use `padj`, not `pvalue`.** We test tens of thousands of genes, so by chance alone thousands would have `pvalue < 0.05`. The `padj` column (Benjamini–Hochberg) corrects for this.

> ❓ **Why are some `padj` values `NA`?** DESeq2 sets `padj` to `NA` for genes it filtered out automatically (very low counts, or flagged as outliers). This is expected — those genes simply didn't have enough signal to test fairly.

> ✍️ **Your turn.** Count how many genes are significant at a 5% false discovery rate:
> ```R
> sum(res$padj < 0.05, na.rm = TRUE)
> ```
> How many did you get? Now change the threshold to `0.01` — how many survive? What does that tell you about how confident you can be?

### Shrinking the fold changes

For genes with low counts, the raw `log2FoldChange` is noisy and can look enormous by chance. Shrinking pulls unreliable estimates toward zero, giving fold changes you can actually rank and plot:

```R
res_shrunk <- lfcShrink(dds, coef = "condition_kd_vs_wild", type = "apeglm")
```

> If `apeglm` isn't installed, run `BiocManager::install("apeglm")`, or use `type = "normal"`. Use `resultsNames(dds)` to confirm the exact `coef` name for your data.

## Visualising the results

**MA plot** — fold change vs. mean expression, with significant genes highlighted:

```R
plotMA(res_shrunk, ylim = c(-5, 5))
```

**Plot the counts for your top gene** — a great sanity check that a hit is real and not driven by one sample:

```R
topGene <- rownames(res)[which.min(res$padj)]
plotCounts(dds, gene = topGene, intgroup = "condition")
```

**Volcano plot** — significance vs. effect size, the classic RNA-seq figure:

```R
res_df <- as.data.frame(res)
with(res_df, plot(log2FoldChange, -log10(padj),
     pch = 20, main = "Volcano plot",
     xlab = "log2 fold change", ylab = "-log10 adjusted p-value"))
# Highlight significant genes in red
with(subset(res_df, padj < 0.05),
     points(log2FoldChange, -log10(padj), pch = 20, col = "red"))
```

> ✍️ **Your turn — close the loop.** Go back to the prediction you made at the very start. The Rap1 target gene on chromosome I is **CDC19** (pyruvate kinase; systematic name `YAL038W`, also known as PYK1).
> 1. Find CDC19 in your results table:
>    ```R
>    res[grep("CDC19|YAL038W", rownames(res)), ]
>    ```
>    (Whether the row is named `CDC19` or `YAL038W` depends on how you loaded the counts — try both.)
> 2. Rap1 *activates* CDC19, and our manipulated samples are a Rap1 **knockdown** — so did you correctly predict a **negative** log2FoldChange? Is it significant (`padj < 0.05`)?
> 3. Look at the gene directly across the six samples:
>    ```R
>    plotCounts(dds, gene = "CDC19", intgroup = "condition")   # or "YAL038W"
>    ```
>
> 🧠 **Reflect.** Remember this is a small, largely synthetic test dataset with **only one chromosome** — so CDC19 may *not* actually come out significant, or may not move in the expected direction. That is itself the lesson: a biologically sensible hypothesis still has to be supported by data that has enough power to detect it. Write one sentence on what you found, and whether this dataset lets you draw any real conclusion about Rap1.
