If you are tired of the "it works on my machine" excuse, Docker is the solution you have been looking for. This guide will walk you through the core concepts and help you run your first containerized application.

## 1. Introduction: what is Docker?

To truly understand Docker, we need to compare it with the traditional way of isolating environments: Virtual Machines (VMs). While both allow you to run isolated instances of software, they do so at very different layers of your hardware.

**Virtual Machines: The "Heavyweight" Approach**

A Virtual Machine is an emulation of a physical computer. It runs on top of a Hypervisor (software like VMware or VirtualBox) that carves out a portion of your hardware—CPU, RAM, and Disk—to create a completely independent environment. The most important thing to note is that every VM includes its own full Guest Operating System. If you want to run a tiny Python script in a VM, you have to load several gigabytes of Windows or Linux just to support it. This leads to:

* **High overhead:** Significant memory and CPU consumption.
* **Slow boot times:** You have to wait for the entire OS to start.

**Docker Containers: The "Lightweight" Alternative**

Docker takes a different approach called OS-level virtualization. Instead of virtualizing the hardware, Docker virtualizes the Operating System itself. Containers run as isolated processes on the host machine but share the host's Linux kernel. They only package the application and the specific libraries needed to run it. They don't need a guest OS.

| Feature | Virtual Machines (VMs) | Docker Containers |
| :--- | :--- | :--- |
| **Operating System** | Each VM has its own full Guest OS. | All containers share the Host OS kernel. |
| **Size** | Large (usually several GBs). | Very small (often just a few MBs). |
| **Startup Time** | Minutes (needs to boot the OS). | Seconds (starts like a normal app). |
| **Isolation** | Fully isolated (more secure by default). | Process-level isolation (very secure, but shares kernel). |
| **Efficiency** | High resource consumption. | Highly efficient; you can run dozens on one PC. |


## 2. Installation: Setting Up Your Environment

Before we proceed, it is important to note that if you are working on a shared server (for example, a university cluster or a company staging environment), Docker is most likely already installed and configured by the system administrator. You should check this by typing `docker --version` in your terminal.

However, if you wish to run Docker on your own local machine, follow the instructions below based on your hardware requirements.

### 2.a. Standard Installation (CPU-only)

This is the go-to option for general web development and standard applications.

**Windows & macOS:**

