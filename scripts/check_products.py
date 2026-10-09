"""
Verify that every cost breakdown reconciles.

The shop page tells customers that the figures add up to the price and that the
VAT line is the real rate. That is a promise, and a promise nobody checks is
just a nice sentence — so this checks it, and `make check` runs it.

Two things are verified per product:

  1. The breakdown lines sum to the price, to the cent.
  2. Any line labelled VAT matches the configured rate, computed from the GROSS
     price: vat = gross * rate / (100 + rate). Not gross * rate/100 — that is
     the classic error, and it overstates the tax by about a fifth.

Exits non-zero on any mismatch, so a wrong figure fails the build rather than
quietly misleading someone.

Run:  python3 scripts/check_products.py   (or: make check)
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOLERANCE = 0.005  # half a cent


def load_yaml(path):
    try:
        import yaml
    except ImportError:
        sys.exit("pyyaml is needed: pip install -r scripts/requirements.txt")
    return yaml.safe_load(path.read_text())


def vat_rate():
    config = load_yaml(ROOT / "_config.yml")
    return float((config.get("shop") or {}).get("vat_rate", 0))


def main():
    products = load_yaml(ROOT / "_data" / "products.yml") or []
    rate = vat_rate()
    problems = []

    for item in products:
        name = item.get("name", "<unnamed>")
        lines = item.get("breakdown")
        if not lines:
            print(f"  skip   {name} (no breakdown)")
            continue

        price = float(item["price"])
        total = sum(float(line["amount"]) for line in lines)
        if abs(total - price) > TOLERANCE:
            problems.append(
                f"{name}: breakdown sums to {total:.2f} but price is {price:.2f} "
                f"(out by {total - price:+.2f})"
            )

        for line in lines:
            if not re.search(r"\bvat\b", str(line.get("label", "")), re.I):
                continue
            expected = price * rate / (100 + rate)
            actual = float(line["amount"])
            if abs(actual - expected) > TOLERANCE + 0.01:
                problems.append(
                    f"{name}: VAT line is {actual:.2f}, but {rate:g}% of a "
                    f"{price:.2f} gross price is {expected:.2f}"
                )

        print(f"  ok     {name}  ({len(lines)} lines, {total:.2f})")

    if problems:
        print("\nFAILED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)

    print(f"\nAll {len(products)} products reconcile, VAT at {rate:g}%.")


if __name__ == "__main__":
    main()
