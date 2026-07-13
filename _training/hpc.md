---
layout: "training"
title: "Running a pipeline on an HPC"
num: "\u2605"
type: "Reference"
order: 5
bonus: true
---

🧭 [◀️ Part 3 · nf-core RNA-Seq](/training/nfcore-rnaseq/) &nbsp;|&nbsp; [🏠 Course menu](/training/)

🚀 **Start now:** [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Eco-Flow/training)

---

⏱ **Estimated time:** ~20 minutes reading &nbsp;•&nbsp; 🟣 Bonus / optional &nbsp;•&nbsp; Reference, not a hands-on run

> 🎯 **Who is this for?** Only for those who expect to run pipelines on a **High-Performance Computing (HPC) cluster** at your institution. This is a *conceptual guide with pointers*, not a step-by-step you can run here (every cluster is different).

### What you'll learn

- Why running on an HPC needs a **config**
- Things to find out **from your HPC team** before you start
- Where to find **existing configs** you can reuse or adapt
- How to sketch a minimal config (with optional **SGE** and **Slurm** examples)
- How to **test** a config on a tiny pipeline before a real run
- 🎁 A bonus section: once you have a config, how to actually launch a run

---

## Background

Remember from [Part 2](/training/pipelines/) that Nextflow **separates *what* the pipeline does from *where* it runs**. That's the whole trick here: to move a pipeline onto an HPC you **do not change the pipeline at all**. You just give Nextflow a **configuration** describing your cluster — which job scheduler it uses, what resources to request, and which container engine to use.

You've actually done this already! In [Part 3](/training/nfcore-rnaseq/) you ran with `-c .../codespaces.config` to cap memory. An HPC config is the exact same idea, just describing a cluster instead of a Codespace.

The two things that change on an HPC are:

| On Codespaces / a laptop | On an HPC |
| --- | --- |
| Nextflow runs each task as a **local** process | Nextflow **submits each task as a job** to a scheduler (e.g. Slurm, SGE, etc.) |
| Tools come from **Docker** containers | Tools usually come from **Singularity/Apptainer** containers (Docker is often not allowed) |

Both are set in a config file. The rest of this page is about writing (or borrowing) that file.

---

## Step 1 — Talk to your HPC admin 🧑‍💼

**This is the most important step, and it's mostly non-technical.** Every cluster is configured differently, and your admin/support team already knows the answers. Ask them:

- **Which scheduler** does the cluster use? (**Slurm**, **SGE/UGE**, **PBS/Torque**, **LSF**…) — this sets the Nextflow `executor`.
- **Which container engine** is available? (Almost always **Singularity** or **Apptainer**; Docker is usually forbidden on shared clusters.)
- **How do I load software** — is there a module system? (e.g. `module load nextflow`, `module load singularity`), or can I download my own software.
- **Which queues/partitions** should I submit to, and what are the **limits** (max CPUs, memory, wall-time per job)?
- **Where should work/scratch data go?** Clusters usually have a fast **scratch** filesystem for the (large) Nextflow `work/` directory.
- **Do compute nodes have internet access?** If not, you'll need to pre-download pipelines and containers on a login node first.
- **Is there an account/project code** you must charge jobs to?

> 💡 Write these answers down — every one maps directly to a line in your config below.

