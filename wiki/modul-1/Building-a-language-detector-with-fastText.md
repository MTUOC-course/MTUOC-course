A step-by-step tutorial for building a language detector with **fastText**

# 1. Introduction

**Language identification** is the task of automatically recognizing the language of a given text, document, or audio sample.  For textual data, this task can be performed using a language identification model based on **fastText**, an open-source library designed for efficient learning of word representations and sentence classification.

The resulting tool is fast and efficient, making it suitable for large-scale language detection tasks. It requires less than 1 MB of memory in its compressed form and is capable of processing thousands of documents per second, making it practical for real-time applications.

For language identification, two pretrained models are available: ```lid.176.bin``` and its compressed version ```lid.176.ftz```. These models are trained on large multilingual datasets and support a wide range of languages.

We can download these models from the model release page: https://fasttext.cc/docs/en/language-identification.html

Below we can see the list of ISO language codes corresponding to the supported languages.

### ISO Codes of Languages Supported

```
af als am an ar arz as ast av az azb ba bar bcl be bg bh bn bo bpy br bs bxr ca cbk ce ceb ckb co cs cv cy da de diq dsb dty dv el eml en eo es et eu fa fi fr frr fy ga gd gl gn gom gu gv he hi hif hr hsb ht hu hy ia id ie ilo io is it ja jbo jv ka kk km kn ko krc ku kv kw ky la lb lez li lmo lo lrc lt lv mai mg mhr min mk ml mn mr mrj ms mt mwl my myv mzn nah nap nds ne new nl nn no oc or os pa pam pfl pl pms pnb ps pt qu rm ro ru rue sa sah sc scn sco sd sh si sk sl so sq sr su sv sw ta te tg th tk tl tr tt tyv ug uk ur uz vec vep vi vls vo wa war wuu xal xmf yi yo yue zh

```

## 1.1. Building your own Language Detector 

While the two pretrained models already available support 176 languages, they may not be sufficient for every use case. In particular, when working with low-resource or less commonly represented languages with limited annotated data, it may be necessary to train a custom language detector.

In these situations, fastText allows you to build a fast and lightweight model using only a few command-line instructions, as we will demonstrate in the following sections of this tutorial.


# 2. Practical Part

In this practical section, we will explain step by step how to build your own language detector using fastText. 

We will base the tutorial on a real case study: a language detection model designed to recognize both some major languages and several minor romance languages spoken in Italy that are not well covered by the available pretrained models (such as Ligurian, Friulian, and Ladin).

In our setup, we trained a model capable of distinguishing 12 languages:

```
pms, lmo, rm, lij, fur, lld, la, it, en, fr, es, de

```
The inclusion of major languages (such as English, French, Spanish, German, and Italian) is important because they frequently appear in real-world data and often co-occur with minority languages. Adding them helps reduce misclassification and makes the model more robust in realistic multilingual settings.


## 2.1. Building *fastText* as a Command Line Tool

To get started with fastText, the first step is to install and build the library from source. This can be done by cloning the official repository and compiling it using ```make```:

```
git clone https://github.com/facebookresearch/fastText.git
cd fastText
make

```
Once the compilation is completed, fastText is available as a command line tool. 

Running the binary without any arguments will display the built-in documentation and list all supported commands:

```
./fasttext

```

This will print an overview of the available functionalities:

```

usage: fasttext <command> <args>

The commands supported by fasttext are:

  supervised              train a supervised classifier
  quantize                quantize a model to reduce the memory usage
  test                    evaluate a supervised classifier
  test-label              print labels with precision and recall scores
  predict                 predict most likely labels
  predict-prob            predict most likely labels with probabilities
  skipgram                train a skipgram model
  cbow                    train a cbow model
  print-word-vectors      print word vectors given a trained model
  print-sentence-vectors  print sentence vectors given a trained model
  print-ngrams            print ngrams given a trained model and word
  nn                      query for nearest neighbors
  analogies               query for analogies
  dump                    dump arguments,dictionary,input/output vectors

```
In this tutorial, we focus mainly on three core functionalities: ```supervised```, ```test```, and ```predict```. 

These correspond respectively to training a language detector, evaluating its performance, and using it to make predictions on new unseen data.

