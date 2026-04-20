from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator


CAPABILITY_FAMILIES = [
    {
        "capability_family_id": "research",
        "label": "Research",
        "description": "Search, retrieval, evidence gathering, and source comparison.",
    },
    {
        "capability_family_id": "synthesis_reporting",
        "label": "Synthesis And Reporting",
        "description": "Summarization, explanation, and management reporting.",
    },
    {
        "capability_family_id": "planning_orchestration",
        "label": "Planning And Orchestration",
        "description": "Task decomposition, sequencing, scheduling, allocation, and replanning.",
    },
    {
        "capability_family_id": "tool_use",
        "label": "Tool Use",
        "description": "Reliable tool calling, application feature use, and API invocation.",
    },
    {
        "capability_family_id": "workflow_execution",
        "label": "Workflow Execution",
        "description": "End-to-end multi-step execution that changes system state.",
    },
    {
        "capability_family_id": "computer_use",
        "label": "Computer Use",
        "description": "Browser, desktop, and GUI interaction.",
    },
    {
        "capability_family_id": "policy_compliance",
        "label": "Policy Compliance",
        "description": "Rule following, escalation logic, approvals, and governance constraints.",
    },
    {
        "capability_family_id": "technical_execution",
        "label": "Technical Execution",
        "description": "Code, terminal, configuration, and implementation-heavy work.",
    },
]

CAPABILITY_IDS = [item["capability_family_id"] for item in CAPABILITY_FAMILIES]

SOURCE_TYPE_WEIGHTS = {
    "official_leaderboard": 1.00,
    "official_dataset": 0.95,
    "official_paper": 0.90,
    "third_party_reproduction": 0.85,
    "vendor_report": 0.75,
    "self_reported": 0.60,
}

def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_str(value: object) -> str:
    return "" if value is None else str(value).strip()


def parse_float(value: object, *, field_name: str) -> float:
    text = clean_str(value)
    if not text:
        raise ValueError(f"Missing numeric value for {field_name}")
    return float(text)


def optional_float(value: object) -> float | None:
    text = clean_str(value)
    if not text:
        return None
    return float(text)


def maybe_add(record: dict, key: str, value: object) -> None:
    text = clean_str(value)
    if text:
        record[key] = text


def build_parser() -> argparse.ArgumentParser:
    script_path = Path(__file__).resolve()
    dashboard_dir = script_path.parent.parent
    input_dir = dashboard_dir / "input"
    output_root = dashboard_dir / "output"
    parser = argparse.ArgumentParser(
        description="Build a monthly PM exposure dashboard snapshot from benchmark result inputs.",
    )
    parser.add_argument("--snapshot-month", required=True, help="Snapshot month in YYYY-MM format.")
    parser.add_argument(
        "--models",
        default=str(input_dir / "models.csv"),
        help="Path to models CSV. Defaults to dashboard/input/models.csv.",
    )
    parser.add_argument(
        "--benchmark-results",
        default=str(input_dir / "benchmark_results.csv"),
        help="Path to benchmark results CSV. Defaults to dashboard/input/benchmark_results.csv.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional output directory. Defaults to dashboard/output/<snapshot-month>/.",
    )
    return parser


def validate_snapshot_month(snapshot_month: str) -> None:
    try:
        datetime.strptime(snapshot_month, "%Y-%m")
    except ValueError as exc:
        raise ValueError(f"snapshot_month must be YYYY-MM, got {snapshot_month}") from exc


def load_benchmark_matrix(path: Path) -> tuple[list[dict], dict[str, dict]]:
    rows = []
    lookup = {}
    for raw in read_csv_rows(path):
        row = {
            "benchmark_id": clean_str(raw["benchmark_id"]),
            "benchmark_label": clean_str(raw["benchmark_label"]),
            "benchmark_variant": clean_str(raw["benchmark_variant"]),
            "dashboard_role": clean_str(raw["dashboard_role"]),
            "dashboard_weight": parse_float(raw["dashboard_weight"], field_name="dashboard_weight"),
            "official_source_url": clean_str(raw["official_source_url"]),
            "last_verified_date": clean_str(raw["last_verified_date"]),
        }
        for family in CAPABILITY_IDS:
            row[family] = parse_float(raw[family], field_name=f"{row['benchmark_id']}:{family}")
        rows.append(row)
        lookup[row["benchmark_id"]] = row
    return rows, lookup


