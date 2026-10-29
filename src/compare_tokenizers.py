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
    """Load the parallel test set.

    Each item holds the same sentence in three versions, so every tokenizer
    is measured on identical meaning and the languages are directly comparable:
        {"id": 1, "uz_latn": "...", "uz_cyrl": "...", "en": "..."}

    encoding="utf-8" is required: Uzbek Cyrillic (ў, қ, ғ, ҳ) and the Latin
    apostrophe (o', g') would break with the system default encoding.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_tokenizers() -> dict:
    """Return {name: encode_function}. Each function: str -> list[int].

    tiktoken and Hugging Face have different APIs. Wrapping both into a plain
    `encode(text) -> ids` function lets fertility() treat them all the same.

    - gpt2        : ~50k vocab, GPT-2 (2019), almost only English data
    - cl100k_base : ~100k vocab, GPT-3.5 / GPT-4
    - o200k_base  : ~200k vocab, GPT-4o, more multilingual data
    - qwen2.5     : ~151k vocab, open-weights model (HF)

    add_special_tokens=False: HF tokenizers may add special tokens (e.g. BOS)
    that are not part of the text and would inflate the token count.
    """
    tokenizers = {}
    for name in ["gpt2", "cl100k_base", "o200k_base"]:
        enc = tiktoken.get_encoding(name)
        tokenizers[name] = enc.encode

    qwen = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")
    tokenizers["qwen2.5"] = lambda text: qwen.encode(text, add_special_tokens=False)
    return tokenizers
    


def fertility(encode, texts: list[str]) -> float:
    """Fertility = total tokens / total words. Lower is better.

    1.0 means one token per word (ideal). 3.0 means each word is split into
    ~3 pieces on average, so the text costs ~3x more tokens (money, context).

    Totals are summed over all sentences first and divided once at the end
    (not averaged per sentence), so long and short sentences get fair weight.
    Words are counted with a plain whitespace split, same rule for every language.
    """
    total_tokens = 0
    total_words = 0
    for text in texts:
        tokens = encode(text)
        words = text.split()
        total_tokens += len(tokens)
        total_words += len(words)
    return total_tokens / total_words if total_words > 0 else 0.0


def show_split(name: str, tokenizer, text: str) -> None:
    """Print how a tokenizer splits text into pieces.

    Unlike load_tokenizers(), this takes the raw tokenizer object (not just
    encode), because it also needs decode().

    Each id is decoded one by one, so we see the actual subword pieces,
    e.g. ['Sun', "'", 'iy', ' intel', 'lekt']. This makes the fertility
    number visible: many small pieces = high fertility.

    Note: in byte-level BPE one Cyrillic letter is 2 UTF-8 bytes, and a token
    can hold only part of a character. Decoding such a token alone gives '�'.
    """
    if isinstance(tokenizer, tiktoken.Encoding):
        ids = tokenizer.encode(text)
    else:  # Hugging Face tokenizer
        ids = tokenizer.encode(text, add_special_tokens=False)

    pieces = [tokenizer.decode([i]) for i in ids]
    print(f"{name:12} {len(ids):3} tokens  {pieces}")


def build_table(results: dict) -> str:
    """Build a Markdown table: fertility per tokenizer and language.

    `results` shape: {tokenizer_name: {lang: fertility}}.

    The last two columns divide Uzbek fertility by English fertility.
    "2.5x" means the same message in Uzbek costs 2.5 times more tokens than
    in English with that tokenizer. This ratio is the main finding of Part 2.
    """
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
    """Run the full benchmark: load -> measure -> show splits -> save table + chart."""
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