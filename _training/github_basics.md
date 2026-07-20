---
layout: "training"
title: "Interacting with code on GitHub"
num: "6"
type: "Practical"
order: 6
---

🚀 **Start now:** [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Eco-Flow/training) — *first launch takes a couple of minutes to build.*

⏱ **Estimated time:** ~45–60 minutes &nbsp;•&nbsp; 🟡 Practical

So far you've *run* pipelines other people built. In real research you'll also need to **interact** with that code — report a problem you hit, ask for a feature, fix a typo in the docs, or contribute an improvement. On GitHub, that all happens through a small set of tools: the **README**, **Issues**, and **Pull Requests**. In this part you'll learn what each one is for, and then watch (and try) the full loop: **spot a problem → open an issue → fix it with Claude Code → open a pull request.**

We'll use a real pipeline as our example: **[`Eco-Flow/nanoporemetabarcoding`](https://github.com/Eco-Flow/nanoporemetabarcoding)** — the same pipeline you ran in Part 5.

> ℹ️ **You don't need to be a programmer for this.** Reporting a clear issue or fixing a README typo is a genuine, valued contribution to open-source science — and it's how most people make their *first* contribution.

### What you'll do

- Understand a GitHub repository: the **README**, the **code**, the **Issues** tab and the **Pull Requests** tab
- Learn what makes a **good issue** and write one
- Watch a **live demo**: turn an issue into a fix using **Claude Code**
- Understand the nf-core **fork → branch → commit → pull request** flow — how a change gets reviewed and merged
- **Your turn:** find something to improve in the pipeline and open your own issue (and, optionally, a PR)

---

## Step 0 — What is a GitHub repository?

A **repository** ("repo") is a project's home on GitHub: its code, its history, its documentation, and the conversations around it. Open the example now and keep it in a browser tab:

👉 **https://github.com/Eco-Flow/nanoporemetabarcoding**

Across the top you'll see tabs. The four that matter for this lesson:

| Tab | What it holds |
| --- | --- |
| **Code** | The actual files, plus the README rendered underneath |
| **Issues** | To-do list / bug tracker — things that need doing or fixing |
| **Pull requests** | Proposed changes to the code, waiting to be reviewed and merged |
| **README** (shown on Code) | The front page — what the project is and how to use it |

> ▶️ **Have a look around.** Click into the **Code** tab and open a couple of files (e.g. `main.nf`, `nextflow.config`). You're not expected to understand them — just get a feel for how a real pipeline repo is laid out.

---

## Step 1 — The README

The **README** is the first thing anyone sees. It's the file GitHub renders automatically under the file list on the **Code** tab. A good README answers, quickly:

- **What** does this project do?
- **How** do I install / run it?
- **What** inputs does it need, and what outputs does it produce?
- **Where** do I go for help?