def load_task_matrix(path: Path) -> list[dict]:
    rows = []
    for raw in read_csv_rows(path):
        row = {
            "task_id": clean_str(raw["task_id"]),
            "onet_task_text": clean_str(raw["onet_task_text"]),
            "benchmark_observability": clean_str(raw["benchmark_observability"]),
        }
        for family in CAPABILITY_IDS:
            row[family] = parse_float(raw[family], field_name=f"{row['task_id']}:{family}")
        rows.append(row)
    return rows


def load_models(path: Path) -> tuple[list[dict], dict[str, dict]]:
    models = []
    lookup = {}
    for raw in read_csv_rows(path):
        model_id = clean_str(raw.get("model_id"))
        if not model_id:
            continue
        row = {
            "model_id": model_id,
            "display_name": clean_str(raw["display_name"]),
            "provider": clean_str(raw["provider"]),
        }
        maybe_add(row, "release_date", raw.get("release_date"))
        maybe_add(row, "notes", raw.get("notes"))
        models.append(row)
        lookup[model_id] = row
    if not models:
        raise ValueError(f"No model rows found in {path}")
    return models, lookup


def normalize_score(metric_unit: str, score_raw: float) -> float:
    if metric_unit == "percent_100":
        normalized = score_raw
    elif metric_unit == "proportion_0_1":
        normalized = score_raw * 100
    else:
        raise ValueError(f"Unsupported metric_unit: {metric_unit}")
    if normalized < 0 or normalized > 100:
        raise ValueError(f"Normalized score must be within 0-100, got {normalized}")
    return round(normalized, 4)


def load_benchmark_results(
    path: Path,
    *,
    snapshot_month: str,
    model_lookup: dict[str, dict],
    benchmark_lookup: dict[str, dict],
) -> list[dict]:
    rows = []
    seen_keys = set()
    for raw in read_csv_rows(path):
        row_snapshot_month = clean_str(raw.get("snapshot_month")) or snapshot_month
        if row_snapshot_month != snapshot_month:
            continue
        model_id = clean_str(raw.get("model_id"))
        benchmark_id = clean_str(raw.get("benchmark_id"))
        if model_id not in model_lookup:
            raise ValueError(f"Benchmark result references unknown model_id: {model_id}")
        if benchmark_id not in benchmark_lookup:
            raise ValueError(f"Benchmark result references unknown benchmark_id: {benchmark_id}")

        benchmark_meta = benchmark_lookup[benchmark_id]
        benchmark_variant = clean_str(raw.get("benchmark_variant")) or benchmark_meta["benchmark_variant"]
        comparability_group = clean_str(raw.get("comparability_group")) or f"{benchmark_id}:{benchmark_variant}"
        metric_name = clean_str(raw.get("metric_name"))
        metric_unit = clean_str(raw.get("metric_unit"))
        score_raw = parse_float(raw.get("score_raw"), field_name=f"{model_id}:{benchmark_id}:score_raw")
        normalized = optional_float(raw.get("score_normalized_100"))
        score_normalized_100 = round(normalized, 4) if normalized is not None else normalize_score(metric_unit, score_raw)
        source_type = clean_str(raw.get("source_type"))
        if source_type not in SOURCE_TYPE_WEIGHTS:
            raise ValueError(f"Unsupported source_type: {source_type}")
        result_quality_weight = optional_float(raw.get("result_quality_weight"))
        if result_quality_weight is None:
            result_quality_weight = SOURCE_TYPE_WEIGHTS[source_type]
        if result_quality_weight < 0 or result_quality_weight > 1:
            raise ValueError(f"result_quality_weight must be between 0 and 1, got {result_quality_weight}")

        record = {
            "snapshot_month": snapshot_month,
            "model_id": model_id,
            "benchmark_id": benchmark_id,
            "benchmark_variant": benchmark_variant,
            "comparability_group": comparability_group,
            "metric_name": metric_name,
            "metric_unit": metric_unit,
            "score_raw": round(score_raw, 4),
            "score_normalized_100": score_normalized_100,
            "score_date": clean_str(raw.get("score_date")),
            "source_url": clean_str(raw.get("source_url")) or benchmark_meta["official_source_url"],
            "official_source_url": benchmark_meta["official_source_url"],
            "source_type": source_type,
            "result_quality_weight": round(result_quality_weight, 4),
        }
        maybe_add(record, "scaffold_type", raw.get("scaffold_type"))
        maybe_add(record, "notes", raw.get("notes"))

        key = (snapshot_month, model_id, benchmark_id, benchmark_variant)
        if key in seen_keys:
            raise ValueError(f"Duplicate benchmark result row for key {key}")
        seen_keys.add(key)
        rows.append(record)

    if not rows:
        raise ValueError(f"No benchmark results found for snapshot_month={snapshot_month} in {path}")
    return rows


