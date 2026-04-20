from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from run_monthly_dashboard_snapshot import (
    CAPABILITY_IDS,
    build_snapshot,
    clean_str,
    compute_capability_scores,
    compute_occupation_realized_exposure,
    compute_task_realized_exposure,
    load_benchmark_matrix,
    load_benchmark_results,
    load_json,
    load_models,
    load_task_matrix,
    load_task_scores,
    validate_snapshot,
    validate_snapshot_month,
    write_csv,
    write_json,
)


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.lower())).strip()


def load_registry(path: Path) -> tuple[dict, list[dict]]:
    registry = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for item in registry.get("frontier_models", []):
        frontier_model_id = clean_str(item.get("frontier_model_id"))
        if not frontier_model_id:
            continue
        include_terms = [normalize_text(clean_str(term)) for term in item.get("include_terms", []) if clean_str(term)]
        rows.append(
            {
                "frontier_model_id": frontier_model_id,
                "display_name": clean_str(item.get("display_name")) or frontier_model_id,
                "provider": clean_str(item.get("provider")) or "Unknown",
                "include_terms": include_terms,
                "notes": clean_str(item.get("notes")),
            }
        )
    if not rows:
        raise ValueError(f"No frontier model rows found in {path}")
    return registry, rows


def build_parser() -> argparse.ArgumentParser:
    script_path = Path(__file__).resolve()
    dashboard_dir = script_path.parent.parent
    input_dir = dashboard_dir / "input"
    repo_root = dashboard_dir.parent.parent
    parser = argparse.ArgumentParser(
        description="Build a frontier LLM model view by collapsing public benchmark systems into model families.",
    )
    parser.add_argument("--snapshot-month", required=True, help="Snapshot month in YYYY-MM format.")
    parser.add_argument(
        "--models",
        default=str(input_dir / "models.csv"),
        help="Path to the full model registry CSV. Defaults to dashboard/input/models.csv.",
    )
    parser.add_argument(
        "--benchmark-results",
        default=str(input_dir / "benchmark_results.csv"),
        help="Path to benchmark results CSV. Defaults to dashboard/input/benchmark_results.csv.",
    )
    parser.add_argument(
        "--registry",
        default=str(dashboard_dir / "frontier_model_registry.json"),
        help="Path to the frontier model registry JSON.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional output directory. Defaults to dashboard/output/<snapshot-month>/frontier_models/.",
    )
    parser.add_argument(
        "--docs-dir",
        default=str(repo_root / "docs"),
        help="Docs directory for GitHub Pages data output. Defaults to repo_root/docs.",
    )
    return parser


def resolve_frontier_matches(
    *,
    models: list[dict],
    benchmark_results: list[dict],
    registry_rows: list[dict],
) -> tuple[list[dict], list[dict]]:
    models_by_id = {row["model_id"]: row for row in models}
    matches = []
    unmatched_results = []

    for result in benchmark_results:
        model = models_by_id[result["model_id"]]
        search_fields = [
            normalize_text(model["display_name"]),
            normalize_text(model["model_id"]),
        ]
        matched_registry = None
        matched_term = ""
        for registry_row in registry_rows:
            for include_term in registry_row["include_terms"]:
                if include_term and any(include_term in field for field in search_fields):
                    matched_registry = registry_row
                    matched_term = include_term
                    break
            if matched_registry:
                break

        if not matched_registry:
            unmatched_results.append(
                {
                    "snapshot_month": result["snapshot_month"],
                    "source_model_id": result["model_id"],
                    "source_display_name": model["display_name"],
                    "provider": model["provider"],
                    "benchmark_id": result["benchmark_id"],
                    "benchmark_variant": result["benchmark_variant"],
                }
            )
            continue

        matches.append(
            {
                "snapshot_month": result["snapshot_month"],
                "frontier_model_id": matched_registry["frontier_model_id"],
                "frontier_display_name": matched_registry["display_name"],
                "frontier_provider": matched_registry["provider"],
                "frontier_notes": matched_registry["notes"],
                "matching_term": matched_term,
                "source_model_id": result["model_id"],
                "source_display_name": model["display_name"],
                "source_provider": model["provider"],
                "benchmark_id": result["benchmark_id"],
                "benchmark_variant": result["benchmark_variant"],
                "comparability_group": result["comparability_group"],
                "metric_name": result["metric_name"],
                "metric_unit": result["metric_unit"],
                "score_raw": result["score_raw"],
                "score_normalized_100": result["score_normalized_100"],
                "score_date": result["score_date"],
                "source_url": result["source_url"],
                "official_source_url": result["official_source_url"],
                "source_type": result["source_type"],
                "result_quality_weight": result["result_quality_weight"],
                "scaffold_type": clean_str(result.get("scaffold_type")),
                "notes": clean_str(result.get("notes")),
            }
        )

    return matches, unmatched_results


