## What is a Virtual Environment?

A Virtual Environment is an isolated workspace for a Python project. It allows you to install specific versions of libraries (dependencies) for a particular project without affecting the global Python installation of your operating system.

## Why should you use one?

When working with Machine Translation, you might need different versions of libraries like OpenNMT, transformers, or flask for different projects.

* **Avoid Conflicts**: Prevents issues when two projects require different versions of the same library.
* **Clean System**: Keeps your operating system's Python environment lean and stable.

Reproducibility: Makes it easier to share your project requirements with others (e.g., via a `requirements.txt` file).

## Working with venv in Linux

Follow these steps to manage your environments via the Terminal.

### 1. Creating the Environment
Navigate to your project folder and run the following command. We usually name the environment folder .venv or env:

`python3 -m venv env`

This creates a directory named `env` containing a copy of the Python binary and a local site-packages folder. You can name the environment as you want, for example envMTUOC:

`python3 -m venv envMTUOC`


## 2. Activating the Environment

Before installing any library, you must "enter" the environment:

`source env/bin/activate`

or whatever other name you used to create the environent:

`source envMTUOC/bin/activate`

These commands are in the case when the virtual environment directory is in the working directory. If it is elsewhere, use the full paths.

How do you know it worked? Your Terminal prompt will now show the name of the environment in parentheses at the beginning of the line, like this: `(env) user@computer:~/project$`

### 3. Installing Packages

Once activated, any package you install using pip will stay inside that isolated folder:

`python3 -m pip install packagename`

To install all the requirements in the `requirements.txt` file write:

`python3 -m pip install -r requirements.txt`

### 4. Deactivating the Environment

When you are finished working on your project, you can exit the virtual environment and return to the system's default Python by simply typing:

`deactivate`

