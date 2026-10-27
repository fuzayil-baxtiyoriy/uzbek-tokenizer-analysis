from pathlib import Path

from datasets import load_dataset

TARGET_MB = 15
OUT_PATH = Path("data/uz_wiki.txt")


def main():
    ds = load_dataset("wikimedia/wikipedia", "20231101.uz",
                      split="train", streaming=True)

    target_bytes = TARGET_MB * 1024 * 1024
    written = 0
    articles = 0

    with OUT_PATH.open("w", encoding="utf-8") as f:
        for row in ds:
            text = row["text"].strip()
            if len(text) < 200:  # skip short stub articles
                continue
            f.write(text + "\n\n")
            written += len(text.encode("utf-8"))
            articles += 1
            if written >= target_bytes:
                break

    print(f"Saved {articles} articles, {written / 1024 / 1024:.1f} MB -> {OUT_PATH}")


if __name__ == "__main__":
    main()