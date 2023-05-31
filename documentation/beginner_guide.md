# Beginner's setup instructions

New to Python? Follow these steps to set up a Python environment on your machine.

### Install Miniconda

We recommend installing [Miniconda](), which will let you create and manage Python environments,  control which version of Python you are using, and install packages using the `conda` program.

### Create a virtual environment

Once you've installed `conda`, open your terminal.
- On `Windows`: launch the **Anaconda Prompt** from the start menu.
- On `Mac`: launch **Terminal** from the start menu.
- On `Linux`: open a terminal window. 

Create a virtual environment for Python version 3.9 using this command:

```
conda create -n mousetumornet python=3.9
```

After that, activate your clean Python environment using `conda activate`.

```
conda activate mousetumornet
```

Once your environment is activated, you can install the Mousetumornet code in it (`pip install` [...]). Go back to [Installation](../README.md#installation) and follow the instructions.

To learn more about managing Python environments with `conda`, see the [documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).