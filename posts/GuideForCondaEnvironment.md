# Creation of a custom Python environment in the UPF HPC environment

One of the most important things for a machine-learning related PhD is the need of great computing power. Normally, in research centers and universities, this is solved by the availability of a cluster infrastructure with large computing capabilities, accessible by all the researchers, where one can send experiments and processing jobs. During my PhD, I have spent countless hours battling with the High Performance Computing (HPC) of my university, Universitat Pompeu Fabra.

My lack of knowledge on this kind of infrastructure, the large amount of bugs found (including one that rendered half of the folders in my directory inaccessible) and lack of documentation for some of the options have transformed seemingly easy tasks into huge timesinks, something that as a PhD student I want to avoid as much as possible. We have enough timesinks already!

A problem I found was trying to install libraries that were not available in the module system of the HPC. While there are a lot of available modules, it is not easy to, for example, install specific packages (as root capabilities are not available) or modify existing Python libraries or install new ones. Regarding Python, I am used to work in environments where I can control everything, and that is something that I cannot do in the HPC module.

For this reason, I have created a Python environment () directly in my HPC directory. This way, I can have a completely personalizable Python environment without using any of the provided modules, that I can modify and control. I decided to use **Anaconda** to create the environment. Here I detail the steps I performed to create it.

As a first step, we remove any active modules so that they don't interefere:

```
module purge
```

Then, we need to download and install Anaconda. You can install it wherever you like:

```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/project/anaconda3
```

Then, we need to update the PATH variable to the installed package.
```
export PATH="$HOME/project/anaconda3/bin:$PATH"
```

We can add this line to .bashrc file to apply it automatically each time we enter the HPC environment. I prefer to do it manually each time, so that if I need to use the default Python modules I can do it seamlessly, but it is up to you.

Now we are prepared to create the custom environment. We have to decide which version of Python do you want to install. In any case, there can be different environments for different Python versions.

```
conda create -y -n envname python=3.6 anaconda
```

*envname* can be any name. Now, we can activate it:

```
source activate envname
```

And we have a complete customizable Python environment in the HPC cluster without using any of the modules. We can modify the libraries and use *pip* and *conda* packages without any limitations or errors. If we want to reactivate the environment, we just need to export the PATH to anaconda3 again and activate the environment again.

Note that this is not necessary to work with the HPC and use the full capabilities of the cluster server, as one could just load the required modules off-the-shelf and work with them. However, for people that works better in a fully customizable environment, just like me, this is the faster, easier and safer solution that I have found. As a follow-up to this guide, I have also described how to use jupyter notebooks and jupyter-lab, with all their potential, directly from an HPC cluster. You can find it here.

Happy computing!

Sources:

https://research.computing.yale.edu/support/hpc/user-guide/using-gpus-python-deep-learning
