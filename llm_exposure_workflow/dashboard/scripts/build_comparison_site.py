from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_js_data(path: Path, variable_name: str, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, ensure_ascii=False)
    path.write_text(f"window.{variable_name} = {payload};\n", encoding="utf-8")


def clean_str(value: object) -> str:
    return "" if value is None else str(value).strip()


def parse_float(value: object, *, field_name: str) -> float:
    text = clean_str(value)
    if not text:
        raise ValueError(f"Missing numeric value for {field_name}")
    return float(text)


def detect_latest_snapshot(output_root: Path) -> str:
    snapshot_dirs = [path.name for path in output_root.iterdir() if path.is_dir()]
    if not snapshot_dirs:
        raise FileNotFoundError(f"No dashboard snapshots found under: {output_root}")
    return sorted(snapshot_dirs)[-1]


def build_parser() -> argparse.ArgumentParser:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[3]
    dashboard_dir = script_path.parent.parent
    parser = argparse.ArgumentParser(
        description="Build GitHub Pages site data for the PM exposure comparison table.",
    )
    parser.add_argument(
        "--snapshot-month",
        default=None,
        help="Snapshot month in YYYY-MM format. Defaults to the latest dashboard/output/<month>/ directory.",
    )
    parser.add_argument(
        "--docs-dir",
        default=str(repo_root / "docs"),
        help="Destination docs directory. Defaults to repo_root/docs.",
    )
    parser.add_argument(
        "--models",
        default=str(dashboard_dir / "input" / "models.csv"),
        help="Path to models CSV. Defaults to dashboard/input/models.csv.",
    )
    return parser