## 2.2. Our Data

We need a dataset to train our model. The first step is to decide which languages we want to include in the language detector. This choice should be made carefully, considering the languages that are likely to appear in the texts we intend to process or clean.  

Once the target languages have been defined, the next step is to collect a set of sentences for each language. It is important to try to keep the dataset relatively balanced, meaning that each language should be represented by a similar number of examples. This helps prevent the model from becoming biased toward languages with more training data and improves overall detection performance, especially for less frequent or smaller languages.

In our case, we aimed for around 100,000 segments per language. However, since we were working with smaller languages, collecting data was not always easy, and for one of the 12 languages we only had about 50,000 segments. Despite these differences, maintaining a reasonably balanced dataset remains the most important factor.

In our case, we used our own datasets, but an alternative is to use publicly available resources. One useful option is **Tatoeba**, which provides sentence-level data in many languages and can be downloaded from: https://tatoeba.org/ca/downloads

If you decide to use this dataset, the training data can be downloaded and extracted as follows:

```
wget http://downloads.tatoeba.org/exports/sentences.tar.bz2
bunzip2 sentences.tar.bz2
tar xvf sentences.tar

```




### 2.2.1. Put our Data into *fastText* Format

To prepare our training data for fastText, we first need to convert the raw corpora into the required format, where each line starts with a label followed by the corresponding sentence. This format is essential because fastText uses labeled data for supervised learning: in the case of language detection, each label corresponds to an ISO language code and must begin with the ```__label__``` prefix. This allows the model to distinguish language labels from the words in the text. The classifier is then trained to predict the correct language label based on the words contained in each document.

If the data comes from a structured source such as Tatoeba, this can be done directly from a CSV file using:

```
awk -F"\t" '{print"__label__"$2" "$3}' < sentences.csv | shuf > all.txt

```

This extracts the language label and the sentence, formats them according to fastText requirements, and shuffles the dataset to avoid ordering bias.

When working with separate corpora for each language, we first standardize each file by adding the corresponding ISO language code as a label. In our case, for example with Piedmontese, we proceed as follows:

```
sed 's/^/__label__pms /' piemontese.txt > corpus_pms.txt

```
This ensures that every line in the corpus is correctly labeled.

Once all language-specific corpora are prepared, they can be combined into a single dataset:
 

```
cat corpus-pms.txt corpus_lmo.txt > corpus_total.txt

```
For larger collections of files, we can concatenate everything in a folder using a wildcard. This approach is particularly useful when working with multiple corpora, as it avoids listing each file individually and allows us to process them all at once.

In our case, we stored all the corpora for the 12 languages in a single directory called ```my_corpora```. We then used ```cat``` to merge all ```.txt``` files in that folder, where the wildcard ```*.txt``` automatically selects all files without explicitly naming them.

The output is then piped into ```shuf```, which randomly shuffles the lines to ensure that the dataset is well mixed and not ordered by language or source. Finally, the resulting data is saved into a single combined file.

```
cat my_corpora/*.txt | shuf > corpus_total.txt

```

### 2.2.2. Shuffle the Data

After combining all language-specific corpora into a single dataset, it is important to ensure that the final file is well mixed. Without this step, the data may still preserve a partial ordering based on the original files or languages, which could introduce bias during training and affect the quality of the model.

For instance, after merging files such as:

```
cat corpus-pms.txt corpus_lmo.txt > corpus_total.txt

```

the resulting dataset can still contain grouped segments from the same language. To avoid this, we randomly shuffle all lines in the final corpus:

```
shuf corpus_total.txt > corpus_shuffled.txt

```
This operation ensures that examples from all languages are evenly distributed throughout the dataset, improving randomness and making the subsequent training and validation split more reliable.

### 2.2.3. Training and Validation

Before training our first language detector, we need to split the data into train and validation. We will use the validation set to evaluate how good the learned classifier is on new data.
A common and effective strategy is to reserve about 90% of the data for the training set and 10% for validation, although other splits can also be used depending on the specific task and dataset size.

In our example, starting from the full corpus, we applied a 90/10 split. In our case, starting from a total of 1,137,455 examples, this corresponds to approximately 113,745 samples for validation and 1,023,710 samples for training. This allowed us to train the model on the majority of the data while still keeping a representative portion for validation.

