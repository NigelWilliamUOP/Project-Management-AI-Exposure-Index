from __future__ import annotations

import argparse
import csv
import io
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import requests


REQUEST_TIMEOUT = 30


def clean_str(value: object) -> str:
    return "" if value is None else str(value).strip()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def normalize_text(value: object) -> str:
    text = clean_str(value).casefold()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_header(value: object) -> str:
    text = normalize_text(value)
    return re.sub(r"[^a-z0-9]+", "", text)


def build_parser() -> argparse.ArgumentParser:
    script_path = Path(__file__).resolve()
    dashboard_dir = script_path.parent.parent
    input_dir = dashboard_dir / "input"
    output_dir = dashboard_dir / "output"
    parser = argparse.ArgumentParser(
        description="Fetch benchmark results into dashboard/input/benchmark_results.csv with alias resolution and manual fallback.",
    )
    parser.add_argument("--snapshot-month", required=True, help="Snapshot month in YYYY-MM format.")
    parser.add_argument(
        "--fetch-registry",
        default=str(dashboard_dir / "benchmark_fetch_registry.json"),
        help="Path to benchmark fetch registry JSON.",
    )
    parser.add_argument(
        "--model-aliases",
        default=str(input_dir / "model_aliases.csv"),
        help="Path to model alias CSV.",
    )
    parser.add_argument(
        "--manual-results",
        default=str(input_dir / "manual_benchmark_results.csv"),
        help="Path to manual benchmark result CSV.",
    )
    parser.add_argument(
        "--output-benchmark-results",
        default=str(input_dir / "benchmark_results.csv"),
        help="Path to resolved benchmark results CSV for the dashboard runner.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional output directory for fetch logs. Defaults to dashboard/output/fetch/<snapshot-month>/.",
    )
    return parser


def validate_snapshot_month(snapshot_month: str) -> None:
    try:
        datetime.strptime(snapshot_month, "%Y-%m")
    except ValueError as exc:
        raise ValueError(f"snapshot_month must be YYYY-MM, got {snapshot_month}") from exc


def requests_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "pm-agentic-ai-dashboard-fetcher/1.0 (+research pipeline)",
            "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        }
    )
    return session


def load_aliases(path: Path) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for raw in read_csv_rows(path):
        alias_text = clean_str(raw.get("alias_text"))
        model_id = clean_str(raw.get("model_id"))
        if not alias_text or not model_id:
            continue
        benchmark_id = clean_str(raw.get("benchmark_id")) or "*"
        match_type = clean_str(raw.get("match_type")) or "exact"
        priority = int(clean_str(raw.get("priority")) or "100")
        grouped[benchmark_id].append(
            {
                "benchmark_id": benchmark_id,
                "model_id": model_id,
                "match_type": match_type,
                "alias_text": alias_text,
                "priority": priority,
                "notes": clean_str(raw.get("notes")),
            }
        )
    for benchmark_id in grouped:
        grouped[benchmark_id].sort(key=lambda row: (row["priority"], row["model_id"], row["alias_text"]))
    return grouped


def load_manual_rows(path: Path, snapshot_month: str) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for raw in read_csv_rows(path):
        row_snapshot_month = clean_str(raw.get("snapshot_month")) or snapshot_month
        if row_snapshot_month != snapshot_month:
            continue
        benchmark_id = clean_str(raw.get("benchmark_id"))
        if not benchmark_id:
            continue
        grouped[benchmark_id].append(raw)
    return grouped


