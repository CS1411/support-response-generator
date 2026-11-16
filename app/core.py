"""Core logic: corpus preparation, n-gram model with smoothing, suggestions."""
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_PATH = Path(__file__).resolve().parent.parent / "corpus" / "support.txt"


# --- Milestone 1: prepare an anonymized corpus of support interactions.
def clean_text(text: str) -> str:
    """Mask personal details, lowercase, and collapse whitespace."""
    text = re.sub(r"\S+@\S+", "emailaddr", text)
    text = re.sub(r"\b\d{3}-\d{3}-\d{4}\b", "phonenum", text)
    text = re.sub(r"#\d+", "orderid", text)
    return re.sub(r"[ \t]+", " ", text).strip().lower()


def to_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"[.!?\n]+", text) if s.strip()]


def to_tokens(sentence: str) -> list[str]:
    return re.findall(r"[a-z']+", sentence.lower())


def build_corpus(raw_lines: list[str]) -> list[str]:
    """Anonymize raw support replies and return one cleaned reply per line."""
    return [clean_text(line) for line in raw_lines if line.strip()]


def load_corpus(path: Path = CORPUS_PATH) -> list[str]:
    return [line for line in path.read_text().splitlines() if line.strip()]


# --- Milestone 2: n-gram model with add-k smoothing.
class NgramModel:
    """Counts n-grams and gives smoothed next-word probabilities."""

    def __init__(self, n: int = 3, k: float = 0.1):
        self.n, self.k = n, k
        self.counts: dict[tuple, Counter] = defaultdict(Counter)
        self.vocab: set[str] = {"</s>"}

    def _padded(self, sentence: str) -> list[str]:
        return ["<s>"] * (self.n - 1) + to_tokens(sentence) + ["</s>"]

    def fit(self, lines: list[str]) -> "NgramModel":
        for line in lines:
            for sent in to_sentences(line):
                toks = self._padded(sent)
                self.vocab.update(toks[self.n - 1:])
                for i in range(len(toks) - self.n + 1):
                    self.counts[tuple(toks[i:i + self.n - 1])][toks[i + self.n - 1]] += 1
        return self

    def prob(self, context: tuple, word: str) -> float:
        c = self.counts.get(context, Counter())
        return (c[word] + self.k) / (sum(c.values()) + self.k * len(self.vocab))

    def perplexity(self, lines: list[str]) -> float:
        log_sum, total = 0.0, 0
        for line in lines:
            for sent in to_sentences(line):
                toks = self._padded(sent)
                for i in range(len(toks) - self.n + 1):
                    ctx, w = tuple(toks[i:i + self.n - 1]), toks[i + self.n - 1]
                    log_sum += math.log(self.prob(ctx, w))
                    total += 1
        return math.exp(-log_sum / total)


# --- Milestone 3: suggest next words and continue a partial response.
def _context(model: NgramModel, prefix: str) -> tuple:
    toks = ["<s>"] * (model.n - 1) + to_tokens(prefix)
    return tuple(toks[-(model.n - 1):]) if model.n > 1 else ()


def suggest_next(model: NgramModel, prefix: str, top_k: int = 3) -> list[tuple[str, float]]:
    """Most likely next words after `prefix`, as (word, probability). Never suggests end-of-sentence."""
    ctx = _context(model, prefix)
    seen = model.counts.get(ctx, Counter())
    words = [w for w, _ in seen.most_common() if w != "</s>"][:top_k]
    return [(w, model.prob(ctx, w)) for w in words]


def continue_text(model: NgramModel, prefix: str, max_words: int = 12) -> str:
    """Greedily extend `prefix` one most-likely word at a time."""
    text = prefix.lower().strip()
    for _ in range(max_words):
        best = suggest_next(model, text, top_k=1)
        if not best:
            break
        text = f"{text} {best[0][0]}".strip()
    return text
