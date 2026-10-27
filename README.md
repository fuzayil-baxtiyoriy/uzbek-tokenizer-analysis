# Uzbek Tokenizer Analysis

> **Why is using LLMs in Uzbek more expensive — and how much can a custom tokenizer fix it?**

🚧 **Status:** work in progress — see [PLAN.md](PLAN.md) for the roadmap.

## Motivation

LLM APIs charge per token, and a model's context window is measured in tokens.
Most popular tokenizers (GPT-2, GPT-4, Llama, Qwen) were trained mostly on English text,
so Uzbek words are split into many more pieces. That means Uzbek users:

- pay **more** for the same message,
- fit **less** text into the context window,
- and get models that "see" Uzbek words as fragments instead of meaningful units.

This project measures that gap and builds a small Uzbek BPE tokenizer to see how much it can be closed.
Uzbek is written in both **Latin** and **Cyrillic** scripts, so both are compared.

## What this project does

| Part | Description | Status |
|---|---|---|
| 1. Data | Uzbek Wikipedia subset + parallel test set (uz-Latin / uz-Cyrillic / English) | ⬜ |
| 2. Benchmark | Compare existing tokenizers (`gpt2`, `cl100k_base`, `o200k_base`, Qwen, Llama) | ⬜ |
| 3a. BPE from scratch | Minimal byte-pair encoding implementation in pure Python | ⬜ |
| 3b. Custom tokenizer | Train Uzbek BPE tokenizers (8k / 16k / 32k vocab) with HF `tokenizers` | ⬜ |
| 4. Pipeline | Sliding-window dataset → token embeddings → positional embeddings (PyTorch) | ⬜ |

## Metric

**Fertility** = number of tokens / number of words. Lower is better (1.0 = one token per word).

## Results

_Coming soon._

| Tokenizer | English | Uzbek (Latin) | Uzbek (Cyrillic) |
|---|---|---|---|
| gpt2 | – | – | – |
| cl100k_base | – | – | – |
| o200k_base | – | – | – |
| Qwen | – | – | – |
| uz-bpe-16k (ours) | – | – | – |

## Key findings

_Coming soon._

## Project structure

```
uzbek-tokenizer-analysis/
├── data/
│   └── test_sentences.json     # parallel test set: uz-Latin, uz-Cyrillic, English
├── src/
│   ├── compare_tokenizers.py   # Part 2: benchmark existing tokenizers
│   ├── bpe_from_scratch.py     # Part 3a: minimal BPE implementation
│   ├── train_hf_tokenizer.py   # Part 3b: train Uzbek tokenizers
│   └── pipeline.py             # Part 4: dataloader + embeddings
├── results/                    # tables and charts
├── notes/                      # study notes
├── PLAN.md                     # roadmap and checklist
└── requirements.txt
```

## How to run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/compare_tokenizers.py
```

## Background

Built while studying Chapter 2 ("Working with text data") of
*Build a Large Language Model (From Scratch)* by Sebastian Raschka.

## Author

**Dilshod Bakhtiyorov** — Backend Engineer moving into Generative AI · Tashkent, Uzbekistan
