## 1. Introduction

In this tutorial we will explore several simple scripts to perform translations using models in [Hugging Face](https://huggingface.co) using the Transformer library. These scripts are very simple and basic, but they can serve as a basis for more complex programs.

## 2. SalamandraTA

This is a model specially finetuned for translation-related taks that is distributed in two sizes. The description of the models can be found at:

* [salamandraTA-2b-instruct](https://huggingface.co/BSC-LT/salamandraTA-2b-instruct)
* [salamandraTA-7b-instruct](https://huggingface.co/BSC-LT/salamandraTA-7b-instruct)

Basic program:

requirements ([requirements.txt](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/blob/main/HuggingFace/requirements.txt)):

```
torch
transformers
accelerate
```

program ([translateSalamandraTA.py](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/blob/main/HuggingFace/translateSalamandraTA.py)):

```
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def translate_salamandra_manual(text, model_id, source_lang, target_lang):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        dtype=torch.bfloat16
    )


    system_prompt = "You are a professional translator."
    user_prompt = f"Translate the following text from {source_lang} into {target_lang}.\n{source_lang}: {text} \n{target_lang}:"

    full_prompt = (
        f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        f"<|im_start|>user\n{user_prompt}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

    inputs = tokenizer(full_prompt, return_tensors="pt", add_special_tokens=False).to(model.device)
    input_length = inputs.input_ids.shape[1]

    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_new_tokens=400,
        num_beams=5,
        early_stopping=True,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.convert_tokens_to_ids("<|im_end|>") # Forcem que sàpiga quan parar
    )

    result = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
    
    return result.replace("<|im_end|>", "").strip()

if __name__ == "__main__":
    model_id = "BSC-LT/salamandraTA-2b-instruct"
    
    src = "English"
    tgt = "Catalan"
    frase = "Artificial intelligence (AI) is the capability of computational systems to perform tasks typically associated with human intelligence, such as learning, reasoning, problem-solving, perception, and decision-making.."

    traduccio = translate_salamandra_manual(frase, model_id, src, tgt)
    print(f"\nTranslation: {traduccio}")

``` 

## 3. Tower-Plus

Tower-Plus is also a LLM specialized for translation. It is distributed in three sizes:

* [Tower-Plus-2B](https://huggingface.co/Unbabel/Tower-Plus-2B)
* [Tower-Plus-9B](https://huggingface.co/Unbabel/Tower-Plus-9B)
* [Tower-Plus-72B](https://huggingface.co/Unbabel/Tower-Plus-72B)

Basic program:

requirements ([requirements.txt](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/blob/main/HuggingFace/requirements.txt)):

```
torch
transformers
accelerate
```

program ([translateTowerPlus.py](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/blob/main/HuggingFace/translateTowerPlus.py))

```
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def translate_tower(text, model_id, source_lang, target_lang):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        dtype=torch.bfloat16
    )
    messages = [
        {
            "role": "user", 
            "content": f"Translate the following {source_lang} source text to {target_lang}:\n{source_lang}: {text}\n{target_lang}: "
        }
    ]
    prompt = tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(model.device)
    input_length = inputs.input_ids.shape[1]
    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_new_tokens=256,
        do_sample=False,  # Com diu l'exemple d'Unbabel
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id
    )
    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    generated_tokens = outputs[0][input_length:]
    translation = tokenizer.decode(generated_tokens, skip_special_tokens=True)
    return translation.strip()

if __name__ == "__main__":
    model_id = "Unbabel/Tower-Plus-2B"
    src = "English"
    tgt = "Portuguese (Portugal)" 
    sentence = "The bridge between two languages is built with artificial intelligence."

    print(f"Loading {model_id}...")
    resultat = translate_tower(sentence, model_id, src, tgt)

    print("-" * 30)
    print(f"Source: {sentence}")
    print(f"Target: {resultat}")
    print("-" * 30)

```

## 4. TranslateGemma

TranslateGemma models are a family of specialized open-weight multimodal models, built upon Google's Gemma 2 architecture and fine-tuned specifically for high-fidelity translation tasks. Their core innovation lies in their ability to bridge visual and linguistic modalities, enabling the seamless extraction and translation of text directly from images—such as signs or documents—within a single inference step. By utilizing a structured instruction format with ISO language codes, they achieve professional-grade accuracy across dozens of languages while remaining efficient enough for local deployment.

TranslateGemma models are distributed in three different sizes: 4B, 12B and 27B](https://huggingface.co/collections/google/translategemma)


Basic program:

requirements ([requirements.txt](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/blob/main/HuggingFace/requirements.txt)):

program [translateTranslateGemma.py](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/blob/main/HuggingFace/translateTranslateGemma.py):

```
import torch
from transformers import pipeline, GenerationConfig

def run_translategemma_demo():
    model_id = "google/translategemma-4b-it"
    
    print(f"Loading {model_id}...")
    
    pipe = pipeline(
        "image-text-to-text",
        model=model_id,
        device_map="auto",
        dtype=torch.bfloat16
    )


    gen_config = GenerationConfig.from_pretrained(model_id)
    gen_config.max_length = None 
    gen_config.pad_token_id = pipe.tokenizer.eos_token_id

    # --- EXAMPLE 1: TEXT TRANSLATION---
    text_to_translate = "The translation of this sentence was done by a multimodal model."
    msg_text = [{
        "role": "user",
        "content": [{
            "type": "text",
            "source_lang_code": "en",
            "target_lang_code": "ca",
            "text": text_to_translate,
        }]
    }]

    print("\n--- Translating Text ---")
    gen_config.max_new_tokens = 200
    
    out_text = pipe(text=msg_text, generate_kwargs={"generation_config": gen_config})
    print(f"Translation: {out_text[0]['generated_text'][-1]['content']}")

    # --- EXAMPLE 2: IMAGE TRANSLATION ---
    image_url = "https://c7.alamy.com/comp/2YAX36N/traffic-signs-in-czech-republic-pedestrian-zone-2YAX36N.jpg"
    msg_image = [{
        "role": "user",
        "content": [{
            "type": "image",
            "source_lang_code": "cs",
            "target_lang_code": "ca",
            "url": image_url,
        }]
    }]

    print("\n--- Translating Image ---")
    out_image = pipe(text=msg_image, generate_kwargs={"generation_config": gen_config})
    print(f"Result: {out_image[0]['generated_text'][-1]['content']}")

if __name__ == "__main__":
    run_translategemma_demo()
```

## 4. Llama 3.1

Meta’s Llama 3.1 is a collection of large language models (LLMs) built on a standard decoder-only transformer architecture, optimized for high-density data processing. The series is categorized by parameter count into three tiers: 8B, 70B, and 405B, each designed for specific hardware constraints and performance requirements. A key technical advancement in this release is the expansion of the context window to 128,000 tokens, which allows the model to retain and process significantly more information in a single prompt compared to previous iterations.

In terms of deployment, the models utilize Grouped-Query Attention (GQA) across all sizes to maintain inference speed even as the context grows. The 405B variant serves as the primary engine for complex reasoning and data generation, while the 8B and 70B models are often used for downstream tasks and local integration due to their lower VRAM requirements. By releasing the model weights under a permissive license, the architecture facilitates independent benchmarking and fine-tuning, allowing developers to implement the system on private infrastructure without relying on external APIs.

Llama 3.1 is a general-purpose Large Language Model (LLM) rather than a dedicated translation system. Unlike task-specific architectures, it is designed for a broad range of computational linguistics, including structured data extraction, logical inference, and code synthesis. Its underlying transformer architecture is optimized for diverse sequence-to-sequence tasks, enabling it to function as a versatile foundation for various natural language processing (NLP) applications.

The model's multilingual capabilities are a result of extensive training on massive datasets incorporating over 30 languages. While it is not an encoder-decoder translation engine by design, its high-dimensional token embeddings and cross-lingual semantic mapping allow it to perform complex translation tasks effectively. Because it processes context at a systemic level, it can translate between language pairs while maintaining technical terminology and grammatical consistency, often outperforming smaller, specialized translation models in zero-shot scenarios.

requirements [requirements.txt](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/blob/main/HuggingFace/requirements.txt):

program [testLlama.py](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/blob/main/HuggingFace/testLlama.py)

```
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TextStreamer

def run_llama_inference():
    model_id = "meta-llama/Llama-3.1-8B-Instruct"
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        quantization_config=quantization_config
    )

    prompt_text = "Explain the importance of open-source AI models in three bullet points."

    messages = [
        {"role": "system", "content": "You are a technical assistant."},
        {"role": "user", "content": prompt_text}
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True
    ).to(model.device)

    # Initialize the streamer
    streamer = TextStreamer(tokenizer, skip_prompt=True)

    print(f"Generating response for model: {model_id}\n")
    print("-" * 30)

    # The generate method will now print tokens as they are created
    model.generate(
        **inputs,
        max_new_tokens=256,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        streamer=streamer
    )
    
    print("-" * 30)

if __name__ == "__main__":
    run_llama_inference()

```

Try changing the prompt and use some prompts for translation.

