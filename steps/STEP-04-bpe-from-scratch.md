# Step 4: BPE from scratch — results and takeaways

**Code:** `src/bpe_from_scratch.py` — pure Python, byte-level BPE.
**Training text:** Uzbek Wikipedia (`data/uz_wiki.txt`), Latin script.

## Runs

| Setting | Time | Vocab size |
|---|---|---|
| 20,000 chars, 50 merges | 0.1 s | 306 |
| 200,000 chars, 500 merges | 8.8 s | 756 |

## 1. First merges — Uzbek suffixes

First 30 of 500 merges:

```
'a ', 'ar', 'i ', 'an', 'sh', ', ', 'ʻ', 'in', 'lar', 'iy', 'il', 'oʻ', 'at', 'on',
'da ', 'as', '. ', 'ch', 'or', 'di', 'an ', 'li', 'ir', 'ing', '�', 'al', 'va ',
'ing ', 'iy ', 'ma'
```

Grammatical pieces found among the learned merges:

| Token | In grammar |
|---|---|
| `lar` | plural suffix |
| `da ` | locative case (*uyda* — "at home") |
| `ga ` | dative case (*uyga* — "to home") |
| `dan ` | ablative case (*uydan* — "from home") |
| `ing` | genitive case (*-ning*) |
| `va ` | most frequent conjunction ("and") |
| `oʻ`, `gʻ` | special letters of the Uzbek Latin alphabet |

**Takeaway:** the algorithm only counts "which pair is most frequent?", yet the result reflects the
agglutinative structure of Uzbek (stem + suffixes). Nobody taught it grammar.

Tokens ending in a space (`da `, `ga `, `va `): a suffix comes at the end of a word and is followed by
a space, so the tokenizer also learned word boundaries. (GPT-2 puts the space at the *start* of a token
instead, because it pre-splits text with a regex; our BPE has no pre-tokenization.)

## 2. Last merges — stems and words

```
'omonidan ', 'bu', 'alan', 'rez', 'okim', 'lumot', 'osiy ', 'ma ', 'adem', 'ed', 'umum',
'aʼ', 'atsiy', 'inchi ', 'arix', 'lov', 'tarix', 'An', 'umla', 'oxir'
```

As merges grow, BPE moves from suffixes to word stems: `tarix` (history), `umum` (general),
`lumot` (*maʼlumot*, information), `okim` (*hokim*, governor), `omonidan ` (*tomonidan*, "by").
This mirrors typical Wikipedia topics.

## 3. The `ʻ` and `�` tokens

- `ʻ` (U+02BB) is one character but **2 bytes** in UTF-8 (`CB BB`). Because `oʻ` and `gʻ` are so
  frequent, these two bytes were merged very early.
- `�` is an **incomplete UTF-8 sequence** — part of a character. For example, the first 2 bytes of a
  3-byte character such as `—` (U+2014) or `’` (U+2019) merged, but the third byte has not been
  joined yet. (A single byte from a 2-byte character gives `�` too.) Decoding it alone is impossible,
  so `errors="replace"` shows `�`. The `�` pieces in GPT-2's Cyrillic output come from the same effect.

This is live proof that BPE works on **bytes**, not letters.

## 4. Fertility

| Tokenizer | Vocab | en | uz_latn | uz_cyrl |
|---|---|---|---|---|
| gpt2 | 50,257 | 1.22 | 3.34 | 8.33 |
| BPE, 50 merges | 306 | 5.02 | 5.47 | 13.51 |
| BPE, 500 merges | 756 | 3.92 | 3.73 | 12.60 |

**a) The languages swapped places.** With GPT-2, English is much better than Uzbek. With our tokenizer,
Uzbek beats English (3.73 < 3.92). → A tokenizer is good at the language it was trained on.
The problem is not the Uzbek language, it is the training data.

**b) A 66× smaller vocab gets close to GPT-2.** 756 vs 50,257 tokens; on Uzbek Latin 3.73 vs 3.34.
With a large vocab (Step 5) we expect to beat GPT-2.

**c) Cyrillic is very bad (12.60).** The Wikipedia dump is in Latin script: only 125 Cyrillic
characters appear in the 200k training chars, and only one Cyrillic merge was learned (`а`, `D0 B0`).
Almost every Cyrillic letter stays split into 2 bytes — the same problem GPT-2 has.

**d) Number of merges:** 50 → 500 merges takes Uzbek Latin from 5.47 → 3.73.

## 5. Hidden problem — the apostrophe

- Wikipedia: `oʻ` — character `ʻ` (U+02BB, modifier letter turned comma), 2,457 times in the training text
- Test sentences: `o'` — character `'` (U+0027, plain keyboard apostrophe), only 15 times in the training text

To a computer these are two different characters. The learned `oʻ`, `gʻ` merges do not fire on the
test sentences, so the 3.73 score looks worse than it really is.

Uzbek texts mix `'`, `ʻ`, `’`, `ʼ`. Fix: **normalization** — map all variants to one character before
training and encoding. → Added in Step 5.

Careful: Wikipedia uses two different marks — `ʻ` for `oʻ`/`gʻ` and `ʼ` (U+02BC) for the glottal stop
(*maʼlumot*). Mapping both to `'` loses that distinction. It does not matter for fertility, but the
choice should be deliberate.

## 6. Speed

200,000 chars / 500 merges → 8.8 s. For 15 MB of text (75×) and 16,000 merges (32×), pure Python would
take about 8.8 × 75 × 32 ≈ 21,000 s ≈ **6 hours**: every merge re-scans the whole list
(O(N × merges)).

Why real tokenizers (HF `tokenizers`, `tiktoken`) are fast:

1. **Algorithm:** they update pair counts only where a merge happened (incremental counts) instead of
   recounting everything, and they pre-split text into words so each repeated word is processed once.
2. **Language:** they are written in Rust.

## 7. Q&A

**Why does `merge([1, 1, 1], (1, 1), 99)` return `[99, 1]`?**
It scans left to right. Once the first two `1`s merge, the middle `1` is used up and cannot join the
next pair. Each element belongs to at most one pair. (`get_pair_counts` does count overlapping pairs:
`aaa` contains 2 × `aa`.)

**Why does `encode("xyz")` return `[120, 121, 122]`?**
There is no `x`, `y`, `z` merge in the training text. But any character is made of bytes, and all 256
bytes are always in the vocab. There are no unknown words — only "poorly known" ones.

**Why did the round-trip test pass on emoji?**
Emoji are bytes too. If no merge applies, each byte stays its own token and `decode` reassembles them.
The 🇺🇿 flag = 2 characters × 4 bytes = 8 tokens (verified: no merge covers these bytes).

## Next step

Step 5: apostrophe normalization + Hugging Face `tokenizers` on the full data with 8k / 16k / 32k
vocab → add to the Part 2 chart.