def flatten_record(value: Any, prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    if isinstance(value, dict):
        for key, child in value.items():
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            out.update(flatten_record(child, next_prefix))
    elif isinstance(value, list):
        out[prefix] = value
    else:
        out[prefix] = value
    return out


def find_value_by_candidates(record: dict[str, Any], candidates: list[str]) -> Any:
    normalized_map = {normalize_header(key): value for key, value in record.items()}
    for candidate in candidates:
        value = normalized_map.get(normalize_header(candidate))
        if value not in (None, ""):
            return value
    for candidate in candidates:
        cand = normalize_header(candidate)
        for key, value in normalized_map.items():
            if cand and (key.endswith(cand) or cand in key):
                if value not in (None, ""):
                    return value
    return None


def parse_numeric_score(value: object, *, score_multiplier: float = 1.0) -> float:
    if isinstance(value, (int, float)):
        return round(float(value) * score_multiplier, 4)
    text = clean_str(value)
    if not text:
        raise ValueError("Missing score value")
    text = text.replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        raise ValueError(f"Could not parse numeric score from {text!r}")
    return round(float(match.group(0)) * score_multiplier, 4)


def match_alias(source_model_name: str, benchmark_id: str, alias_lookup: dict[str, list[dict]]) -> tuple[str | None, str | None]:
    source_norm = normalize_text(source_model_name)
    candidates = alias_lookup.get(benchmark_id, []) + alias_lookup.get("*", [])
    matched_model_ids = []
    for alias in candidates:
        alias_text = clean_str(alias["alias_text"])
        alias_norm = normalize_text(alias_text)
        match_type = alias["match_type"]
        matched = False
        if match_type == "exact":
            matched = source_norm == alias_norm
        elif match_type == "contains":
            matched = alias_norm in source_norm
        elif match_type == "regex":
            matched = re.search(alias_text, source_model_name, flags=re.IGNORECASE) is not None
        else:
            raise ValueError(f"Unsupported match_type: {match_type}")
        if matched:
            matched_model_ids.append(alias["model_id"])
    unique = sorted(set(matched_model_ids))
    if not unique:
        return None, "no_alias_match"
    if len(unique) > 1:
        return None, f"ambiguous_alias_match:{'|'.join(unique)}"
    return unique[0], None


def get_html(session: requests.Session, url: str) -> str:
    response = session.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text


def fetch_html_table_rows(session: requests.Session, source: dict, fetch_date: str) -> tuple[list[dict], list[dict]]:
    html = get_html(session, source["source_url"])
    tables = pd.read_html(io.StringIO(html), flavor=["lxml"])
    inspected = []
    model_candidates = source.get("model_column_candidates", [])
    score_candidates = source.get("score_column_candidates", [])
    display_name_candidates = source.get("display_name_columns", [])
    for index, table in enumerate(tables):
        frame = table.copy()
        if isinstance(frame.columns, pd.MultiIndex):
            frame.columns = [" ".join(clean_str(part) for part in col if clean_str(part)) for col in frame.columns]
        else:
            frame.columns = [clean_str(col) for col in frame.columns]
        normalized_columns = {col: normalize_header(col) for col in frame.columns}
        inspected.append({"table_index": index, "columns": list(frame.columns)})

        model_col = None
        score_col = None
        for column, normalized in normalized_columns.items():
            if normalized in {normalize_header(item) for item in model_candidates}:
                model_col = column
                break
        for column, normalized in normalized_columns.items():
            if normalized in {normalize_header(item) for item in score_candidates}:
                score_col = column
                break

        if not model_col or not score_col:
            continue

        rows = []
        for _, row in frame.iterrows():
            source_model_name = clean_str(row.get(model_col))
            if display_name_candidates:
                display_parts = []
                normalized_display = {normalize_header(item) for item in display_name_candidates}
                for column, normalized in normalized_columns.items():
                    if normalized in normalized_display:
                        value = clean_str(row.get(column))
                        if value and value not in display_parts:
                            display_parts.append(value)
                if display_parts:
                    source_model_name = " | ".join(display_parts)
            if not source_model_name:
                continue
            score_raw = parse_numeric_score(row.get(score_col), score_multiplier=float(source.get("score_multiplier", 1.0)))
            rows.append(
                {
                    "benchmark_id": source["benchmark_id"],
                    "source_model_name": source_model_name,
                    "score_raw": score_raw,
                    "score_date": fetch_date,
                    "source_url": source["source_url"],
                    "adapter": source["adapter"],
                    "notes": clean_str(source.get("notes")),
                }
            )
        if rows:
            return rows, inspected
    raise ValueError(f"No matching HTML table found. Inspected tables: {inspected}")


def fetch_hf_dataset_rows(session: requests.Session, source: dict, fetch_date: str) -> tuple[list[dict], dict]:
    dataset_id = source["dataset_id"]
    split_resp = session.get(
        "https://datasets-server.huggingface.co/splits",
        params={"dataset": dataset_id},
        timeout=REQUEST_TIMEOUT,
    )
    split_resp.raise_for_status()
    split_payload = split_resp.json()
    splits = split_payload.get("splits") or []
    if not splits:
        raise ValueError(f"No splits returned for dataset {dataset_id}")
    chosen = splits[0]
    config_name = chosen["config"]
    split_name = chosen["split"]
    total_rows = int(chosen.get("num_rows") or chosen.get("num_examples") or 0)
    if total_rows <= 0:
        total_rows = 200

    rows = []
    offset = 0
    page_size = 100
    row_model_candidates = source.get("row_model_field_candidates", [])
    row_score_candidates = source.get("row_score_field_candidates", [])
    while offset < total_rows:
        resp = session.get(
            "https://datasets-server.huggingface.co/rows",
            params={
                "dataset": dataset_id,
                "config": config_name,
                "split": split_name,
                "offset": offset,
                "length": page_size,
            },
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        payload = resp.json()
        row_items = payload.get("rows") or []
        if not row_items:
            break
        for item in row_items:
            record = flatten_record(item.get("row", {}))
            source_model_name = find_value_by_candidates(record, row_model_candidates)
            score_value = find_value_by_candidates(record, row_score_candidates)
            if source_model_name in (None, "") or score_value in (None, ""):
                continue
            rows.append(
                {
                    "benchmark_id": source["benchmark_id"],
                    "source_model_name": clean_str(source_model_name),
                    "score_raw": parse_numeric_score(score_value, score_multiplier=float(source.get("score_multiplier", 1.0))),
                    "score_date": fetch_date,
                    "source_url": source["source_url"],
                    "adapter": source["adapter"],
                    "notes": clean_str(source.get("notes")),
                }
            )
        offset += page_size
    if not rows:
        raise ValueError(f"No usable rows extracted from Hugging Face dataset {dataset_id}")
    meta = {
        "dataset_id": dataset_id,
        "config": config_name,
        "split": split_name,
        "requested_rows": total_rows,
        "extracted_rows": len(rows),
    }
    return rows, meta


def build_resolved_result(source: dict, snapshot_month: str, model_id: str, score_raw: float, score_date: str, source_url: str, notes: str) -> dict:
    return {
        "snapshot_month": snapshot_month,
        "model_id": model_id,
        "benchmark_id": source["benchmark_id"],
        "benchmark_variant": clean_str(source.get("benchmark_variant")),
        "comparability_group": clean_str(source.get("comparability_group")),
        "metric_name": clean_str(source.get("metric_name")),
        "metric_unit": clean_str(source.get("metric_unit")),
        "score_raw": round(score_raw, 4),
        "score_normalized_100": "",
        "score_date": score_date,
        "scaffold_type": clean_str(source.get("scaffold_type")),
        "source_url": source_url,
        "source_type": clean_str(source.get("source_type")),
        "result_quality_weight": clean_str(source.get("result_quality_weight")),
        "notes": notes,
    }


def coerce_manual_row(source: dict, snapshot_month: str, raw: dict) -> dict:
    score_raw = clean_str(raw.get("score_raw"))
    if not score_raw:
        raise ValueError(f"Manual row missing score_raw for benchmark_id={source['benchmark_id']}")
    return {
        "snapshot_month": clean_str(raw.get("snapshot_month")) or snapshot_month,
        "model_id": clean_str(raw.get("model_id")),
        "benchmark_id": source["benchmark_id"],
        "benchmark_variant": clean_str(raw.get("benchmark_variant")) or clean_str(source.get("benchmark_variant")),
        "comparability_group": clean_str(raw.get("comparability_group")) or clean_str(source.get("comparability_group")),
        "metric_name": clean_str(raw.get("metric_name")) or clean_str(source.get("metric_name")),
        "metric_unit": clean_str(raw.get("metric_unit")) or clean_str(source.get("metric_unit")),
        "score_raw": round(float(score_raw), 4),
        "score_normalized_100": clean_str(raw.get("score_normalized_100")),
        "score_date": clean_str(raw.get("score_date")) or datetime.now(timezone.utc).date().isoformat(),
        "scaffold_type": clean_str(raw.get("scaffold_type")) or clean_str(source.get("scaffold_type")),
        "source_url": clean_str(raw.get("source_url")) or clean_str(source.get("source_url")),
        "source_type": clean_str(raw.get("source_type")) or clean_str(source.get("source_type")),
        "result_quality_weight": clean_str(raw.get("result_quality_weight")) or clean_str(source.get("result_quality_weight")),
        "notes": clean_str(raw.get("notes")) or clean_str(source.get("notes")),
    }


def dedupe_rows(rows: list[dict]) -> list[dict]:
    deduped = []
    seen = set()
    for row in rows:
        key = (
            clean_str(row.get("snapshot_month")),
            clean_str(row.get("model_id")),
            clean_str(row.get("benchmark_id")),
            clean_str(row.get("benchmark_variant")),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def main() -> None:
    args = build_parser().parse_args()
    snapshot_month = clean_str(args.snapshot_month)
    validate_snapshot_month(snapshot_month)

    script_path = Path(__file__).resolve()
    dashboard_dir = script_path.parent.parent
    output_dir = Path(args.output_dir) if args.output_dir else dashboard_dir / "output" / "fetch" / snapshot_month
    output_benchmark_results = Path(args.output_benchmark_results)

    fetch_registry = load_json(Path(args.fetch_registry))
    sources = [row for row in fetch_registry.get("sources", []) if row.get("enabled", True)]
    alias_lookup = load_aliases(Path(args.model_aliases))
    manual_rows_by_benchmark = load_manual_rows(Path(args.manual_results), snapshot_month)
    fetch_date = datetime.now(timezone.utc).date().isoformat()
    session = requests_session()

    resolved_rows: list[dict] = []
    raw_source_rows: list[dict] = []
    unresolved_rows: list[dict] = []
    source_logs: list[dict] = []

    for source in sources:
        benchmark_id = source["benchmark_id"]
        log_entry: dict[str, Any] = {
            "benchmark_id": benchmark_id,
            "adapter": source["adapter"],
            "source_url": source["source_url"],
            "status": "pending",
            "resolved_count": 0,
            "unresolved_count": 0,
            "raw_count": 0,
            "manual_fallback_count": 0,
            "errors": [],
        }

        automated_source_rows: list[dict] = []
        try:
            if source["adapter"] == "manual_csv":
                automated_source_rows = []
                log_entry["status"] = "manual_only"
            elif source["adapter"] == "html_table":
                automated_source_rows, meta = fetch_html_table_rows(session, source, fetch_date)
                log_entry["status"] = "fetched"
                log_entry["meta"] = meta
            elif source["adapter"] == "hf_dataset_rows":
                automated_source_rows, meta = fetch_hf_dataset_rows(session, source, fetch_date)
                log_entry["status"] = "fetched"
                log_entry["meta"] = meta
            else:
                raise ValueError(f"Unsupported adapter: {source['adapter']}")
        except Exception as exc:
            log_entry["status"] = "error"
            log_entry["errors"].append(str(exc))

        for row in automated_source_rows:
            raw_source_rows.append(
                {
                    "snapshot_month": snapshot_month,
                    "benchmark_id": benchmark_id,
                    "source_model_name": row["source_model_name"],
                    "score_raw": row["score_raw"],
                    "score_date": row["score_date"],
                    "source_url": row["source_url"],
                    "adapter": row["adapter"],
                    "notes": row.get("notes", ""),
                }
            )
            model_id, reason = match_alias(row["source_model_name"], benchmark_id, alias_lookup)
            if model_id:
                resolved_rows.append(
                    build_resolved_result(
                        source,
                        snapshot_month=snapshot_month,
                        model_id=model_id,
                        score_raw=row["score_raw"],
                        score_date=row["score_date"],
                        source_url=row["source_url"],
                        notes=row.get("notes", ""),
                    )
                )
            else:
                unresolved_rows.append(
                    {
                        "snapshot_month": snapshot_month,
                        "benchmark_id": benchmark_id,
                        "source_model_name": row["source_model_name"],
                        "score_raw": row["score_raw"],
                        "score_date": row["score_date"],
                        "source_url": row["source_url"],
                        "reason": reason,
                    }
                )

        log_entry["raw_count"] = len(automated_source_rows)
        log_entry["resolved_count"] = len([row for row in resolved_rows if row["benchmark_id"] == benchmark_id])
        log_entry["unresolved_count"] = len([row for row in unresolved_rows if row["benchmark_id"] == benchmark_id])

        manual_candidates = manual_rows_by_benchmark.get(benchmark_id, [])
        if source.get("allow_manual_fallback", True) and manual_candidates:
            existing_keys = {
                (
                    row["snapshot_month"],
                    row["model_id"],
                    row["benchmark_id"],
                    row["benchmark_variant"],
                )
                for row in resolved_rows
                if row["benchmark_id"] == benchmark_id
            }
            added = 0
            for raw in manual_candidates:
                manual_row = coerce_manual_row(source, snapshot_month, raw)
                key = (
                    manual_row["snapshot_month"],
                    manual_row["model_id"],
                    manual_row["benchmark_id"],
                    manual_row["benchmark_variant"],
                )
                if key in existing_keys:
                    continue
                resolved_rows.append(manual_row)
                existing_keys.add(key)
                added += 1
            log_entry["manual_fallback_count"] = added
            if log_entry["status"] in {"manual_only", "error"} and added:
                log_entry["status"] = "manual_fallback"

        source_logs.append(log_entry)

    resolved_rows = dedupe_rows(resolved_rows)

    summary = {
        "snapshot_month": snapshot_month,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_count": len(sources),
        "resolved_result_count": len(resolved_rows),
        "raw_source_row_count": len(raw_source_rows),
        "unresolved_row_count": len(unresolved_rows),
        "sources": source_logs,
    }

    write_csv(
        output_benchmark_results,
        [
            "snapshot_month",
            "model_id",
            "benchmark_id",
            "benchmark_variant",
            "comparability_group",
            "metric_name",
            "metric_unit",
            "score_raw",
            "score_normalized_100",
            "score_date",
            "scaffold_type",
            "source_url",
            "source_type",
            "result_quality_weight",
            "notes",
        ],
        resolved_rows,
    )
    write_csv(
        output_dir / "resolved_benchmark_results.csv",
        [
            "snapshot_month",
            "model_id",
            "benchmark_id",
            "benchmark_variant",
            "comparability_group",
            "metric_name",
            "metric_unit",
            "score_raw",
            "score_normalized_100",
            "score_date",
            "scaffold_type",
            "source_url",
            "source_type",
            "result_quality_weight",
            "notes",
        ],
        resolved_rows,
    )
    write_csv(
        output_dir / "raw_source_rows.csv",
        [
            "snapshot_month",
            "benchmark_id",
            "source_model_name",
            "score_raw",
            "score_date",
            "source_url",
            "adapter",
            "notes",
        ],
        raw_source_rows,
    )
    write_csv(
        output_dir / "unresolved_source_rows.csv",
        [
            "snapshot_month",
            "benchmark_id",
            "source_model_name",
            "score_raw",
            "score_date",
            "source_url",
            "reason",
        ],
        unresolved_rows,
    )
    write_json(output_dir / "fetch_log.json", summary)


if __name__ == "__main__":
    main()
