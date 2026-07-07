#!/usr/bin/env python3
"""Convert CS661 lecture PDFs to Markdown with per-page PNG renders."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "markdown_files" / "lecture pdf"
OUT_DIR = ROOT / "docs" / "lectures"
ASSETS_DIR = OUT_DIR / "assets"
DPI = 150
SKIP_PATTERNS = ("after_mid", "after_midesem")
ZOOM = DPI / 72.0


def lecture_stem(pdf_path: Path) -> str:
    return pdf_path.stem


def lecture_title(stem: str) -> str:
    base = re.sub(
        r"_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        "",
        stem,
        flags=re.IGNORECASE,
    )
    base = base.replace("_", " ")
    base = re.sub(r"\bpart\s+(\d+)\b", r"(Part \1)", base, flags=re.IGNORECASE)
    return base.strip()


def should_skip(pdf_path: Path) -> bool:
    name_lower = pdf_path.name.lower()
    return any(pattern in name_lower for pattern in SKIP_PATTERNS)


def render_pages(doc: fitz.Document, assets_path: Path) -> list[Path]:
    assets_path.mkdir(parents=True, exist_ok=True)
    matrix = fitz.Matrix(ZOOM, ZOOM)
    rendered: list[Path] = []
    for page_index in range(len(doc)):
        page_num = page_index + 1
        out_file = assets_path / f"page_{page_num:03d}.png"
        pix = doc[page_index].get_pixmap(matrix=matrix, alpha=False)
        pix.save(str(out_file))
        rendered.append(out_file)
    return rendered


def extract_embedded_images(doc: fitz.Document, assets_path: Path) -> list[tuple[str, Path]]:
    """Extract embedded raster images not already covered by page renders."""
    assets_path.mkdir(parents=True, exist_ok=True)
    seen_xrefs: set[int] = set()
    extracted: list[tuple[str, Path]] = []
    counter = 0

    for page_index in range(len(doc)):
        page = doc[page_index]
        for image_info in page.get_images(full=True):
            xref = image_info[0]
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)
            try:
                base_image = doc.extract_image(xref)
            except Exception:
                continue
            if not base_image:
                continue
            width = base_image.get("width", 0)
            height = base_image.get("height", 0)
            # Skip tiny icons/decorative assets; page renders cover slide content.
            if width < 80 or height < 80:
                continue
            ext = base_image.get("ext", "png")
            if ext == "jpeg":
                ext = "jpg"
            counter += 1
            label = f"embedded_{counter:03d}"
            out_file = assets_path / f"{label}.{ext}"
            out_file.write_bytes(base_image["image"])
            extracted.append((label, out_file))

    return extracted


def extract_page_text(doc: fitz.Document) -> list[str]:
    pages: list[str] = []
    for page_index in range(len(doc)):
        text = doc[page_index].get_text("text").strip()
        pages.append(text)
    return pages


def relative_asset_path(md_path: Path, asset_path: Path) -> str:
    return asset_path.relative_to(md_path.parent).as_posix()


def build_markdown(
    *,
    title: str,
    source_pdf: Path,
    page_texts: list[str],
    page_images: list[Path],
    embedded_images: list[tuple[str, Path]],
    md_path: Path,
) -> str:
    today = date.today().isoformat()
    rel_source = source_pdf.relative_to(ROOT).as_posix()

    lines: list[str] = [
        "---",
        f"title: \"{title}\"",
        f"source_pdf: \"{rel_source}\"",
        f"converted: {today}",
        f"pages: {len(page_images)}",
        "---",
        "",
        f"# {title}",
        "",
        f"**Source:** `{rel_source}`  ",
        f"**Converted:** {today}  ",
        f"**Pages:** {len(page_images)}",
        "",
        "## Lecture Text",
        "",
    ]

    for idx, text in enumerate(page_texts, start=1):
        lines.append(f"<!-- Page {idx} -->")
        lines.append(text if text else f"*(Page {idx}: no extractable text)*")
        lines.append("")

    lines.extend(["## Figures", ""])
    for idx, image_path in enumerate(page_images, start=1):
        rel = relative_asset_path(md_path, image_path)
        lines.append(f"### Page {idx}")
        lines.append("")
        lines.append(f"![Page {idx}]({rel})")
        lines.append("")

    if embedded_images:
        lines.extend(["## Embedded Images", ""])
        for label, image_path in embedded_images:
            rel = relative_asset_path(md_path, image_path)
            lines.append(f"### {label}")
            lines.append("")
            lines.append(f"![{label}]({rel})")
            lines.append("")

    lines.extend(
        [
            "## Table of Figures",
            "",
            "| Figure | Asset | Description |",
            "|--------|-------|-------------|",
        ]
    )
    for idx, image_path in enumerate(page_images, start=1):
        rel = relative_asset_path(md_path, image_path)
        snippet = (page_texts[idx - 1].splitlines()[0][:80] if page_texts[idx - 1] else "").replace("|", "\\|")
        lines.append(f"| Page {idx} | `{rel}` | {snippet or 'Slide image'} |")

    for label, image_path in embedded_images:
        rel = relative_asset_path(md_path, image_path)
        lines.append(f"| {label} | `{rel}` | Embedded raster image |")

    lines.append("")
    return "\n".join(lines)


def convert_pdf(pdf_path: Path) -> dict:
    stem = lecture_stem(pdf_path)
    title = lecture_title(stem)
    md_path = OUT_DIR / f"{stem}.md"
    assets_path = ASSETS_DIR / stem

    doc = fitz.open(pdf_path)
    try:
        page_images = render_pages(doc, assets_path)
        embedded_images = extract_embedded_images(doc, assets_path)
        page_texts = extract_page_text(doc)
        markdown = build_markdown(
            title=title,
            source_pdf=pdf_path,
            page_texts=page_texts,
            page_images=page_images,
            embedded_images=embedded_images,
            md_path=md_path,
        )
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        md_path.write_text(markdown, encoding="utf-8")
        return {
            "pdf": pdf_path.name,
            "md": str(md_path.relative_to(ROOT)),
            "pages": len(page_images),
            "embedded": len(embedded_images),
            "assets_dir": str(assets_path.relative_to(ROOT)),
            "status": "ok",
        }
    finally:
        doc.close()


def write_index(results: list[dict]) -> None:
    lines = [
        "# CS661 Lecture Markdown Index",
        "",
        "Image-rich Markdown conversions of CS661 lecture slide decks.",
        "Each file includes extracted text plus per-page PNG renders for full visual context.",
        "",
        f"**Last converted:** {date.today().isoformat()}",
        "",
        "## Lectures",
        "",
        "| Lecture | Pages | Embedded | Markdown |",
        "|---------|-------|----------|----------|",
    ]
    for row in sorted(results, key=lambda r: r["pdf"].lower()):
        if row["status"] != "ok":
            continue
        md_name = Path(row["md"]).name
        lines.append(
            f"| {lecture_title(lecture_stem(Path(row['pdf'])))} | {row['pages']} | {row['embedded']} | [{md_name}]({md_name}) |"
        )
    lines.extend(
        [
            "",
            "## Skipped",
            "",
            "- `cs661_after_midesem.pdf` (post-midsem compilation; excluded by project policy)",
            "",
            "## Asset Layout",
            "",
            "```",
            "docs/lectures/",
            "  LectureN_....md",
            "  assets/",
            "    LectureN_.../",
            "      page_001.png",
            "      page_002.png",
            "      ...",
            "```",
            "",
        ]
    )
    (OUT_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not PDF_DIR.is_dir():
        print(f"PDF directory not found: {PDF_DIR}", file=sys.stderr)
        return 1

    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    results: list[dict] = []
    failures: list[str] = []

    for pdf_path in pdfs:
        if should_skip(pdf_path):
            print(f"SKIP: {pdf_path.name}")
            continue
        print(f"Converting: {pdf_path.name} ...", flush=True)
        try:
            result = convert_pdf(pdf_path)
            results.append(result)
            print(
                f"  -> {result['pages']} pages, {result['embedded']} embedded, {result['md']}"
            )
        except Exception as exc:
            failures.append(f"{pdf_path.name}: {exc}")
            print(f"  FAIL: {exc}", file=sys.stderr)

    write_index(results)

    print("\n=== Summary ===")
    print(f"Processed: {len(results)}")
    print(f"Failures: {len(failures)}")
    print(f"Total page images: {sum(r['pages'] for r in results)}")
    print(f"Total embedded images: {sum(r['embedded'] for r in results)}")
    print(f"Output: {OUT_DIR}")
    if failures:
        print("\nFailures:")
        for item in failures:
            print(f"  - {item}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