def load_task_scores(path: Path) -> list[dict]:
    rows = []
    for raw in read_csv_rows(path):
        rows.append(
            {
                "task_id": clean_str(raw["task_id"]),
                "onet_task_text": clean_str(raw["onet_task_text"]),
                "onet_importance": parse_float(raw["onet_importance"], field_name=f"{raw['task_id']}:onet_importance"),
                "importance_weight": parse_float(raw["importance_weight"], field_name=f"{raw['task_id']}:importance_weight"),
                "DAE": parse_float(raw["DAE"], field_name=f"{raw['task_id']}:DAE"),
                "OC": parse_float(raw["OC"], field_name=f"{raw['task_id']}:OC"),
                "IC": parse_float(raw["IC"], field_name=f"{raw['task_id']}:IC"),
                "SE": parse_float(raw["SE"], field_name=f"{raw['task_id']}:SE"),
            }
        )
    return rows


def compute_capability_scores(
    models: list[dict],
    benchmark_results: list[dict],
    benchmark_matrix_lookup: dict[str, dict],
) -> list[dict]:
    max_denominator = {}
    for family in CAPABILITY_IDS:
        max_denominator[family] = sum(
            row[family] * row["dashboard_weight"] for row in benchmark_matrix_lookup.values()
        )

    results_by_model: dict[str, list[dict]] = {}
    for row in benchmark_results:
        results_by_model.setdefault(row["model_id"], []).append(row)

    capability_rows = []
    for model in models:
        model_results = results_by_model.get(model["model_id"], [])
        snapshot_month = model_results[0]["snapshot_month"] if model_results else ""
        for family in CAPABILITY_IDS:
            numerator = 0.0
            denominator = 0.0
            contributing = []
            for result in model_results:
                benchmark_meta = benchmark_matrix_lookup[result["benchmark_id"]]
                family_weight = benchmark_meta[family]
                if family_weight <= 0:
                    continue
                contribution_weight = family_weight * benchmark_meta["dashboard_weight"] * result["result_quality_weight"]
                numerator += result["score_normalized_100"] * contribution_weight
                denominator += contribution_weight
                contributing.append(result["benchmark_id"])
            capability_score = round(numerator / denominator, 4) if denominator else 0.0
            coverage_weight = round(denominator / max_denominator[family], 4) if max_denominator[family] else 0.0
            capability_rows.append(
                {
                    "snapshot_month": snapshot_month,
                    "model_id": model["model_id"],
                    "capability_family_id": family,
                    "capability_score_100": capability_score,
                    "coverage_weight": coverage_weight,
                    "benchmark_count": len(sorted(set(contributing))),
                    "contributing_benchmark_ids": sorted(set(contributing)),
                }
            )
    return capability_rows


