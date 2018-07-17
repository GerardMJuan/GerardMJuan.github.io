---
layout: post
title: Creation of a custom Python environment in the UPF HPC environment
---

One of the most important aspects of a machine learning related PhD is the large computing power needed for the experiments. Normally, in research centers and universities, this is solved by the availability of a cluster infrastructure with large computing capabilities, accessible by every researcher. During my PhD, I have spent countless hours battling with the [High Performance Computing (HPC)](https://guiesbibtic.upf.edu/recerca/hpc/home) unit of my university, Universitat Pompeu Fabra.

My initial lack of knowledge on this kind of infrastructure, the large amount of bugs found (including one that rendered half of the folders in my directory inaccessible, that was fun) and the lack of documentation for some of the options transformed seemingly easy tasks into huge timesinks, something that as a PhD student I want to avoid as much as possible. We have enough things to worry about as it is.

A big problem I found was trying to install libraries that were not available in the module system of the HPC. While there are a lot of available modules, it is not easy to, for example, install specific packages (as root capabilities are not available), modify existing Python libraries or install new ones. Focusing on Python, which is the language I normally use in my research, I like to work in environments where I can control everything, and that is something that I cannot do using the existing HPC software.

For this reason, I have created a [Python environment](https://docs.python.org/3/tutorial/venv.html) directly in my HPC directory. This way, I can have a completely personalized Python kernel that I can modify and control and without using any of the provided modules. I use [**Anaconda**](https://anaconda.org/) to create the environment. The purpose of this small blog post is to detail the steps I followed during the installation.

After logging in, and as a first step, we remove any possible active modules so that they don't interfere:

```
module purge
```

Then, we need to download and install Anaconda. You can install it wherever you like:

```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/project/anaconda3
```

We update the PATH variable to the installed package. We can add this line to .bashrc file to apply it automatically each time we enter the HPC environment. I prefer to do it manually each time, so that if I need to use the default Python modules I can do it seamlessly, but it is up to you.

```
export PATH="$HOME/project/anaconda3/bin:$PATH"
```

Now we are prepared to create the custom environment. We have to decide which version of Python do you want to install. In any case, you can create different Python environments for different versions.

```
conda create -y -n envname python=3.6 anaconda
```

*envname* will be the name of the virtual environment. You can choose any name. To activate the environment, we just have to run (this will have to be done at the start of each session):

```
source activate envname
```

And we have a complete customizable Python environment in the HPC cluster without using any of the modules. We can modify the libraries and use **pip** and **conda** to install packages without any limitations. To reactivate the environment, we just define the PATH to include anaconda3 again and reactivate the environment.

Note that this is not necessary to work with the HPC and use the full capabilities of the cluster server, as one could just load the required modules off-the-shelf and work with them. However, for people that works better in a fully customizable environment and needs to install weird packages, just like me, this is the faster, easier and safer solution that I have found.

Happy computing!

Sources:

https://research.computing.yale.edu/support/hpc/user-guide/using-gpus-python-deep-learning
