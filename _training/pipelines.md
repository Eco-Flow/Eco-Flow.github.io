---
layout: "training"
title: "Pipelines with Nextflow"
num: "2"
type: "Lecture"
order: 2
---


<img src="/assets/training/img/pipe.jpeg" alt="drawing" width="200"/>

This section is presented as a lecture. A video link will be added after the course.

Below we have a brief summary:

## Why pipelines ?

Pipelines help automate a series of tasks, allowing better handling, consistency and traceability.

They are useful when running each step manually would be arduous.

## Nextflow

<img src="/assets/training/img/nextflow.png" alt="drawing" width="200"/>

Nextflow is primarily a language, that helps you scaffold a series of tasks into a modern reproducible workflow/pipeline.
It provides a way to automate program downloads (using containers), passing of data through a pipeline (with its data flow programming model) and is modular which allows reuse of modules across any pipeline.

Check out the documentation [here](https://www.nextflow.io/docs/latest/index.html)<br />

Not only this, Nextflow has lots of other features that make it really useful:<br />

**Runtime**: Has simple ways to run the pipelines across different infrastructure (on HPC, locally, AWS, etc.)<br />
**Version Control**: Is integrated with Github and other version control software, for transparent coding and tracebility.<br />
**Unit testing**: Has a way to test each module using nf-test unit testing, to help ensure all constituent parts don't fail<br />
**Community**: It is a huge and diverse community all commited to build reproducible, effective and automated data pipelines ([nf-core.io](https://nf-co.re/))<br />
<p>

To learn more about Nextflow, there is excellent training material at https://training.nextflow.io/

## Nextflow basic structure

Nextflow has a consistent structure that is built up of two main concepts:

**Processes**: a particular job/script/program (1 or multiple) that can have its own inputs/output and a script block. 
The building blocks of Nextflow, which can be seen as a module.

and

**Channels**: which carry the data from input or to output and also pass data between processes.
Here, processes expect data to be in channels, so that Nextflow knows how to handle each data type.


A typical process looks like the following:

```
process TRIM {

   input:
   path 'sample.1.fastq'    
   output:
   path 'sample.1.trim.fastq' 


   script:
   """
   trim_galore -o sample.1.trim.fastq sample.1.fastq 
   """
   
}
```

In the above process:<br />
we have a singular input, in this case a specific fastq file.<br />
we have a singular output, in this case the output trimmed fastq file<br />
we have a script scope, spearated by `"""`, that says what command to run<br />

## Next

When you are ready:

Head to part 3 -> [click here](/training/nfcore_rnaseq/)

or

Head back to menu   -> [click here](/training/)
<br/>
