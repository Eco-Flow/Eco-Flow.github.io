---
layout: "training"
title: "Command line basics"
num: "1"
type: "Practical \u00b7 optional"
order: 1
---

🧭 [◀️ Part 0 · Setup](/training/setup/) &nbsp;|&nbsp; [🏠 Course menu](/training/) &nbsp;|&nbsp; **Next:** [Part 2 · Pipelines ▶️](/training/pipelines/)

🚀 **Start now:** [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Eco-Flow/training) — *first launch takes a couple of minutes to build.*

---

⏱ **Estimated time:** ~45 minutes &nbsp;•&nbsp; 🟢 Beginner &nbsp;•&nbsp; No prior experience needed

This section gives you a short, hands-on introduction to the command line — the tool you'll use to run a **Nextflow** pipeline later in the course.

Rather than read a long list of commands, you'll **learn a little, then immediately try it**. Every "Try it" box has a hidden **Expected output** so you can check you're on the right track. Don't just read the commands — type them!

> 💡 **How to use this page:** Keep a terminal open beside these notes. When you hit a **▶️ Try it** box, type the commands yourself. When you finish, tick the checklist at the bottom.

### What you'll be able to do by the end

- Move around the file system and inspect files and folders
- Create, copy, move and delete files and directories
- View and search inside text files
- Chain commands together with pipes and redirection
- Use variables and the `$PATH` to install a program (Nextflow!)

---

## What is the terminal?

<img src="/assets/training/img/cmd.png" alt="drawing" width="200"/>

The terminal is where you type instructions to tell the computer what to do — no clicking required.

We use a **UNIX** terminal: an operating system (OS) with a core set of commands available to run code and operate on a computer. Every command in this tutorial is a UNIX command.

A few terms you may hear:

| Term | Meaning |
| --- | --- |
| **LINUX** | A flavour of UNIX with extensions on the base OS |
| **CLI** | Command Line Interface (your terminal) |
| **UI** | User Interface (your desktop with clickable icons) |

MacOS and LinuxOS machines have a UNIX terminal by default. On Windows you'd normally install something like the Windows Subsystem for Linux (WSL). **For this course you're already in a UNIX environment, so there's nothing to install** — just open a terminal and follow along.

---

## Block 1 — Finding your way around

<img src="/assets/training/img/knife.png" alt="drawing" width="300"/>

Your first job is always to answer two questions: *where am I?* and *what's here?*

| Command | What it does |
| --- | --- |
| `pwd` | **P**rint **w**orking **d**irectory — tells you where you are right now |
| `ls` | **L**i**s**t the files and folders in the current directory |
| `tree` | Print the directory structure as a tree |
| `cd` | **C**hange **d**irectory (move into another folder) |
| `man` | Print the **man**ual for a command (press `q` to quit) |

`cd` has a few handy shortcuts:

- `cd ./directory` — move *into* a folder called `directory`
- `cd ..` — go **up** one directory
- `cd -` — jump **back** to the previous directory
- `cd` (on its own) — go to your **home** directory

> 📍 **Where should I be?** For every exercise you should be inside the **`eco-flow-training`** folder. In the Codespaces environment your terminal opens there automatically and the full path is `/workspaces/training/eco-flow-training`. If you're running the course from a local clone the path will look different (e.g. `/Users/you/training/eco-flow-training`) — what matters is that it **ends in `eco-flow-training`**. If it doesn't, run `cd` into it before continuing.

> ▶️ **Try it — where am I and what's here?**
>
> ```bash
> pwd
> ls
> ```
>
> <details>
> <summary>✅ Expected output</summary>
>
> `pwd` prints the folder you're in. In Codespaces that's:
>
> ```
> /workspaces/training/eco-flow-training
> ```
>
> (Locally the start of the path differs, but it should still end in `eco-flow-training`.)
>
> `ls` lists what's inside it — you should see the course folders, including `data`, `docs` and `exercise`:
>
> ```
> README.md  codespaces.config  condition.tsv  data  docs  exercise  hello-nextflow
> ```
>
> (Your exact list may vary slightly depending on the environment.)
> </details>

> ▶️ **Try it — look inside a folder without moving into it, then see the whole tree**
>
> ```bash
> ls data
> tree
> ```
>
> <details>
> <summary>✅ Expected output</summary>
>
> `ls data` shows the FASTQ sequencing files you'll analyse later in the course:
>
> ```
> SRR6357070_1.fastq.gz  SRR6357070_2.fastq.gz  SRR6357071_1.fastq.gz  ...
> ```
>
> `tree` draws the same information as a branching structure:
>
> ```
> .
> ├── data
> │   ├── SRR6357070_1.fastq.gz
> │   └── ...
> ├── docs
> └── exercise
> ```
> </details>

