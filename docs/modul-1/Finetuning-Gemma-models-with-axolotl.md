## 1. Introduction

### 1.1. Gemma models

#### Introduction to Google's Gemma Models

Welcome to this tutorial on **Gemma**, a family of lightweight, state-of-the-art open models built by Google DeepMind. Developed using the same research, technology, and architectural infrastructure as the frontier Gemini models, Gemma represents a major paradigm shift for developers who want to build, fine-tune, and deploy highly capable AI locally or on cost-effective infrastructure. 

Unlike black-box APIs, Gemma provides **open weights**, granting complete data sovereignty and letting you control your entire operational stack.

---

#### Architectural Evolution & Generations

Since its inception, the Gemma ecosystem has rapidly evolved to bridge the gap between edge efficiency and server-tier performance. 

* **Gemma 1 & 2 (2024):** Introduced highly efficient dense architectures (ranging from 2B to 27B parameters) using innovations like Grouped-Query Attention (GQA) and knowledge distillation, establishing class-leading performance for text-only tasks.
* **Gemma 3 (2025):** Expanded capabilities into native multimodality (supporting text and vision inputs) and vastly expanded multilingual support across 140+ distinct languages.
* **Gemma 4 (2026):** The current flagship generation. It introduces native audio capabilities, massive context windows, and a highly competitive Mixture-of-Experts (MoE) variant, allowing models to punch far above their parameter weight.

---

#### Model Sizes & Core Specifications

The modern Gemma ecosystem is segmented into clear tiers depending on your deployment environment—ranging from a standard smartphone to a high-end cloud server.

| Model Variant | Architecture | Context Window | Primary Input Modalities | Targeted Deployment |
| :--- | :--- | :--- | :--- | :--- |
| **Gemma 4 E2B** (~2.3B) | Dense | 128K tokens | Text, Image, Audio | Mobile devices, IoT, ultra-low power laptops |
| **Gemma 4 E4B** (~4.5B) | Dense | 128K tokens | Text, Image, Audio | High-end phones, edge servers, Raspberry Pi |
| **Gemma 4 12B** | Dense | 256K tokens | Text, Image, Audio | Consumer GPUs, developer workstations |
| **Gemma 4 26B A4B** | MoE *(3.8B active)* | 256K tokens | Text, Image | Cost-sensitive high-throughput servers |
| **Gemma 4 31B** | Dense | 256K tokens | Text, Image | Frontier-level reasoning, complex coding, server-tier fine-tuning |

> **What is MoE?** Mixture-of-Experts (MoE) means that while the model holds 25.2B total parameters, it only fires roughly 3.8B parameters per token. This gives you the speed and inference cost of a 4B model but the contextual depth and quality of a much larger one.

---

#### Licensing: Open and Flexible

One of the most critical updates in the Gemma timeline involves its legal framework:

* **Gemma 4 ships under the Apache 2.0 License.** This is a completely free, permissive, open-source license. It allows for commercial use, modification, and distribution without the restrictive user-threshold clauses or specialized compliance tracking found in competitor licenses.
* *Note on Older Generations:* Gemma 1, 2, and 3 were released under a custom "Gemma Terms of Use" (a source-available license). While highly permissive for commercial applications, it contained specific use restrictions that made corporate legal reviews more rigid compared to the absolute freedom of Apache 2.0.

---

#### Key Takeaways for the Tutorial

As we move forward into the technical implementation, keep these three key advantages of Gemma in mind:

1. **Native Multimodality:** You are not just processing text. With the edge variants, you can feed images and raw audio natively into the model without needing external encoders.
2. **Asymmetric Context Windows:** The jump to 128K and 256K context windows means you can feed entire code repositories, technical manuals, or hours of audio context directly into a model running on local hardware.
3. **Agentic Capabilities:** Gemma has been heavily post-trained for native function calling, advanced logical reasoning, and structured data outputs, making it the perfect core engine for autonomous AI agents.

---

If you want to learn more about the Gemma family, you can read:

Gemma team. (2024) [Gemma: Open Models Based on Gemini Research and Technology](https://arxiv.org/abs/2403.08295v4)


## 2. Getting Gemma4

We will use the Gemma4 family in this tutorial because is the newer version in the time of writing and because its license, that allows free downloading without the need of HF tokens.

Although axolotl allows for the automatic downloading of models and datasets, in this tutorial we will download both the models and datasets locally.

To get Gemma4 12B we can write:

`git clone https://huggingface.co/google/gemma-4-12B`

To get Gemma4 12B it (the instructed finetunded) we can write:

`git clone https://huggingface.co/google/gemma-4-12B-it`


