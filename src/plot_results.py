"""Grouped bar chart of fertility per tokenizer and language."""
import matplotlib.pyplot as plt

LANG_LABELS = {"en": "English", "uz_latn": "Uzbek (Latin)", "uz_cyrl": "Uzbek (Cyrillic)"}


def plot_fertility(results: dict, out_path: str = "results/fertility_chart.png") -> None:
    names = list(results.keys())
    langs = list(LANG_LABELS.keys())
    width = 0.8 / len(langs)

    fig, ax = plt.subplots(figsize=(9, 5))
    for i, lang in enumerate(langs):
        xs = [x + i * width for x in range(len(names))]
        ys = [results[n][lang] for n in names]
        bars = ax.bar(xs, ys, width, label=LANG_LABELS[lang])
        ax.bar_label(bars, fmt="%.2f", fontsize=8)

    ax.set_xticks([x + width for x in range(len(names))])
    ax.set_xticklabels(names)
    ax.set_ylabel("Fertility (tokens per word, lower is better)")
    ax.set_title("Tokenizer fertility: English vs Uzbek")
    ax.axhline(1.0, color="gray", linestyle="--", linewidth=0.8)
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    print(f"Saved chart -> {out_path}")