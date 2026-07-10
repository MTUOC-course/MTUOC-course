## 1. Introduction

[Opus-MT](https://github.com/Helsinki-NLP/Opus-MT) is a project closely associated with the [OPUS corpora](https://opus.nlpl.eu/), dedicated to the distribution of a vast collection of open-source Neural Machine Translation (NMT) models. These models are fully compatible and can be deployed directly via the MTUOC-server.

### Further Reading

For a comprehensive understanding of the project's architecture and its mission to broaden access to translation technology, please refer to the following publication:

Reference: Tiedemann, J., Aulamo, M., Bakshandaeva, D., Boggia, M., Grönroos, S. A., Nieminen, T., ... & Virpioja, S. (2024). Democratizing neural machine translation with OPUS-MT. Language Resources and Evaluation, 58(2), 713-755.

Full Article Access: [Available via Springer](https://link.springer.com/article/10.1007/s10579-023-09704-w)

### Available Models

To explore the extensive list of language pairs and pre-trained engines available within the Opus-MT framework, you can visit the official repository:

Official Model Registry: [Opus-MT Trained Models on GitHub](https://github.com/Helsinki-NLP/Opus-MT-train/tree/master/models)

### Testing OpusMT in a Pyhton script

We can use a simple python script ([translateOpusMT.py](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/blob/main/OpusMT/translateOpusMT.py) to test OpusMT models. Before using the script, don't forget to install the [requirements.txt](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/blob/main/OpusMT/requirements.txt):

```
transformers
torch
sentencepiece
sacremoses
```

The script is the following. Feel free to change the model to test and the sentence to translate.

```
from transformers import MarianMTModel, MarianTokenizer

def translate_text(text, model_name):
    """
    Translates a given string using a specific Opus-MT model.
    """
    # 1. Load the tokenizer and the model from Hugging Face
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # 2. Tokenize the input text
    # The 'pt' return_tensors means we are using PyTorch
    inputs = tokenizer(text, return_tensors="pt", padding=True)

    # 3. Generate the translated tokens
    translated_tokens = model.generate(**inputs)

    # 4. Decode the tokens back into a human-readable string
    result = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return result

if __name__ == "__main__":
    # Configuration
    model_id = "Helsinki-NLP/opus-mt-en-es"
    input_sentence = "This is a translation test using OpusMT"

    print("Loading model and performing translation...")
    
    # Execution
    translation = translate_text(input_sentence, model_id)

    # Output
    print("-" * 30)
    print(f"Original text:    {input_sentence}")
    print(f"Translated text:  {translation}")
    print("-" * 30)
```

As we don't want to translate isolate sentences one by one, the use of MTUOC-server to start a OpusMT model is very handy and the server adds several additional features.

## 2. Starting OpusMT in MTUOC-server

To start the MTUOC-server using a model from OpusMT we need to configure 2 files:

**config-server.yaml**

We simply need to set the `MTEngine` field to **OpusMT** and the model's config file in the `model_config`

```
MTengine: OpusMT
model_config: ./opus-mt-en-es/config-OpusMT.yaml
...
```

**config-OpusMT.yaml**

```
OpusMT:
  #model_path: Helsinki-NLP/opus-mt-en-es
  model_path: "./opus-mt-en-es"
  beam_size: 5
  num_hypotheses: 5
  multilingual_prefix: ""
  device: cuda
  #cuda cpu
```

In `model_path` we need to state the model we want to use. You can see the full list of models [here](https://huggingface.co/models?sort=downloads&search=Helsinki). Most of the models are bilingual, that is, they can translate from one source language to one target language. For bilingual models we state `multilingual_prefix: ""`, that is, no multilingual prefix. In OpusMT, however, some models are multilingual, meaning that they can translate from and to several languages. In this case we use the `multilingual_prefix`  in the form of **>>id<<** (where id is a valid target language ID of the model.) For example, **>>ca<<** to translate to Catalan.

The parameters `beam_search` and `num_hypotheses` are related to the number of translation candidates the model will provide for each source sentence.

You may need to install the requirements. If you plan to use only OpusMT you don't need to install the whole set of requirements for MTUOC-server, but the specific ones that are in the requirements-OpusMT.txt file. The requirements are:

```
regex
pyyaml
ftfy
huggingface_hub
requests
lxml
transformers
torch
sentencepiece
sacremoses
flask
waitress
websocket-client
```
