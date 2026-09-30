"""Gabungkan paket data dengan pemeriksaan ID duplikat."""
import argparse
import json
from pathlib import Path
from app_support import ROOT, combine_opportunities


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "opportunities.json")
    args = parser.parse_args()
    payload = combine_opportunities(args.files)
    if args.output.resolve() in {p.resolve() for p in args.files}:
        parser.error("Output tidak boleh menimpa file sumber.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Tersimpan {len(payload['opportunities'])} opportunity: {args.output}")


if __name__ == "__main__":
    main()
