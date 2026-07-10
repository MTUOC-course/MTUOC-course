## 1. Introduction

When operating in a shared-resource environment, it is critical to acknowledge that GPUs do not natively support process-level concurrency in the same way CPUs do. Once a GPU's VRAM or compute capacity is saturated, subsequent processes will fail to initialize. This often leads to resource contention: if a new task seizes resources during a temporary lull in an active process, the original job will likely crash upon resuming its workload. To mitigate these risks, we require a robust, deterministic scheduling system. To ensure equitable resource distribution and maintain system integrity, we have implemented **SLURM (Simple Linux Utility for Resource Management)**.

### 1.1. What is SLURM?

SLURM is a workload manager that acts as an intermediary between you and the server's hardware. Instead of running processes directly, you request resources (CPUs, RAM, GPUs).

Key benefits:

* Resource Isolation: No more "Out of Memory" errors caused by other users.
* Job Queuing: If the GPUs are busy, SLURM queues your job and starts it automatically once they are free.
* Fairness: It prevents a single user from monopolizing all system resources.

## 2. Essential Commands

| Command | Purpose |
| :--- | :--- |
| `sinfo` | Check the overall status of the cluster nodes. |
| `squeue` | View the current job queue (who is running what). |
| `sbatch <script.sh>` | Submit a non-interactive job to the background. |
| `srun --pty bash` | Start an interactive session (for debugging/testing). |
| `scancel <job_id>` | Terminate a running or pending job. |


## 3. How to Submit a Training Job (sbatch)

To run a heavy training process, you must create a shell script (.sh). SLURM reads the configuration from special headers starting with #SBATCH.

### A. Basic Template

Ideal for simple tests or single-GPU tasks:

```
#!/bin/bash
#SBATCH --job-name=my_experiment      # Name of the job
#SBATCH --gres=gpu:1                  # Request 1 GPU (e.g., gpu:2 or gpu:4)
#SBATCH --cpus-per-task=8             # Request 8 CPU cores
#SBATCH --mem=64G                     # Request 64GB of RAM
#SBATCH --output=logs/job_%j.log      # Standard output log (%j = Job ID)
#SBATCH --error=logs/job_%j.err       # Error log

# 1. Load your environment
source /path/to/your/env/bin/activate

# 2. Run your code
python train.py --config my_config.yaml
```

### B. Advanced Production Script

For multi-GPU training and high-reliability tasks, we recommend this robust template:
Bash

```
#!/bin/bash
#SBATCH --job-name=train_eole_big
#SBATCH --gres=gpu:4                  # Requesting 4 GPUs
#SBATCH --cpus-per-task=32            # High CPU count for data loading
#SBATCH --mem=350G                    # Memory allocation
#SBATCH --output=logs/eole_%j.log
#SBATCH --error=logs/eole_%j.err

# --- Environment Setup ---
# Ensures the script runs in the directory where it was submitted
cd "$SLURM_SUBMIT_DIR"

# Explicitly isolate assigned GPUs to prevent framework interference
export CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES

source /path/to/your/env/bin/activate

# --- Execution ---
export TORCH_NCCL_TIMEOUT=3600
echo "Starting job ${SLURM_JOB_ID} on $(date) with GPUs: $CUDA_VISIBLE_DEVICES"

eole train -config configBIG.yaml

echo "Job finished on $(date)"
```

**Why use these specific commands?**

While the #SBATCH headers request the hardware, the following lines ensure your code executes predictably within a shared cluster environment:

* `cd "$SLURM_SUBMIT_DIR"`: By default, SLURM might initialize a job in a system path. This command forces the environment to switch to the directory where you executed the sbatch command. This ensures your relative file paths (e.g., configBIG.yaml or local datasets) are correctly resolved.
* `export CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES`: Although SLURM manages resource allocation, some "eager" libraries (like PyTorch or TensorFlow) may attempt to scan all system GPUs. By re-exporting this variable, you create a strict sandbox. Your process will only "see" its assigned GPUs, preventing accidental memory collisions with other active users.
* `%j` in filenames: Including this placeholder in your logs (e.g., job_%j.log) automatically appends the unique Job ID. This prevents new executions from overwriting the results of previous experiments.

To launch it:

`sbatch train_job.sh`

Where train_job.sh is the name of you script.

## 4. Interactive Mode (srun)

If you need to test your code or run a quick script interactively, do not run it on the login node. Instead, request an interactive allocation:

`srun --gres=gpu:1 --mem=32G --cpus-per-task=4 --pty bash`

This will grant you a dedicated terminal session within the allocated resources. Once you type exit, the resources are released for others.

## 5. Important Guidelines

* Do Not Use nohup or &: SLURM handles background execution. Once you sbatch, you can safely disconnect from the server.
* Resource Accuracy: Be conservative with RAM requests. Requesting 300GB of RAM for a 10GB task prevents others from working.
* GPU Visibility: SLURM automatically sets the CUDA_VISIBLE_DEVICES environment variable. Your code will only "see" the GPUs you have been assigned.

## 6. Troubleshooting

If your job status is PD (Pending), run squeue to see why.

* (Resources): Waiting for GPUs/RAM to be freed.
* (Priority): Waiting for higher-priority jobs to finish.

## 7. Why Non-GPU Tasks Must Also Use SLURM

It is a common misconception that SLURM is only for GPU-bound training. In reality, managing CPU and RAM allocation is just as critical for system stability.

