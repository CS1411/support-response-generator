"""One test per milestone."""
"""One test per milestone."""
from app.core import build_corpus, clean_text, load_corpus, to_tokens
from app.sample_data import generate_raw


def test_milestone_1_corpus_is_anonymized_and_tokenized():
    assert clean_text("Mail me@x.com about order #12345 or 555-123-4567") == \
        "mail emailaddr about order orderid or phonenum"
    joined = " ".join(build_corpus(generate_raw(50)))
    assert not any(p in joined for p in ("@", "#1", "555-"))
    assert to_tokens("Order orderid, please!") == ["order", "orderid", "please"]
    assert len(load_corpus()) >= 100
from app.core import NgramModel



def test_milestone_2_smoothing_gives_unseen_words_probability():
    m = NgramModel(n=2, k=0.5).fit(["i drink coffee", "i drink tea"])
    ctx = ("drink",)
    assert m.prob(ctx, "coffee") > m.prob(ctx, "water") > 0
    assert abs(sum(m.prob(ctx, w) for w in m.vocab) - 1) < 1e-9
    assert m.perplexity(["i drink coffee"]) < m.perplexity(["coffee drink i"])
from app.core import continue_text, suggest_next



def test_milestone_3_suggestions_and_continuation():
    m = NgramModel(n=2, k=0.1).fit(["i drink coffee", "i drink coffee", "i drink tea"])
    top = suggest_next(m, "i drink", top_k=2)
    assert [w for w, _ in top] == ["coffee", "tea"] and top[0][1] > top[1][1]
    assert suggest_next(m, "zzz unknown") == []
    assert continue_text(m, "i drink") == "i drink coffee"


def test_milestone_4_cli_suggest(capsys):
    from app.cli import main
    main(["suggest", "your", "refund", "-k", "2"])
    out = capsys.readouterr().out
    assert "next words:" in out and "draft" in out