We applied this split as follows:

```
head -n 113745 corpus_total.txt > validation.txt
```
```
tail -n +113746 corpus_total.txt > training.txt

````
## 2.3 Train and Evaluate the Model

Now that the dataset has been prepared and properly formatted, we can proceed with the training phase. In this step, we use fastText to build the language detection model starting from the labeled data, so that it can later be evaluated on unseen examples.

```
$ ./fasttext supervised -input training.txt -output langdetect -dim 16

Read 21M words
Number of words:  1927126
Number of labels: 12
Progress: 100.0% words/sec/thread: 1779455 lr:  0.000000 avg.loss:  0.195806 ETA:   0h 0m 0s
```

The ```-input``` option specifies the training file containing the labeled examples, while the ```-output``` option defines the name of the model to be saved. At the end of training, fastText generates a ```.bin``` file (in this case ```langdetect.bin```) containing the trained language detector.

During training, fastText also prints a log of the learning process, including information such as the number of words and labels, the current loss value, the learning rate, and the training speed. This output is useful to monitor how the model is converging and to check that the training process is proceeding correctly.

Once the model has been trained, the next step is to evaluate its performance on unseen data. This allows us to understand how well the language detector generalizes beyond the training set.

To evaluate the model, we use the validation set:

```
$ ./fasttext test langdetect.bin validation.txt

N       113745
P@1     0.911
R@1     0.911


```
The evaluation reports two main metrics: precision at 1 ```(P@1)``` and recall at 1 ```(R@1)```.

Precision measures how many of the predicted labels are correct, while recall measures how many of the true labels are correctly identified by the model. Both values are computed at the top prediction (k=1), meaning the model’s most likely label is considered.

## 2.4. Improvements by Changing some Default Parameters

We can improve the baseline fastText model by adjusting several training parameters. In our case, we used the following configuration:

```
./fasttext supervised -input training.txt -output langdetect_v2 -lr 0.8 -epoch 50 -wordNgrams 3 -minn 3 -maxn 6 -dim 100

```
As you can see from the command line above, we can improve the model’s performance by increasing the number of ```epochs```, which determines how many times the model sees the training data during training, allowing it to learn more stable and accurate patterns. In our case, we set it to ```50``` (```-epoch 50```).

Another way to improve the model is by adjusting the ```learning rate```, which controls how much the model changes after processing each training example. In our case, we set the learning rate to ```0.8``` (```-lr 0.8```), allowing the model to learn faster by updating its weights more aggressively after each iteration.

In addition, you can enable word ```n-grams```. We used word n-grams up to length 3 (```-wordNgrams 3```) to help the classifier capture short word sequences and contextual patterns, rather than relying only on single words.

Another way to improve the baseline model is to use ```subword features```, which enhance the classifier by taking into account the internal structure of words. We activated these features with ```-minn 3``` and ```-maxn 6```, so that words were represented through character n-grams of length 3 to 6. For example, using character n-grams of length 3, the word skiing would be represented as:

```
{ skiing, ski, kii, iin, ing }

```

A key advantage of subword features is that out-of-vocabulary or misspelled words can still be represented through their character n-grams, making the classifier more robust, especially with small training datasets or morphologically rich languages.

Finally, you can also set the ```embedding dimension```. In our case, we set it to ```100``` (```-dim 100```) in order to obtain richer vector representations while maintaining computational efficiency.

## 2.5. How is the Model Performing?

After training, we can analyse the model’s performance from different perspectives, moving from a global evaluation to a more detailed, label-level inspection. fastText provides several evaluation tools that help us understand not only how accurate the model is overall, but also how it behaves for each individual language and how confident its predictions are on single examples.

The following command uses the trained fastText model to predict the top 3 most probable languages for each input sentence, along with their associated probabilities. It is particularly useful for inspecting individual predictions and understanding how confident the model is for each language.

We can provide input either from a ```.txt file``` or by typing sentences directly in the terminal to test them interactively, as you can see from the following code:

```
$ ./fasttext predict-prob langdetect.bin - 3