The easiest way is to download Docker Desktop. Go to the [official Docker website](https://www.docker.com/products/docker-desktop/). Download the installer and follow the wizard.

Note for Windows users: Ensure that WSL 2 (Windows Subsystem for Linux) is enabled, as it provides significantly better performance than the old Hyper-V backend.

**Linux (Ubuntu/Debian):** 

You should install Docker using the official repository to ensure you get the latest version.

```
sudo apt-get update
sudo apt-get install docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

### 2.b. Advanced Installation (With GPU Support)

If you are planning to work on Machine Learning, Deep Learning, or Heavy Graphics Processing, simply having Docker is not enough. You need to allow the container to "talk" to your NVIDIA graphics card.

Requirements:

* A physical NVIDIA GPU.
* The latest NVIDIA Drivers installed on your host machine.

**Steps for Linux:**

To enable GPU support, you need to install the NVIDIA Container Toolkit. This acts as a bridge between Docker and your GPU drivers.

1. Configure the production repository:

`curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg`

2. Install the toolkit:

`sudo apt-get install -y nvidia-container-toolkit`

3. Restart the Docker daemon to apply changes:

`sudo systemctl restart docker`

**How to verify the GPU installation:** 

Run the following command. If everything is set up correctly, you should see a table showing your GPU statistics:

`docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi`

Important: While Docker Desktop for Windows now supports GPU acceleration automatically through WSL2, Linux users must manually install the toolkit mentioned above to gain hardware access.

## 3. First Steps: Hands-on with Ubuntu 24.04

In this section, we will learn how to create a container, manage its identity, and execute commands. We will use a "raw" Ubuntu 24.04 image, which is perfect for testing because it is essentially a blank slate.

### Step 1: Creating Containers

When you create a container, you have two options for naming it.

**Option A: The Anonymous Way (Random Name)**

If you don't provide a name, Docker will invent one for you.

`docker run -it ubuntu:24.04 /bin/bash`

If you run docker `ps -a` in another terminal, you might see a name like goofy_pasteur or zen_archimedes.

**Option B: The Professional Way (Custom Name)**

It is much better to assign a specific name for easier management:

`docker run -it --name my_ubuntu_lab ubuntu:24.04 /bin/bash`

Note: The `-it` flags are crucial here. `-i` (interactive) keeps the input open, and `-t` (tty) gives you a functional terminal interface.

### Step 2: Working Inside the Container

Once inside the Ubuntu prompt, you are the root user. Let's try to use a tool that isn't installed yet:

`curl --version`

Result: bash: curl: command not found

Install the tool:

`apt update && apt install -y curl`

Verify it works:

`curl -I https://www.google.com`

Now, exit the container by typing `exit`.

### Step 3: Executing Commands from the Outside

One of the most useful features of Docker is the ability to run commands inside a container without entering its shell. This is perfect for automation.

First, restart your container (since exit stops it):

`docker start my_ubuntu_lab`

Now, instead of "logging in," let's run curl directly from your host machine's terminal:

`docker exec my_ubuntu_lab curl -I https://www.github.com`

What happened? Docker sent the command to the running container, executed it, and printed the result directly to your screen. This is a very efficient way to interact with services without leaving your main workspace.

### Step 4: Lifecycle Management (Stop & Remove)

Before you can delete a container, you must ensure it is not running. Docker prevents the accidental deletion of active processes.

1. Stop the container:

`docker stop my_ubuntu_lab`

1. Remove the container:

`docker rm my_ubuntu_lab`

The Shortcut: If you want to delete a container immediately without stopping it first, you can use the "force" flag:

`docker rm -f my_ubuntu_lab`

### Step 5: Final Check

To ensure everything is clean, list all your containers:

`docker ps -a`

If the list is empty, you have successfully mastered the basics of container creation, external execution, and cleanup!

**Summary: basic commands:**

| Command | Description |
| :--- | :--- |
| `docker run -it --name <name> <image>` | Create and enter a new named container. |
| `docker ps -a` | Show all containers (running and stopped). |
| `docker start <name>` | Wake up a stopped container. |
| `docker exec <name> <command>` | Run a command inside a running container from the outside. |
| `docker stop <name>` | Stop a container gracefully. |
| `docker rm <name>` | Delete a stopped container permanently. |




## 4. Sharing Data: Bind Mounts

In this section, we will see how to bridge the gap between your physical computer (the Host) and the virtualized environment of the container. This is crucial because, by default, containers are "ephemeral"—meaning any data created inside them is lost as soon as the container is deleted.

A Bind Mount allows you to map a specific folder (or even your entire hard drive) from your computer to a directory inside the container. It works like a real-time mirror: any change made on one side is immediately reflected on the other.

### 4.a. Mapping a Specific Folder

This is the most common and safest way to work. Suppose you have a project folder on your Desktop. You can "mount" it inside the Ubuntu container like this:

**On Linux/macOS:**

`docker run -it --name lab_session -v /Users/yourname/Desktop/my_project:/work ubuntu:24.04 /bin/bash`

**On Windows (PowerShell):**

`docker run -it --name lab_session -v C:\Users\yourname\Desktop\my_project:/work ubuntu:24.04 /bin/bash`

* Left side of the colon (:): The path on your real computer.
* Right side of the colon (:): The path inside the Docker container (it will be created automatically if it doesn't exist).

### 4.b. Mounting the Entire Hard Drive

In some advanced scenarios—for example, if you need to run a script that scans your whole system or accesses multiple drives—you might want to mount your entire user directory or even the root of your hard drive.

**Warning: Be extremely careful when doing this. If you run a command like rm -rf / inside the container while your whole disk is mounted, you could delete the files on your actual computer.**

To mount your entire User folder:

* Linux/macOS: `-v ~:/host_system`
* Windows: `-v C:\:/host_system`

**Example command (Linux/macOS):**

`docker run -it --name full_access -v /:/total_disk ubuntu:24.04 /bin/bash`

Once inside, if you type ls /total_disk, you will see your computer's actual file system (Applications, Users, System, etc.).

### 4.c. Useful Shortcut: Mounting the Current Directory

If you are already in the terminal and you are inside the folder you want to share, you don't need to type the full path. You can use these variables:

* Linux/macOS: `-v $(pwd):/app`
* Windows (PowerShell): `-v ${PWD}:/app`

**Why is this better than copying files?**

* No Duplicate Data: You aren't "uploading" files to the container; you are just giving the container permission to see them.
* Live Editing: You can keep your favorite code editor (VS Code, Sublime) open on your computer. Every time you save a file, the container sees the update instantly.
* Persistence: You can delete the container, upgrade the image, or restart Docker. Your files stay exactly where they were on your hard drive.

**Summary Table: Volume Flags**

| Flag Syntax | Context |
| :--- | :--- |
| `-v /absolute/path:/target` | Mounts a specific local folder from your computer. |
| `-v $(pwd):/target` | Mounts the folder you are currently in (Linux/macOS). |
| `-v /:/target` | Mounts the entire root of your hard drive (Use with caution!). |
| `-v /path:/target:ro` | **Read-Only:** The container can see files but cannot modify them. |



## 4. Leveraging Pre-built Images for Machine Translation

One of the greatest advantages of Docker is avoiding "dependency hell." Instead of spending hours compiling C++ libraries or fixing Python version conflicts, you can use images where the software is already optimized and ready to go.

### 4.a. Marian NMT

Marian is a high-performance NMT engine. Compiling it manually requires specific versions of Boost and CUDA. With Docker, you can simply pull it:

`docker run --rm -it lefterav/marian-nmt:1.11.0_sentencepiece_cuda-11.3.0`

Benefit: Provides a ready-to-use environment for training and translation with Marian.

### 4.b. OpenNMT

OpenNMT is one of the most popular frameworks for neural translation. Since it relies heavily on PyTorch or TensorFlow, using the official Docker image ensures the backend is correctly configured.

`docker run --rm -it yujioshima/opennmt-py`

### 4.c. Eole (Specific GPU version)

Eole is a modern toolkit built on top of OpenNMT. Because it requires very specific versions of the NVIDIA drivers and PyTorch to function correctly, the "tags" (the text after the colon) can be quite long.

`docker run --rm -it ghcr.io/eole-nlp/eole:0.1.2-torch2.5.1-ubuntu22.04-cuda12.4`

## 5. Managing Images: The pull Command

Until now, we have primarily used docker run, which is a "three-in-one" command that:

* Downloads the image (if not present locally).
* Creates the container instance.
* Executes the specified process.

However, in professional environments—especially when dealing with massive Machine Translation images (which can exceed 10GB)—it is standard practice to separate the download from the execution using `docker pull`.

Why use docker pull?

* Pre-loading Environments: You can download heavy images (like Eole or Marian) in the background while you continue other tasks.
* Offline Readiness: Once an image is "pulled," you no longer require an internet connection to instantiate containers from it.
* Verification: Performing a pull first allows you to verify that the tag and registry permissions are correct before committing to a complex run command with multiple volumes and GPU flags.

**Step-by-Step Execution**

To download the specific Eole image we verified earlier without running it immediately:

`docker pull ghcr.io/eole-nlp/eole:0.1.2-torch2.5.1-ubuntu22.04-cuda12.4`

Once the download is complete, you can verify that the image is stored on your local disk:

`docker images`

Now, when you are ready to work, executing the run command will be instantaneous because Docker will find the image locally:
Bash

`docker run --rm -it --gpus all ghcr.io/eole-nlp/eole:0.1.2-torch2.5.1-ubuntu22.04-cuda12.4`

**Comparison: run vs. pull**

| Feature | `docker run` | `docker pull` |
| :--- | :--- | :--- |
| **Primary Action** | Creates and starts a container instance. | Only downloads the image to the local host. |
| **Internet Dependency** | Required only if the image is missing locally. | Always required to check for the latest version. |
| **System Impact** | Consumes RAM, CPU, and Disk (active process). | Consumes Disk Space only (static storage). |
| **Typical Use Case** | Immediate execution, testing, or processing. | Preparing environments or updating specific tags. |

**Updated Commands Table for GitHub Wiki**

| Command | Purpose |
| :--- | :--- |
| `docker pull <image>` | Downloads the image from a registry to your local host. |
| `docker images` | Lists all images currently stored on your machine. |
| `docker rmi <image_id>` | **Remove Image:** Deletes the image from your disk to free up space. |
| `docker run <image>` | Instantiates a container (pulls automatically if missing). |


## 6. Automating with Dockerfiles

Creating your own image ensures that your environment is exactly the same every time you (or a colleague) run it.

### 6.a. The Anatomy of a Dockerfile

Create a file named Dockerfile (no extension) in your project folder. Here are the most common instructions:

* FROM: The base image you are starting from (e.g., ubuntu:24.04).
* WORKDIR: Sets the "home" directory inside the container for any subsequent commands.
* COPY: Moves files from your real computer into the container image.
* RUN: Executes commands during the build process (like installing software).
* CMD: The default command that runs only when the container starts.

### 6.b. A Practical Example

Let's create an image that comes pre-installed with curl and a custom script.

The Dockerfile:

```
# Start from Ubuntu 24.04
FROM ubuntu:24.04

# Avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt update && apt install -y curl python3

# Create a working directory
WORKDIR /app

# Copy a local script into the container
# (Assuming you have a 'script.py' in your folder)
COPY script.py .

# What to do when the container starts
CMD ["python3", "script.py"]
```

### 6.c. Building the Image

Once your Dockerfile is saved, you need to "bake" it into an image using the build command.

`docker build -t my_custom_tool:v1 .`

* -t: Stands for "tag." It gives your image a name and a version (v1).
* .: This is very important! It tells Docker to look for the Dockerfile in the current directory.

### 6.d. Running Your Custom Image

Now that the image is built, you can run it just like you did with the official Ubuntu image:

`docker run --name test_run my_custom_tool:v1`

**Why use a Dockerfile instead of manual changes?**

* Version Control: You can put your Dockerfile on GitHub. Anyone can download it and recreate your exact environment.
* Layer Caching: If you change your script but not your installations, Docker is smart enough to only rebuild the "COPY" part, making updates extremely fast.
* Documentation: The Dockerfile itself serves as documentation of exactly what software and versions your project requires.

| Instruction / Command | Purpose |
| :--- | :--- |
| `FROM <image>` | Defines the base Operating System or environment (e.g., `ubuntu:24.04`). |
| `WORKDIR /path` | Sets the default working directory for all following instructions. |
| `COPY <src> <dest>` | Copies files or directories from the Host (your PC) to the Image. |
| `RUN <command>` | Executes commands during the **build** process (e.g., installing software). |
| `CMD ["cmd"]` | Specifies the default command that runs when the **container starts**. |
| `docker build -t <name> .` | The CLI command used to create an image from your `Dockerfile`. |


## 7. Running Long Processes: Using tmux with Docker

When performing heavy tasks like model training, you should never run Docker directly in your main terminal. If the connection is interrupted, the container stops. Instead, you should run it inside a tmux session.

**What is tmux?**

tmux creates a "persistent" terminal session on your computer. You can start a process, "detach" from the session (leave it running in the background), and "attach" back later to check the progress.

**A. Basic Workflow**

1. Create a new session:

Give it a name so you can find it later (e.g., translation).

`tmux new -s sessionname`

2. Inside this new screen, start your long-running process:

`docker run --rm -it --gpus all eole-image eole train ...`

3. Detach from the session:
    
Press Ctrl + B, then let go and press D.

The terminal will return to your normal prompt, but Docker is still running in the background.

5. Re-attach later:
    
When you want to see if the process is finished:
    
`tmux attach -t sessionname`

**B. Why this is essential for Docker**

* Stability: If your SSH connection to a server drops, tmux keeps the session alive.
* Multi-tasking: You can have one tmux window showing nvidia-smi (to monitor GPU usage) and another window running the actual Docker container.
* Logging: You can scroll back through the tmux history to see logs that might have been lost in a standard terminal buffer.

**C. Useful tmux Shortcuts for your Wiki**

| Action | Shortcut / Command |
| :--- | :--- |
| **Create New Session** | `tmux new -s <name>` |
| **Detach** (Leave session running in background) | `Ctrl + B`, then `D` |
| **List All Active Sessions** | `tmux ls` |
| **Re-attach to a Session** | `tmux attach -t <name>` |
| **Kill/Terminate a Session** | `tmux kill-session -t <name>` |
| **Enter Scroll Mode** | `Ctrl + B`, then `[` (Use arrow keys to navigate) |

**D. Combining Docker Detach and tmux** 

While Docker has its own "detached" mode (-d), using tmux is generally preferred for interactive tasks because it allows you to see the standard output (STDOUT) in real-time and interact with the container if it asks for input.

If you are training a model on a remote server, always start tmux first. It is the best insurance against a lost internet connection ruining hours of work.

## 8. Conclusions: Mastering the Containerized Workflow

By implementing the strategies outlined in this tutorial, you have moved from a manual, error-prone setup to a modern, scalable development environment. Whether you are training neural translation models or deploying linguistics tools, Docker provides the consistency needed for academic and professional success.

**Summary of Key Concepts**

* Environment Isolation: No more "it works on my machine" excuses. Docker ensures that dependencies like CUDA, PyTorch, and specialized C++ libraries (Marian/Eole) are encapsulated and version-controlled.
* Data Persistence: Using Bind Mounts (-v) allows you to keep your heavy datasets and models on your host machine while the container handles the processing power.
* Automation: Moving from manual commands to Dockerfiles and Build Scripts allows you to recreate complex environments in seconds rather than hours.
* Operational Stability: Tools like tmux ensure that your long-running translation tasks are protected from network interruptions or local crashes.

**The Golden Rules for a Docker Expert**

* Always use Specific Tags: Avoid using :latest in production. Always specify the version (e.g., 0.1.2-cuda12.4) to ensure your results are reproducible next year.
* Keep Images Clean: Use the --rm flag for one-off tasks to prevent "container bloat" from filling up your hard drive.
* Security First: Never mount your entire root directory (/) unless absolutely necessary, and prefer Read-Only (:ro) mounts for your source datasets.
* Monitor Resources: Use docker stats and nvidia-smi to ensure your containers are utilizing your hardware efficiently.

**Final Commands Cheat Sheet**

| Category | Essential Command |
| :--- | :--- |
| **Cleanup** | `docker system prune` — Deletes all unused containers, networks, and images. |
| **Monitoring** | `docker stats` — Displays a live stream of container(s) resource usage statistics (CPU/RAM). |
| **Hardware** | `nvidia-smi` — Verifies GPU availability and memory usage both inside and outside Docker. |
| **Background** | `tmux ls` — Lists all active persistent sessions to check for running training tasks. |