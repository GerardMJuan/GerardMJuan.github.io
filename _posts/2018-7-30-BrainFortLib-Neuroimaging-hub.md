---
layout: post
title:  BrainFortLib: Neuroimaging scripts hub
---

Processing images and scans of the brain has been a big part of my PhD activity. When I started, I had never worked with brain images before, neither with neuroimaging tools and libraries. I was given a set of scripts that my supervisor had used for processing brain images, but apart from that I had no other support: nobody else in my department worked on brain imaging. Over time, I developed many other scripts and pipelines, and adapting existing ones to my needs. All those scripts are now gathered in a single Github repository, [BrainFortLib](https://github.com/GerardMJuan/BrainFortLib-neuroimage-hub).

My idea behind this repository is that other people can find the scripts useful, either for direct use or as examples to create their own. At least, they are more useful here that in an old, dark, folder in my workstation. Also, it can be really useful for any future PhD students in my group starting on this topic.

## Why BrainFortLib?

Just a fancy name. Brain and Lib are obvious. Fort comes from the residence hall's name I studied in during my undergrad.

## What is this repository about?

In this repository you will find:
* Many lines of Python.
* Scripts adapted to work with the [BIDS](http://bids.neuroimaging.io/) format for neuroimage datasets.
* Scripts to run the code in an HPC environment.
* Registration scripts.
* Preprocessing scripts.

## What is this repository not about?
* Perfectly commented, working "out of the box" scripts. Many are commented, while many are not, and they are coded to work for the [UPF HPC](https://guiesbibtic.upf.edu/recerca/hpc/home) environment. They may not work for other environments, or require minimal modifications which are not provided.
* Full end-to-end pipelines.
* Code is only tested in Linux environments, and some of the scripts are in Bash, so they may not work in other environments.

## When is this updated?
My plan is to keep updating this repository during the rest of my PhD, adding new scripts, cleaning up existing code, and making it more useful. I also try to document everything in the [wiki of the repository](https://github.com/GerardMJuan/BrainFortLib-neuroimage-hub/wiki).

## Can I contribute?
Of course! You can add an [issue](https://github.com/GerardMJuan/BrainFortLib-neuroimage-hub/issues), propose changes, or fork it and use it however you like! All the code of the repository is under a [MIT license](https://github.com/GerardMJuan/BrainFortLib-neuroimage-hub/blob/master/LICENSE).
