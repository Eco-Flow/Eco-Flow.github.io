---
layout: "training"
title: "Run an nf-core RNA-Seq pipeline"
num: "3"
type: "Practical"
order: 3
---

🧭 [◀️ Part 2 · Pipelines](/training/pipelines/) &nbsp;|&nbsp; [🏠 Course menu](/training/) &nbsp;|&nbsp; **Next:** [Part 4 · Differential expression ▶️](./differential.md)

---

In this final practical, we will show you how to run a nf-core RNA-Seq pipeline (https://nf-co.re/rnaseq/3.14.0). 

**nf-core** are a community who build gold standard, reproducible data pipelines, that have become the industry standard.

![image](https://github.com/Eco-Flow/training/assets/9978862/cdb59557-128d-48f8-8df1-0a6b548f89e9)

**nf-core** have a variety of [pipelines](https://nf-co.re/pipelines) that tackle key bioinformatic challenges.

Join them on slack [here](https://nf-co.re/join/slack).

## Practical course

We will run the nf-core pipeline on some example data  provided in the `data` folder. 

In essence, we want to compare the gene expression between wild-type yeast cells and those with a Rap1 gene knock down (KD). 

This comes from an experiment in the following paper:
https://pubmed.ncbi.nlm.nih.gov/30576656/

<img width="400" alt="image" src="https://github.com/Eco-Flow/training/assets/9978862/d51a00c6-4184-4805-b823-3d6248bb2fde">

<br />

<br />

**Step 0. Understanding RNA-Seq**

Before running this RNA-Seq analysis, it is important to understand what RNA-Seq analysis is. This will be covered partly in the lecture.

For more reading, It is worth following other online tutorials such as the following to learn more about how to process RNA-Seq data:

<details>
<summary>Links to great RNA-Seq educational resources</summary>
<br/>

[1. https://www.azenta.com/blog/quick-start-guide-rna-seq-data-analysis#step1](https://www.azenta.com/blog/quick-start-guide-rna-seq-data-analysis#step1)
<br/>

[2. https://bioinformatics-core-shared-training.github.io/RNAseq-R/](https://bioinformatics-core-shared-training.github.io/RNAseq-R/)
<br/>

[3. https://learn.gencore.bio.nyu.edu/rna-seq-analysis/](https://learn.gencore.bio.nyu.edu/rna-seq-analysis/)
<br/>
</details>
<br/>


**Step 1. Check out the raw RNA-Seq data provided**

Check out the folder `data`. It is important to inspect the data yourself manually to see exactly what you have.

Try to `head` one of the fastq files in the `data` folder (don't panic if you get `<��xT�r-�B7�+7P�~~�����...`, this is expected).

The fastq files in this directory are compressed using the command `gzip`, so they are not human readable files.

We haven't covered this in the basic training, but here is a command you could use to head the top of a gzipped file:

`zcat data/SRR6357070_1.fastq.gz | head`

`zcat` is related to `cat` but can read gzipped files.

There is no `zhead`, so we need to pipe the output of `zcat` to `head`.

Can you now count the number of lines in a gzipped file using the same logic as above:

<details>
<summary>Answer</summary>
<br/>

`zcat data/SRR6357070_1.fastq.gz | wc -l`

or

`zcat data/SRR6357070_1.fastq.gz | wc`
</details>
<br/>

**Step 2. Check out the nf-core rnaseq repo**

<br/>

Now go to the nf-core rnaseq github repository, [here](https://nf-co.re/rnaseq/3.14.0), and try to understand what the pipeline is doing and what inputs the pipeline expects.

<img src="/assets/training/img/image.png" alt="drawing" width="700"/>

<details>
<summary>Cheat sheet</summary>
<br/>
Hopefully you found that you require:
  
* a genome (in fasta)

* an annotation (in gtf or gff)

* an input samplesheet that contains links to the raw RNA-Seq fastq data
</details>
<br/>


**Step 3. Build a samplesheet**

<br/>

Now we need to find the data and start building the samplesheet.csv file. The raw data are in `./data`.

<br />
SRR6357070 is wild type (paired end reads)<br />
SRR6357071 is wild type (paired end reads)<br />
SRR6357072 is wild type (paired end reads)<br />
<br />
SRR6357073 is manipulated (single end reads)<br />
SRR6357074 is manipulated (single end reads)<br />
SRR6357075 is manipulated (single end reads)<br />
<br />

<br/>Can you build yourself a sample sheet with the data provided using their full paths, with both wild-type and manipulated replicates.

You can see the example sample sheet [here](https://nf-co.re/rnaseq/3.14.0/docs/usage#samplesheet-input), from the nf-core webpage. 

Choose whichever name for the sample as you wish, and choose auto for the strandedness field.
<br/>
<br/>
<details>
<summary>Cheat sheet</summary>
<br/>

```
sample,fastq_1,fastq_2,strandedness
CONTROL_REP1,/workspaces/training/eco-flow-training/data/SRR6357070_1.fastq.gz,/workspaces/training/eco-flow-training/data/SRR6357070_2.fastq.gz,auto
CONTROL_REP2,/workspaces/training/eco-flow-training/data/SRR6357071_1.fastq.gz,/workspaces/training/eco-flow-training/data/SRR6357071_2.fastq.gz,auto
CONTROL_REP3,/workspaces/training/eco-flow-training/data/SRR6357072_1.fastq.gz,/workspaces/training/eco-flow-training/data/SRR6357072_2.fastq.gz,auto
MANIPULATED_REP1,/workspaces/training/eco-flow-training/data/SRR6357073_1.fastq.gz,,auto
MANIPULATED_REP2,/workspaces/training/eco-flow-training/data/SRR6357074_1.fastq.gz,,auto
MANIPULATED_REP3,/workspaces/training/eco-flow-training/data/SRR6357075_1.fastq.gz,,auto

```
<br/>
<br/>
A sample sheet will contain a sample name, followed by the forward reads (normally R1), followed by the reverse reads (normally R2, if you have them), followed by the strand information (if you want the pipeline to calculate this for you, you use auto, else you write un-stranded, forward or reverse).
</details>
<br/>

You can also see this example template on the nf-core rnaseq website [here](https://raw.githubusercontent.com/nf-core/test-datasets/7f1614baeb0ddf66e60be78c3d9fa55440465ac8/samplesheet/v3.10/samplesheet_test.csv)



**Step 4. Download the genome and annotation**
<br/>
<br/>
Download the genome and gff file to the data folder.

The genome and annotation are on a webpage, so we can use `wget` to download the genome and annotation, as follows:

`wget -O genome.fasta https://raw.githubusercontent.com/nf-core/test-datasets/7f1614baeb0ddf66e60be78c3d9fa55440465ac8/reference/genome.fasta`
<br/>

`wget -O genes.gff.gz https://raw.githubusercontent.com/nf-core/test-datasets/7f1614baeb0ddf66e60be78c3d9fa55440465ac8/reference/genes.gff.gz`


**Step 5. Running the pipeline**
<br/>
<br/>
Run the nf-core RNA-Seq pipeline on your input files. Read the online instructions of what you need to do to run the pipeline (found here: https://nf-co.re/rnaseq/3.14.0/docs/usage). Using your own paths to genome (`--fasta`), annotation (`--gff`) and samplesheet (`--input`). You also need to set an `--outdir` name (to anything you wish), else you will receive an error.
<br/>
<br/>
You should use the `--fasta /path/to/genome.fasta`,  `--gff /path/to/genes.gff.gz`, `--input /path/to/samplesheet.csv` and `--outdir name` flags.

**PLUS**: you need to use the flag `--profile docker` . This is to ensure you are running from docker containers to pull all the programs you need to run nf-core rnaseq. Otherwise you woud have to install all the software manually. In addition, there are other profiles for other container engines (e.g. `--singularity` or `--apptainer`, used when on an HPC, contact your HPC team for help).

**PLUS**: in Codespaces we have limited memory available, so you need to add a special config file:

`-c /workspaces/training/eco-flow-training/codespaces.config`

<br/>
<br/>
<details>
<summary>Cheat sheet</summary>
<br/>
You command should look like:

```
nextflow run nf-core/rnaseq \
-profile docker \
-c /workspaces/training/eco-flow-training/codespaces.config \
--input /workspaces/training/eco-flow-training/samplesheet.csv \
--gff /workspaces/training/eco-flow-training/genes.gff.gz \
--fasta /workspaces/training/eco-flow-training/genome.fasta \
--outdir my_results 
```
</details>
<br/>

 👉🏻 **Important**: Notice the use of single (-) and double (--) flags. Single are nextflow core flags and double are settings within the script/pipeline itself.
 

If it ends in an error, most likely you did not specify the correct paths to the input or output files:

e.g.
```
* Missing required parameter: --input
* Missing required parameter: --outdir
```

OR you did not provide full paths to the genome/annotation 
(provide the path : /workspaces/training/eco-flow-training/genes.gff.gz):

e.g.
```
Caused by:
  Not a valid path value: 'genes.gff.gz'
```

OR maybe you forgot to use the `-profile docker` flag. 

e.g.
```
Command exit status:
  127

Command output:
  (empty)

Command error:
  .command.sh: line 7: fastqc: command not found
```

In this case, `fastqc` is not found because we are trying to find it locally. We don't have it installed, so need to use `-profile docker` to allow the script to find `fastqc`

If you receive a different error, please raise a comment to the tutor.
<br/>


**Step 6. Checking out the documentation**
<br/>
<br/>
You pipeline should now be working.
<br/>

If your pipeline did succeed, you can wait for the pipeline to finish running and start exploring the output of the pipeline.

An overview of all the output types is found here: https://nf-co.re/rnaseq/3.14.0/docs/output. 

Spend 10 minutes exploring the output documentation, and by this time your pipeline run should have finished so you can then explore your own results.

For example:

Check that the reads were of sufficient quality.
<br/>
To know what the fastq quality scores should look like, follow this guide:

https://bioinfo.cd-genomics.com/quality-control-how-do-you-read-your-fastqc-results.html

Find the output FASTQC results (in your output folder, under `<outdir>/FASTQC`), and check if there were any highlighted issues. 

Then we will discuss these in class.

<br/>


**Step 7. Resuming a pipeline and setting flags**

Next, we choose different flags (options) of the nf-core RNA-Seq pipeline. 

In the documents, you should be able to see that you can choose to change the abundance estimator to `rsem`. See [here](https://nf-co.re/rnaseq/3.14.0/docs/usage#alignment-options). Try to work out how you would change your previous nextflow command, to use the star aligner and the rsem quantification tool. **!BUT DO NOT EXECUTE IT!**

<details>
<summary>Answer</summary>
<br/>

```
nextflow run nf-core/rnaseq \
-profile docker \
-c /workspaces/training/eco-flow-training/codespaces.config \
--input /workspaces/training/eco-flow-training/samplesheet.csv \
--gff /workspaces/training/eco-flow-training/genes.gff.gz \
--fasta /workspaces/training/eco-flow-training/genome.fasta \
--outdir my_results
--aligner star_rsem
```
</details>

Now before we execute this script, we need to learn about the nextflow flag `-resume`. Using the `-resume` flag means that nextflow will "remember" the previous runs that were executed, and if any of the steps have been done before, it will use the cache-ing system to save repetition.

Now, if you run the above command with the additional flag `-resume`, then it will only repeat the steps after `RSEM`, as that is the last point in the pipeline where we expect the run to change.

<details>
<summary>What you should see</summary>
<br/>

```
CACHE
```
</details>

<br/>

**Step 8. Check the FASTQC results**




## Finish

You have finished the course. We hope you have learnt some of the basics of pipeline usage with Nextflow.

The next steps are learning to write in Nextflow yourself. There are awesome training materials at https://training.nextflow.io/

Further, Eco-Flow will be providing more foundational Nextflow courses soon, so feel free to email us, and we can add you to our mailing list (ecoflow . ucl @ gmail . com)

---

🧭 [◀️ Part 2 · Pipelines](/training/pipelines/) &nbsp;|&nbsp; [🏠 Course menu](/training/) &nbsp;|&nbsp; **Next:** [Part 4 · Differential expression ▶️](./differential.md)