> 🤔 **Predict, then check:** before you run it, what do you think `cd data` followed by `pwd` will print? Try it, then use `cd -` to jump straight back.

---

## Block 2 — Creating, moving and removing

Now that you can move around, let's make and manage files and folders.

| Command | What it does |
| --- | --- |
| `mkdir` | **M**a**k**e a new **dir**ectory |
| `cp` | **C**o**p**y a file/folder (keeps the original; add `-r` for a directory) |
| `mv` | **M**o**v**e or rename a file/folder (the original name is gone) |
| `rm` | **R**e**m**ove/delete a file (add `-r` for a directory — ⚠️ no undo!) |
| `nano` | Open the `nano` text editor (save & exit with `Ctrl+X`, then `y`, then `Enter`) |

> ⚠️ **There is no recycle bin on the command line.** `rm` deletes permanently and immediately. Read the line twice before you press Enter.

> ▶️ **Try it — make a folder, move into it, and create a file**
>
> ```bash
> mkdir practice
> cd practice
> nano hello.txt      # type a line of text, then Ctrl+X, y, Enter
> ls
> ```
>
> <details>
> <summary>✅ Expected output</summary>
>
> After you save and quit `nano`, `ls` shows your new file:
>
> ```
> hello.txt
> ```
> </details>

> ▶️ **Try it — copy, rename, then clean up**
>
> ```bash
> cp hello.txt hello_backup.txt   # copy (original stays)
> ls
> mv hello_backup.txt goodbye.txt # rename
> ls
> rm goodbye.txt                  # delete the copy
> ls
> ```
>
> <details>
> <summary>✅ Expected output</summary>
>
> The listings change at each step:
>
> ```
> hello.txt  hello_backup.txt     # after cp
> goodbye.txt  hello.txt          # after mv
> hello.txt                       # after rm
> ```
> </details>

> 🤔 **Predict, then check:** you're now inside `practice`. Which command takes you back up to `eco-flow-training`? Run it and confirm with `pwd`.

---

## Block 3 — Viewing what's inside a file

You'll often want to peek inside a file without opening an editor. These commands print file contents straight to the terminal.

