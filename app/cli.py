"""Command-line entry point: `python -m app.cli --help`."""
import argparse

from app.core import NgramModel, continue_text, load_corpus, suggest_next


def show(model: NgramModel, prefix: str, top_k: int) -> None:
    suggestions = suggest_next(model, prefix, top_k)
    if not suggestions:
        print("no suggestions")
        return
    print("next words:", ", ".join(f"{w} ({p:.2f})" for w, p in suggestions))
    print("draft     :", continue_text(model, prefix))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="support-response-generator", description="Customer support agents use this CLI tool to quickly draft responses to common queries by generating next-word suggestions based on a corpus of past support interactions.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("hello", help="check that everything is wired up")
    s = sub.add_parser("suggest", help="suggest next words for a partial reply")
    s.add_argument("prefix", nargs="*", help="partial reply; leave empty for interactive mode")
    s.add_argument("-k", "--top", type=int, default=3, help="how many suggestions to show")
    args = parser.parse_args(argv)
    if args.command == "hello":
        print("Support Response Generator is ready. Open README.md for your milestones.")
    elif args.command == "suggest":
        model = NgramModel(n=3, k=0.1).fit(load_corpus())
        if args.prefix:
            show(model, " ".join(args.prefix), args.top)
        else:
            while line := input("partial reply (blank to quit)> ").strip():
                show(model, line, args.top)


if __name__ == "__main__":
    main()