### 7.11. Preventing Memory Thrashing (Swap)

If a user executes a high-RAM process (e.g., data preprocessing or large dataset extraction) outside of SLURM, the Operating System may run out of physical memory. This forces the kernel to use Swap (disk space as RAM), which causes an immediate and catastrophic drop in performance for everyone. SLURM prevents this by ensuring that if 350GB of RAM is reserved for training, it remains physically available.

### 7.2. CPU Affinity and Data Bottlenecks

Deep learning is not just about GPUs; it requires significant CPU power for data augmentation and batch loading. If unmanaged CPU-intensive tasks monopolize the cores, your GPUs will sit idle while waiting for data. Using SLURM ensures your training job has dedicated access to the required number of cores.

### 7.3. System Visibility

By using SLURM for all significant tasks, the squeue command becomes a "single source of truth." It allows the team to see exactly what is consuming resources without having to investigate system-level processes.

**Example: Submitting a CPU-only Job**

If you need to preprocess a dataset or run a script that doesn't require a GPU, use the following template:
Bash

```
#!/bin/bash
#SBATCH --job-name=data_prep
#SBATCH --cpus-per-task=16    # Requesting 16 cores
#SBATCH --mem=128G            # Requesting 128GB of RAM
#SBATCH --gres=gpu:0          # IMPORTANT: Request zero GPUs
#SBATCH --output=logs/prep_%j.log
#SBATCH --error=logs/prep_%j.err

cd "$SLURM_SUBMIT_DIR"

# Your CPU-intensive command
python prepare_data.py --input /data/raw --output /data/processed
```

 **Policy Rule:** If your task is expected to run for more than 5 minutes or consume more than 8GB of RAM, it must be submitted via SLURM.

## 8. Working Interactively with SLURM (srun)

Sometimes, you don't want to submit a script and wait; you need to debug code, explore a dataset, or test if your environment is correctly configured. For these cases, we use Interactive Sessions.

Running a heavy process directly on the login shell (without SLURM) is strictly prohibited as it bypasses resource management and can crash the server for everyone. Instead, use srun to "check out" a terminal with dedicated resources.
How to start an interactive session:

To request a terminal with 1 GPU, 8 CPUs, and 32GB of RAM:

`srun --gres=gpu:1 --cpus-per-task=8 --mem=32G --pty bash`

What happens next?

* SLURM looks for an available slot.
* Once granted, your prompt will change (though it looks similar, you are now inside a "container" of resources).

You can now run python, nvidia-smi, or any command as if you were on your local machine.

Important: When you are finished, type `exit` to release the resources so others can use them.

**Common Use Cases for srun**

* Debugging: Run your training script for just a few steps to ensure there are no ImportError or syntax issues before committing to a long sbatch job.
* Data Exploration: Open a Python shell to inspect large tensors or preprocess small samples of data.
* Environment Setup: Install new pip packages or compile C++ extensions that require significant CPU/RAM.

**A Note on Persistence**

Unlike sbatch (which runs in the background even if you close your laptop), an interactive srun session will terminate if your connection drops or you close your terminal. > Recommendation: If you plan to run a long-running process, always use `sbatch`. If you are just "tinkering," use `srun`.

**How do I know I am inside an active session?**

It is easy to lose track of whether you are on the "Login Node" or inside a "Slurm Allocation." You can verify your status with these methods:

* Check the Job ID: Run echo $SLURM_JOB_ID. If it returns a number, you are successfully inside an allocation. If it returns an empty line, you are on the bare metal server (be careful!).
* Resource Limits: In an active session, Slurm will prevent you from using more CPUs or RAM than you requested, acting as a sandbox for your work.

**Remember:** Always type `exit` when you finish your interactive work to release the GPUs for your colleagues!

## 9. Exploring Cluster Resources

Before submitting a job, it is good practice to check the available hardware to tailor your resource requests accurately. You can inspect the server's total capacity and current availability using these commands:

### 9.1. Hardware Overview (sinfo)

To see the general state of the node and how many resources are currently free:

`sinfo -o "%n %c %m %G %a"`

* %n: Node name.
* %c: Total CPU cores.
* %m: Total RAM (in Megabytes).
* %G: Total GPUs.
* %a: Availability status (up/down).

### 9.2. Detailed Resource Breakdown (scontrol)

If you want to see exactly how many CPUs are currently in use versus how many are idle, run:

`scontrol show node <node_name>`

(Replace <node_name> with your server's name, e.g., blackwell-server). Use localhost if you're running the command in the server you want to explore.

Look for the `CfgTRES` (Configured Resources) and `AllocTRES` (Allocated Resources) lines. This will tell you:

* CPUs: Total cores vs. those already running jobs.
* Memory: Total RAM vs. reserved RAM.
* GRES: Total GPUs vs. those currently "checked out" by other users.

### 9.3. Real-time Hardware Specs (Non-SLURM)

If you just want to see the "raw" hardware specifications:

* CPUs/Cores: `lscpu | grep "CPU(s):"`
* Total RAM: `free -h`
* GPU Models: `nvidia-smi -L`

**Efficiency First** 

When checking resources, remember that requesting exactly what you need (and no more) allows more jobs to run concurrently.

* Avoid Over-allocating: If your data processing only needs 16GB of RAM, do not request 128GB.
* Check the Queue: Use squeue to see if a colleague is waiting for resources. If you see the server is at 90% capacity, consider if your task can run with fewer GPUs or less memory.