def select_best_rows(matches: list[dict]) -> list[dict]:
    best_by_key: dict[tuple[str, str, str], dict] = {}
    for row in matches:
        key = (row["frontier_model_id"], row["benchmark_id"], row["benchmark_variant"])
        current = best_by_key.get(key)
        if current is None:
            best_by_key[key] = row
            continue
        candidate_key = (
            row["score_normalized_100"],
            row["result_quality_weight"],
            row["source_display_name"].lower(),
            row["source_model_id"],
        )
        current_key = (
            current["score_normalized_100"],
            current["result_quality_weight"],
            current["source_display_name"].lower(),
            current["source_model_id"],
        )
        if candidate_key > current_key:
            best_by_key[key] = row
    return list(best_by_key.values())


def build_frontier_models(
    *,
    registry_rows: list[dict],
    selected_rows: list[dict],
) -> list[dict]:
    selected_ids = {row["frontier_model_id"] for row in selected_rows}
    models = []
    for row in registry_rows:
        if row["frontier_model_id"] not in selected_ids:
            continue
        models.append(
            {
                "model_id": row["frontier_model_id"],
                "display_name": row["display_name"],
                "provider": row["provider"],
                "notes": row["notes"] or "Frontier model family built from matched public benchmark systems.",
            }
        )
    if not models:
        raise ValueError("No frontier model families were resolved from the current snapshot.")
    return models


def build_frontier_benchmark_results(selected_rows: list[dict]) -> list[dict]:
    output_rows = []
    for row in selected_rows:
        note_prefix = (
            f"Best observed public system for {row['frontier_display_name']} on {row['benchmark_id']}: "
            f"{row['source_display_name']} ({row['source_model_id']})."
        )
        note_suffix = f" {row['notes']}" if row.get("notes") else ""
        output_rows.append(
            {
                "snapshot_month": row["snapshot_month"],
                "model_id": row["frontier_model_id"],
                "benchmark_id": row["benchmark_id"],
                "benchmark_variant": row["benchmark_variant"],
                "comparability_group": row["comparability_group"],
                "metric_name": row["metric_name"],
                "metric_unit": row["metric_unit"],
                "score_raw": row["score_raw"],
                "score_normalized_100": row["score_normalized_100"],
                "score_date": row["score_date"],
                "scaffold_type": row["scaffold_type"] or "frontier_family_best_public_system",
                "source_url": row["source_url"],
                "official_source_url": row["official_source_url"],
                "source_type": row["source_type"],
                "result_quality_weight": row["result_quality_weight"],
                "notes": f"{note_prefix}{note_suffix}",
            }
        )
    return output_rows