Une dì ti contarai di cuant che o jeri a vore a Meran.
__label__fur 0.993979 __label__lij 0.00553351 __label__lmo 0.000478289
O soi lade sù fin su la piche de mont.
__label__fur 0.499733 __label__lmo 0.427202 __label__lij 0.0658742
 O Martin Pénet, inte un çenscimento incompleto, o minsoña ciù che 90 interpretaçioin despæge incise in sce di çilindri
__label__lij 0.999917 __label__fur 0.000103221 __label__lld 1.01267e-05
L'omosessualitæ a se attreuva in ben ben de speçie animâ
__label__lij 0.95412 __label__lmo 0.0314805 __label__fur 0.0132229
Ch'el sia pur anca el rè di badee
__label__lmo 1.00001 __label__rm 1.01738e-05 __label__fur 1.00501e-05

```

The next command evaluates the trained fastText language detection model at label level on the validation set, producing per-class metrics such as F1-score, precision, and recall:

```
$ ./fasttext test-label langdetect.bin validation.txt> report_languages.txt

$ more report_languages.txt

F1-Score : 0.987379  Precision : 0.992258  Recall : 0.982548   __label__en
F1-Score : 0.986892  Precision : 0.992872  Recall : 0.980984   __label__de
F1-Score : 0.801937  Precision : 0.795819  Recall : 0.808149   __label__la
F1-Score : 0.975089  Precision : 0.976219  Recall : 0.973962   __label__it
F1-Score : 0.965646  Precision : 0.995738  Recall : 0.937318   __label__pms
F1-Score : 0.993674  Precision : 0.997279  Recall : 0.990095   __label__lld
F1-Score : 0.985455  Precision : 0.988032  Recall : 0.982891   __label__fr
F1-Score : 0.987386  Precision : 0.993053  Recall : 0.981784   __label__es
F1-Score : 0.797039  Precision : 0.794285  Recall : 0.799813   __label__lij
F1-Score : 0.736924  Precision : 0.664821  Recall : 0.826569   __label__lmo
F1-Score : 0.896763  Precision : 0.939293  Recall : 0.857916   __label__rm
F1-Score : 0.752008  Precision : 0.810430  Recall : 0.701443   __label__fur
N       113745
P@1     0.911
R@1     0.911

```
The output file reports the performance of the model for each language label individually. For each class, it shows Precision, Recall, and F1-score, which allow a more fine-grained evaluation compared to global accuracy. 

For example, languages like English (```__label__en```), German (```__label__de```), and French (```__label__fr```) achieve very high scores (around ```0.98–0.99 F1```), indicating strong and balanced performance. Other varieties, such as Lombard (```__label__lmo```) or Ligurian (```__label__lij```), show lower scores, reflecting more difficulty in distinguishing these closely related or low-resource classes.

This type of evaluation is useful to understand which languages are better learned by the model and which ones are more challenging, especially in a multilingual setting with similar linguistic varieties.

## 2.6. Model Compression

As a final step in our workflow, we can significantly reduce the size of the trained model using fastText’s built-in compression techniques.
Compression allows us to obtain a much lighter model while preserving most of its predictive performance, and it can be done in the following way:

```
./fasttext quantize -input training.txt -output langdetect -qnorm -cutoff 50000 -retrain

```
This command shrinks your model by keeping only the most important information and simplifying its mathematical storage.

First, Feature Selection (```-cutoff 50000```) acts as a filter, keeping only the 50,000 most relevant words and n-grams while discarding the rest. Second, Weight Quantization uses "Product Quantization" to replace heavy, precise decimal numbers with small, memory-efficient indexes (centroids).

The specific parameters ensure a balance between size and quality: ```-qnorm``` maintains the consistency of the vectors, while -retrain fine-tunes the model after these cuts to recover lost accuracy. The result is a lightweight ```.ftz``` file that performs nearly as well as the original but occupies a fraction of the space.

To verify the size of the files, we use the following commands, which allow us to check how much space a file or folder occupies on the server:


```
$ du -sh langdetect.bin
162M langdetect.bin

```

```
$ du -sh langdetect.ftz
1.4M langdetect.ftz

```
As we can see, the model size is significantly reduced, going from 162MB to 1.4MB. This makes the compressed version much more efficient in terms of storage and deployment, while still maintaining good performance.



















