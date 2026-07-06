#!/usr/bin/env python3
"""Validate strict UPC math-modeling fonts in WSL."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_WINDOWS_FONTS = [
    "simsun.ttc",
    "simhei.ttf",
    "simkai.ttf",
    "simfang.ttf",
    "times.ttf",
    "timesbd.ttf",
    "timesi.ttf",
    "timesbi.ttf",
]

REQUIRED_PDF_FAMILIES = {
    "SimSun": ("SimSun",),
    "SimHei": ("SimHei",),
    "KaiTi": ("KaiTi", "KaiTi_GB2312"),
    "FangSong": ("FangSong", "FangSong_GB2312"),
    "TimesNewRoman": ("TimesNewRoman", "TimesNewRomanPS"),
}


def check_font_files(font_dir: Path) -> list[str]:
    return [name for name in REQUIRED_WINDOWS_FONTS if not (font_dir / name).exists()]


def read_pdf_fonts(pdf_path: Path) -> str:
    if shutil.which("pdffonts") is None:
        raise RuntimeError("pdffonts is not available")
    result = subprocess.run(
        ["pdffonts", str(pdf_path)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def check_pdf_fonts(pdf_fonts_output: str) -> list[str]:
    missing = []
    for label, aliases in REQUIRED_PDF_FAMILIES.items():
        if not any(alias in pdf_fonts_output for alias in aliases):
            missing.append(label)
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-dir", default="/mnt/c/Windows/Fonts")
    parser.add_argument("--pdf", help="Compiled PDF to inspect with pdffonts")
    args = parser.parse_args()

    font_dir = Path(args.font_dir)
    missing_files = check_font_files(font_dir)
    if missing_files:
        print("Missing strict Windows font files:", file=sys.stderr)
        for name in missing_files:
            print(f"  {font_dir / name}", file=sys.stderr)
        return 2

    if args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            print(f"PDF not found: {pdf_path}", file=sys.stderr)
            return 2
        try:
            pdf_fonts = read_pdf_fonts(pdf_path)
        except Exception as exc:
            print(f"Could not inspect PDF fonts: {exc}", file=sys.stderr)
            return 2
        missing_pdf_families = check_pdf_fonts(pdf_fonts)
        if missing_pdf_families:
            print("PDF is missing strict template font families:", file=sys.stderr)
            for label in missing_pdf_families:
                print(f"  {label}", file=sys.stderr)
            print("\npdffonts output:\n" + pdf_fonts, file=sys.stderr)
            return 1

    print("Strict UPC font check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