def compute_task_realized_exposure(
    *,
    snapshot_month: str,
    models: list[dict],
    capability_scores: list[dict],
    task_matrix: list[dict],
    task_scores: list[dict],
) -> list[dict]:
    capability_lookup = {
        (row["model_id"], row["capability_family_id"]): row for row in capability_scores
    }
    task_score_lookup = {row["task_id"]: row for row in task_scores}
    rows = []
    for model in models:
        for task in task_matrix:
            score_row = task_score_lookup[task["task_id"]]
            structural_exposure = round((0.50 * score_row["DAE"]) + (0.50 * score_row["SE"]), 4)
            capability_fit = 0.0
            benchmark_coverage_ratio = 0.0
            for family in CAPABILITY_IDS:
                family_weight = task[family]
                capability_row = capability_lookup[(model["model_id"], family)]
                capability_fit += family_weight * capability_row["capability_score_100"]
                benchmark_coverage_ratio += family_weight * capability_row["coverage_weight"]
            rows.append(
                {
                    "snapshot_month": snapshot_month,
                    "model_id": model["model_id"],
                    "task_id": task["task_id"],
                    "onet_task_text": task["onet_task_text"],
                    "benchmark_observability": task["benchmark_observability"],
                    "structural_exposure_100": round(structural_exposure, 4),
                    "capability_fit_100": round(capability_fit, 4),
                    "realized_exposure_100": round((structural_exposure * capability_fit) / 100, 4),
                    "oc_100": round(score_row["OC"], 4),
                    "benchmark_coverage_ratio": round(benchmark_coverage_ratio, 4),
                }
            )
    return rows


def compute_occupation_realized_exposure(
    *,
    snapshot_month: str,
    models: list[dict],
    task_scores: list[dict],
    task_realized_rows: list[dict],
    occupation_scores: dict,
) -> list[dict]:
    task_score_lookup = {row["task_id"]: row for row in task_scores}
    rows = []
    by_model: dict[str, list[dict]] = {}
    for row in task_realized_rows:
        by_model.setdefault(row["model_id"], []).append(row)

    for model in models:
        model_rows = by_model.get(model["model_id"], [])
        realized = 0.0
        coverage = 0.0
        for row in model_rows:
            importance_weight = task_score_lookup[row["task_id"]]["importance_weight"]
            realized += importance_weight * row["realized_exposure_100"]
            coverage += importance_weight * row["benchmark_coverage_ratio"]
        rows.append(
            {
                "snapshot_month": snapshot_month,
                "model_id": model["model_id"],
                "occupation_code": occupation_scores["occupation_code"],
                "occupation_label": occupation_scores["occupation_label"],
                "realized_occupation_exposure_100": round(realized, 4),
                "weighted_dae_100": round(occupation_scores["Occupation_DAE"], 4),
                "weighted_se_100": round(occupation_scores["Occupation_SE"], 4),
                "weighted_oc_100": round(occupation_scores["Occupation_OC"], 4),
                "weighted_ic_100": round(occupation_scores["Occupation_IC"], 4),
                "benchmark_coverage_ratio": round(coverage, 4),
                "included_task_count": len(model_rows),
            }
        )
    return rows


