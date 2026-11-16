"""Compare n-gram order and smoothing on held-out replies: `python -m app.evaluate`."""
from app.core import NgramModel, load_corpus


def evaluate(split: float = 0.8) -> list[tuple[int, float, float]]:
    """Return (n, k, held-out perplexity) for every combination. Lower perplexity is better."""
    lines = load_corpus()
    cut = int(split * len(lines))
    train, test = lines[:cut], lines[cut:]
    return [(n, k, NgramModel(n, k).fit(train).perplexity(test)) for n in (2, 3) for k in (1.0, 0.1, 0.01)]


if __name__ == "__main__":
    print("held-out perplexity (80/20 split of the corpus, lower is better)")
    for n, k, pp in evaluate():
        print(f"n={n} k={k:<5} {pp:6.2f}")