In most cases your HPC administrator should be able to help you set all these settings and help make a config for you. But if this is not the case, please shout out to us as Eco-flow, and we will try our best to help get you set up. Also take advantage of the nf-core config repo (https://github.com/nf-core/configs). Here you can even write up an issue and other members of the community should be able to help you build the config.

---

## Step 2 — Check for an existing config (don't reinvent the wheel) ♻️

Before writing anything, check whether someone has **already made a config for your cluster**. The nf-core community maintains a big collection of institutional configs:

- 🌐 **nf-core/configs:** https://nf-co.re/configs
- 📦 **The repo:** https://github.com/nf-core/configs

If your institution is listed, you may be able to run with nothing more than a profile name:

```bash
nextflow run nf-core/rnaseq -profile singularity,<your_institution> ...
```

That single `-profile` pulls in a ready-made, tested config for your cluster. **Always check here first** — it can save you hours.

---

## Step 3 — Find a *similar* config to adapt 🔎

No config for your exact cluster? Find the **closest match** and adapt it. In the [nf-core/configs `conf/` folder](https://github.com/nf-core/configs/tree/master/conf) there are dozens of real institutional configs. Open a few that use the **same scheduler as yours** (e.g. search the files for `executor = 'slurm'`) and use them as a template — they show realistic queue names, resource limits and container settings.

> 📎 Copy the structure, then swap in the specifics your admin gave you in Step 1.

---

## Step 4 — Sketch a minimal config ✍️

A custom config is just a text file (e.g. `mycluster.config`). At its simplest it sets the executor and enables your container engine:

```groovy
// mycluster.config
process {
    executor = 'slurm'        // <-- your scheduler: 'slurm', 'sge', 'pbs', ...
    queue    = 'compute'      // <-- your queue/partition name / Or maybe you don't have a specific queue name
}

// Be a good cluster citizen: don't flood the scheduler with submissions
executor {
    queueSize       = 50          // max jobs queued at once
    submitRateLimit = '10/1min'   // max submissions per minute
}

// Use Singularity/Apptainer instead of Docker
singularity {
    enabled    = true
    autoMounts = true
}
```

You then also point Nextflow at a **cache directory** for containers (so they're downloaded once), usually via an environment variable set before you run:

```bash
export NXF_SINGULARITY_CACHEDIR=/path/to/shared/singularity_cache
```

<details>
<summary>🟨 Optional — a Slurm example</summary>

```groovy
process {
    executor = 'slurm'
    queue    = 'compute'                 // your partition
    // Extra scheduler flags go here, e.g. an account/project to charge:
    clusterOptions = '--account=my_project'
}

executor {
    queueSize       = 100
    submitRateLimit = '10/1min'
}

singularity {
    enabled    = true
    autoMounts = true
}
```

Nextflow translates `cpus`, `memory` and `time` directives into the right `sbatch` requests automatically — you rarely need to write `sbatch` lines yourself.
</details>

<details>
<summary>🟦 Optional — an SGE / UGE example</summary>

```groovy
process {
    executor = 'sge'
    queue    = 'all.q'                   // your queue
    penv     = 'smp'                     // parallel environment name — ASK YOUR ADMIN
    // SGE-specific resource requests often go through clusterOptions:
    clusterOptions = '-l h_vmem=8G'
}

executor {
    queueSize       = 100
    submitRateLimit = '10/1min'
}

singularity {
    enabled    = true
    autoMounts = true
}
```

> ⚠️ The **parallel environment** (`penv`) name is cluster-specific and a very common source of SGE errors — confirm the exact name with your admin.
</details>

> 🔧 **Tune resources with process labels.** nf-core pipelines tag processes with labels like `process_low`, `process_medium`, `process_high`. You can override the resources for each label in your config (e.g. give `process_high` more memory) — see the [nf-core tuning docs](https://nf-co.re/docs/usage/configuration#tuning-workflow-resources).

---

## Step 5 — Get Nextflow and containers ready on the cluster 📦

On many HPCs, there is a way of downloaded approved software, usually something like :

```bash
module load nextflow      # or install per https://www.nextflow.io/docs/latest/install.html
module load singularity   # or apptainer — whatever your cluster provides
java -version             # Nextflow needs Java 17+
```

Or you may be able to install nextflow yourself, following the official guidelines (https://docs.seqera.io/nextflow/install). Then you should have nextflow in your PATH, accessible from any directory you are in, by moving the executable "nextflow" to an executable path, e.g. $HOME/.local/bin/. This requires internet.

If the **compute nodes have no internet**, pre-fetch the pipeline and its containers on the login node first (nf-core provides [`nf-core download`](https://nf-co.re/docs/nf-core-tools/pipelines/download) for exactly this).

---

## Step 6 — Test your config on a tiny pipeline ✅

**Do this before any real analysis.** A quick smoke-test tells you whether your config is actually submitting jobs to the scheduler — much better to find out on a 2-minute test than 12 hours into a real run.

Every nf-core pipeline ships with a built-in **`test`** profile that supplies tiny example data, so you don't need your own samplesheet or genome yet. Run a deliberately small pipeline with your config added:

```bash
nextflow run nf-core/demo -profile test,singularity -c mycluster.config --outdir test_results
```

(`nf-core/demo` is a minimal example pipeline; you could equally test with `-profile test` on `nf-core/rnaseq`.)

### ✅ What to look for

**1. The executor line — this is the key check.** Near the top of the output, Nextflow prints which executor it's using:

```
executor >  sge (3)
```

- If it says **`sge`** (or `slurm`, `pbs`, …) 🎉 your config is working — tasks are being **submitted to the scheduler**.
- If it says **`executor >  local`**, your config was **not** applied and everything is running on the login node (which admins hate!). Re-check the `-c mycluster.config` path and the `executor` line inside it.

**2. Jobs actually in the queue.** Open a second terminal and check the scheduler — you should see Nextflow's jobs appear and clear:

| Scheduler | Command to watch the queue |
| --- | --- |
| Slurm | `squeue -u $USER` |
| SGE / UGE | `qstat` |

**3. A clean finish.** The run should end with something like:

```
-[nf-core/demo] Pipeline completed successfully-
```

and leave a `test_results/` folder behind.

> 🔍 **If a task fails**, Nextflow prints the failing command and a **work directory** path (e.g. `work/a1/b2c3…`). `cd` into it and read `.command.log`, `.command.err` and `.command.sh` — these show exactly what the scheduler ran and why it failed. On an HPC this is your best debugging friend.

Once this tiny test passes, you can trust the config for the real run below.

---

## 🎁 Bonus — actually running it, once you have a config

> This last part is only useful **after** you've done Steps 1–6. 

The run command is just your Part 3 command with two swaps: **`-profile singularity`** instead of `docker`, and **`-c mycluster.config`** for your cluster:

```bash
nextflow run nf-core/rnaseq -r 3.14.0 \
  -profile singularity \
  -c mycluster.config \
  --input samplesheet.csv \
  --fasta genome.fasta \
  --gff genes.gff.gz \
  --outdir my_results \
  -resume
```

### Where does Nextflow itself run?

Here's the part that trips people up. **Nextflow (the "head" or "driver" process) keeps running for the whole pipeline** — it's what submits and monitors all the individual jobs. So it must not be killed when you disconnect. Two common approaches:

**Option A — run the driver in a terminal multiplexer** (simple, good for testing). On a login node, start [`tmux`](https://github.com/tmux/tmux/wiki) or `screen`, launch Nextflow inside it, then detach — it keeps running after you log out.

```bash
tmux new -s rnaseq     # start a session
# ... run the nextflow command above ...
# press Ctrl+b then d to detach; reattach later with: tmux attach -t rnaseq
```

**Option B — submit the driver as its own small job** (cleaner for long/production runs). Write a tiny submission script that requests modest resources (the driver itself is light) and runs the Nextflow command.

<details>
<summary>🟨 Optional — a Slurm submission script (<code>run.sh</code> → <code>sbatch run.sh</code>)</summary>

```bash
#!/bin/bash
#SBATCH --job-name=rnaseq_driver
#SBATCH --partition=compute
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=24:00:00

module load nextflow singularity
export NXF_SINGULARITY_CACHEDIR=/path/to/shared/singularity_cache

nextflow run nf-core/rnaseq -r 3.14.0 \
  -profile singularity \
  -c mycluster.config \
  --input samplesheet.csv \
  --fasta genome.fasta \
  --gff genes.gff.gz \
  --outdir my_results \
  -resume
```

Submit with `sbatch run.sh`.
</details>

<details>
<summary>🟦 Optional — an SGE submission script (<code>run.sh</code> → <code>qsub run.sh</code>)</summary>

```bash
#!/bin/bash
#$ -N rnaseq_driver
#$ -q all.q
#$ -l h_vmem=4G
#$ -l h_rt=24:00:00
#$ -cwd

module load nextflow singularity
export NXF_SINGULARITY_CACHEDIR=/path/to/shared/singularity_cache

nextflow run nf-core/rnaseq -r 3.14.0 \
  -profile singularity \
  -c mycluster.config \
  --input samplesheet.csv \
  --fasta genome.fasta \
  --gff genes.gff.gz \
  --outdir my_results \
  -resume
```

Submit with `qsub run.sh`.
</details>

**Option C — background the driver with `-bg`.** Adding Nextflow's **`-bg`** flag runs the driver as a background process and streams its output to `.nextflow.log` instead of your screen, so you get your prompt back immediately:

```bash
nextflow run nf-core/rnaseq -r 3.14.0 \
  -profile singularity -c mycluster.config \
  --input samplesheet.csv --fasta genome.fasta --gff genes.gff.gz \
  --outdir my_results -resume -bg
```

> ⚠️ **`-bg` on its own may not survive you logging out** of the login node — a disconnect can still kill it. For anything long-running, wrap it so it can't be hung up, e.g. `nohup nextflow run ... -bg &`, or simply start it inside a `tmux`/`screen` session (Option A). Follow progress any time with `tail -f .nextflow.log`.

> 🧵 Whichever option you choose, the driver stays small and long-lived, while the **real work** (alignment, quantification…) is submitted by Nextflow as separate jobs across the cluster — exactly the parallelism from [Part 2](/training/pipelines/), now spread over many compute nodes.

### If something fails

- **Jobs rejected / wrong resources** → your `queue`, `clusterOptions` or `penv` don't match the cluster. Back to Step 1 with your admin.
- **`singularity: command not found` on compute nodes** → the container engine isn't loaded inside jobs; ask how to make it available (often a module load in the config's `beforeScript`).
- **Containers fail to download on compute nodes** → no internet on nodes; pre-download on a login node (Step 5).
- Add **`-resume`** so fixes don't re-run everything from scratch.

---

## Recap

- You don't rewrite the pipeline for an HPC — you **describe the cluster in a config**.
- **Ask your admin** the scheduler, container engine, queues and limits (Step 1). And if they can help you build and test the config.
- **Reuse** an nf-core/configs profile if one exists, or **adapt** a similar one.
- **Test** it first with `-profile test,singularity` on a tiny pipeline and confirm the `executor > slurm/sge` line.
- Run with **`-profile singularity -c mycluster.config`**, keeping the Nextflow driver alive in `tmux`, as a submitted job, or with `-bg`.

---

🧭 [◀️ Part 3 · nf-core RNA-Seq](/training/nfcore-rnaseq/) &nbsp;|&nbsp; [🏠 Course menu](/training/)