def build_snapshot(
    *,
    snapshot_month: str,
    benchmark_matrix: list[dict],
    task_matrix: list[dict],
    models: list[dict],
    benchmark_results: list[dict],
    capability_scores: list[dict],
    task_realized_rows: list[dict],
    occupation_realized_rows: list[dict],
) -> dict:
    snapshot = {
        "schema_version": "1.0.0",
        "snapshot_month": snapshot_month,
        "notes": f"Generated by run_monthly_dashboard_snapshot.py on {datetime.now(timezone.utc).date().isoformat()}.",
        "capability_families": CAPABILITY_FAMILIES,
        "benchmark_capability_matrix": benchmark_matrix,
        "task_capability_matrix": [
            {key: value for key, value in row.items() if key in {"task_id", "onet_task_text", "benchmark_observability", *CAPABILITY_IDS}}
            for row in task_matrix
        ],
        "models": models,
        "benchmark_results": benchmark_results,
        "capability_scores": capability_scores,
        "task_realized_exposure": [
            {
                "snapshot_month": row["snapshot_month"],
                "model_id": row["model_id"],
                "task_id": row["task_id"],
                "structural_exposure_100": row["structural_exposure_100"],
                "capability_fit_100": row["capability_fit_100"],
                "realized_exposure_100": row["realized_exposure_100"],
                "oc_100": row["oc_100"],
                "benchmark_coverage_ratio": row["benchmark_coverage_ratio"],
            }
            for row in task_realized_rows
        ],
        "occupation_realized_exposure": occupation_realized_rows,
    }
    return snapshot


