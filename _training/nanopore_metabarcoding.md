---
layout: "training"
title: "Run the nanopore metabarcoding pipeline"
num: "5"
type: "Practical"
order: 5
---

🚀 **Start now:** [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Eco-Flow/training) — *first launch takes a couple of minutes to build.*

⏱ **Estimated time:** ~60–90 minutes (including pipeline run time) &nbsp;•&nbsp; 🟡 Practical

In this practical you'll run **nanoporemetabarcoding**, a pipeline built by Eco-Flow ([`Eco-Flow/nanoporemetabarcoding`](https://github.com/Eco-Flow/nanoporemetabarcoding)) — from raw Nanopore reads all the way to a taxonomically-annotated ASV table.

> ℹ️ **Not an official nf-core pipeline.** nanoporemetabarcoding was scaffolded with the [nf-core](https://nf-co.re) template and follows its conventions (module structure, config profiles, `-profile docker`, etc.), which is why some of the tooling will feel familiar to Part 3 of this workshop. But it isn't part of the official nf-core pipeline collection, isn't listed on nf-co.re, and has no tagged release yet, as it is still in active development.

<!--
Disclaim
-->
### What you'll do

- Understand what the nanopore metabarcoding pipeline is and how it works
- Inspect raw Nanopore reads
- Work out what inputs the pipeline needs
- **Design** a samplesheet and metadata sheet for a real experimental scenario
- **Run** the pipeline on its built-in test data with Docker containers
- Explore the results — quality reports, BLAST hits, taxonomy, and a community matrix
- **Run** the pipeline on an HPC cluster, using UCL's Myriad as a worked example
- Learn to **`-resume`** a run and change pipeline options (let's see...)

<!--
> ✅ **Before you start**, make sure you've completed [Setup](/training/setup/) and that your terminal is inside the **`eco-flow-training`** folder. Check with:
> ```bash
> pwd     # should end in eco-flow-training
> ```
-->

### The experiment

We'll use a case study to motivate the design steps: **DNA barcoding of adult wasps to identify their prey.**

Adult wasps were collected at two sites: oak woodland and grassland. Each wasp was individually DNA-barcoded (COI) using primers that target that region and prevents host DNA amplification (`WaspExF_*` forward / `LuthienR_*` reverse) to profile its host's diet signature. Each site's wasp PCR products were pooled onto one Nanopore barcode — i.e. **one plate = one ONT barcode = one FASTQ file**, but each *well* inside that plate is its own wasp, told apart later by a second, set of sort sequences used as 'tags'.

> 💡 **What's an exclusion primer?** A wasp carries trace host DNA from its prey in the gut/cuticle residue, but its own DNA is far more abundant in the sample, so a plain universal COI primer pair would mostly just re-sequence the wasp itself. `WaspExF_*` primers — the same tagged primers used for demultiplexing — are designed to be less complementary to the wasp's own COI sequence than to other (host) DNA, so amplification of the wasp's own template is suppressed relative to that trace host signal. It's rarely perfect: some wasp DNA usually still gets through, which is one reason checking control wells for unexpected hits (see Step 6) matters.

| Site | Description | Plate / ONT barcode |
| --- | --- | --- |
| Site A ("Woodland") | Adult wasps collected in oak/hazel woodland | plate01 / barcode01 |
| Site B ("Meadow") | Adult wasps collected in grassland/meadow | plate02 / barcode02 |

Within each plate, three forward tags (`F1`–`F3`) and two reverse tags (`R1`–`R2`) are combined pairwise to label individual wells — giving each wasp (and each control) a unique forward+reverse tag combination.

We'll **design** the samplesheet/metadata for this scenario ourselves in Steps 3–4, then **run** the pipeline for real in Step 5 using the small dummy dataset.

---

## Step 0 — Understand nanopore metabarcoding

Metabarcoding sequences a short, taxonomically-informative marker gene (here, COI) from many samples/individuals at once, then compares each sequence against a reference database to assign it to a species (or best-available taxonomic rank).

With Nanopore sequencing, an entire multi-well PCR plate is typically pooled into **one** sequencing run/barcode — so a second layer of "tags" (short index sequences stuck onto the primers during PCR) is needed to work out which read came from which well.

<details>
<summary>📚 Good background resources</summary>
<!--
- [Nanopore sequencing — how it works (Oxford Nanopore)](https://nanoporetech.com/how-it-works)
- [DNA metabarcoding — a beginner's guide (Nature Ecology & Evolution primer)](https://www.nature.com/articles/s41559-019-0951-3) -->
- [Cutadapt documentation](https://cutadapt.readthedocs.io/) — the demultiplexing tool this pipeline uses
</details>

---

## Step 1 — Inspect the raw data

The pipeline ships with a small built-in test dataset, but we will use a custom one made for this training, following the case study above. Clone the pipeline repository first:

```bash
git clone https://github.com/Eco-Flow/nanoporemetabarcoding.git
cd nanoporemetabarcoding
```

The raw reads live in `wasp_test_data/`. Nanopore FASTQs are gzipped, so peek at them with `zcat` (as in Part 1):

> ▶️ **Try it — peek at a raw FASTQ**
>
> ```bash
> zcat test_data/test.fastq.gz | head -8
> ```
>
> <details>
> <summary>✅ Expected output</summary>
>
> Groups of four lines per read, same FASTQ format as Illumina — but unlike the paired, fixed-length RNA-Seq reads from Part 3, Nanopore reads are **single, variable-length long reads** with no pair:
>
> ```
> @<read id> ...
> ATGCGT...(a few hundred bp, length varies read to read)
> +
> !%'&&$#"...(quality string, same length as the sequence)
> ```
> </details>

> ▶️ **Try it — count the reads**
>
> ```bash
> zcat test_data/test.fastq.gz | wc -l
> ```
>
> FASTQ uses **4 lines per read**, so divide the line count by 4 to get the number of reads. This file is deliberately tiny (a handful of reads per well) so the whole pipeline runs in minutes.

Also inspect the other files you'll need:

```bash
cat wasp_test_data/primers_f.fasta      # forward primer-tag sequences
cat wasp_test_data/primers_r.fasta      # reverse primer-tag sequences
cat wasp_test_data/metadata.csv         # which tag combination = which sample
```

<details>
<summary>📋 Ground truth — what's actually in each plate</summary>

Useful to check yourself against once you reach Step 6. Both plates share the same 6 tag combinations, but each well's simulated species content differs deliberately — Woodland is the more diverse site.

**plate01 — Woodland (`barcode01`)**

| Well | Sample | Composition | Reads |
| --- | --- | --- | --- |
| F1 × R1 | `EXT_NEG_F1_R1` | *(no template — junk)* | 2 |
| F2 × R1 | `WD_wasp01` | *Operophtera brumata* (60) + *Tortrix viridana* (50) + *Thecla betulae* (40) | 150 |
| F3 × R1 | `WD_wasp02` | *Tortrix viridana* (90) + *Colotois pennaria* (60) | 150 |
| F1 × R2 | `WD_wasp03` | *Operophtera brumata* (90) + *Erannis defoliaria* (60) | 150 |
| F2 × R2 | `POS_CON_F2_R2` | *Drosophila melanogaster* (150) | 150 |
| F3 × R2 | `BLANK_F3_R2` | *(no template — junk)* | 2 |

→ 5 real prey species total (*Operophtera brumata*, *Tortrix viridana*, *Thecla betulae*, *Colotois pennaria*, *Erannis defoliaria*), several wells mixing two or three species in one well.

**plate02 — Meadow (`barcode02`)**

| Well | Sample | Composition | Reads |
| --- | --- | --- | --- |
| F1 × R1 | `EXT_NEG_F1_R1` | *(no template — junk)* | 2 |
| F2 × R1 | `MW_wasp01` | *Pieris brassicae* (110) + *Noctua pronuba* (40) | 150 |
| F3 × R1 | `MW_wasp02` | *Pieris brassicae* (150) | 150 |
| F1 × R2 | `MW_wasp03` | *Pieris brassicae* (110) + *Autographa gamma* (40) | 150 |
| F2 × R2 | `POS_CON_F2_R2` | *Drosophila melanogaster* (150) | 150 |
| F3 × R2 | `BLANK_F3_R2` | *(no template — junk)* | 2 |

→ Only 3 real prey species (*Pieris brassicae*, *Noctua pronuba*, *Autographa gamma*), dominated almost entirely by *Pieris brassicae* — much lower richness/evenness than Woodland, on purpose.

Both `EXT_NEG` and `BLANK` are genuinely empty (a couple of short, unclassifiable junk reads) — if your results show a real species hit there instead, that's contamination worth investigating, not expected behaviour.
</details>

---

## Step 2 — Explore the pipeline's requirements

Read the pipeline's own usage docs: [`docs/usage.md`](https://github.com/Eco-Flow/nanoporemetabarcoding/blob/master/docs/usage.md) and the parameter block at the top of [`nextflow.config`](https://github.com/Eco-Flow/nanoporemetabarcoding/blob/master/nextflow.config).

<details>
<summary>Cheat sheet — what the pipeline needs</summary>

To run nanoporemetabarcoding you need:

* a **samplesheet** (`--input`) — one row per Nanopore barcode/plate, pointing to a single merged FASTQ
* a **metadata** sheet (`--metadata`) — one row per well, mapping a forward+reverse tag combination to a sample name
* a **forward primer-tag FASTA** (`--tags_f`) and a **reverse primer-tag FASTA** (`--tags_r`)
* a **reference database** for taxonomy — either `--blast_db` (pre-built) or `--custom_db` (a FASTA the pipeline will build a BLAST DB from)
</details>

> 💡 **What the pipeline does for you** (in containers): trims/filters reads (NanoFilt), QCs raw and filtered reads (NanoPlot), demultiplexes by primer-tag (Cutadapt, twice — forward then reverse), clusters reads per well into consensus "species" sequences (amplicon_sorter), polishes each consensus (Medaka), BLASTs each consensus against your reference database, assigns taxonomy from the best hit (taxonomizr), and builds per-run abundance/presence-absence community matrices.

---

## Step 3 — Design a samplesheet

The **samplesheet** links each Nanopore barcode (one plate) to its FASTQ. It has just two columns:

| Column | Meaning |
| --- | --- |
| `id` | An identifier you choose for the plate/barcode (can be anyrhing, but cannot contain spaces or '_') |
| `fastq` | Path to that plate's single, merged FASTQ file |

> ▶️ **Try it — design `samplesheet.csv` for the wasp experiment**
<!-- >
> Using the table in [The experiment](#the-experiment) (2 sites → 2 plates → 2 barcodes), write out what the samplesheet should look like.
-->
<details>
<summary>Cheat sheet — samplesheet.csv for the wasp scenario</summary>

```csv
id,fastq
plate01,barcode01/plate1_combined.fastq.gz
plate02,barcode02/plate2_combined.fastq.gz
```

One row per ONT barcode/plate. `fastq` must point to a single, existing `.fastq.gz` file — if your sequencer produced several chunk files per barcode, merge them (e.g. `cat`) before writing the samplesheet.
</details>

---

## Step 4 — Design a metadata sheet and primer-tag FASTAs

The **metadata** sheet is what actually resolves each demultiplexed well down to a sample name. It has three columns:

| Column | Meaning |
| --- | --- |
| `id` | Must match a plate `id` from the samplesheet |
| `primer_comb` | `<forward tag header>_<reverse tag header>` — must exactly match headers in your `tags_f`/`tags_r` FASTAs |
| `sample` | The name you want in the final ASV table — must be **unique within each plate** |

> ⚠️ **Key rule:** `primer_comb` is a straight string match against your FASTA headers. If the tag names don't match exactly (typos, case, extra characters), that well's reads won't be assigned to a sample.

> ▶️ **Try it — design the metadata for plate01**
>
> Plate01 has 3 forward tags (`F1_WaspExF_Tab1`, `F2_WaspExF_Tab2`, `F3_WaspExF_Tab3`) and 2 reverse tags (`R1_LuthienR_Tab29`, `R2_LuthienR_Tab54`), giving 6 wells: one extraction blank, one positive control, one PCR blank, and 3 adult wasps netted in the Woodland site. Write out the FASTAs and the metadata rows.

<details>
<summary>Cheat sheet — primers_f.fasta / primers_r.fasta</summary>

```fasta
>F1_WaspExF_Tab1
AACAAGCCCCTTTATCWTSWRRWWTTGS
>F2_WaspExF_Tab2
GGAATGAGTCCTTTATCWTSWRRWWTTGS
>F3_WaspExF_Tab3
AATTGCCGGTCCTTTATCWTSWRRWWTTGS
```

```fasta
>R1_LuthienR_Tab29
GAGTAACCACTTCWGGRTGWCCAAARAAYCA
>R2_LuthienR_Tab54
CGATGAGTTACTTCWGGRTGWCCAAARAAYCA
```
</details>

<details>
<summary>Cheat sheet — metadata.csv for plate01</summary>

```csv
id,primer_comb,sample
plate01,F1_WaspExF_Tab1_R1_LuthienR_Tab29,EXT_NEG_F1_R1
plate01,F2_WaspExF_Tab2_R1_LuthienR_Tab29,WD_wasp01
plate01,F3_WaspExF_Tab3_R1_LuthienR_Tab29,WD_wasp02
plate01,F1_WaspExF_Tab1_R2_LuthienR_Tab54,WD_wasp03
plate01,F2_WaspExF_Tab2_R2_LuthienR_Tab54,POS_CON_F2_R2
plate01,F3_WaspExF_Tab3_R2_LuthienR_Tab54,BLANK_F3_R2
```

`plate02` reuses the same 6 tag combinations (the same primer plate design was run at both sites) — only the `id` and the wasp `sample` names change; controls can share the same short name pattern (`EXT_NEG_F1_R1`, `POS_CON_F2_R2`, `BLANK_F3_R2`) since `id` already keeps plate01 and plate02 apart.
</details>

> 💡 **Always include controls.** `EXT_NEG` (extraction blank — no tissue), `POS_CON` (mock DNA of a known reference species), and `BLANK` (PCR no-template control) are how you catch contamination and confirm the assay worked — track them through the metadata sheet exactly like a real sample.

---

## Step 5 — Run the pipeline

Now put the theory aside and actually run the pipeline — on its small **built-in** test dataset (`test_data/`), so it finishes in minutes regardless of whether your wasp FASTQs exist yet.

Read the parameters block in [`nextflow.config`](https://github.com/Eco-Flow/nanoporemetabarcoding/blob/master/nextflow.config) for the full option list.

<details>
<summary>Cheat sheet — the full command</summary>

```bash
nextflow run main.nf \
-profile docker \
--input test_data/../assets/samplesheet.csv \
--metadata test_data/metadata.csv \
--tags_f test_data/primers_f.fasta \
--tags_r test_data/primers_r.fasta \
--custom_db test_data/test_database.fasta \
--outdir results
```

</details>

> 👉 **Single vs double dashes matter!** A single dash (`-profile`, `-resume`) is a **Nextflow** core option. A double dash (`--input`, `--metadata`, `--outdir`) is a **pipeline** parameter defined by nanoporemetabarcoding.

> ✅ **What success looks like:** Nextflow prints a banner, then a live list of processes as they run (`NANOFILT`, `NANOPLOT`, `CUTADAPT` ×2, `AMPLICON_SORTER`, `MEDAKA`, `BLAST_BLASTN`, `ASSIGN_TAXA`, ...). On the tiny test data this should complete in a few minutes, plus a bit longer the first time while Docker pulls the containers.

### Troubleshooting Step 5

<details>
<summary>❌ <code>Missing required parameter: --input</code> / <code>--outdir</code></summary>

Check every `--input`, `--metadata`, `--tags_f`, `--tags_r` and `--outdir` is present and spelled correctly.
</details>

<details>
<summary>❌ A well/sample is missing from the final ASV table</summary>

Almost always a `primer_comb` mismatch — the tag combination in `metadata.csv` doesn't exactly match `<tags_f header>_<tags_r header>`. Double-check spelling and case.
</details>

<details>
<summary>❌ <code>.command.sh: ... command not found</code> (exit status 127)</summary>

You forgot **`-profile docker`**. Without it, Nextflow expects every tool (Cutadapt, Medaka, BLAST, ...) to already be installed locally.
</details>

---

## Step 6 — Explore the results

Once you see `Pipeline completed successfully`, look inside `results/`:

```bash
ls results
```

<details>
<summary>✅ Roughly what you'll see</summary>

```
nanoplot/  blast/  assign_taxa/  community_matrix/  mafft/  plots/  multiqc/  pipeline_info/  reads_per_step/
```
</details>

**Where to look, in order:**

1. **`multiqc/multiqc_report.html`** — one HTML report summarising QC across all samples (built from NanoStat).
2. **`nanoplot/demultiplexed/<plate>/`** — per-plate read-length/quality plots, generated *after* demultiplexing, so you can sanity-check each well individually.
3. **`reads_per_step/reads_per_step.csv`** — a read-count funnel: how many reads survived filtering, then each demultiplexing step. This is the fastest way to spot a well that dropped to zero reads (usually a `primer_comb` typo).
4. **`blast/<plate>.txt`** — raw BLAST hits for every consensus sequence.
5. **`assign_taxa/<plate>/ASV_table_final.csv`** — the key output: one row per ASV (consensus sequence) per well, with its assigned taxonomy from the best BLAST hit.
6. **`community_matrix/<plate>/<plate>_abundance.csv`** and **`..._presence_absence.csv`** — the ASV table pivoted into a classic samples × taxa community matrix, ready for ecological analysis (diversity indices, ordination, etc.).
7. **`plots/proportion/*.png`** — stacked bar plots of taxonomic composition per barcode, at each rank listed in `--tax_list`.

> 🧬 **If you completed Step 4:** open `assign_taxa/.../ASV_table_final.csv` and check whether `EXT_NEG` and `BLANK` picked up any real hits — if they did, that's contamination worth flagging, exactly as it would be in a real run.

---

## Step 7 — Running on an HPC (Myriad example)

> 🎯 For the general concepts (talking to your HPC admin, writing a config from scratch, testing it) see the bonus **[Running a pipeline on an HPC](/training/hpc/)** — this step is a concrete worked example on top of that, using UCL's **Myriad** cluster.

Because nanoporemetabarcoding was scaffolded from the nf-core template (see the disclaimer at the top of this page), it inherits nf-core's **institutional config** mechanism — so if your institution already has a config, you don't write anything yourself. Browse **[nf-co.re/configs](https://nf-co.re/configs/)** (a searchable, human-friendly view over the [nf-core/configs](https://github.com/nf-core/configs) repo) to check — UCL's Myriad cluster is listed there.

> ⚠️ **Before you run anything, follow the setup steps on your cluster's own config page** — e.g. for Myriad that's **[nf-co.re/configs/ucl_myriad](https://nf-co.re/configs/ucl_myriad/)**. Each institution's page documents cluster-specific prerequisites — for Myriad that means loading a specific Java module (`module load java/temurin-17/17.0.2_8`, added to your `.bashrc`) and installing Nextflow itself into your own `~/bin/`, since it's not preinstalled.
```bash
nextflow run main.nf -profile ucl_myriad --outdir results -resume -bg > log
```

`-profile ucl_myriad` downloads and applies [`ucl_myriad.config`](https://github.com/nf-core/configs/blob/master/conf/ucl_myriad.config) automatically — no `-c` flag, and no separate `-profile singularity` needed (the profile enables Singularity itself). It's worth reading the actual config to see what a real one looks like:

<details>
<summary>What's actually in ucl_myriad.config</summary>

```groovy
executor {
    name = 'sge'
    queueSize = 100
    submitRateLimit = '10/1s'
}

process {
    penv = 'smp'
    clusterOptions = {
        def mem = task.memory.mega
        def cpus = task.cpus
        def memoryPerCpu = mem/cpus
        "-S /bin/bash -l mem=${memoryPerCpu}M "
    }
}

singularity {
    enabled  = true
    cacheDir = "${System.getenv('HOME')}/Scratch/.apptainer/pull"
}
```

Two things worth noticing, since they're easy to get wrong writing your own config:

- **Myriad uses SGE**, whose `-l mem=` flag is **memory per core, not per job** — so the config computes `task.memory / task.cpus` on the fly for every process, rather than using a single fixed value.
- The **Singularity cache** (`cacheDir`) is pointed at `~/Scratch`, not the home directory — home quotas on Myriad are small, and containers are large. Always check where your own cluster wants large/scratch data to live (Step 1 in [hpc.md](/training/hpc/)). This is usally the case for most HPCs.
</details>

> ▶️ **Try it — test the config before a real run**
>
> ```bash
> nextflow run main.nf -profile test_synth,my_hpc_config --outdir my_results
> ```
> Same idea as Step 6 of [hpc.md](/training/hpc/): run the tiny test profile first and check the banner says `executor >  sge`, not `executor >  local` — that confirms jobs are actually going to the scheduler, not running on the login node.

While jobs are running, watch them with `qstat` (Myriad/SGE) — the same command [hpc.md](/training/hpc/) points to for Slurm's `squeue`. Both print a status column whose codes mean the same underlying thing but look different:

| Meaning | `qstat` (SGE/Myriad) | `squeue` (Slurm) |
| --- | --- | --- |
| Running | `r` | `R` |
| Queued, waiting for resources | `qw` | `PD` |
| Held (won't start — e.g. a dependency isn't met) | `hqw` | `PD` *(reason shown separately, e.g. `Dependency`)* |
| Finishing up / cleaning after the job ends | `t` (transferring) | `CG` (completing) |
| Completed successfully | *(drops off `qstat` entirely — check with `qacct -j <jobid>`)* | `CD`, briefly, then drops — check history with `sacct -j <jobid>` |
| Failed to start (config/resource error) | `Eqw` | `F` |
| Hit its time limit | *(job is killed; check `qacct -j <jobid>`)* | `TO` |
| Suspended | `s` / `S` | `S` |
| Being cancelled/deleted | `dr` / `dt` | `CA` |

> 🔍 **`Eqw` is the one you'll actually hit while debugging a config.** It means the job was rejected before it even started — almost always a bad `clusterOptions`/`penv`/queue name. Run `qstat -j <jobid>` (SGE) or `scontrol show job <jobid>` (Slurm) to see *why* it was rejected, rather than just that it was.

In some HPCs, running Nextflow directly from the login node is not recommended (contact your HPC admin for more information). In that case, submit your Nextflow command it as its own SGE (or slurm, if that is your HPC scheduler) job rather than running it directly in your terminal:

<details>
<summary>Cheat sheet — <code>run_nanopore_myriad.sh</code> (submit with <code>qsub run_nanopore_myriad.sh</code>)</summary>

```bash
#!/bin/bash -l
#$ -l h_rt=4:00:0
#$ -l mem=4G
#$ -N nanoporemetabarcoding

module load java/temurin-17/17.0.2_8

nextflow run main.nf \
  -profile ucl_myriad \
  --input wasp_test_data/samplesheet.csv \
  --metadata wasp_test_data/metadata.csv \
  --tags_f wasp_test_data/primers_f.fasta \
  --tags_r wasp_test_data/primers_r.fasta \
  --custom_db wasp_test_data/custom_db.fasta \
  --outdir my_results \
  -resume
```

The `-l mem=4G` / `-l h_rt=4:00:0` here are for the **driver job only** (Nextflow itself is light) — the actual pipeline steps get their own resources per-process from `ucl_myriad.config`, submitted as separate SGE jobs by Nextflow.
</details>

> 💡 **Other schedulers (Slurm, etc.):** the same institutional-profile trick applies wherever nf-core/configs has a listed cluster — check https://nf-co.re/configs first. If yours isn't listed, [hpc.md](/training/hpc/) has side-by-side minimal config examples for both **SGE** and **Slurm**: the main differences are `executor.name` (`'sge'` vs `'slurm'`), how you request memory (SGE: per-core via `clusterOptions`; Slurm: per-job via `--mem`), and the queue/partition option name. A Slurm submission script for this same pipeline would look like `hpc.md`'s own Slurm example, swapping in nanoporemetabarcoding's `--input`/`--metadata`/`--tags_f`/`--tags_r`/`--custom_db` flags shown above.

> 🙋 **No institutional config for your cluster?** Just get your HPC admin in touch with us at Eco-Flow and we will build one.

---

## Step 8 — Resuming a run and changing options

### Changing an option

Taxonomy assignment has adjustable identity thresholds per rank — e.g. `--spident` (species), `--gpident` (genus). Work out how you'd tighten the species-level threshold to 98% identity, but **don't run it yet**:

<details>
<summary>Answer — the modified command</summary>

```bash
nextflow run main.nf \
-profile test,docker \
--outdir my_results \
--spident 98
```
</details>

### The `-resume` flag

Add **`-resume`** and Nextflow reuses cached results for any step whose inputs haven't changed — so re-running the command above only re-executes taxonomy assignment (and anything downstream of it), not the demultiplexing or clustering steps.

> ✅ **What you'll see with `-resume`:** unchanged processes marked `cached`, e.g. `[a1/b2c3] ...:CUTADAPT_FORWARD (plate01) [100%] 1 of 1, cached: 1 ✔`.

---

## Finish

🎉 **You've finished this practical.** You've gone from raw Nanopore reads to a taxonomically-annotated, per-sample ASV table and community matrix — and designed a samplesheet/metadata scheme for a real multi-plate, primer-tagged experiment.

**Next steps:**

- Adapt what you designed in Steps 3–4 to your **own** primer-tag scheme and run it on your own data.
- Explore the full parameter list in [`nextflow.config`](https://github.com/Eco-Flow/nanoporemetabarcoding/blob/master/nextflow.config) — worth tuning per-rank identity thresholds (`--spident`/`--gpident`/`--fpident`/`--opident`) and `--tax_list` for your own taxonomic group.
- Running on a cluster other than Myriad? Step 7 above covers the concrete example; the bonus **[Running a pipeline on an HPC](/training/hpc/)** covers the general concepts (including a Slurm walkthrough).
