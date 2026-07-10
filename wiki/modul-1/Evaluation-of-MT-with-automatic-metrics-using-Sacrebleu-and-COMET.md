## Files for the tutorial

To do this tutorial you can use your own files or the ones at: [https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/tree/main/evaluation](https://github.com/mtuoc/MTUOC-Machine-Translation-Practical-Course/tree/main/evaluation)

## 1. Evaluating Machine Translation: Metrics and Methodologies

The evaluation of Machine Translation (MT) is a critical bottleneck in the development of NLP systems. While human evaluation remains the "gold standard," it is often prohibitively expensive and time-consuming. This has led to the rise of automated metrics, which allow for rapid, reproducible, and scalable assessment.

### 1.1. The Trade-offs of Automated Metrics

Before diving into the tools, it is essential to understand the inherent tension between efficiency and accuracy.

| Feature | Advantages | Disadvantages |
| :--- | :--- | :--- |
| **Speed** | Instantaneous feedback during model training. | |
| **Nuance** | | Lack of Nuance: Difficulty capturing sarcasm, tone, or style. |
| **Cost** | Cost-effectiveness: Eliminates the need for paid bilingual experts. | |
| **Accuracy** | | Surface-level Bias: Often over-penalizes synonyms that are technically correct. |
| **Reliability** | Reproducibility: Consistent scores across different environments. | |
| **Dependency** | | Reference Dependency: Performance is strictly tied to the quality of the "Gold Standard" reference. |

### 1.2. SacreBLEU: Standardization in Evaluation

In the past, comparing MT research was difficult because different researchers used different preprocessing steps. SacreBLEU solved this by providing a tool that outputs "shareable, determinate, and reproducible" scores. 

If you want to know more about this tool, you can read:

[Post, M. (2018, October). A call for clarity in reporting BLEU scores. In Proceedings of the third conference on machine translation: Research papers (pp. 186-191).](https://aclanthology.org/W18-6319/)

SacreBLEU manages three primary string-based metrics:

* **A. BLEU (Bilingual Evaluation Understudy)** BLEU measures the precision of n-grams (sequences of words) between the MT output and the reference.
  * Mechanism: It calculates how many words/phrases in the machine output appear in the human reference.  
  * Limitation: It is notoriously bad at the sentence level and does not account for meaning if the exact words differ.

   [Papineni, K., Roukos, S., Ward, T., & Zhu, W. J. (2002, July). Bleu: a method for automatic evaluation of machine translation. In Proceedings of the 40th annual meeting of the Association for Computational Linguistics (pp. 311-318).](https://aclanthology.org/P02-1040.Pdf]

* **B. chrF2 (Character n-gram F-score)**: Unlike BLEU, which looks at whole words, chrF looks at character sequences.

  * Mechanism: It uses a combination of precision and recall on character n-grams.
  * Strength: It is particularly effective for morphologically rich languages (like Finnish or Hungarian) where word endings change frequently.

  [Popović, M. (2015, September). chrF: character n-gram F-score for automatic MT evaluation. In Proceedings of the tenth workshop on statistical machine translation (pp. 392-395).](https://aclanthology.org/W15-3049.pdf)

* **C. TER (Translation Edit Rate)**: TER measures the amount of editing a human would need to do to make the machine output match the reference exactly.

  * Mechanism: It calculates the number of insertions, deletions, substitutions, and shifts required.
  * Interpretation: A lower TER score indicates a better translation (less work for a human editor).

  [Snover, M., Dorr, B., Schwartz, R., Micciulla, L., & Makhoul, J. (2006). A study of translation edit rate with targeted human annotation. In Proceedings of the 7th Conference of the Association for Machine Translation in the Americas: Technical Papers (pp. 223-231).](https://aclanthology.org/2006.amta-papers.25/)

* **3. COMET: The Neural Paradigm Shift**: While SacreBLEU metrics look for literal overlaps in text, COMET (Cross-lingual Optimized Metric for Evaluation of Translation) represents a new generation of "neural metrics." Developed by Unbabel, COMET leverages multilingual embeddings (from models like XLM-RoBERTa) to evaluate translations based on meaning rather than just matching characters.

  * Semantic Awareness: COMET can recognize that "The sofa is comfortable" and "The couch is cozy" are excellent translations of each other, even though they share zero n-grams.
  * Contextual Input: Unlike BLEU, COMET typically takes the Source Text into account alongside the Reference, allowing it to detect if the machine has hallucinated information not present in the original.
  * Correlation: COMET currently shows a much higher correlation with human judgment than any of the string-based metrics mentioned above.
  
  [Rei, R., Stewart, C., Farinha, A. C., & Lavie, A. (2020, November). COMET: A neural framework for MT evaluation. In Proceedings of the 2020 conference on empirical methods in natural language processing (emnlp) (pp. 2685-2702).](https://aclanthology.org/2020.emnlp-main.213/)

## 2. Sacrebleu

### 2.1. Installation

Install the official Python module from PyPI (Python>=3.9 only):

`pip install sacrebleu`

### 2.2. Basic usage

We have the test set newstest2019-ref.eng-GB.txt with the reference translation newstest2019-ref.spa.txt and the translation to evaluate eval.en-OpusMT.es. If we want to evaluate the BLEU score, we can write:

`sacrebleu newstest2019-ref.spa.txt -i eval.en-OpusMT.es -m bleu`

And well get: 
```
{
 "name": "BLEU",
 "score": 39.3,
 "signature": "nrefs:1|case:mixed|eff:no|tok:13a|smooth:exp|version:2.6.0",
 "verbose_score": "69.0/46.8/34.0/25.2 (BP = 0.965 ratio = 0.966 hyp_len = 52264 ref_len = 54116)",
 "nrefs": "1",
 "case": "mixed",
 "eff": "no",
 "tok": "13a",
 "smooth": "exp",
 "version": "2.6.0"
}
```
We can, of course, calculate several metrics at the same time:

`sacrebleu newstest2019-ref.spa.txt -i eval.en-OpusMT.es -m bleu chrf ter`

getting

```
sacrebleu newstest2019-ref.spa.txt -i eval.en-OpusMT.es -m bleu chrf ter
[
{
 "name": "BLEU",
 "score": 39.3,
 "signature": "nrefs:1|case:mixed|eff:no|tok:13a|smooth:exp|version:2.6.0",
 "verbose_score": "69.0/46.8/34.0/25.2 (BP = 0.965 ratio = 0.966 hyp_len = 52264 ref_len = 54116)",
 "nrefs": "1",
 "case": "mixed",
 "eff": "no",
 "tok": "13a",
 "smooth": "exp",
 "version": "2.6.0"
},
{
 "name": "chrF2",
 "score": 63.6,
 "signature": "nrefs:1|case:mixed|eff:yes|nc:6|nw:0|space:no|version:2.6.0",
 "nrefs": "1",
 "case": "mixed",
 "eff": "yes",
 "nc": "6",
 "nw": "0",
 "space": "no",
 "version": "2.6.0"
},
{
 "name": "TER",
 "score": 46.6,
 "signature": "nrefs:1|case:lc|tok:tercom|norm:no|punct:yes|asian:no|version:2.6.0",
 "nrefs": "1",
 "case": "lc",
 "tok": "tercom",
 "norm": "no",
 "punct": "yes",
 "asian": "no",
 "version": "2.6.0"
}
]
```

And we can get the values for several translations at the same time:

```
sacrebleu newstest2019-ref.spa.txt -i eval.en-OpusMT.es eval.en-NLLB600dist.es eval.en-salamandraTA-2b-instruct.es -m bleu chrf ter
sacreBLEU: Found 3 systems.
[
    {
        "system": "eval.en-OpusMT.es",
        "BLEU": "39.3",
        "chrF2": "63.6",
        "TER": "46.6"
    },
    {
        "system": "eval.en-NLLB600dist.es",
        "BLEU": "39.8",
        "chrF2": "64.0",
        "TER": "46.0"
    },
    {
        "system": "eval.en-salamandraTA-2b-instruct.es",
        "BLEU": "35.0",
        "chrF2": "61.5",
        "TER": "52.5"
    }
]
```



We have several options for the final results, for example **text**:

```
sacrebleu newstest2019-ref.spa.txt -i eval.en-OpusMT.es eval.en-NLLB600dist.es eval.en-salamandraTA-2b-instruct.es -m bleu chrf ter --format text
sacreBLEU: Found 3 systems.
```

| System | BLEU | chrF2 | TER |
| :--- | :---: | :---: | :---: |
| eval.en-OpusMT.es | 39.3 | 63.6 | 46.6 |
| eval.en-NLLB600dist.es | 39.8 | 64.0 | 46.0 |
| eval.en-salamandraTA-2b-instruct.es | 35.0 | 61.5 | 52.5 |

```
-----------------
Metric signatures
-----------------
 - BLEU       nrefs:1|case:mixed|eff:no|tok:13a|smooth:exp|version:2.6.0
 - chrF2      nrefs:1|case:mixed|eff:yes|nc:6|nw:0|space:no|version:2.6.0
 - TER        nrefs:1|case:lc|tok:tercom|norm:no|punct:yes|asian:no|version:2.6.0

```

or **latex**:

```
sacrebleu newstest2019-ref.spa.txt -i eval.en-OpusMT.es eval.en-NLLB600dist.es eval.en-salamandraTA-2b-instruct.es -m bleu chrf ter --format latex
sacreBLEU: Found 3 systems.
\begin{tabular}{rccc}
\toprule
                              System &  BLEU  &  chrF2  &  TER  \\
\midrule
                   eval.en-OpusMT.es &  39.3  &  63.6   & 46.6  \\
              eval.en-NLLB600dist.es &  39.8  &  64.0   & 46.0  \\
 eval.en-salamandraTA-2b-instruct.es &  35.0  &  61.5   & 52.5  \\
\bottomrule
\end{tabular}

-----------------
Metric signatures
-----------------
 - BLEU       nrefs:1|case:mixed|eff:no|tok:13a|smooth:exp|version:2.6.0
 - chrF2      nrefs:1|case:mixed|eff:yes|nc:6|nw:0|space:no|version:2.6.0
 - TER        nrefs:1|case:lc|tok:tercom|norm:no|punct:yes|asian:no|version:2.6.0
```

Please, note that in both cases the system provides the "Metric signatures", that is, the exact configuration figures for each metric (in the example they are the default ones). This information is important and allow for the replication of the experiments and results.


### 2.3. Advanced Evaluation: Statistical Significance with Paired Bootstrap Resampling

When comparing multiple MT systems, a higher score (e.g., +0.5 BLEU) does not automatically guarantee that one model is superior to another. To confirm that these improvements are mathematically significant and not due to chance, we can use Paired Bootstrap Resampling.

**The Command**

To execute this analysis, we designate the first input file as the baseline and compare subsequent systems against it. Append the --paired-bs flag to your command:

`sacrebleu newstest2019-ref.spa.txt -i eval.en-OpusMT.es eval.en-NLLB600dist.es eval.en-salamandraTA-2b-instruct.es -m bleu chrf ter \
    --paired-bs --format text`

**How it Works: The Methodology**

This feature is a high-performance implementation of the standard statistical tests used in MT research (compliant with the reference Moses implementation).

* Bootstrap Resampling (95% Confidence Intervals): The tool takes your original test set and creates thousands of "pseudo-test sets" by randomly sampling sentences with replacement. It calculates the metric for each sample to estimate a 95% Confidence Interval (CI). This tells us the range in which the true score likely falls.
* Significance Testing (p-values): By comparing the baseline (OpusMT) against the other systems (NLLB and salamandra) across these resamples, sacrebleu calculates a p-value. **A p-value < 0.05 typically indicates that the difference in performance is statistically significant.**
* Customization: By default, the tool performs 1000 iterations. You can increase this for higher precision using the --paired-bs-n flag, though the default is generally sufficient for most C1-level research papers.

**Understanding the Output** 

The output is a table like this one:

| System | BLEU ($\mu \pm 95\%$ CI) | chrF2 ($\mu \pm 95\%$ CI) | TER ($\mu \pm 95\%$ CI) |
| :--- | :---: | :---: | :---: |
| **Baseline: eval.en-OpusMT.es** | 39.3 (39.3 ± 0.9) | 63.6 (63.6 ± 0.6) | 46.6 (46.7 ± 0.8) |
| **eval.en-NLLB600dist.es** | 39.8 (39.8 ± 0.8) <br> *(p = 0.0180)** | 64.0 (64.0 ± 0.6) <br> *(p = 0.0090)** | 46.0 (46.0 ± 0.8) <br> *(p = 0.0010)** |
| **eval.en-salamandraTA-2b-instruct.es** | 35.0 (35.0 ± 0.8) <br> *(p = 0.0010)** | 61.5 (61.6 ± 0.5) <br> *(p = 0.0010)** | 52.5 (52.5 ± 0.9) <br> *(p = 0.0010)** |

And a text explanation:

```
------------------------------------------------------------
Paired bootstrap resampling test with 1000 resampling trials
------------------------------------------------------------
 - Each system is pairwise compared to Baseline: eval.en-OpusMT.es.
   Actual system score / bootstrap estimated true mean / 95% CI are provided for each metric.

 - Null hypothesis: the system and the baseline translations are essentially
   generated by the same underlying process. For a given system and the baseline,
   the p-value is roughly the probability of the absolute score difference (delta)
   or higher occurring due to chance, under the assumption that the null hypothesis is correct.

 - Assuming a significance threshold of 0.05, the null hypothesis can be rejected
   for p-values < 0.05 (marked with "*"). This means that the delta is unlikely to be attributed
   to chance, hence the system is significantly "different" than the baseline.
   Otherwise, the p-values are highlighted in red.

 - NOTE: Significance does not tell whether a system is "better" than the baseline but rather
   emphasizes the "difference" of the systems in terms of the replicability of the delta.
```

When interpreting the results from a paired bootstrap resampling run, we move beyond point estimates to look at the distribution of potential scores.

1. Mean and Confidence Intervals (μ±95% CI)

The values shown as 39.8±0.8 represent the mean score (μ) across all bootstrap samples and the 95% Confidence Interval.

Interpretation: We are 95% confident that the true BLEU score for the NLLB model on this domain lies between 39.0 and 40.6.

If the intervals of two systems do not overlap, it is a strong visual indicator of a significant difference, though not a definitive statistical proof—which is why we need the p-value.

2. The p-value (p)

The p-value represents the probability that the observed difference between the system and the baseline occurred by pure chance.

In this table: For the NLLB system's BLEU score, p=0.018.

Significance Threshold: In most scientific literature, a threshold of p<0.05 is required to reject the null hypothesis. Since 0.018<0.05, we can officially state that NLLB performs significantly better than OpusMT on this dataset.

3. The Asterisk (*)

The asterisk is a shorthand notation used in research papers to denote Statistical Significance.

* One asterisk (*): Usually means p<0.05.
* Two asterisks ():** Often used for p<0.01.
* No asterisk: Indicates that even if the score is higher, the improvement is "marginal" or "statistically insignificant," meaning the models are essentially performing at the same level.

Looking at the data in our example, NLLB600dist is the superior model across all three metrics (higher BLEU/chrF2 and lower TER), and these gains are statistically confirmed. Conversely, while salamandraTA-2b shows a significant difference (p=0.001), it is significantly worse than the baseline in this specific test set, as evidenced by its lower BLEU and higher TER.


## 3. COMET

### 3.1 Moving Beyond String Matching to Neural Metrics

While SacreBLEU provides a reliable baseline, it often fails to account for synonyms and structural variations. COMET addresses this by using multilingual encoders (XLM-RoBERTa) to map source, machine output, and reference sentences into a shared vector space.

### 3.1. Installation and Requirements

To run COMET it is advisable to have GPU support, but it can also be run without GPU support, but it will be quite slow (be patient). To install COMET (it is highly recommended to use a virtual environment) write:

`pip install unbabel-comet`

Note: COMET relies on heavy neural weights. Upon first execution, the tool will automatically download the required model checkpoints (often >2GB). Ensure you have adequate disk space and a stable connection.

### 3.2. Selecting the Right Model

COMET is a framework, not a single algorithm. Depending on your needs, you can choose between different architectures:

* Unbabel/wmt22-comet-da (default and recommended): The current "workhorse" for MT evaluation. It is reference-based and trained on Direct Assessments (DA).
* Unbabel/wmt22-cometkiwi-da (Reference-free): A Quality Estimation (QE) model. It evaluates the translation by looking only at the source text, which is invaluable when no human reference is available.
* Unbabel/XCOMET-XL: A more recent, "explainable" model that not only gives a score but can also pinpoint specific errors within the sentence.

### 3.3. Practical Evaluation: Running the Comparison

To maintain consistency with our previous analysis, we will evaluate our three systems using the standard reference-based model.

The Scoring Command: You can pass multiple translation files simultaneously. The source file (-s) and the reference file (-r) remain constant, while the hypotheses (-t) vary.
Bash

`comet-score -s newstest2019-ref.eng-GB.txt -r newstest2019-ref.spa.txt -t eval.en-OpusMT.es eval.en-NLLB600dist.es eval.en-salamandraTA-2b-instruct.es --model Unbabel/wmt22-comet-da`

NOTE: as wmt22-comet-da is the default model, you can omit --model Unbabel/wmt22-comet-da. Anyway, it is always a good practice to indicate the model.

As a result, you'll get a score for each segment and the final scores for each system.

```
eval.en-OpusMT.es	score: 0.8352
eval.en-NLLB600dist.es	score: 0.8474
eval.en-salamandraTA-2b-instruct.es	score: 0.8548
``` 

### 3.4. Statistical Analysis: comet-compare

Just as we did with SacreBLEU, we must determine if the COMET score differences are statistically significant. COMET provides a dedicated script for this that uses Paired T-Tests and Bootstrap Resampling.
Bash

`comet-compare -s newstest2019-ref.eng-GB.txt -r newstest2019-ref.spa.txt -t eval.en-OpusMT.es eval.en-NLLB600dist.es eval.en-salamandraTA-2b-instruct.es --model Unbabel/wmt22-comet-da`

And we'll get:

```
x_name: eval.en-OpusMT.es
y_name: eval.en-NLLB600dist.es

Bootstrap Resampling Results:
x-mean:	0.8354
y-mean:	0.8476
ties (%):	0.0000
x_wins (%):	0.0000
y_wins (%):	1.0000

Paired T-Test Results:
statistic:	-9.9123
p_value:	0.0000
Null hypothesis rejected according to t-test.
Scores differ significantly across samples.
eval.en-NLLB600dist.es outperforms eval.en-OpusMT.es.
==========================
x_name: eval.en-OpusMT.es
y_name: eval.en-salamandraTA-2b-instruct.es

Bootstrap Resampling Results:
x-mean:	0.8354
y-mean:	0.8549
ties (%):	0.0000
x_wins (%):	0.0000
y_wins (%):	1.0000

Paired T-Test Results:
statistic:	-11.1545
p_value:	0.0000
Null hypothesis rejected according to t-test.
Scores differ significantly across samples.
eval.en-salamandraTA-2b-instruct.es outperforms eval.en-OpusMT.es.
==========================
x_name: eval.en-NLLB600dist.es
y_name: eval.en-salamandraTA-2b-instruct.es

Bootstrap Resampling Results:
x-mean:	0.8476
y-mean:	0.8549
ties (%):	0.0033
x_wins (%):	0.0000
y_wins (%):	0.9967

Paired T-Test Results:
statistic:	-5.0565
p_value:	0.0000
Null hypothesis rejected according to t-test.
Scores differ significantly across samples.
eval.en-salamandraTA-2b-instruct.es outperforms eval.en-NLLB600dist.es.

Summary
If system_x is better than system_y then:
Null hypothesis rejected according to t-test with p_value=0.05.
Scores differ significantly across samples.
system_x \ system_y                  eval.en-OpusMT.es    eval.en-NLLB600dist.es    eval.en-salamandraTA-2b-instruct.es
-----------------------------------  -------------------  ------------------------  -------------------------------------
eval.en-OpusMT.es                                         False                     False
eval.en-NLLB600dist.es               True                                           False
eval.en-salamandraTA-2b-instruct.es  True                 True
```


**Interpreting COMET Scores**

Unlike BLEU, which ranges from 0 to 100, COMET scores typically range between 0 and 1 (though some older versions used different scales).
* Higher is better: A score closer to 1.0 indicates a near-perfect translation according to the model's semantic understanding.
* Negative Scores: Occasionally, very poor translations can result in negative values, indicating a total lack of semantic correspondence.

Once the `comet-compare` execution is complete, the tool generates a comprehensive statistical report. Unlike simpler metrics, COMET utilizes Bootstrap Resampling and Paired T-Tests to ensure that the delta between two models is not merely a byproduct of data noise.

**Statistical Foundations**

The output provides a rigorous look at how two systems compare across thousands of iterations:

* Win Ratio (x_wins vs. y_wins): This metric represents the percentage of bootstrap samples in which a specific system outperformed its competitor. For instance, if y_wins is 1.0000, it signifies that System Y was superior in 100% of the simulated scenarios.
* Ties: This indicates the frequency with which the two systems performed identically. In neural evaluation, ties are increasingly rare due to the high sensitivity of the embeddings.
* The p-value: Following standard statistical conventions, a p<0.05 allows us to reject the Null Hypothesis (the assumption that there is no significant difference between the models). In our current results, p=0.0000 indicates absolute statistical confidence.

**Current System Standings* 

Based on the COMET scores, we observe a clear hierarchy of performance that differs from our previous string-based analysis.

I. OpusMT vs. NLLB600dist: While NLLB shows a respectable mean score of 0.8476, it significantly outperforms the OpusMT baseline (0.8354). The statistical test confirms this with a win ratio of 100%, suggesting that NLLB's neural architecture consistently produces more semantically accurate translations.

II. The Emergence of SalamandraTA-2b-instruct. The most notable result is the performance of Salamandra.

* It achieves the highest mean score in the set (0.8549).
* In a direct head-to-head comparison with NLLB, it wins 99.67% of the time.
* The summary matrix explicitly marks the comparison as True, meaning Salamandra is statistically superior to both OpusMT and NLLB according to the WMT22-COMET-DA model.

**Summary Matrix** 

The summary table at the end of the report acts as a definitive leaderboard. If a cell is marked True, it confirms that the system in that row is statistically better than the system in that column.

## 4. Final Conclusions: Synthesizing the Evaluation Results

The discrepancy between our SacreBLEU and COMET results provides a profound case study in modern Machine Translation evaluation. While string-based metrics and neural-based metrics often correlate, the outliers—like SalamandraTA-2b-instruct—reveal the limitations of relying on a single source of truth.

### 4.1. The "Metric Gap": Why Salamandra Flipped the Script

In our evaluation, Salamandra ranked last in BLEU but first in COMET. This phenomenon is typically attributed to the nature of Instruction-tuned Large Language Models (LLMs):

* Lexical Flexibility: BLEU requires a word-for-word match with the human reference. Because Salamandra is an "instruct" model, it tends to be more descriptive or uses more sophisticated synonyms. While semantically correct, these variations are penalized by BLEU as "errors."
* Semantic Adequacy: COMET recognizes that a translation can be "correct" without being an "exact match." It rewards the model for capturing the intent and nuances of the English source text, which is where Salamandra clearly excels.
* The Verdict: If your priority is a literal, predictable translation, BLEU's top model (NLLB) might be your choice. However, if you seek naturalness and semantic depth, COMET’s winner (Salamandra) is superior.

### 4.2. The Golden Rule: Human-in-the-Loop

While automated metrics like SacreBLEU and COMET are indispensable for rapid iteration and statistical validation, they are not infallible. For high-stakes or professional-grade translation, Human Evaluation remains an mandatory final step.

A comprehensive evaluation strategy should ideally include:

* Direct Assessment (DA): Human experts rate the translation on a scale (e.g., 0–100) based on how well it conveys the meaning of the source.
* Error Analysis (MQM): Utilizing frameworks like the Multidimensional Quality Metrics to categorize specific issues (e.g., terminology, grammar, style).
* Post-editing Effort: Measuring the time and number of keystrokes a human translator needs to correct the machine output.

## #4.3. Final Recommendations

To conclude this tutorial, remember that evaluation is not about finding a single "perfect" number, but about understanding the behavior of your model.

* Use SacreBLEU for a quick, reproducible baseline and to ensure lexical consistency.
* Use COMET to capture semantic quality and to better predict actual human preference.
* Always perform a qualitative check: Spend time reading at least 50–100 segments of the output. Often, a model with a high COMET score might still have "hallucinations" or stylistic quirks that no automated tool can yet fully quantify.
