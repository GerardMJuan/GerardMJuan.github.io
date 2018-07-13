# Using Jupyter Notebooks and JupyterLab from the UPF HPC


In this small blog post I will detail how to use Jupyter applications (notebooks and JupyterLab) from a computing node in a HPC. This post is a follow-up to the previous post, so I will assume that you already have defined a custom Python environment. If that is not the case, you will need to install on your own the Jupyter package, but the general procedure still applies.

Jupyter notebooks are really useful because of their interactivity, for learning, and to help with experiment reproducibility. I wanted to use Jupyter with the HPC computing module, and this is the easiest and quickest way to do it.

First, we need to enter an interactive node. We can do it with srun:

```
srun --nodes=1 --partition=high --mem=2GB --pty bash -i
```

This command has a lot of options. A more detailed description of srun can be found here.


In case we need to load any modules, we have to run these two sources to access the module system and load them. If we do not need any, this is optional.

```
source /etc/profile.d/lmod.sh
source /etc/profile.d/easybuild.sh
```

Now that we are in the desired computing node, we load our Python environment:

```
export PATH="$HOME/project/anaconda3/bin:$PATH"
source activate myenv
```

We assume that Jupyter is already installed in this environment (and, if you created with Anaconda, it should be). If not, we can install it simply by doing:

```
pip install jupyter

```

And now we execute the order. This command is a bit more complicated and needs a more in depth explanation:

```
export XDG_RUNTIME_DIR=""
jupyter notebook --ip $(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1) --no-browser
http://127.0.0.1:8888/.
```

The first line simply removes an error of permissions in the HPC module, without affecting anything else. With the *--ip* order, we are telling the Jupyter notebook to run at a specific

Jupyter tutorial:

EXECUTION
---------
Installed kernelspec venv in /homedtic/gmarti/.local/share/jupyter/kernels/venv

Important to remove no permission error





FINAL STEPS FOR SOMETHING THAT SEEMS TO WORK:

# Enter the node

# Make source of modules
source /etc/profile.d/lmod.sh
source /etc/profile.d/easybuild.sh

# load cuda modules
module restore cuda

# Load anaconda path and environment
export PATH="$HOME/project/anaconda3/bin:$PATH"
source activate dlnn

# Start Jupyter
export XDG_RUNTIME_DIR=""
jupyter lab --ip $(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1) --no-browser
http://127.0.0.1:8888/.