| Command | What it does |
| --- | --- |
| `cat` | Print **all** lines of a file (also joins/**cat**enates files together) |
| `zcat` | Same as `cat`, but for gzipped (`.gz`) files |
| `head` | Print the **top** lines of a file (`-n` sets how many) |
| `tail` | Print the **bottom** lines of a file (`-n` sets how many) |
| `wc` | **W**ord **c**ount — lines, words and characters (`-l` for lines only) |
| `sort` | Sort lines |
| `uniq` | Collapse **adjacent** duplicate lines into one |

> 💡 `uniq` only removes duplicates that are **next to each other**, so you almost always `sort` first (you'll do exactly this in Block 5).

> ▶️ **Try it — read a text file top and bottom**
>
> There's a poem in `exercise/cancao_do_exilio`. Let's look at it.
>
> ```bash
> cd exercise
> head -n 4 cancao_do_exilio
> tail -n 2 cancao_do_exilio
> wc cancao_do_exilio
> ```
>
> <details>
> <summary>✅ Expected output</summary>
>
> `head -n 4` prints the first four lines of the poem, `tail -n 2` prints the last two, and `wc` reports three numbers — **lines, words, characters**:
>
> ```
>       27     116     662 cancao_do_exilio
> ```
>
> (The three numbers are lines, words and characters, followed by the filename.)
> </details>

> ▶️ **Try it — peek inside a compressed FASTQ file**
>
> Your sequencing data is gzipped, so plain `cat` would print garbage. Use `zcat` instead:
>
> ```bash
> cd ../data
> zcat SRR6357070_1.fastq.gz | head -n 4
> ```
>
> <details>
> <summary>✅ Expected output</summary>
>
> The first **read** in a FASTQ file — four lines: an ID, the DNA sequence, a `+`, and quality scores:
>
> ```
> @SRR6357070.1 1/1
> GATCGGAAGAGCACACGTCTGAACTCCAGTCAC...
> +
> AAAAAEEEEEEEEEEEEEEEEEEEEEEEEEEEE...
> ```
> </details>

> 🤔 **Predict, then check:** a FASTQ file uses 4 lines per read. If `zcat file | wc -l` prints `4000`, how many reads is that? (Scroll to Block 5 to actually count them with a pipe.)

---

## Block 4 — Searching inside files

Reading a whole file is fine when it's short. When it's long, you want to **search**.

| Command | What it does |
| --- | --- |
| `grep` | Print every line that contains a word/pattern |
| `echo` | Print text (or the contents of a variable) to the terminal |
| `history` | Show the commands you've already run |

Useful `grep` flags:

- `grep -c word file` — **count** matching lines instead of printing them
- `grep -n word file` — show the **line number** of each match
- `grep -i word file` — case-**insensitive** search

> ▶️ **Try it — find a word in the poem**
>
> ```bash
> cd ../exercise
> grep palmeiras cancao_do_exilio
> grep -c palmeiras cancao_do_exilio
> grep -n Deus cancao_do_exilio
> ```
>
> <details>
> <summary>✅ Expected output</summary>
>
> `grep` prints each line containing *palmeiras*; `-c` collapses that to a count; `-n` prefixes each match with its line number:
>
> ```
> ... lines containing "palmeiras" ...
> 4                                # from grep -c
> 23:Não permita Deus que eu morra # from grep -n
> ```
> </details>

> 🤔 **Predict, then check:** what does `history | grep grep` do? Run it and see — it searches your own command history for every time you used `grep`.

---

## Block 5 — Pipes, redirection and wildcards

<img src="/assets/training/img/hieroglyph.jpeg" alt="drawing" width="300"/>

This is where the command line becomes powerful: you **chain** small commands together. A few special characters do the plumbing.

| Symbol | Meaning |
| --- | --- |
| <code>&#124;</code> | **Pipe** — send the output of one command into the next |
| `>` | Redirect output to a file (**overwrites** — ⚠️ replaces the file if it exists) |
| `>>` | Redirect output to a file (**appends** — adds to the end) |
| `*` | Wildcard — matches any characters (e.g. `*.gz` = all files ending `.gz`) |
| `#` | Comment — the rest of the line is ignored |
| `$` | Marks a variable (see Block 7) |

The classic example reads a file, sorts it, keeps unique lines, and saves the result:

```bash
cat file | sort | uniq > sorted_uniq_file
```

> ▶️ **Try it — count the reads in a FASTQ file with a pipe**
>
> ```bash
> cd ../data
> zcat SRR6357070_1.fastq.gz | wc -l
> ```
>
> Remember: 4 lines per read, so divide the answer by 4.
>
> <details>
> <summary>✅ Expected output</summary>
>
> A single number — the total number of lines in the uncompressed file:
>
> ```
> 200000
> ```
>
> That's `200000 / 4 = 50000` reads. Piping meant we never had to save an uncompressed copy to disk.
> </details>

> ▶️ **Try it — use a wildcard and save the result to a file**
>
> ```bash
> ls *.gz                       # every gzipped file in this folder
> ls *_1.fastq.gz > read1_files.txt
> cat read1_files.txt
> ```
>
> <details>
> <summary>✅ Expected output</summary>
>
> `ls *.gz` lists only the `.gz` files; the second command doesn't print anything (it went into the file instead); `cat` shows what was saved:
>
> ```
> SRR6357070_1.fastq.gz
> SRR6357071_1.fastq.gz
> SRR6357072_1.fastq.gz
> ...
> ```
> </details>

> 🤔 **Predict, then check:** what's the difference between running the `ls ... > read1_files.txt` line twice with `>` versus `>>`? Try both and `cat` the file each time.

---

## Block 6 — Flags and file permissions

### Flags change how a command behaves

A **flag** is an option you add after a command, usually starting with `-`. Here are common flags for `ls`:

| Flag | Effect |
| --- | --- |
| `-l` | long format (one file per line, with details) |
| `-a` | show hidden files (those starting with `.`) |
| `-h` | human-readable sizes (KB/MB instead of bytes) |
| `-t` | sort by time modified |
| `-S` | sort by size |
| `-r` | reverse the order |

You can combine flags: `ls -lah`. To see every flag a command supports, use `man command_name`.

> ▶️ **Try it — inspect files in detail**
>
> ```bash
> ls -lh
> ls -lS      # largest first
> ```
>
> <details>
> <summary>✅ Expected output</summary>
>
> Long format shows permissions, owner, size and date for each file:
>
> ```
> -rw-r--r--  1 user  group  2.2M May 22 09:34 SRR6357070_1.fastq.gz
> ...
> ```
>
> The left-most column (`-rw-r--r--`) is the **permissions** — that's what we change next.
> </details>

### Permissions decide who can do what

`chmod` (**ch**ange **mod**e) sets who is allowed to **read**, **write** or **execute** a file.

- **Who:** `u` user (owner) · `g` group · `o` other · `a` all
- **Change:** `+` add · `-` remove
- **What:** `r` read · `w` write · `x` execute

For example, `chmod a+r file` lets **all** users **read** the file, and `chmod u+x script.sh` lets **you** **execute** a script. You'll use exactly this in the capstone to run your own script.

---

## Block 7 — Variables and the `$PATH`

Variables store information and are written with a `$` sign. **Environment variables** are available anywhere on the machine and are usually UPPERCASE:

| Variable | Holds |
| --- | --- |
| `PATH` | All directories where executable programs are searched for |
| `HOME` | The path to your home directory |
| `USER` | Your username |
| `NXF_VER` | The Nextflow version to use |

> ▶️ **Try it — print some variables**
>
> ```bash
> echo $USER
> echo $HOME
> echo $PATH
> ```
>
> <details>
> <summary>✅ Expected output</summary>
>
> `echo $PATH` prints a colon-separated list of directories the shell searches for programs:
>
> ```
> /opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
> ```
> </details>

Why does `$PATH` matter? If a program lives in one of those directories, you can run it by name from **anywhere** — no full path needed. You add a directory to `$PATH` with `export`:

```bash
export PATH=$PATH:/workspaces/training/eco-flow-training
```

This puts our course folder on the `$PATH`, so any executable script there becomes visible no matter where you are. **You'll rely on this in the capstone to install Nextflow.**

---

## Reference — other handy commands

You won't need all of these today, but they're worth knowing.

| Command | What it does |
| --- | --- |
| `wget` | Download the contents of a URL (`-O` sets the output name) |
| `curl` | Download the contents of a URL (`-o` sets the output name) |
| `which` | Show the path to a program (e.g. `which perl`) |

<details>
<summary>Extra commands (not needed for this course)</summary>

| Command | What it does |
| --- | --- |
| `ssh` | Access a remote server/cluster |
| `export` | Set an environment variable |
| `open` | Open a file the "expected" way (e.g. a PDF) |
| `cut` | Cut out selected columns/sections of a file |
| `gzip` | Compress or decompress files to save space |

</details>

### A note on programming languages

Some scripts are written in other languages. You run them by naming the interpreter first:

- `bash my_script.sh` — bash, a UNIX command language
- `perl my_script.pl` — Perl, a versatile scripting language
- `python my_script.py` — Python, a modern general-purpose language
- `Rscript my_script.R` — R, for statistics
- `java ...` — Java, an object-oriented language

Many scripts start with a **shebang** (`#!`) on the first line, telling UNIX which interpreter to use — so you can run the script directly without naming the language:

```bash
#!/bin/bash
#!/usr/bin/env Rscript
#!/usr/bin/env python3
```

### Paths, quickly

- A **full (absolute) path** starts with `/`, e.g. `/workspaces/training/eco-flow-training`
- A **relative path** starts from where you are, using `.` (here), `..` (up one) or `~` (home), e.g. `./data/SRR6357070_1.fastq.gz`

---

# 🏁 Capstone challenge — install Nextflow yourself

You now know enough to do something real: **download the Nextflow program, make it executable, and put it on your `$PATH`.** This is exactly how you'd install a bioinformatics tool for real.

Work through the steps. Each has a hidden **Cheat sheet** if you get stuck — but try first!

### Step 1 — Set up a workspace

Make sure you're in the course root, then create the folder you'll use for the RNA-seq run later.

```bash
pwd            # the path should end in eco-flow-training
mkdir rnaseq_experiment
```

<details>
<summary>Cheat sheet</summary>

```bash
# In Codespaces the course folder is /workspaces/training/eco-flow-training.
# If pwd shows you're somewhere else, cd into eco-flow-training first, then:
mkdir rnaseq_experiment
ls                                          # you should now see rnaseq_experiment
```
</details>

### Step 2 — Write and run your own script

Create a file `list.sh` containing the single line `ls -la`, using `nano`.

<details>
<summary>Cheat sheet — creating the file</summary>

```bash
nano list.sh
# type:  ls -la
# then Ctrl+X, y, Enter
```
</details>

Now try to run it just by typing its name:

```bash
list.sh
```

> ❌ You'll see `bash: list.sh: command not found`. The shell only auto-finds programs on the `$PATH` (Block 7) — and your current folder isn't on it.

So point at the file directly with `bash`:

```bash
bash ./list.sh
```

> ❌ Now you'll see `bash: ./list.sh: Permission denied`. The file isn't marked executable yet.

Fix that with `chmod` (Block 6), then run it:

```bash
chmod u+x ./list.sh
bash ./list.sh
```

<details>
<summary>✅ Expected output</summary>

The script runs `ls -la` and lists everything in the folder, including your new `list.sh` and `rnaseq_experiment`:

```
total 24
drwxr-xr-x  ... .
drwxr-xr-x  ... ..
-rwxr--r--  ... list.sh
drwxr-xr-x  ... rnaseq_experiment
...
```

Notice the `x` in `-rwxr--r--` — that's the execute permission you just added.
</details>

### Step 3 — Download and install Nextflow

Nextflow is already installed in this environment, but we'll download our own copy for practice. First check the Java prerequisite (already installed here as v17):

```bash
java -version
```

Now download Nextflow. This uses `curl` (like `wget`) to fetch the installer and pipe it straight into `bash`:

```bash
curl -s https://get.nextflow.io | bash
```

> 💡 `-s` is "silent" (hides the progress noise). The `|` pipe sends the downloaded script directly into `bash` to run it.

Check the downloaded file and make sure it's executable:

```bash
ls -l nextflow
chmod +x nextflow
```

Right now there are **two** Nextflows — the pre-installed one and your new copy. See which one the shell finds first:

```bash
which nextflow
echo $PATH
```

To make **your** copy the default, move it into a directory that's already on the `$PATH` (`/usr/local/bin`), then confirm:

```bash
mv nextflow /usr/local/bin/nextflow
which nextflow
nextflow info
```

<details>
<summary>Cheat sheet — full sequence</summary>

```bash
curl -s https://get.nextflow.io | bash
chmod +x nextflow
mv nextflow /usr/local/bin/nextflow
which nextflow      # -> /usr/local/bin/nextflow
nextflow info       # prints the version you just installed
```
</details>

<details>
<summary>✅ Expected output</summary>

`nextflow info` prints version and system details:

```
Version: 24.x.x build xxxx
System: ...
Runtime: ...
```
</details>

### Step 4 — Make an alias (optional 🟡)

When you type the same command a lot, an **alias** turns it into a short word. Aliases live in `~/.bash_profile` (in your home directory). A couple already exist there:

```bash
alias lss='ls -al'      # lss = long listing incl. hidden files
alias h1='head -n 1'    # h1  = show the first line of a file
```

Add your own alias that shows the last 5 commands you ran.

<details>
<summary>Cheat sheet</summary>

Add this line to `~/.bash_profile` (e.g. with `nano ~/.bash_profile`):

```bash
alias hist5='history | tail -n 5'
```

Then reload the file so the shell knows about it:

```bash
source ~/.bash_profile
hist5        # try it — and try lss and h1 too
```

You can name the alias anything, as long as it isn't already a command.
</details>

### Step 5 — Save your history (optional 🟡)

It's good practice to keep a record of what you did. Save your session `history` to a file:

```bash
history > my_history.txt
```

Then, in the VS Code file panel on the left, right-click `my_history.txt` and choose **Download** to save it to your own machine.

---

## ✅ Section checklist

Tick these off — if you can do them all, you're ready for the pipeline lecture.

- [ ] I can find where I am (`pwd`) and list files (`ls`)
- [ ] I can create, copy, move and delete files and folders
- [ ] I can view a file with `cat`/`zcat`, `head` and `tail`
- [ ] I can search a file with `grep` and count with `wc`
- [ ] I can chain commands with a pipe `|` and save output with `>`
- [ ] I can read `ls -l` permissions and change them with `chmod`
- [ ] I understand what `$PATH` is and installed Nextflow onto it

---

## 🛟 Troubleshooting — the three errors everyone hits

| Message | What it means | Fix |
| --- | --- | --- |
| `command not found` | The shell can't find a program by that name | Check spelling; if it's a script in the current folder, run it as `bash ./script.sh` or add it to `$PATH` |
| `Permission denied` | The file isn't marked executable | `chmod u+x file` (Block 6) |
| `No such file or directory` | The path is wrong or you're in the wrong place | Run `pwd` and `ls` to check where you are, then fix the path |

---

## Next

Head back to the menu → [click here](/training/)

Head to Part 2 → [click here](/training/pipelines/)

---

🧭 [◀️ Part 0 · Setup](/training/setup/) &nbsp;|&nbsp; [🏠 Course menu](/training/) &nbsp;|&nbsp; **Next:** [Part 2 · Pipelines ▶️](/training/pipelines/)
