# Support Response Generator

[![Built with askThili](https://ask.thili.ai/api/v1/public/projects/5vkucaq7p4/badge.svg)](https://ask.thili.ai/b/5vkucaq7p4)

This Support Response Generator is a CLI tool designed for retail customer support agents. It leverages a next-word prediction model, trained on past support interactions, to offer quick and relevant suggestions for drafting responses to common queries. The goal is to enhance agent efficiency and response consistency.

## What you are building

**Goal.** You will build a command-line interface (CLI) tool that helps customer support agents quickly draft responses by generating next-word suggestions.

**Done when.** The tool successfully processes a corpus of support interactions, implements an n-gram model with smoothing, generates relevant next-word suggestions, and provides a functional command-line interface for agents.

## Milestones

Tick these off as you go, and commit after each one.

- [x] **1. Prepare an anonymized corpus of customer support interactions.**  
      Hint: Focus on tokenization and cleaning the text for your corpus.
- [x] **2. Implement the n-gram model with smoothing.**  
      Hint: Use the n-gram model and smoothing techniques learned in the drill.
- [x] **3. Create a text generation function to suggest response continuations.**  
      Hint: Apply your n-gram model to predict the most probable next words.
- [x] **4. Build a command-line interface for agents to get suggestions.**  
      Hint: Design a simple CLI to input partial responses and display predictions.

## Run it

You need Python 3.12 and git.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then choose a model; see the comments inside
python -m app.cli hello
pytest
```

Your work goes in `app/core.py` (one stub per milestone) and `tests/test_core.py`. The first tests pass already; they
check the plumbing.

## Settings and secrets

Model settings live in `.env`, which is ignored by git. **Never commit `.env` or paste a key into code.** If a key ever
reaches GitHub, treat it as leaked and make a new one.

## Stretch ideas

- Allow the agent to specify the number of next-word suggestions to display.
- Implement a simple mechanism for the agent to select a suggested word to append it to the current response.
- Display the probability score alongside each suggested word.
