---
layout: post
title: Guide to use Jupyter in an HPC environment
---

In this small blog post I will detail how to use [Jupyter](https://jupyter.org/) applications (notebooks and JupyterLab) from a computing node in a HPC. This post is a follow-up to [the previous post](2018-7-16-Guide-For-Conda-Environment.md).  

I will assume that you already have defined a custom Python environment. If that is not the case, you will need to install on your own the Jupyter package, but the general procedure still applies.

Jupyter notebooks are really useful because of their interactivity, learning, and to help with experiment reproducibility. I wanted to use Jupyter with the HPC computing module, to run programs interactively on the cluster using all the capabilities of the Jupyter Notebooks. This small guide is specific for the [UPF cluster](https://guiesbibtic.upf.edu/recerca/hpc/home), but it could be applied to any HPC environment with minor changes.

First, we need to enter an interactive node. We can do it with the *srun* command:

```
srun --nodes=1 --partition=high --mem=4GB --pty bash -i
```

This command has a lot of options. A more detailed description of srun can be [found here](https://slurm.schedmd.com/srun.html). In case we need to load any modules, after accessing an interactive module we have to run these two sources to access the module system and load them. If we do not need any, this is optional.

```
source /etc/profile.d/lmod.sh
source /etc/profile.d/easybuild.sh
```

Now that we are in the desired computing node, we load our desired Python environment. This command will depend on the directory where anaconda is installed, and the name of your environment:

```
export PATH="$HOME/project/anaconda3/bin:$PATH"
source activate myenv
```

We assume that Jupyter is already installed in this environment (and, if you created with Anaconda, it should be). If not, we can install it simply by doing:

```
pip install jupyter
```
And now we execute the order. This command is a bit more complicated:

```
export XDG_RUNTIME_DIR=""
jupyter notebook --ip $(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1) --no-browser
```

The first line simply removes an error of permissions in the HPC module, without affecting anything else. With the *--ip* order, we are telling the Jupyter notebook to run at the ip address of the node, so that we can access it later from our personal computer. The following part of the code automatically gets the ip address of the adapter. Finally, the *--no-browser* order tells jupyter to not open a browser window. We will do this from our local computer.

After running this code, Jupyter will tell you the ip address where this notebook is running. From a local terminal in your computer, run this code.

```
ssh -NL 8888:IP_ADDRESS:8888 USER@hpc.s.upf.edu
```

Where IP_ADDRESS is ip address where the notebook is running. After successfully logging in, you just have to visit http://127.0.0.1:8888/ to access the notebook from a local browser, running on the HPC cluster. And that's it! You can work seamessly in Jupyter from your local computer, with all the computing power that the cluster offers. This can also be used to run [Jupyter Lab](https://github.com/jupyterlab/jupyterlab), with the same steps.

Source:

https://ulhpc-tutorials.readthedocs.io/en/latest/python/advanced/
