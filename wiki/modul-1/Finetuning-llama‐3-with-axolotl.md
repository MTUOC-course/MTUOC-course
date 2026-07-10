### Example 1. Finetuning llama-3 with lora

Once the examples are downloaded, we go to the folder:

```
cd examples/llama-3
```

We will use the configuration file: lora-1b.yml so lets take a look at it:

```
base_model: NousResearch/Llama-3.2-1B
# Automatically upload checkpoint and final model to HF
# hub_model_id: username/custom_model_name

datasets:
  - path: teknium/GPT4-LLM-Cleaned
    type: alpaca

val_set_size: 0.1
output_dir: ./outputs/lora-out

adapter: lora
lora_model_dir:

sequence_len: 2048
sample_packing: true
eval_sample_packing: true


lora_r: 16
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

wandb_project:
wandb_entity:
wandb_watch:
wandb_name:
wandb_log_model:

gradient_accumulation_steps: 2
micro_batch_size: 2
num_epochs: 1

optimizer: adamw_8bit
lr_scheduler: cosine
learning_rate: 0.0002

bf16: auto
tf32: false

gradient_checkpointing: true
resume_from_checkpoint:
logging_steps: 1
attn_implementation: flash_attention_2

loss_watchdog_threshold: 5.0
loss_watchdog_patience: 3

warmup_ratio: 0.1
evals_per_epoch: 4
saves_per_epoch: 1
weight_decay: 0.0
special_tokens:
  pad_token: "<|end_of_text|>"

# save_first_step: true  # uncomment this to validate checkpoint saving works with your config
```

This is the explanation of the whole configuration file:

---

**1. Model and Dataset Selection**

* **`base_model: NousResearch/Llama-3.2-1B`**: Specifies the core, pre-trained model you are starting with. In this case, it's a lightweight, efficient 1-billion-parameter version of Llama 3.2.
* **`datasets`**: Defines the training data.
    * **`path: teknium/GPT4-LLM-Cleaned`**: The Hugging Face dataset path containing high-quality, GPT-4-generated instruction data.
    * **`type: alpaca`**: Instructs Axolotl to parse the dataset using the Alpaca format (`Instruction`, `Input`, `Output`).
* **`val_set_size: 0.1`**: Reserves 10% of the dataset for validation to monitor performance and check for overfitting, while 90% is used for training.
* **`output_dir: ./outputs/lora-out`**: The directory where training checkpoints and the final trained adapter weights will be saved.

**2. Efficiency and Context Window**

* **`sequence_len: 2048`**: The maximum context window (token length) for the model during training.
* **`sample_packing: true` & `eval_sample_packing: true`**: A crucial efficiency feature. Instead of padding shorter sequences with useless pad tokens to reach the 2048 length, it packs multiple short examples into a single 2048-token chunk. This drastically speeds up training.

**3. LoRA (Low-Rank Adaptation) Hyperparameters**

Instead of training all billions of parameters, LoRA freezes the base model and injects small, trainable rank decomposition matrices.

* **`adapter: lora`**: Tells Axolotl to perform Parameter-Efficient Fine-Tuning (PEFT) using LoRA.
* **`lora_r: 16`**: The rank of the update matrices. A higher rank allows the model to learn more complex features but increases memory usage and parameter count.
* **`lora_alpha: 32`**: A scaling factor for the LoRA weights. A common rule of thumb is to set alpha to $2 \times r$.
* **`lora_dropout: 0.05`**: Applies a 5% dropout rate to prevent overfitting.
* **`lora_target_modules`**: Specifies exactly which layers within the Transformer architecture will receive LoRA adapters. Targeting all linear layers (as done here with `q_proj`, `v_proj`, `gate_proj`, etc.) generally yields the best performance.

**4. Training Hyperparameters & Optimizer**

* **`gradient_accumulation_steps: 2`** & **`micro_batch_size: 2`**: Controls the effective batch size. Each GPU processes 2 samples at a time (`micro_batch_size`), and gradients are accumulated over 2 steps before updating weights. This simulates a larger batch size of 4 ($2 \times 2$) to stabilize training without running out of VRAM.
* **`num_epochs: 1`**: The model will train through the entire dataset exactly once.
* **`optimizer: adamw_8bit`**: Uses an 8-bit quantized version of the AdamW optimizer. This significantly reduces GPU memory consumption compared to standard 32-bit AdamW.
* **`learning_rate: 0.0002`**: The peak learning rate ($2 \times 10^{-4}$).
* **`lr_scheduler: cosine`**: Decreases the learning rate over time following a cosine curve, allowing for precise convergence at the end of training.
* **`warmup_ratio: 0.1`**: Spends the first 10% of training gradually ramping up the learning rate from 0 to the peak value to prevent destabilization early on.

**5. Hardware Optimization & Memory Management**

* **`bf16: auto`**: Enables Bfloat16 precision if your hardware (like an NVIDIA Ampere or newer GPU) supports it. This cuts memory use in half compared to FP32 while maintaining numerical stability.
* **`gradient_checkpointing: true`**: Saves massive amounts of VRAM by discarding intermediate activations during the forward pass and recomputing them during the backward pass.
* **`attn_implementation: flash_attention_2`**: Utilizes FlashAttention-2, a highly optimized GPU kernel that speeds up attention computation and lowers memory overhead.

