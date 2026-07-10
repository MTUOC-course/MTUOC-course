## 1. Introduction

In this tutorial we will follow some examples of the [Axolotl tutorial](https://docs.axolotl.ai/docs/getting-started.html), making some modifications and extensions. Before starting, we will remind some useful docker instructions and examples.

We will assume the following working directory, change this to adapt to your directories.

`/scratch/aoliverg/axolotltutorial`

To learn more about LLMs and finetuning techniques we recommend the reading of the following technical report:

Venkatesh Balavadhani Parthasarathy, Ahtsham Zafar, Aafaq Khan, Arsalan Shahid. (2024) [The Ultimate Guide to Fine-Tuning LLMs from Basics to Breakthroughs: An Exhaustive Review of Technologies, Research, Best Practices, Applied Research Challenges and Opportunities](https://arxiv.org/abs/2408.13296)

## 2. Using axolotl in docker

### 2.1. Starting a docker iterative session with axolotl installed

```
docker run --gpus all --rm -it --ipc=host --shm-size=32gb --ulimit memlock=-1 --ulimit stack=67108864 -v /home/user/axolotltutorial:/data -w /data axolotlai/axolotl:main-latest bash
```

## 3. Following some of the basic examples of the tutorial

### 3.1. Downloading all the examples 

To download all the examples of the tutorial, run inside the docker interactive session:

```
axolotl fetch examples
```

### 3.2. Examples

* [Finetuning llama-3](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/wiki/Finetuning-llama%E2%80%903-with-axolotl) 


### 3.3. Making inference

Now we can do some inference to the fine-tuned model. In the docker interactive session write:

```
CUDA_VISIBLE_DEVICES="0" python -m axolotl.cli.inference lora-1b.yml --interactive --base_model="./outputs/lora-out/merged"
```

Please note that as the whole model fits in one single GPU, we set `CUDA_VISIBLE_DEVICES="0"`, otherwise axolotl will try to accommodate the model in all the available GPUs and this will lead to errors.

Now we get an interactive sessions where we can ask questions to the fine-tuned model:

```
================================================================================
Give me an instruction (Ctrl + D to submit): 
================================================================================
### Instruction:
Can you suggest me some healthy food?

### Response:
================================================================================
The attention mask is not set and cannot be inferred from input because pad token is same as eos token. As a consequence, you may observe unexpected behavior. Please pass your input's `attention_mask` to obtain reliable results.
<|begin_of_text|>### Instruction:
Can you suggest me some healthy food?

### Response: 
Yes, there are many delicious and healthy food options available. Here's a suggested list of some great options to add more fruits, vegetables, whole grains, lean protein, and low-fat dairy products in your daily diet:

1. Fruits - Apples, berries, oranges, grapes, bananas, kiwi, peaches, plums, strawberries

2. Vegetables- Broccoli, carrots, spinach, zucchini, corn, cucumber, tomatoes, lettuce, kale 

3. Whole Grains- Brown rice, quinoa, whole wheat bread, oats, wild rice

4. Lean Protein Sources- Chicken, turkey, fish, beans, lentils, eggs, nuts, seeds, tofu

5. Low-Fat Dairy Products- Greek yogurt, cottage cheese, milk, low-fat cheese, and milk.

Remember, it’s also important to get plenty of physical activity, avoid processed or packaged foods, limit added sugars, and eat a balanced diet that includes diverse and colorful produce.<|end_of_text|>
================================================================================
<|begin_of_text|>### Instruction:
Can you suggest me some healthy food?

### Response: 
Yes, there are many delicious and healthy food options available. Here's a suggested list of some great options to add more fruits, vegetables, whole grains, lean protein, and low-fat dairy products in your daily diet:

1. Fruits - Apples, berries, oranges, grapes, bananas, kiwi, peaches, plums, strawberries

2. Vegetables- Broccoli, carrots, spinach, zucchini, corn, cucumber, tomatoes, lettuce, kale 

3. Whole Grains- Brown rice, quinoa, whole wheat bread, oats, wild rice

4. Lean Protein Sources- Chicken, turkey, fish, beans, lentils, eggs, nuts, seeds, tofu

5. Low-Fat Dairy Products- Greek yogurt, cottage cheese, milk, low-fat cheese, and milk.

Remember, it’s also important to get plenty of physical activity, avoid processed or packaged foods, limit added sugars, and eat a balanced diet that includes diverse and colorful produce.<|end_of_text|>
================================================================================
Give me an instruction (Ctrl + D to submit): 
================================================================================

```

Don't forget to press `Ctrl + D` to send the prompt.

### 3.4. Exiting the docker interactive session:

Now, to exit the docker:

* Write `exit` and Enter.
* `Ctrl + D`


### 3.5. Running the fine-tuning process outside docker:

To do so, write:

```
docker run -d --gpus all --rm \
    --name axolotl_fft_job \
    --ipc=host \
    --shm-size=32gb \
    --ulimit memlock=-1 \
    --ulimit stack=67108864 \
    -v /scratch/aoliverg/axolotltutorial:/data \
    -w /data \
    axolotlai/axolotl:main-latest \
    accelerate launch -m axolotl.cli.train examples/llama-3/lora-1b.yml
```

To look at the progress write:

`docker logs -f axolotl_fft_job`


### 3.6. Run the process with SLRUM

When using a shared computer it is very important to run the processes with SLRUM (or a similar queuing system). Write a script (p.e. runSlrum.sh) with the following content:


```
#!/bin/bash
#SBATCH --job-name=axolotl-fft
#SBATCH --partition=prod
#SBATCH --gres=gpu:1                  # To use 1 GPU (you can stat gpu:all to use all the available GPUs)
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4             # CPU cores assigned to the task
#SBATCH --mem=32G                     # RAM memory reserved for the process
#SBATCH --time=24:00:00               # Max time 24 hours. Don't use this if you're not sure how long it will take.
#SBATCH --output=fft_axolotl_%j.log   # Where to store the log file (%j means the job id) (ex: fft_axolotl_1234.log)
#SBATCH --error=fft_axolotl_%j.err    # Where to store the error messages of the job (%j means the job id) (ex: fft_axolotl_1234.err)

# We run the process
docker run --gpus all --rm \
    --ipc=host \
    --shm-size=32gb \
    --ulimit memlock=-1 \
    --ulimit stack=67108864 \
    -v /scratch/aoliverg/axolotltutorial:/data \
    -w /data \
    axolotlai/axolotl:main-latest \
    accelerate launch -m axolotl.cli.train examples/llama-3/lora-1b.yml
```

### 3.7 Logging the GPU consumption

When performing experiments it is useful to create a log file of the GPU consumption. This will allow us to report on the energy consumption. This is an information that is frequently required in scientific papers.

To get the log we can add the following lines before `docker run...`:

```
# To clean up the processes when the main process terminates.
trap 'kill $(jobs -p) 2>/dev/null' EXIT INT TERM

# Monitoring GPU usage in a csv file
nvidia-smi --query-gpu=timestamp,index,name,power.draw,utilization.gpu,memory.used --format=csv,nounits -l 1 > GPU_consum_${SLURM_JOB_ID}.csv 2>&1 &
```



