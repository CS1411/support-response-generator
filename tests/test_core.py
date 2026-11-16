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
