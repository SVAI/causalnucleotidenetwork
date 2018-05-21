# Deep Induction

Maybe DeepDuction...

Project by **causalnucleotidenetwork** at the [SVAI](https://sv.ai/#silicon-valley-artificial-intelligence) 2018 [Hackathon P1RCC](https://sv.ai/p1rcc).


## The Idea

Thought up in a whirlwind of ideas in 2-hours with insightful minds of:

- [Aleksandra Zalcman](https://github.com/commandlinegirl) 
- [Naina Thangaraj](https://github.com/nainathangaraj)
- [Steve Osazuwa](https://github.com/Damien-Black)
- [Arkarachai Fungtammasan](https://github.com/Arkarachai)

When interacting with patients researchers/doctors/clinicians have access data in various forms:

* Observations
* NGS
* EHR
* etc...

However information isn't always complete or fully populated. This project seeks to tackle the problem of sparsity in this problem space. Specifically our problem statement is.

> Given some information about the patient can we infer phenotypic or even genotypic data

Take a look at our first steps and hopefully we spark some insights and conversations as we work together towards a cure.

## Method Overview

> Given some information about the patient can we infer phenotypic or even genotypic data

We view this problem statement as a form of [inductive reasoning](https://en.wikipedia.org/wiki/Inductive_reasoning). At a high level our approach follows suite:

1. Learn the complex structure of Papillary Kidney Carcinoma patients
2. Cluster patients to structure our complex data
3. Glean scientific insight into these clusters
	A. Similar phenotypes or genotypes
4. Acquire observations/data on a new patient
5. Classify them in a cluster
6. Inductively deduce additional features of the patient based on their assigned cluster

### Learning Complex Structure

We employ a variational autoencoder to learn structure of p1RCC patients using gene expression data. The technique is originally form a [paper](https://www.biorxiv.org/content/early/2017/10/02/174474) by Gregory P. Way and Casey S. Greene.

Our notebook(s) contains the code and some additional documentation for our VAE implementation, again heavily inspire by Gregory P. Way and Casey S. Greene.

### Data 

Primary source of data as [TCGA](https://cancergenome.nih.gov/)
* FPKM gene expression results (Clemson's PanTCGA Expression Data)
* Clinical observations (xml) files

This repo contains module to parse, link, process clinical and FPKM data.

## Citations

Extracting a Biologically Relevant Latent Space from Cancer Transcriptomes with Variational Autoencoders
Gregory P. Way, Casey S. Greene
bioRxiv 174474; doi: https://doi.org/10.1101/174474

Special thanks to the [SVAI](https://sv.ai/) team for putting together such a great event!