def build_payload(
    *,
    repo_root: Path,
    snapshot_month: str,
    models_path: Path,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    dashboard_dir = repo_root / "llm_exposure_workflow" / "dashboard"
    snapshot_dir = dashboard_dir / "output" / snapshot_month

    occupation_rows = read_csv_rows(snapshot_dir / "occupation_realized_exposure.csv")
    benchmark_rows = read_csv_rows(snapshot_dir / "benchmark_results_normalized.csv")
    model_rows = read_csv_rows(models_path)

    if not occupation_rows:
        raise ValueError(f"No occupation rows found in {snapshot_dir / 'occupation_realized_exposure.csv'}")

    models_by_id = {
        clean_str(row.get("model_id")): {
            "display_name": clean_str(row.get("display_name")) or clean_str(row.get("model_id")),
            "provider": clean_str(row.get("provider")) or "Unknown",
            "release_date": clean_str(row.get("release_date")),
            "notes": clean_str(row.get("notes")),
        }
        for row in model_rows
    }

    benchmarks_by_model: dict[str, set[str]] = defaultdict(set)
    benchmark_variants_by_model: dict[str, set[str]] = defaultdict(set)
    for row in benchmark_rows:
        model_id = clean_str(row.get("model_id"))
        benchmark_id = clean_str(row.get("benchmark_id"))
        benchmark_variant = clean_str(row.get("benchmark_variant"))
        if model_id and benchmark_id:
            benchmarks_by_model[model_id].add(benchmark_id)
        if model_id and benchmark_variant:
            benchmark_variants_by_model[model_id].add(benchmark_variant)

    first_row = occupation_rows[0]
    occupation = {
        "occupation_code": clean_str(first_row.get("occupation_code")),
        "occupation_label": clean_str(first_row.get("occupation_label")),
        "weighted_dae_100": round(parse_float(first_row.get("weighted_dae_100"), field_name="weighted_dae_100"), 2),
        "weighted_se_100": round(parse_float(first_row.get("weighted_se_100"), field_name="weighted_se_100"), 2),
        "weighted_oc_100": round(parse_float(first_row.get("weighted_oc_100"), field_name="weighted_oc_100"), 2),
        "weighted_ic_100": round(parse_float(first_row.get("weighted_ic_100"), field_name="weighted_ic_100"), 2),
        "included_task_count": int(parse_float(first_row.get("included_task_count"), field_name="included_task_count")),
    }

    table_rows: list[dict[str, object]] = []
    for row in occupation_rows:
        model_id = clean_str(row.get("model_id"))
        model_meta = models_by_id.get(
            model_id,
            {
                "display_name": model_id,
                "provider": "Unknown",
                "release_date": "",
                "notes": "",
            },
        )
        benchmarks = sorted(benchmarks_by_model.get(model_id, set()))
        benchmark_variants = sorted(benchmark_variants_by_model.get(model_id, set()))
        table_rows.append(
            {
                "model_id": model_id,
                "display_name": model_meta["display_name"],
                "provider": model_meta["provider"],
                "release_date": model_meta["release_date"],
                "realized_occupation_exposure_100": round(
                    parse_float(
                        row.get("realized_occupation_exposure_100"),
                        field_name="realized_occupation_exposure_100",
                    ),
                    4,
                ),
                "benchmark_coverage_ratio": round(
                    parse_float(row.get("benchmark_coverage_ratio"), field_name="benchmark_coverage_ratio"),
                    4,
                ),
                "benchmark_count": len(benchmarks),
                "benchmarks": benchmarks,
                "benchmark_variants": benchmark_variants,
                "notes": model_meta["notes"],
            }
        )

    table_rows.sort(
        key=lambda item: (
            -float(item["realized_occupation_exposure_100"]),
            -float(item["benchmark_coverage_ratio"]),
            str(item["display_name"]).lower(),
        ),
    )

    for index, row in enumerate(table_rows, start=1):
        row["rank"] = index

    exposure_values = [float(row["realized_occupation_exposure_100"]) for row in table_rows]
    coverage_values = [float(row["benchmark_coverage_ratio"]) for row in table_rows]
    top_row = table_rows[0]

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "snapshot_month": snapshot_month,
        "repo_name": "Project-Management-AI-Exposure-Index",
        "occupation": occupation,
        "summary": {
            "tracked_model_count": len(table_rows),
            "benchmark_result_count": len(benchmark_rows),
            "provider_count": len({clean_str(row["provider"]) for row in table_rows}),
            "top_model": {
                "model_id": top_row["model_id"],
                "display_name": top_row["display_name"],
                "provider": top_row["provider"],
                "realized_occupation_exposure_100": top_row["realized_occupation_exposure_100"],
            },
            "median_realized_occupation_exposure_100": round(statistics.median(exposure_values), 4),
            "mean_benchmark_coverage_ratio": round(statistics.fmean(coverage_values), 4),
        },
        "rows": table_rows,
    }
    return payload, table_rows


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[3]
    dashboard_output_root = repo_root / "llm_exposure_workflow" / "dashboard" / "output"
    snapshot_month = clean_str(args.snapshot_month) or detect_latest_snapshot(dashboard_output_root)
    docs_dir = Path(args.docs_dir).resolve()
    docs_data_dir = docs_dir / "data"
    models_path = Path(args.models).resolve()

    payload, table_rows = build_payload(
        repo_root=repo_root,
        snapshot_month=snapshot_month,
        models_path=models_path,
    )

    json_path = docs_data_dir / "latest-comparison.json"
    js_path = docs_data_dir / "latest-comparison.js"
    csv_path = docs_data_dir / "latest-comparison.csv"

    write_json(json_path, payload)
    write_js_data(js_path, "PM_EXPOSURE_DATA", payload)
    write_csv(
        csv_path,
        fieldnames=[
            "rank",
            "model_id",
            "display_name",
            "provider",
            "realized_occupation_exposure_100",
            "benchmark_coverage_ratio",
            "benchmark_count",
            "benchmarks",
            "benchmark_variants",
            "release_date",
            "notes",
        ],
        rows=[
            {
                **row,
                "benchmarks": ", ".join(row["benchmarks"]),
                "benchmark_variants": ", ".join(row["benchmark_variants"]),
            }
            for row in table_rows
        ],
    )

    print(f"Built comparison site data for snapshot {snapshot_month}")
    print(f"JSON: {json_path}")
    print(f"JS: {js_path}")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
