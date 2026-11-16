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
