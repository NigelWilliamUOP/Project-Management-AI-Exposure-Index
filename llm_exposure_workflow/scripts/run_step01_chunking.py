from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(r"C:\Users\mrnig\Documents\codex\AI and Project Management jobs")
WORKFLOW = ROOT / "llm_exposure_workflow"
MANIFEST_PATH = WORKFLOW / "chunking_manifest.json"


LICENSE_PATTERNS = [
    re.compile(r"PMI Member benefit licensed to: Nigel Williams - 555889\..*", re.IGNORECASE),
    re.compile(r"Licensed To: Nigel Williams PMI MemberID: 555889.*", re.IGNORECASE),
    re.compile(r"This copy is a PMI Member benefit, not for distribution, sale, or reproduction\.", re.IGNORECASE),
    re.compile(r"Not for distribution, sale, or reproduction\.", re.IGNORECASE),
]


@dataclass
class Chunk:
    chunk_id: str
    source_id: str
    standard_source: str
    document_type: str
    display_title: str
    page_start: int
    page_end: int
    word_count: int
    text: str
    coverage_hints: list[str]


def load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_page_text(text: str) -> str:
    text = text.replace("\x00", "")
    for pattern in LICENSE_PATTERNS:
        text = pattern.sub("", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def page_rows_for_source(source: dict, manifest: dict) -> list[dict]:
    pdf_path = ROOT / source["relative_path"]
    reader = PdfReader(str(pdf_path))
    rows = []
    page_start = source["page_range"]["start"]
    page_end = min(source["page_range"]["end"], len(reader.pages))
    marker_template = manifest["defaults"]["page_marker_format"]
    for page_number in range(page_start, page_end + 1):
        raw_text = reader.pages[page_number - 1].extract_text() or ""
        clean_text = normalize_page_text(raw_text)
        rows.append(
            {
                "source_id": source["source_id"],
                "standard_source": source["source_id"],
                "document_type": source["document_type"],
                "display_title": source["display_title"],
                "page_number": page_number,
                "text": f"{marker_template.format(page_number=page_number)}\n{clean_text}".strip(),
                "char_count": len(clean_text),
                "word_count": len(clean_text.split()),
            }
        )
    return rows


def split_paragraphs(page_rows: list[dict]) -> list[tuple[int, str]]:
    paragraphs: list[tuple[int, str]] = []
    for row in page_rows:
        page_number = row["page_number"]
        chunks = [part.strip() for part in re.split(r"\n\s*\n", row["text"]) if part.strip()]
        for chunk in chunks:
            paragraphs.append((page_number, chunk))
    return paragraphs


def build_chunks_for_source(source: dict, manifest: dict, page_rows: list[dict]) -> list[Chunk]:
    settings = manifest["defaults"]["chunking"]
    target_words = settings["target_words"]
    min_words = settings["min_words"]
    max_words = settings["max_words"]
    overlap_words = settings["overlap_words"]

    paragraphs = split_paragraphs(page_rows)
    chunks: list[Chunk] = []
    buffer_parts: list[str] = []
    buffer_pages: list[int] = []
    chunk_ordinal = 1

    def flush_buffer() -> None:
        nonlocal buffer_parts, buffer_pages, chunk_ordinal
        if not buffer_parts:
            return
        text = "\n\n".join(buffer_parts).strip()
        words = text.split()
        if len(words) < min_words and chunks:
            # Merge undersized tail into prior chunk.
            prior = chunks[-1]
            merged_text = f"{prior.text}\n\n{text}".strip()
            chunks[-1] = Chunk(
                chunk_id=prior.chunk_id,
                source_id=prior.source_id,
                standard_source=prior.standard_source,
                document_type=prior.document_type,
                display_title=prior.display_title,
                page_start=prior.page_start,
                page_end=max(prior.page_end, max(buffer_pages)),
                word_count=len(merged_text.split()),
                text=merged_text,
                coverage_hints=prior.coverage_hints,
            )
        else:
            page_start = min(buffer_pages)
            page_end = max(buffer_pages)
            chunk_id = manifest["defaults"]["chunking"]["chunk_id_pattern"].format(
                chunk_id_prefix=source["chunk_id_prefix"],
                page_start=page_start,
                chunk_ordinal=chunk_ordinal,
            )
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    source_id=source["source_id"],
                    standard_source=source["source_id"],
                    document_type=source["document_type"],
                    display_title=source["display_title"],
                    page_start=page_start,
                    page_end=page_end,
                    word_count=len(words),
                    text=text,
                    coverage_hints=source["coverage_hints"],
                )
            )
            chunk_ordinal += 1
        if overlap_words > 0 and buffer_parts:
            words = text.split()
            overlap = " ".join(words[-overlap_words:]).strip()
            if overlap:
                buffer_parts = [overlap]
                buffer_pages = [max(buffer_pages)]
            else:
                buffer_parts = []
                buffer_pages = []
        else:
            buffer_parts = []
            buffer_pages = []

    for page_number, paragraph in paragraphs:
        candidate_text = "\n\n".join(buffer_parts + [paragraph]).strip()
        candidate_words = len(candidate_text.split())
        if buffer_parts and candidate_words > max_words:
            flush_buffer()
        buffer_parts.append(paragraph)
        buffer_pages.append(page_number)
        if len(" ".join(buffer_parts).split()) >= target_words:
            flush_buffer()

    flush_buffer()
    return chunks


def main() -> None:
    manifest = load_manifest()
    merged_chunks: list[dict] = []
    raw_dir = ROOT / manifest["output_targets"]["raw_pages_dir"]
    chunk_dir = ROOT / manifest["output_targets"]["source_chunks_dir"]
    raw_dir.mkdir(parents=True, exist_ok=True)
    chunk_dir.mkdir(parents=True, exist_ok=True)

    duplicates = {row["relative_path"] for row in manifest.get("duplicates", []) if row.get("action") == "skip"}

    for source in sorted(manifest["sources"], key=lambda item: item["ingest_order"]):
        if not source.get("enabled", True):
            continue
        if source["relative_path"] in duplicates:
            continue
        page_rows = page_rows_for_source(source, manifest)
        write_jsonl(ROOT / source["output_files"]["raw_pages_file"], page_rows)

        chunks = build_chunks_for_source(source, manifest, page_rows)
        source_chunk_rows = [
            {
                "chunk_id": chunk.chunk_id,
                "source_id": chunk.source_id,
                "standard_source": chunk.standard_source,
                "document_type": chunk.document_type,
                "display_title": chunk.display_title,
                "page_start": chunk.page_start,
                "page_end": chunk.page_end,
                "word_count": chunk.word_count,
                "coverage_hints": chunk.coverage_hints,
                "text": chunk.text,
            }
            for chunk in chunks
        ]
        write_jsonl(ROOT / source["output_files"]["source_chunks_file"], source_chunk_rows)
        merged_chunks.extend(source_chunk_rows)

    merged_chunks.sort(key=lambda row: (row["source_id"], row["page_start"], row["chunk_id"]))
    write_jsonl(ROOT / manifest["output_targets"]["merged_chunk_file"], merged_chunks)

    summary = {
        "source_count": len([s for s in manifest["sources"] if s.get("enabled", True)]),
        "duplicate_skip_count": len(duplicates),
        "merged_chunk_count": len(merged_chunks),
    }
    (WORKFLOW / "output" / "step1_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
