"""Entry point — run with: python -m newsfeed"""

import sys


def main() -> None:
    # Ensure the terminal supports colours before importing curses UI
    try:
        from .ui import launch
    except ImportError as exc:
        print(f"Error importing UI: {exc}", file=sys.stderr)
        sys.exit(1)

    launch()


if __name__ == "__main__":
    main()
