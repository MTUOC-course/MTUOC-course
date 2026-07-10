## 1. Introduction

In this tutorial the process of finetuning an LLM with axolotl using LoRA is explained. If you want to perform a full finetuning, there is a separate tutorial available.

In this tutorial we will divide the whole finetuning process in three steps: preprocessing, finetuning and merging.

Before starting the tutorial, you should have a clear idea of what LoRA is:

### What is LoRA? (Low-Rank Adaptation)

LoRA is an efficient fine-tuning technique designed to adapt large pre-trained models to specific tasks or datasets without the massive computational cost of updating all the model's parameters.
How it works:

Instead of modifying the entire weight matrix of a model (which can have billions of parameters), LoRA freezes the original weights and injects two much smaller, trainable matrices (called A and B) into each layer.

* The Analogy: Imagine you have a massive, heavy encyclopedia (the base model). Instead of rewriting every single page to add new information, you attach small "Post-it" notes (LoRA adapters) to the relevant pages. When you read the book, you combine the original text with what's on the notes.

* The "Rank" (r): In your config, you set lora_r: 64. This "rank" determines the size of these small matrices. A higher rank allows the model to learn more complex patterns but increases the file size and memory usage.

**Why use it?**

* Efficiency: You only train a tiny fraction (often <1%) of the total parameters.
* Hardware Friendly: It allows you to fine-tune large models on consumer or mid-range GPUs much faster.
* Portability: The resulting "adapters" are very small (megabytes instead of gigabytes), making them easy to share or swap.
* No "Catastrophic Forgetting": Since the original weights are frozen, the model is less likely to lose the general knowledge it already had.

After preprocessing and finetuning, by doing a Merge, you are taking those "Post-it notes" and permanently printing their information back into the pages of the encyclopedia to create a new, singular book.

**Directory Infrastructure**

To prevent naming conflicts between the host machine and the Docker container's root mount point, we can organize the host directory as follows:

Host path: /unitname/username/dirname

```
/unitname/username/dirname
├── model_base/          # Source weights (Salamandra-2B)
├── dataset_files/       # Your JSONL files (train/val)
├── temp_prepared/       # Tokenized output
├── lora_output/         # Trained adapters and checkpoints
└── config.yaml          # The configuration file
```

## 2. Step-by-Step Workflow

### 2.1. Preprocessing

This step tokenizes your raw text and prepares it for the GPU.

```
docker run --gpus all --rm --ipc=host -v /unitname/username/dirname/:/data -w /data axolotlai/axolotl:main-latest python3 -m axolotl.cli.preprocess config.yaml
```

### 2.2. Fine-tuning (LoRA)

This initiates the actual training. We use accelerate launch to manage the 4-GPU distribution.

```
docker run --gpus all --rm --ipc=host --shm-size=32gb --ulimit memlock=-1 --ulimit stack=67108864 -v /unitname/username/dirname:/data   -w /data axolotlai/axolotl:main-latest accelerate launch -m axolotl.cli.train config.yaml
```

### 2.3. Merging the Adapters

This step mathematically merges the trained LoRA layers and the updated embeddings into the base model to create a standalone model.

```
docker run --gpus all --rm --ipc=host -v /unitname/username/dirname:/data -w /data axolotlai/axolotl:main-latest python3 -m axolotl.cli.merge_lora config.yaml --lora_model_dir=/data/lora_output
```

The final model will be stored in: /unitname/username/dirname/lora_output/merged

### 2.4 Final Configuration (config.yaml)

All the previous processes have been performed using a configuration file. The exemple below is a valid configuration file for finetuning a SalamandraTA-instruct model already downloaded at /data/model_base/. For other LLMs some aspects should be adapted.

Note how all paths now explicitly reference /data/ as the root, avoiding any ambiguity with the internal dataset_files folder.
YAML

```
# Model and Tokenizer
base_model: /data/model_base/
model_type: AutoModelForCausalLM
tokenizer_type: AutoTokenizer
is_llama_derived_model: true

# New tokens for ChatML and EOS
tokens:
  - "<|im_start|>"
  - "<|im_end|>"
special_tokens:
  eos_token: "<|im_end|>"
  pad_token: "<|im_end|>"

# Datasets
datasets:
  - path: /data/dataset_files/train.jsonl
    ds_type: json
    type: chat_template
    chat_template: chatml
    field_messages: conversations
    message_property_mappings:
      role: from
      content: value

test_datasets:
  - path: /data/dataset_files/val.jsonl
    ds_type: json
    type: chat_template
    chat_template: chatml
    field_messages: conversations
    message_property_mappings:
      role: from
      content: value

val_set_size: 0
dataset_prepared_path: /data/temp_prepared
output_dir: /data/lora_output

# Sequence Parameters
sequence_length: 4096
sample_packing: true
pad_to_sequence_len: true

# LoRA Configuration
adapter: lora
lora_r: 64
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules:
  - gate_proj
  - down_proj
  - up_proj
  - q_proj
  - v_proj
  - k_proj
  - o_proj

# CRITICAL: Save layers for new tokens
lora_modules_to_save:
  - embed_tokens
  - lm_head

# Hyperparameters (Optimized for 4 GPUs @ 96GB)
gradient_accumulation_steps: 4
micro_batch_size: 8
num_epochs: 3
optimizer: adamw_torch
learning_rate: 0.0002
lr_scheduler: cosine

# Evaluation and Saving Strategy
evaluation_strategy: steps
eval_steps: 100
save_steps: 100
logging_steps: 10
save_total_limit: 2

# Hardware Acceleration
bf16: true
tf32: true
flash_attention: true

# Parallelism
fsdp: []
fsdp_config: {}
```

**Final Considerations**

* Verification: After the merge, ensure the /data/lora_output/merged directory contains model.safetensors and the updated tokenizer_config.json.
* Clean-up: Once the merge is verified, you can safely delete temp_prepared and the intermediate checkpoint-XXXX folders to reclaim space on /scratch.