**6. Logging, Evaluation, and Safety**

* **`logging_steps: 1`**: Logs training metrics (like loss) to the console after every single step.
* **`evals_per_epoch: 4`**: Evaluates the model on the validation set 4 times throughout the epoch to check progress.
* **`saves_per_epoch: 1`**: Saves a model checkpoint once per epoch.
* **`loss_watchdog_threshold: 5.0`** & **`loss_watchdog_patience: 3`**: A safety net. If the training loss suddenly spikes or explodes above 5.0 for 3 consecutive steps, Axolotl will automatically abort the training to save you compute time and money.
* **`special_tokens`**: Maps the padding token to the existing `<|end_of_text|>` token, ensuring Llama 3.2 handles sequence boundaries correctly.

---

Regarding the dataset, the path configuration refers to an online repository hosted on the **Hugging Face Hub**. 

Specifically, you can find it at the following URL:
`https://huggingface.co/datasets/teknium/GPT4-LLM-Cleaned`

How does Axolotl find it?

When you run the training script, Axolotl automatically connects to the Hugging Face API, searches for the user/organization `teknium` and the repository name `GPT4-LLM-Cleaned`, downloads the dataset files to your local cache directory (usually `~/.cache/huggingface/datasets`), and then processes it using the `alpaca` formatting structure.

Can I change it to a local file?

es! If you want to use a local dataset instead of fetching it from Hugging Face, you can download a `.json` or `.jsonl` file and change the path to point to your local machine:

```yaml
datasets:
  - path: ./my_local_data/train.json
    type: alpaca
```

This dataset has the form:

```
 {
    "instruction": "Give three tips for staying healthy.",
    "input": "",
    "output": "1. Eat a balanced and nutritious diet: Make sure your meals are inclusive of a variet
y of fruits and vegetables, lean protein, whole grains, and healthy fats. This helps to provide your
 body with the essential nutrients to function at its best and can help prevent chronic diseases.\n\
n2. Engage in regular physical activity: Exercise is crucial for maintaining strong bones, muscles, 
and cardiovascular health. Aim for at least 150 minutes of moderate aerobic exercise or 75 minutes o
f vigorous exercise each week.\n\n3. Get enough sleep: Getting enough quality sleep is crucial for p
hysical and mental well-being. It helps to regulate mood, improve cognitive function, and supports h
ealthy growth and immune function. Aim for 7-9 hours of sleep each night."
  },
```

To start the training write:

```
axolotl train lora-1b.yml
```

After some minutes in a powerful computer with GPU available, you'll get:

```
{'train_runtime': '158.8', 'train_samples_per_second': '26.2', 'train_steps_per_second': '1.638', 'train_loss': '1.567', 'memory/max_active (GiB)': '2.42', 'memory/max_allocated (GiB)': '2.42', 'memory/device_reserved (GiB)': '7.89', 'epoch': '1', 'tokens/train_per_sec_per_gpu': '0'}
100%|█████████████████████████████████████████████████████████████| 260/260 [02:38<00:00,  1.64it/s]
[2026-06-20 15:38:29,823] [INFO] [axolotl.train] Training completed! Saving trained model to ./outputs/lora-out.
[2026-06-20 15:38:30,136] [INFO] [axolotl.train] Model successfully saved to ./outputs/lora-out
```

And you'll have the following files:

```
/data/examples/llama-3/outputs/lora-out# ls
README.md            adapter_model.safetensors  config.json  tokenizer.json
adapter_config.json  checkpoint-260             debug.log    tokenizer_config.json
```

Now, if we want to make a merge of the original model with the Lora weights we can write:

```
axolotl merge-lora lora-1b.yml --lora-model-dir="./outputs/lora-out"
```

And we will have the merged model in: `./outputs/lora-out/merged/`


**TIP**
load_in_8bit: true and adapter: lora enables LoRA adapter finetuning.

* To perform Full finetuning, remove these two lines.
* To perform QLoRA finetuning, replace with load_in_4bit: true and adapter: qlora.

We will now perform a full finetuning, creating a full-1b.yml with the changes. And setting:

```
base_model: NousResearch/Llama-3.2-1B
is_llama_derived_model: true

datasets:
  - path: teknium/GPT4-LLM-Cleaned
    type: alpaca

val_set_size: 0.1
output_dir: ./outputs/full-fft-out

# Leaving adapter empty the full fine-tuning will be activated
adapter:

sequence_len: 2048
sample_packing: true
eval_sample_packing: true

wandb_project:
wandb_entity:
wandb_watch:
wandb_name:
wandb_log_model:

gradient_accumulation_steps: 2
micro_batch_size: 2
num_epochs: 1

optimizer: adamw_torch
lr_scheduler: cosine
learning_rate: 0.00002

bf16: auto
tf32: true

gradient_checkpointing: true
resume_from_checkpoint:
logging_steps: 1
attn_implementation: flash_attention_2

loss_watchdog_threshold: 5.0
loss_watchdog_patience: 3

warmup_ratio: 0.1
evals_per_epoch: 4
saves_per_epoch: 1
weight_decay: 0.0
special_tokens:
  pad_token: "<|end_of_text|>"
```

In a full fine-tuning, we don't need to merge the weights, as all the weights are fine-tuned. The final model will be at:

`output_dir: ./outputs/full-fft-out`

