"""Part 2 — Compare existing tokenizers on Uzbek (Latin/Cyrillic) and English.

TODO:
  1. Load data/test_sentences.json
  2. Load tokenizers: tiktoken (gpt2, cl100k_base, o200k_base) + HF Qwen
  3. For each tokenizer and language: fertility = tokens / words
  4. Print how one sentence is split (decode each token id)
  5. Save results/fertility_table.md and results/fertility_chart.png
"""


import json
from pathlib import Path
from plot_results import plot_fertility

import tiktoken
from transformers import AutoTokenizer

DATA_PATH = Path("data/test_sentences.json")
RESULTS_DIR = Path("results")
LANGS = ["en", "uz_latn", "uz_cyrl"]


def load_sentences(path: Path) -> list[dict]:
    # read json file and return list of dicts, each dict: {lang: sentence}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_tokenizers() -> dict:
    """Return {name: encode_function}. Each function: str -> list[int]."""
    tokenizers = {}
    for name in ["gpt2", "cl100k_base", "o200k_base"]:
        enc = tiktoken.get_encoding(name)
        tokenizers[name] = enc.encode

    qwen = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")
    tokenizers["qwen2.5"] = lambda text: qwen.encode(text, add_special_tokens=False)
    return tokenizers
    


def fertility(encode, texts: list[str]) -> float:
    total_tokens = 0
    total_words = 0
    for text in texts:
        tokens = encode(text)
        words = text.split()
        total_tokens += len(tokens)
        total_words += len(words)
    return total_tokens / total_words if total_words > 0 else 0.0


def show_split(name: str, tokenizer, text: str) -> None:
    """Print how a tokenizer splits text into pieces."""
    if isinstance(tokenizer, tiktoken.Encoding):
        ids = tokenizer.encode(text)
    else:  # Hugging Face tokenizer
        ids = tokenizer.encode(text, add_special_tokens=False)

    pieces = [tokenizer.decode([i]) for i in ids]
    print(f"{name:12} {len(ids):3} tokens  {pieces}")


def build_table(results: dict) -> str:
    """Build a Markdown table: fertility per tokenizer and language."""
    lines = [
        "| Tokenizer | en | uz_latn | uz_cyrl | uz_latn / en | uz_cyrl / en |",
        "|---|---|---|---|---|---|",
    ]
    for name, scores in results.items():
        en = scores["en"]
        latn = scores["uz_latn"]
        cyrl = scores["uz_cyrl"]
        lines.append(
            f"| {name} | {en:.2f} | {latn:.2f} | {cyrl:.2f} "
            f"| {latn / en:.2f}× | {cyrl / en:.2f}× |"
        )
    return "\n".join(lines)


def main():
      # 1. Load data and tokenizers
      sentences = load_sentences(DATA_PATH)
      tokenizers = load_tokenizers()
      print(f"Loaded {len(sentences)} sentences, {len(tokenizers)} tokenizers\n")

      # 2. Fertility for every tokenizer x language
      results = {}  # {tokenizer_name: {lang: fertility}}
      for name, encode in tokenizers.items():
          results[name] = {}
          for lang in LANGS:
              texts = [s[lang] for s in sentences]
              results[name][lang] = fertility(encode, texts)

      # 3. How one example sentence is split
      raw_tokenizers = {
          "gpt2": tiktoken.get_encoding("gpt2"),
          "cl100k_base": tiktoken.get_encoding("cl100k_base"),
          "o200k_base": tiktoken.get_encoding("o200k_base"),
          "qwen2.5": AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B"),
      }
      example = sentences[2]  # 3rd sentence: "Sun'iy intellekt ..."
      for lang in LANGS:
          print(f"--- {lang}: {example[lang]}")
          for name, tok in raw_tokenizers.items():
              show_split(name, tok, example[lang])
          print()

      # 4. Results table
      table = build_table(results)
      print(table)
      RESULTS_DIR.mkdir(exist_ok=True)
      (RESULTS_DIR / "fertility_table.md").write_text(table, encoding="utf-8")
      print(f"\nSaved table -> {RESULTS_DIR / 'fertility_table.md'}")

      # 5. Chart
      plot_fertility(results)


if __name__ == "__main__":
    main()