def build_frontier_site_payload(
    *,
    snapshot_month: str,
    docs_repo_name: str,
    occupation_scores: dict,
    occupation_realized_rows: list[dict],
    matches: list[dict],
    selected_rows: list[dict],
    task_count: int,
) -> tuple[dict, list[dict]]:
    matches_by_frontier: dict[str, list[dict]] = defaultdict(list)
    selected_by_frontier: dict[str, list[dict]] = defaultdict(list)
    for row in matches:
        matches_by_frontier[row["frontier_model_id"]].append(row)
    for row in selected_rows:
        selected_by_frontier[row["frontier_model_id"]].append(row)

    rows = []
    for row in occupation_realized_rows:
        frontier_id = row["model_id"]
        selected = sorted(selected_by_frontier.get(frontier_id, []), key=lambda item: item["benchmark_id"])
        matched = matches_by_frontier.get(frontier_id, [])
        best_systems = [f"{item['benchmark_id']}: {item['source_display_name']}" for item in selected]
        benchmarks = sorted({item["benchmark_id"] for item in selected})
        rows.append(
            {
                "frontier_model_id": frontier_id,
                "display_name": next((item["frontier_display_name"] for item in selected), frontier_id),
                "provider": next((item["frontier_provider"] for item in selected), "Unknown"),
                "realized_occupation_exposure_100": round(row["realized_occupation_exposure_100"], 4),
                "benchmark_coverage_ratio": round(row["benchmark_coverage_ratio"], 4),
                "benchmark_count": len(benchmarks),
                "benchmarks": benchmarks,
                "selected_systems": best_systems,
                "source_system_count": len({item["source_model_id"] for item in matched}),
                "selected_system_count": len({item["source_model_id"] for item in selected}),
                "notes": next((item["frontier_notes"] for item in selected if item["frontier_notes"]), ""),
            }
        )

    rows.sort(
        key=lambda item: (
            -float(item["realized_occupation_exposure_100"]),
            -float(item["benchmark_coverage_ratio"]),
            str(item["display_name"]).lower(),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["rank"] = index

    exposure_values = [float(row["realized_occupation_exposure_100"]) for row in rows]
    coverage_values = [float(row["benchmark_coverage_ratio"]) for row in rows]
    top_row = rows[0]
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "snapshot_month": snapshot_month,
        "repo_name": docs_repo_name,
        "view_type": "frontier_model_families",
        "methodology": {
            "aggregation_rule": "For each frontier model family and benchmark, keep the highest-scoring matched public system entry in the current snapshot, then recompute the PM exposure scores from those family-level benchmark rows.",
            "caution": "This is a best-observed public-system view of underlying model families, not a scaffold-neutral laboratory comparison.",
        },
        "occupation": {
            "occupation_code": clean_str(occupation_scores["occupation_code"]),
            "occupation_label": clean_str(occupation_scores["occupation_label"]),
            "weighted_dae_100": round(occupation_scores["Occupation_DAE"], 2),
            "weighted_se_100": round(occupation_scores["Occupation_SE"], 2),
            "weighted_oc_100": round(occupation_scores["Occupation_OC"], 2),
            "weighted_ic_100": round(occupation_scores["Occupation_IC"], 2),
            "included_task_count": task_count,
        },
        "summary": {
            "tracked_model_count": len(rows),
            "matched_source_system_count": len({row["source_model_id"] for row in matches}),
            "selected_benchmark_row_count": len(selected_rows),
            "provider_count": len({clean_str(row["provider"]) for row in rows}),
            "top_model": {
                "frontier_model_id": top_row["frontier_model_id"],
                "display_name": top_row["display_name"],
                "provider": top_row["provider"],
                "realized_occupation_exposure_100": top_row["realized_occupation_exposure_100"],
            },
            "median_realized_occupation_exposure_100": round(statistics.median(exposure_values), 4),
            "mean_benchmark_coverage_ratio": round(statistics.fmean(coverage_values), 4),
        },
        "rows": rows,
    }
    return payload, rows


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    snapshot_month = clean_str(args.snapshot_month)
    validate_snapshot_month(snapshot_month)

    script_path = Path(__file__).resolve()
    dashboard_dir = script_path.parent.parent
    workflow_dir = dashboard_dir.parent
    repo_root = workflow_dir.parent
    structural_output_dir = workflow_dir / "output"
    output_dir = Path(args.output_dir) if args.output_dir else dashboard_dir / "output" / snapshot_month / "frontier_models"
    docs_dir = Path(args.docs_dir)
    docs_data_dir = docs_dir / "data"

    benchmark_matrix_path = dashboard_dir / "benchmark_capability_matrix.csv"
    task_matrix_path = dashboard_dir / "task_capability_matrix.csv"
    schema_path = dashboard_dir / "dashboard_snapshot.schema.json"
    task_scores_path = structural_output_dir / "task_scores.csv"
    occupation_scores_path = structural_output_dir / "occupation_scores.json"

    benchmark_matrix, benchmark_lookup = load_benchmark_matrix(benchmark_matrix_path)
    task_matrix = load_task_matrix(task_matrix_path)
    all_models, model_lookup = load_models(Path(args.models))
    all_benchmark_results = load_benchmark_results(
        Path(args.benchmark_results),
        snapshot_month=snapshot_month,
        model_lookup=model_lookup,
        benchmark_lookup=benchmark_lookup,
    )
    task_scores = load_task_scores(task_scores_path)
    occupation_scores = load_json(occupation_scores_path)
    registry_meta, registry_rows = load_registry(Path(args.registry))

    matches, unmatched_results = resolve_frontier_matches(
        models=all_models,
        benchmark_results=all_benchmark_results,
        registry_rows=registry_rows,
    )
    if not matches:
        raise ValueError("No frontier matches were resolved from the current benchmark results.")

    selected_rows = select_best_rows(matches)
    frontier_models = build_frontier_models(registry_rows=registry_rows, selected_rows=selected_rows)
    frontier_benchmark_results = build_frontier_benchmark_results(selected_rows)

    capability_scores = compute_capability_scores(frontier_models, frontier_benchmark_results, benchmark_lookup)
    task_realized_rows = compute_task_realized_exposure(
        snapshot_month=snapshot_month,
        models=frontier_models,
        capability_scores=capability_scores,
        task_matrix=task_matrix,
        task_scores=task_scores,
    )
    occupation_realized_rows = compute_occupation_realized_exposure(
        snapshot_month=snapshot_month,
        models=frontier_models,
        task_scores=task_scores,
        task_realized_rows=task_realized_rows,
        occupation_scores=occupation_scores,
    )

    snapshot = build_snapshot(
        snapshot_month=snapshot_month,
        benchmark_matrix=benchmark_matrix,
        task_matrix=task_matrix,
        models=frontier_models,
        benchmark_results=frontier_benchmark_results,
        capability_scores=capability_scores,
        task_realized_rows=task_realized_rows,
        occupation_realized_rows=occupation_realized_rows,
    )
    snapshot["schema_version"] = "frontier-1.0.0"
    snapshot["notes"] = (
        "Frontier model family view generated by build_frontier_model_view.py using the best observed "
        "public system per benchmark for each curated model family."
    )
    validate_snapshot(snapshot, schema_path)

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "frontier_model_snapshot.json", snapshot)
    write_json(output_dir / "frontier_model_registry.json", registry_meta)
    write_csv(
        output_dir / "frontier_model_source_matches.csv",
        fieldnames=[
            "snapshot_month",
            "frontier_model_id",
            "frontier_display_name",
            "frontier_provider",
            "matching_term",
            "source_model_id",
            "source_display_name",
            "source_provider",
            "benchmark_id",
            "benchmark_variant",
            "score_normalized_100",
            "result_quality_weight",
            "selected_for_frontier",
        ],
        rows=[
            {
                "snapshot_month": row["snapshot_month"],
                "frontier_model_id": row["frontier_model_id"],
                "frontier_display_name": row["frontier_display_name"],
                "frontier_provider": row["frontier_provider"],
                "matching_term": row["matching_term"],
                "source_model_id": row["source_model_id"],
                "source_display_name": row["source_display_name"],
                "source_provider": row["source_provider"],
                "benchmark_id": row["benchmark_id"],
                "benchmark_variant": row["benchmark_variant"],
                "score_normalized_100": f"{row['score_normalized_100']:.4f}",
                "result_quality_weight": f"{row['result_quality_weight']:.4f}",
                "selected_for_frontier": "yes"
                if any(
                    selected["frontier_model_id"] == row["frontier_model_id"]
                    and selected["benchmark_id"] == row["benchmark_id"]
                    and selected["benchmark_variant"] == row["benchmark_variant"]
                    and selected["source_model_id"] == row["source_model_id"]
                    for selected in selected_rows
                )
                else "no",
            }
            for row in matches
        ],
    )
    write_csv(
        output_dir / "frontier_model_unmatched_rows.csv",
        fieldnames=[
            "snapshot_month",
            "source_model_id",
            "source_display_name",
            "provider",
            "benchmark_id",
            "benchmark_variant",
        ],
        rows=unmatched_results,
    )
    write_csv(
        output_dir / "frontier_model_benchmark_results.csv",
        fieldnames=[
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
        rows=[
            {
                **row,
                "score_raw": f"{row['score_raw']:.4f}",
                "score_normalized_100": f"{row['score_normalized_100']:.4f}",
                "result_quality_weight": f"{row['result_quality_weight']:.4f}",
            }
            for row in frontier_benchmark_results
        ],
    )
    write_csv(
        output_dir / "frontier_model_occupation_realized_exposure.csv",
        fieldnames=[
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
        rows=[
            {
                **row,
                "realized_occupation_exposure_100": f"{row['realized_occupation_exposure_100']:.4f}",
                "weighted_dae_100": f"{row['weighted_dae_100']:.4f}",
                "weighted_se_100": f"{row['weighted_se_100']:.4f}",
                "weighted_oc_100": f"{row['weighted_oc_100']:.4f}",
                "weighted_ic_100": f"{row['weighted_ic_100']:.4f}",
                "benchmark_coverage_ratio": f"{row['benchmark_coverage_ratio']:.4f}",
            }
            for row in occupation_realized_rows
        ],
    )

    site_payload, site_rows = build_frontier_site_payload(
        snapshot_month=snapshot_month,
        docs_repo_name="Project-Management-AI-Exposure-Index",
        occupation_scores=occupation_scores,
        occupation_realized_rows=occupation_realized_rows,
        matches=matches,
        selected_rows=selected_rows,
        task_count=len(task_scores),
    )

    write_json(docs_data_dir / "frontier-models.json", site_payload)
    (docs_data_dir / "frontier-models.js").write_text(
        "window.PM_FRONTIER_MODEL_DATA = "
        + json.dumps(site_payload, indent=2, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    write_csv(
        docs_data_dir / "frontier-models.csv",
        fieldnames=[
            "rank",
            "frontier_model_id",
            "display_name",
            "provider",
            "realized_occupation_exposure_100",
            "benchmark_coverage_ratio",
            "benchmark_count",
            "benchmarks",
            "selected_systems",
            "source_system_count",
            "selected_system_count",
            "notes",
        ],
        rows=[
            {
                **row,
                "benchmarks": ", ".join(row["benchmarks"]),
                "selected_systems": " | ".join(row["selected_systems"]),
            }
            for row in site_rows
        ],
    )

    print(f"Built frontier model view for snapshot {snapshot_month}")
    print(f"Frontier families: {len(frontier_models)}")
    print(f"Matched source systems: {len({row['source_model_id'] for row in matches})}")
    print(f"Selected benchmark rows: {len(selected_rows)}")
    print(f"Site JSON: {docs_data_dir / 'frontier-models.json'}")


if __name__ == "__main__":
    main()