def validate_snapshot(snapshot: dict, schema_path: Path) -> None:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(snapshot), key=lambda err: list(err.path))
    if errors:
        messages = []
        for err in errors[:10]:
            path = ".".join(str(part) for part in err.path) or "<root>"
            messages.append(f"{path}: {err.message}")
        raise ValueError("Snapshot validation failed:\n" + "\n".join(messages))


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    snapshot_month = clean_str(args.snapshot_month)
    validate_snapshot_month(snapshot_month)

    script_path = Path(__file__).resolve()
    dashboard_dir = script_path.parent.parent
    workflow_dir = dashboard_dir.parent
    structural_output_dir = workflow_dir / "output"
    output_dir = Path(args.output_dir) if args.output_dir else dashboard_dir / "output" / snapshot_month

    benchmark_matrix_path = dashboard_dir / "benchmark_capability_matrix.csv"
    task_matrix_path = dashboard_dir / "task_capability_matrix.csv"
    schema_path = dashboard_dir / "dashboard_snapshot.schema.json"
    task_scores_path = structural_output_dir / "task_scores.csv"
    occupation_scores_path = structural_output_dir / "occupation_scores.json"

    benchmark_matrix, benchmark_lookup = load_benchmark_matrix(benchmark_matrix_path)
    task_matrix = load_task_matrix(task_matrix_path)
    models, model_lookup = load_models(Path(args.models))
    benchmark_results = load_benchmark_results(
        Path(args.benchmark_results),
        snapshot_month=snapshot_month,
        model_lookup=model_lookup,
        benchmark_lookup=benchmark_lookup,
    )
    task_scores = load_task_scores(task_scores_path)
    occupation_scores = load_json(occupation_scores_path)

    capability_scores = compute_capability_scores(models, benchmark_results, benchmark_lookup)
    task_realized_rows = compute_task_realized_exposure(
        snapshot_month=snapshot_month,
        models=models,
        capability_scores=capability_scores,
        task_matrix=task_matrix,
        task_scores=task_scores,
    )
    occupation_realized_rows = compute_occupation_realized_exposure(
        snapshot_month=snapshot_month,
        models=models,
        task_scores=task_scores,
        task_realized_rows=task_realized_rows,
        occupation_scores=occupation_scores,
    )

    snapshot = build_snapshot(
        snapshot_month=snapshot_month,
        benchmark_matrix=benchmark_matrix,
        task_matrix=task_matrix,
        models=models,
        benchmark_results=benchmark_results,
        capability_scores=capability_scores,
        task_realized_rows=task_realized_rows,
        occupation_realized_rows=occupation_realized_rows,
    )
    validate_snapshot(snapshot, schema_path)

    normalized_result_rows = []
    for row in benchmark_results:
        out = dict(row)
        out["result_quality_weight"] = f"{row['result_quality_weight']:.4f}"
        out["score_raw"] = f"{row['score_raw']:.4f}"
        out["score_normalized_100"] = f"{row['score_normalized_100']:.4f}"
        normalized_result_rows.append(out)

    capability_csv_rows = []
    for row in capability_scores:
        capability_csv_rows.append(
            {
                "snapshot_month": row["snapshot_month"],
                "model_id": row["model_id"],
                "capability_family_id": row["capability_family_id"],
                "capability_score_100": f"{row['capability_score_100']:.4f}",
                "coverage_weight": f"{row['coverage_weight']:.4f}",
                "benchmark_count": row["benchmark_count"],
                "contributing_benchmark_ids": "|".join(row["contributing_benchmark_ids"]),
            }
        )

    task_csv_rows = []
    for row in task_realized_rows:
        task_csv_rows.append(
            {
                "snapshot_month": row["snapshot_month"],
                "model_id": row["model_id"],
                "task_id": row["task_id"],
                "onet_task_text": row["onet_task_text"],
                "benchmark_observability": row["benchmark_observability"],
                "structural_exposure_100": f"{row['structural_exposure_100']:.4f}",
                "capability_fit_100": f"{row['capability_fit_100']:.4f}",
                "realized_exposure_100": f"{row['realized_exposure_100']:.4f}",
                "oc_100": f"{row['oc_100']:.4f}",
                "benchmark_coverage_ratio": f"{row['benchmark_coverage_ratio']:.4f}",
            }
        )

    occupation_csv_rows = []
    for row in occupation_realized_rows:
        occupation_csv_rows.append(
            {
                "snapshot_month": row["snapshot_month"],
                "model_id": row["model_id"],
                "occupation_code": row["occupation_code"],
                "occupation_label": row["occupation_label"],
                "realized_occupation_exposure_100": f"{row['realized_occupation_exposure_100']:.4f}",
                "weighted_dae_100": f"{row['weighted_dae_100']:.4f}",
                "weighted_se_100": f"{row['weighted_se_100']:.4f}",
                "weighted_oc_100": f"{row['weighted_oc_100']:.4f}",
                "weighted_ic_100": f"{row['weighted_ic_100']:.4f}",
                "benchmark_coverage_ratio": f"{row['benchmark_coverage_ratio']:.4f}",
                "included_task_count": row["included_task_count"],
            }
        )

    summary = {
        "snapshot_month": snapshot_month,
        "model_count": len(models),
        "benchmark_result_count": len(benchmark_results),
        "capability_score_count": len(capability_scores),
        "task_realized_exposure_count": len(task_realized_rows),
        "occupation_realized_exposure_count": len(occupation_realized_rows),
        "output_dir": str(output_dir),
    }

    write_json(output_dir / "dashboard_snapshot.json", snapshot)
    write_json(output_dir / "snapshot_summary.json", summary)
    write_csv(
        output_dir / "benchmark_results_normalized.csv",
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
            "official_source_url",
            "source_type",
            "result_quality_weight",
            "notes",
        ],
        normalized_result_rows,
    )
    write_csv(
        output_dir / "capability_scores.csv",
        [
            "snapshot_month",
            "model_id",
            "capability_family_id",
            "capability_score_100",
            "coverage_weight",
            "benchmark_count",
            "contributing_benchmark_ids",
        ],
        capability_csv_rows,
    )
    write_csv(
        output_dir / "task_realized_exposure.csv",
        [
            "snapshot_month",
            "model_id",
            "task_id",
            "onet_task_text",
            "benchmark_observability",
            "structural_exposure_100",
            "capability_fit_100",
            "realized_exposure_100",
            "oc_100",
            "benchmark_coverage_ratio",
        ],
        task_csv_rows,
    )
    write_csv(
        output_dir / "occupation_realized_exposure.csv",
        [
            "snapshot_month",
            "model_id",
            "occupation_code",
            "occupation_label",
            "realized_occupation_exposure_100",
            "weighted_dae_100",
            "weighted_se_100",
            "weighted_oc_100",
            "weighted_ic_100",
            "benchmark_coverage_ratio",
            "included_task_count",
        ],
        occupation_csv_rows,
    )


if __name__ == "__main__":
    main()
