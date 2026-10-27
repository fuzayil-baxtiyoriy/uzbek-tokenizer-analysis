"""Part 2 — Compare existing tokenizers on Uzbek (Latin/Cyrillic) and English.

TODO:
  1. Load data/test_sentences.json
  2. Load tokenizers: tiktoken (gpt2, cl100k_base, o200k_base) + HF Qwen
  3. For each tokenizer and language: fertility = tokens / words
  4. Print how one sentence is split (decode each token id)
  5. Save results/fertility_table.md and results/fertility_chart.png
"""
