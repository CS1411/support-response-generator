# Support Response Generator

[![Built with askThili](https://ask.thili.ai/api/v1/public/projects/5vkucaq7p4/badge.svg)](https://ask.thili.ai/b/5vkucaq7p4)
[![tests](https://github.com/CS1411/support-response-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/CS1411/support-response-generator/actions/workflows/ci.yml)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue)
![Dependencies](https://img.shields.io/badge/runtime%20dependencies-none-brightgreen)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

A command-line tool that helps retail customer support agents draft replies faster. Type the start of a reply and it suggests the most likely next words, with probabilities, and drafts a continuation. It is powered by an n-gram language model written in pure Python (standard library only) and trained on past support replies.

```console
$ python -m app.cli suggest your refund
next words: for (0.80)
draft     : your refund for order orderid and it will ship within two business days
```

## Contents

- [Features](#features)
- [Quick start](#quick-start)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Results](#results)
- [Project structure](#project-structure)
- [Testing](#testing)
- [Data](#data)
- [Limitations](#limitations)
- [License](#license)

## Features

- **Next-word suggestions** with a probability score for each one.
- **Reply continuation**: extends a partial reply into a full draft.
- **Anonymized corpus**: emails, phone numbers and order ids are masked before the model sees them.
- **Smoothed trigram model**: unseen word pairs never get zero probability.
- **Adjustable output**: choose how many suggestions to show with `-k`.
- **Interactive mode** for working through several replies in a row.
- **No runtime dependencies**: nothing to install except the test runner.

## Quick start

Requires Python 3.12 and git.

```bash
git clone https://github.com/CS1411/support-response-generator.git
cd support-response-generator
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m app.cli hello
```

`requirements.txt` only contains the test runner (`pytest`). The tool itself uses the standard library.

## Usage

Suggest next words for a partial reply:

```bash
python -m app.cli suggest thanks for
python -m app.cli suggest i have checked order -k 5
```

Run with no reply to use interactive mode (press Enter on a blank line to quit):

```bash
python -m app.cli suggest
```

| Option | Meaning | Default |
|--------|---------|---------|
| `prefix` | The partial reply to complete | interactive mode |
| `-k`, `--top` | How many suggestions to show | 3 |

Sample runs are saved in [`docs/sample_output.txt`](docs/sample_output.txt).

## How it works

1. **Prepare the corpus.** Each reply is lowercased, personal details are replaced by placeholders (`emailaddr`, `phonenum`, `orderid`), and the text is split into sentences and word tokens. Sentence boundaries are marked with `<s>` and `</s>` so the model learns how replies start and end.
2. **Count n-grams.** For every pair of words, the model counts which word follows it (a trigram model, so the context is the previous two words).
3. **Smooth the probabilities.** With add-k smoothing, the probability of word `w` after a context is

   `P(w | context) = (count(context, w) + k) / (count(context) + k * |V|)`

   where `|V|` is the vocabulary size and `k = 0.1`. Word pairs never seen in training still get a small non-zero probability.
4. **Suggest and continue.** Suggestions are the words most often seen after the last two words typed (never the end-of-sentence marker). The draft repeatedly appends the most likely next word until nothing follows or 12 words are added.

## Results

Held-out perplexity on an 80/20 split of the corpus, from `python -m app.evaluate` (saved in [`docs/evaluation.txt`](docs/evaluation.txt)). Perplexity can be read as how many equally likely words the model is choosing between at each step, so lower is better.

| n-gram order | k = 1.0 | k = 0.1 | k = 0.01 |
|--------------|---------|---------|----------|
| 2 (bigram) | 4.52 | 2.58 | 2.34 |
| 3 (trigram) | 3.84 | 1.79 | **1.55** |

- Trigrams beat bigrams because two words of context pin down which template a reply follows.
- Small `k` beats add-1: with a vocabulary this size, add-1 hands too much probability to words that never follow the context.
- The app uses a trigram with `k = 0.1`, a more cautious setting than the best score above, to avoid over-trusting a small corpus.

More examples:

```console
$ python -m app.cli suggest thanks for
next words: contacting (0.49), your (0.45)
draft     : thanks for contacting us

$ python -m app.cli suggest please reply to
next words: emailaddr (0.79)
draft     : please reply to emailaddr so you can send the item back
```

## Project structure

```
app/
  core.py          corpus cleaning, n-gram model, suggestions
  sample_data.py   synthetic support replies with fake personal details
  evaluate.py      perplexity comparison of n and k
  cli.py           command-line interface
corpus/support.txt anonymized training corpus
docs/              saved example output and evaluation results
tests/             one test per milestone plus a CLI smoke test
.github/workflows/ci.yml   runs the tests on every push
```

## Testing

```bash
pytest
```

The tests cover anonymization and tokenization, the smoothing maths (probabilities sum to 1, unseen words get non-zero probability), suggestions and continuation, the CLI, and the evaluation result. They run automatically on GitHub for every push.

## Data

The corpus is **synthetic**. `app/sample_data.py` generates 400 templated support replies containing fake emails, phone numbers and order ids, and `app/core.py` anonymizes them into `corpus/support.txt`. No real customer data is used. To use real replies, put one reply per line in `corpus/support.txt` after anonymizing them with `clean_text`.

## Limitations

- The corpus is small and highly repetitive (every reply is built from 6 openers, 10 bodies and 5 closers), so the perplexity numbers are optimistic. Real support text is far more varied and would score much higher.
- A trigram only remembers two words, so a long continuation can jump between templates and stop making sense. The "your refund" draft above is an example: it drifts into shipping.
- A word never seen in training is never suggested. Smoothing only changes the probabilities of known words.
- Suggestions are not checked for correctness. An agent must read a draft before sending it.
- Not built: picking a suggestion to append it to the reply automatically.

## License

MIT. See [LICENSE](LICENSE).
