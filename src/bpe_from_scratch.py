"""Part 3a — Minimal byte-level BPE in pure Python."""
import json
import time
from pathlib import Path

DATA_PATH = Path("data/uz_wiki.txt")
TEST_PATH = Path("data/test_sentences.json")
TRAIN_CHARS = 200_000   # start small: pure Python is slow (then try 200_000)
NUM_MERGES = 500      # then try 500


def get_pair_counts(ids: list[int]) -> dict[tuple[int, int], int]:
    """Count how often each adjacent pair of ids appears."""
    pair_counts = {}
    for i in range(len(ids) - 1):
        pair = (ids[i], ids[i + 1])
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    return pair_counts


def merge(ids: list[int], pair: tuple[int, int], new_id: int) -> list[int]:
    """Replace every occurrence of `pair` in `ids` with `new_id`."""
    new_ids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and (ids[i], ids[i + 1]) == pair:
            new_ids.append(new_id)
            i += 2  # skip the next id since it's part of the merged pair
        else:
            new_ids.append(ids[i])
            i += 1
    return new_ids


class BPETokenizer:
    def __init__(self):
        self.merges = {}   # {(id1, id2): new_id}
        self.vocab = {}    # {id: bytes}

    def train(self, text: str, num_merges: int, verbose: bool = False) -> None:
        ids = list(text.encode("utf-8"))
        self.vocab = {i: bytes([i]) for i in range(256)}

        for i in range(num_merges):
            counts = get_pair_counts(ids)
            if not counts:
                break
            pair = max(counts, key=counts.get)
            new_id = 256 + i
            ids = merge(ids, pair, new_id)
            self.merges[pair] = new_id
            self.vocab[new_id] = self.vocab[pair[0]] + self.vocab[pair[1]]

            if verbose:
                piece = self.vocab[new_id].decode("utf-8", errors="replace")
                print(f"merge {i + 1}: {pair} -> {new_id} {piece!r} (count={counts[pair]})")

    def encode(self, text: str) -> list[int]:
        ids = list(text.encode("utf-8"))
        while len(ids) >= 2:
            counts = get_pair_counts(ids)
            pair = min(counts, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break
            ids = merge(ids, pair, self.merges[pair])
        return ids

    def decode(self, ids: list[int]) -> str:
        raw = b"".join(self.vocab[token_id] for token_id in ids)
        return raw.decode("utf-8", errors="replace")


def print_merges(tok: BPETokenizer, items: list) -> None:
    for _pair, new_id in items:
        piece = tok.vocab[new_id].decode("utf-8", errors="replace")
        print(f"  {new_id}: {piece!r}")


def main():
    # 1. Read training text
    text = DATA_PATH.read_text(encoding="utf-8")[:TRAIN_CHARS]
    print(f"Training on {len(text):,} chars, {NUM_MERGES} merges")

    # 2. Train and measure time
    tok = BPETokenizer()
    start = time.perf_counter()
    tok.train(text, NUM_MERGES)
    elapsed = time.perf_counter() - start
    print(f"Trained in {elapsed:.1f}s, vocab size = {len(tok.vocab)}")

    # 3. First 30 merges: the most frequent pieces
    merges = list(tok.merges.items())
    print("\nFirst 30 merges:")
    print_merges(tok, merges[:30])

    # 4. Last 20 merges: longer pieces
    print("\nLast 20 merges:")
    print_merges(tok, merges[-20:])

    # 5. Round-trip test
    samples = ["Salom dunyo!", "Сунъий интеллект", "O'zbekiston 🇺🇿", text[:500]]
    for sample in samples:
        assert tok.decode(tok.encode(sample)) == sample, sample
    print("\nRound-trip OK")

    # 6. Fertility on the test sentences
    sentences = json.loads(TEST_PATH.read_text(encoding="utf-8"))
    for lang in ["en", "uz_latn", "uz_cyrl"]:
        texts = [s[lang] for s in sentences]
        tokens = sum(len(tok.encode(t)) for t in texts)
        words = sum(len(t.split()) for t in texts)
        print(f"Fertility ({lang:7}): {tokens / words:.2f}")
    print("(gpt2 for comparison: en 1.22, uz_latn 3.34, uz_cyrl 8.33)")


if __name__ == "__main__":
    main()