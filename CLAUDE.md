# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

**Uzbek Tokenizer Analysis** — measures how inefficiently popular LLM tokenizers handle Uzbek
(Latin and Cyrillic scripts) compared to English, and trains a small Uzbek BPE tokenizer to close the gap.

Built while studying Chapter 2 of *Build a Large Language Model (From Scratch)* (Sebastian Raschka).
The roadmap and checklist live in `PLAN.md` — read it to know which part is in progress.

## This is a learning project — rules for Claude

The author (Dilshod) is a backend engineer learning GenAI. The goal is **understanding**, not finished code.

- **Do not write full implementations** of the TODOs in `src/` unless explicitly asked ("write it for me").
- Default mode: explain the concept, give hints, point to the relevant Raschka section (2.2–2.8),
  review the author's code, and explain errors.
- When reviewing code: point out bugs and shape mismatches, suggest the fix in words or a minimal snippet.
- Small helpers that are not the learning goal (plotting, file I/O, argparse) may be written directly.
- Always explain **why**, not only **what**.
- Respond in **Uzbek** (Latin script). Code, comments, commit messages and README stay in **English**.

## Structure

```
data/test_sentences.json     # parallel set: uz_latn, uz_cyrl, en (target: 20 sentences)
data/uz_wiki.txt             # Uzbek Wikipedia subset — gitignored, not committed
src/compare_tokenizers.py    # Part 2: benchmark tiktoken + HF tokenizers
src/bpe_from_scratch.py      # Part 3a: pure-Python BPE (learning core)
src/train_hf_tokenizer.py    # Part 3b: HF `tokenizers` ByteLevel BPE, vocab 8k/16k/32k
src/pipeline.py              # Part 4: sliding-window dataset + token/positional embeddings
results/                     # fertility_table.md, fertility_chart.png, tokenizers/
notes/                       # study notes
```

## Key definitions

- **Fertility** = tokens / words (split on whitespace). Lower is better.
- Tokenizers to compare: `gpt2`, `cl100k_base`, `o200k_base` (tiktoken), `Qwen/Qwen2.5-0.5B` (HF), plus our own.
- BPE round-trip must hold: `decode(encode(x)) == x`.

## Commands

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python src/compare_tokenizers.py
python src/bpe_from_scratch.py
python src/train_hf_tokenizer.py
python src/pipeline.py
```

## Conventions

- Python 3.10+, standard library first; dependencies only from `requirements.txt`.
- Keep scripts runnable top-to-bottom with a `main()` and `if __name__ == "__main__":`.
- Never commit large data (`data/*.txt`) or model files over a few MB.
- Results that go into README must be reproducible by running the scripts.
- Small, focused commits with clear English messages (e.g. `Add fertility benchmark for tiktoken encodings`).

## Definition of done

See the checklist at the end of `PLAN.md`. Update the checkboxes in `PLAN.md` and the
status column in `README.md` when a part is finished.