READMEs are written in **Markdown** — the same simple formatting language these course notes use (`#` for headings, `` ` `` for code, `-` for lists). If you can read these notes, you can edit a README.

> ▶️ **Read it critically.** Open the [nanoporemetabarcoding README](https://github.com/Eco-Flow/nanoporemetabarcoding/blob/master/README.md). As you read, keep a note of anything that is unclear, out of date, has a typo, or is missing. **Keep that list** — we'll use it in Step 6.

---

## Step 2 — Issues: the project's to-do list

An **Issue** is a single tracked conversation about *one* thing that needs attention — a bug, a question, a feature request, or a documentation gap. Anyone with a GitHub account can open one.

**What makes a *good* issue?** A maintainer should be able to understand and act on it without having to ask you five follow-up questions. Aim for:

1. **A clear, specific title** — "Typo in README installation command" beats "docs broken".
2. **What you expected** to happen.
3. **What actually happened** (paste the exact error message if there is one).
4. **How to reproduce it** — the exact command you ran, and where.
5. **Your environment** if relevant (Codespaces vs local, pipeline version / `-r` tag).

> 💡 **Bug vs feature vs question.** A **bug** is "something is broken." A **feature request** is "it would be better if it also did X." A **question** is "how do I…?". Labelling your issue as the right kind helps maintainers triage it. GitHub lets maintainers add **labels** (like `bug`, `enhancement`, `documentation`) to sort them.

> ▶️ **Look at real issues.** Open the [Issues tab](https://github.com/Eco-Flow/nanoporemetabarcoding/issues) (try the **Closed** filter too, to see resolved ones). Notice how the clear ones are easy to follow and the vague ones aren't.

---

## Step 3 — Demo: from issue to fix with Claude Code

> 🎬 **Instructor-led demo.** Your tutor will walk through this live. Follow along — you'll do your own version in Step 6. If you're working solo, you can attempt each step yourself.

Here's the full loop we'll demonstrate, using a small, mundane example: **fixing a typo in the README.** (It's deliberately low-stakes — the point is to see the *whole workflow* clearly, not to solve something hard.)

**1. Open the issue.** On the Issues tab → **New issue**. For example:

> **Title:** Typo in README — "pipline" should be "pipeline"
>
> **Body:** The Introduction section of the README spells it "pipline" instead of "pipeline". Small thing, but worth fixing so it reads cleanly.
> *Where:* README.md, Introduction section.

**2. Bring in Claude Code.** [Claude Code](https://www.anthropic.com/claude-code) is an AI coding assistant that runs in your terminal (it's what powers the assistant in these Codespaces). You can point it straight at an issue and ask it to help:

- **Fork** the repository to your own account first (see Step 4), then open **your fork** in a Codespace (green **Code → Codespaces** button on your fork).
- In the terminal, start Claude Code and describe the task, e.g.:

  ```
  > Look at issue #<number> in this repo. Fix the typo it describes in the
  > README ("pipline" → "pipeline"), and check the rest of the file for the
  > same misspelling.
  ```

- Claude Code reads the relevant files, proposes an edit to `README.md`, and you review it. **You are always in control** — nothing changes until you accept it.

> 🧠 **Claude Code is an assistant, not an oracle.** It's fast and good at boilerplate, but *you* are responsible for the change. Read every edit it proposes, and check the result — exactly as we did when we verified pipeline commands earlier in this course.

**3. See the change.** Once accepted, the file on disk is updated. In the next step we turn that local change into a reviewable **pull request**.

---

## Step 4 — Fork, branch, commit & pull request

You don't have permission to push directly to someone else's project — and even maintainers don't edit the main code directly. The standard open-source flow, and the one **[nf-core recommends](https://nf-co.re/docs/contributing/)**, is the **fork → branch → pull request** model:

1. **Fork** — make your *own* copy of the whole repository under your GitHub account (the **Fork** button, top-right of the repo). You have full write access to *your* fork; the original ("upstream") is untouched.
2. **Branch** — on your fork, make a named branch to work on (e.g. `fix/readme-gzip-note`) rather than committing to `master`/`main`. This keeps each change isolated and lets you have several in flight.
3. **Commit** — save a snapshot of your change with a short message describing *what* and *why* ("Document that inputs must be gzipped").
4. **Push** the branch to your fork on GitHub.
5. **Open a Pull Request (PR)** — from *your fork's branch* → *the upstream repo*. The PR shows a **diff** (red = removed, green = added) so reviewers can see exactly what changed.
6. **Review & merge** — a maintainer reads the diff, may ask for changes, and when happy, **merges** it into the upstream project. Your fix is now part of the pipeline. 🎉

```
upstream/master  ●─────────────────────────●───►   (the real repo — you can't push here)
                                           ▲
                          fork + PR        │ merge
                                           │
your-fork/master ●────────────────────────┘
                  \                      /
   your branch     ●──●──●   ──────►   PR   (review → merge upstream)
                 commits
```

> 💡 **Why fork *and* branch?** The fork gives you a copy you're allowed to change; the branch keeps each separate fix tidy and reviewable. Together they mean the real pipeline always stays working, every change is **reviewed** before it lands, and there's a permanent record of *why* it was made — the backbone of reproducible, collaborative science.

> 🔁 **Keeping your fork up to date.** Over time the upstream repo moves on. Before starting new work, sync your fork (GitHub shows a **"Sync fork"** button, or you can `git pull` from upstream) so you branch off the latest code.

> 🌿 **nf-core branch convention — target `dev`, not `master`.** Official nf-core pipelines keep **two** long-lived branches:
> - **`master`** — the stable, *released* code. Only tagged releases are merged here; you never PR straight into it.
> - **`dev`** — the working/integration branch where new changes are collected and tested before the next release.
>
> So when contributing to an nf-core pipeline, you branch off **`dev`** and open your PR **against `dev`**. (The Eco-Flow `nanoporemetabarcoding` pipeline is still in early development and uses a single `master` branch, so here you'll target `master` — but recognise the `dev`/`master` split when you meet it on the official pipelines.)

> 🤖 **Claude Code can drive this too.** With the `gh` GitHub CLI it can fork the repo, create the branch, commit with a sensible message, push, and open the PR against upstream for you. You still review the diff and approve — it just handles the mechanics.

---

## Step 5 — Releases: how a version becomes "official"

Once enough changes have collected on `dev` and been tested, maintainers cut a **release**: they merge `dev` into `master` and create a **tag** — a permanent, named snapshot of the code at that moment, like `3.14.0`. On GitHub these show up under the **Releases** section (right-hand side of the repo's front page, and the **[Releases](https://github.com/Eco-Flow/nanoporemetabarcoding/releases)** / tags page).

Why this matters to you as a *user*:

- A tag never changes. `master` and `dev` keep moving, but `3.14.0` will always be exactly the same code — which is precisely why we pinned it with **`-r 3.14.0`** back in [Part 3](/training/nfcore-rnaseq/). Running a tagged release is what makes an analysis **reproducible**.
- Releases usually come with **release notes** / a `CHANGELOG` describing what's new, fixed, or broken since the last version — read these before upgrading.
- Version numbers follow **semantic versioning** (`MAJOR.MINOR.PATCH`): a bumped *patch* (`3.14.0 → 3.14.1`) is a small fix, a *minor* (`3.14 → 3.15`) adds features, and a *major* (`3.x → 4.0`) may change behaviour in ways that break old commands.

> 💡 **Rule of thumb:** develop and contribute against `dev`, but **run** your real analyses against a **tagged release** (`-r <version>`) so you always know exactly which code produced your results.

---

## Step 6 — Your turn

Now do it yourself. Use the list of README problems you noted in **Step 1** (or find a fresh issue).

> ▶️ **Exercise A — open an issue (everyone should do this).**
>
> On [`Eco-Flow/nanoporemetabarcoding`](https://github.com/Eco-Flow/nanoporemetabarcoding/issues), open a **New issue** for one concrete improvement you found. Make it a *good* issue (Step 2 checklist): clear title, what's wrong, and — if it's a bug — how to reproduce it. Submit it.

> ▶️ **Exercise B — propose the fix (optional, go further).**
>
> Follow the nf-core fork-based flow from Step 4:
> 1. **Fork** [`Eco-Flow/nanoporemetabarcoding`](https://github.com/Eco-Flow/nanoporemetabarcoding) to your own account, then open **your fork** in a **Codespace**.
> 2. Make a **branch** (e.g. `fix/readme-...`).
> 3. Use **Claude Code** to make the change you described — for a small README fix you can even do it in the GitHub web editor (pencil ✏️ icon on the file on your fork's branch).
> 4. **Commit**, push, and open a **pull request** *from your fork's branch to the upstream repo*. Reference your issue with `Fixes #<your issue number>` in the PR description — GitHub will auto-close the issue when the PR merges.
> 5. Read your own **diff** in the PR — does it show exactly (and *only*) what you intended?

> ✅ **What good looks like:** an issue a maintainer could act on without asking you anything, and (for B) a small, focused PR whose diff is easy to read and clearly linked to its issue.

---

## Finish

🎉 **You can now interact with a codebase, not just run it.** You know what a README, an Issue and a Pull Request are for, how a change flows from *problem* → *branch* → *commit* → *PR* → *merge*, and how to use **Claude Code** to help you make that change.

**Next steps:**

- Make your first contribution to a real project — even a typo fix counts. nf-core actively welcomes newcomers: see their [contributing guide](https://nf-co.re/docs/contributing/).
- Learn a little more Git (the version-control tool underneath GitHub) with the friendly [GitHub Skills](https://skills.github.com/) courses.
- Read more about [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and how it fits into a real development workflow.
