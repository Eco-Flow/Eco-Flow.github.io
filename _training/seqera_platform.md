---
layout: "training"
title: "Monitoring runs with Seqera Platform"
num: "8"
type: "Practical \u00b7 optional"
order: 8
file: "seqera_platform.md"
---

🚀 **Start now:** [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Eco-Flow/training) — *first launch takes a couple of minutes to build.*

---

⏱ **Estimated time:** ~30 minutes &nbsp;•&nbsp; 🟡 Practical · optional

> 🎯 **Who is this for?** Anyone who'd rather follow their runs in a web browser than in a terminal — especially once runs move to an HPC and take hours or days. You'll need a free Seqera account (Step 1). Everything here works from Codespaces, your laptop, or a cluster.

### What you'll learn

- What Seqera Platform is, and what it does (and doesn't) do for you
- How to create an access token, and keep it safe
- How to watch a run live in the browser, and read what it tells you
- How to do the same for runs on your HPC
- What's involved in *launching* pipelines from the Platform

---

## Step 0 — What is Seqera Platform?

**[Seqera Platform](https://seqera.io/platform/)** is a web interface for Nextflow runs, built by the same people who make Nextflow. It was called **Nextflow Tower** until 2023, which is why the token and the command-line flag below still say "tower".

It gives you, in a browser:

- **live progress** of a run: every task, its status, and its logs
- **resource usage**: how much CPU and memory each step really used
- **a record** of what was run: the exact command, parameters and config
- optionally, a **Launchpad** to start pipelines by filling in a form instead of typing a command

> 🧠 **It doesn't run anything itself.** Your pipeline still runs where it always did: your Codespace, your laptop, your HPC, or a cloud account. The Platform watches those runs (and can *submit* them for you, see Step 5). It's a dashboard, not a computer.

| Flavour | What it is |
| :--- | :--- |
| **Seqera Cloud** | Hosted at [cloud.seqera.io](https://cloud.seqera.io), free to sign up and use for monitoring. This is what we'll use. |
| **Seqera Enterprise** | The same software, installed and run by your own institution. If your organisation has one, use its address instead of cloud.seqera.io. |

---

## Step 1 — Create an account and an access token

1. Go to **[cloud.seqera.io](https://cloud.seqera.io)** and sign in with GitHub, Google, or an email address. (With email, you're sent a sign-in link rather than setting a password.)
2. Once you're in, open the **user menu** (your name, top right) and choose **Settings → Your tokens**.
3. Select **Add token**, give it a name you'll recognise (e.g. `codespaces-training`), and create it.
4. **Copy the token now.** It's shown only once. If you lose it, delete it and make a new one.

<!-- TODO: add screenshots of the token page and the runs page -->

> 🔐 **A token is a password.** Anyone holding it can act as you in the Platform. Don't paste it into a file you might commit, a chat message, or a shared notebook. If it leaks, delete it on this page — that immediately stops it working.

> 👥 **Workspaces.** New accounts also get access to the **Community Showcase** workspace, which comes with ready-made nf-core pipelines and some free cloud compute to try them on. Your own runs, like the ones below, go to your personal workspace by default.

---

## Step 2 — Give the token to Nextflow 🖥️

Nextflow reads the token from an environment variable called `TOWER_ACCESS_TOKEN`:

```bash
export TOWER_ACCESS_TOKEN=<paste your token here>
```

That lasts until you close the terminal. Two better options for everyday use:

<details markdown="1">
<summary>💾 Keep it across sessions (recommended in Codespaces)</summary>

Add it as a **Codespaces secret**, so every Codespace you open has it automatically and it never touches the repository:

1. Go to **[github.com/settings/codespaces](https://github.com/settings/codespaces)** → **New secret**.
2. Name it `TOWER_ACCESS_TOKEN`, paste the value, and give it access to this repository.
3. Rebuild or reopen your Codespace, then check it arrived: `echo ${TOWER_ACCESS_TOKEN:0:4}` (prints just the first few characters).

On your own machine or a cluster, the equivalent is a line in `~/.bashrc`. On a shared cluster, make sure the file isn't readable by others (`chmod 600 ~/.bashrc`).
</details>

<details markdown="1">
<summary>🔑 Or store it in Nextflow's own secrets</summary>

```bash
nextflow secrets set tower_access_token "$TOWER_ACCESS_TOKEN"
```

Then refer to it from a config file, instead of writing the token itself:

```groovy
tower {
    enabled     = true
    accessToken = secrets.tower_access_token
}
```
</details>

> ⚠️ **Never write the token directly into `nextflow.config`** or any file in a git repository. That's one of the most common ways secrets get published by accident.

---

## Step 3 — Watch a run live 🖥️

Add **`-with-tower`** to any `nextflow run` command. Let's use the same small pipeline as [Part 7](/training/hpc/):

```bash
nextflow run nf-core/demo -r 1.2.0 -profile test,docker --outdir demo_results -with-tower
```

Near the top of the output, Nextflow prints a link to the run — **Ctrl-click** (or Cmd-click) it to open the Platform in your browser:

```
Monitor the execution with Seqera Platform using this URL: https://cloud.seqera.io/user/<your-name>/watch/<run-id>
```

The page updates as the run progresses. There's a lot on it; these are the parts worth knowing:

| Tab | What it's good for |
| :--- | :--- |
| **Tasks** | Every task, with its status (pending, running, cached, succeeded, failed) and the resources it used. Click one to see its command, work directory and logs — the same things you dug out of `work/` by hand in [Part 3](/training/nfcore-rnaseq/). |
| **Metrics** | Charts of how much CPU and memory each process *actually* used, against what it asked for. |
| **Logs** | The Nextflow console output, downloadable. |
| **Configuration** | The exact command and the fully resolved configuration used for this run. |
| **Inputs** / **Outputs** | The parameters and input files, and the reports and files produced. |
| **Run Info** | A summary: who ran it, where, with which Nextflow version and executor. |

> ▶️ **Challenge — read the run**
>
> 1. In **Tasks**, open the FASTQC task and find the **work directory** and the **command** it ran. Does the command look like the `.command.sh` you read in Part 3?
> 2. In **Metrics**, which process used the most memory? In [Part 7 Step 2](/training/hpc/) you found that FASTQC *asks* for 12 GB. How much did it actually use?
> 3. Run the command again with `-resume` added. What changes in the **Tasks** tab?

<details markdown="1">
<summary>✅ What you should notice</summary>

1. It's the same command, containers and work directory that Nextflow writes into `work/`. The Platform is showing you the same information, without you needing to find the hash.
2. On this tiny test dataset, every step uses a small fraction of what it requests — a few hundred MB at most. Requests are sized for real data, which is exactly why over-requesting is so common, and why the Metrics tab is useful when tuning a real pipeline for your cluster.
3. The re-run appears as a **separate run** in the Platform, with its tasks marked **cached** instead of running again.
</details>

> 💡 **Nothing leaves your machine except metadata.** Nextflow sends the Platform the run's progress, commands and resource figures, not your sequencing data or results.

---

## Step 4 — Monitoring your HPC runs 🏢

This is where the Platform really earns its place: a run on a cluster can last for days, and checking on it otherwise means logging back in and hunting through logs.

It's the same flag. In the driver job script from [Part 7 Step 5](/training/hpc/), add the token and `-with-tower`:

```bash
export TOWER_ACCESS_TOKEN=<your token>       # better: put this in ~/.bashrc

nextflow run nf-core/rnaseq -r 3.26.0 \
  -profile singularity,<your_cluster> \
  --input samplesheet.csv --fasta genome.fasta --gff genes.gff.gz \
  --outdir results \
  -with-tower \
  -resume
```

Or turn it on in a config file instead of the flag, which is tidier if you always want it:

```groovy
tower {
    enabled = true
    // accessToken is read from $TOWER_ACCESS_TOKEN
    // endpoint = 'https://api.cloud.seqera.io'   // change this for an Enterprise instance
}
```

Two things to check on a cluster:

- **Outbound internet.** The machine running the *driver* (the login node, or the node your driver job lands on) must be able to reach `api.cloud.seqera.io` over HTTPS. Compute nodes don't need it. If your cluster blocks outbound traffic, ask your HPC team, or use your institution's Enterprise instance if it has one.
- **Where the token lives.** `~/.bashrc` is convenient, but on a shared filesystem make sure it's private (`chmod 600 ~/.bashrc`).

Now you can close your laptop and check the run from a phone. When a task fails, the Tasks tab gives you its error and log without an `ssh` session.

---

## Step 5 — Launching pipelines from the Platform (overview)

Monitoring only sends information *out*. The Platform can also **start** runs for you, which is how labs give pipelines to colleagues who don't use the command line. You don't need this for the course, but it's worth knowing what's involved.

| Piece | What it does |
| :--- | :--- |
| **Compute environment** | Where runs happen: AWS/Google/Azure, or your HPC. You set it up once. |
| **Launchpad** | A form per pipeline: pick parameters, press Launch. Runs go to the compute environment you chose. |
| **Datasets** | Samplesheets uploaded and versioned in the Platform, selectable from the Launchpad. |
| **Secrets** | Credentials (e.g. for private registries) that pipelines can use without anyone seeing them. |

For an **HPC**, the interesting piece is the **[Agent](https://docs.seqera.io/platform-cloud/supported_software/agent/overview)**. Clusters almost never accept inbound connections, so instead of the Platform connecting in, you run a small program on the login node that connects *out* to the Platform and waits for work. It's a single binary, started inside `tmux` so it keeps running (the same trick as Part 7's Option A), and it submits jobs to your scheduler as you.

> 🧭 **Is it worth it?** If you're comfortable running pipelines from the terminal, monitoring (Steps 3–4) gives you most of the benefit for five minutes of setup. The Launchpad pays off when several people need to run the same pipeline, or when the people running it aren't command-line users. Setting up a compute environment usually needs your HPC or cloud team involved.

---

## Recap

- Seqera Platform is a **dashboard** for Nextflow runs. Your compute stays where it is.
- Create a token (**Settings → Your tokens**), and pass it to Nextflow with **`TOWER_ACCESS_TOKEN`** — never in a file in git.
- Add **`-with-tower`** to any run, or set `tower.enabled = true` in a config.
- The **Tasks** and **Metrics** tabs show what each step ran and what it really used: the easiest way to see whether your resource requests make sense.
- On an HPC, this means watching a multi-day run without logging in. The driver just needs outbound HTTPS.

---

## Finish

🎉 **You can now watch your runs from anywhere**, and you've seen what the Platform offers beyond monitoring.

**Next steps:**

- Need to set up Nextflow on a cluster with no config yet? See ★ **[Advanced: setting up Nextflow for your HPC](/training/hpc-config/)**.
- The official [Seqera Platform docs](https://docs.seqera.io/platform-cloud/) go much deeper, and Seqera's own [Hello Nextflow training](https://training.nextflow.io/latest/hello_nextflow/) finishes with a chapter on the Platform.
- Eco-Flow will be providing more foundational Nextflow courses soon — email us to join the mailing list: **ecoflow . ucl @ gmail . com**
