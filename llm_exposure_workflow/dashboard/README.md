# Dashboard Spec

## Purpose

This folder defines the data layer for a monthly dashboard that compares the PMI-grounded project management exposure index against live agentic AI benchmark performance.

The design separates:

- a stable `structural` layer based on the O*NET plus PMI coding already produced in this project,
- a monthly `capability` layer based on benchmark results for specific models,
- and a derived `realized exposure` layer that combines the two.

## Files

- `dashboard_snapshot.schema.json`: schema for one monthly snapshot file
- `benchmark_capability_matrix.csv`: exact benchmark-to-capability mapping
- `task_capability_matrix.csv`: exact task-to-capability mapping for the 21 O*NET tasks
- `benchmark_fetch_registry.json`: source-by-source fetch adapter registry
- `scripts/run_monthly_dashboard_snapshot.py`: monthly ingestion and scoring runner
- `scripts/fetch_benchmark_results.py`: benchmark fetcher with alias resolution and manual fallback
- `input/models.csv`: starter model registry input
- `input/benchmark_results.csv`: starter benchmark result input
- `input/model_aliases.csv`: alias map from source leaderboard names to canonical `model_id`
- `input/manual_benchmark_results.csv`: manual rows for benchmarks without stable public feeds
- `examples/example_models.csv`: example model registry
- `examples/example_benchmark_results.csv`: example benchmark results
- `frontier_model_registry.json`: curated frontier-model family registry for the second comparison view
- `scripts/build_frontier_model_view.py`: builder for the frontier-model family benchmark and public webpage data

## Capability Families

Use the following capability families consistently across benchmarks and tasks:

- `research`: search, retrieval, evidence gathering, source comparison
- `synthesis_reporting`: summarization, explanation, comparison, management writeups
- `planning_orchestration`: decomposition, sequencing, scheduling, allocation, replanning
- `tool_use`: reliable function calling, API invocation, application feature use
- `workflow_execution`: end-to-end multi-step execution that changes system state
- `computer_use`: direct GUI or browser or desktop interaction
- `policy_compliance`: following rules, constraints, approvals, escalation logic, governance
- `technical_execution`: code, terminal, configuration, implementation-heavy work

## Primary Benchmarks

These should drive the monthly dashboard first:

- `gaia`
- `bfcl_v4`
- `webarena_verified`
- `osworld_verified`
- `tau3_bench`

## Secondary Benchmarks

These are useful but should not dominate the PM dashboard:

- `browsecomp`
- `swe_bench_verified`
- `terminal_bench_2`

## Formula Layer

### 1. Normalize benchmark scores

Convert all incoming scores to a `0-100` scale:

- if the source is already a percentage, keep it as-is
- if the source is `0-1`, multiply by `100`
- if the source is pass@k, use the chosen pass metric consistently and record it in `metric_name`

### 2. Compute model capability scores

For model `m`, month `t`, capability family `f`:

```text
CapabilityScore(m,t,f) =
  sum_b [ NormalizedScore(m,t,b)
          * BenchmarkCapabilityWeight(b,f)
          * DashboardWeight(b)
          * ResultQualityWeight(m,t,b) ]
  /
  sum_b [ BenchmarkCapabilityWeight(b,f)
          * DashboardWeight(b)
          * ResultQualityWeight(m,t,b) ]
```

Recommended result quality weights:

- `official_leaderboard`: `1.00`
- `official_dataset`: `0.95`
- `official_paper`: `0.90`
- `third_party_reproduction`: `0.85`
- `vendor_report`: `0.75`
- `self_reported`: `0.60`

### 3. Compute task capability fit

For task `i`, model `m`, month `t`:

```text
CapabilityFit(i,m,t) =
  sum_f [ TaskCapabilityWeight(i,f) * CapabilityScore(m,t,f) ]
```

Because the task matrix rows sum to `1.0`, no extra denominator is needed.

### 4. Compute realized task exposure

Use the existing structural task scores from `output/task_scores.csv`.

Recommended structural baseline:

```text
StructuralExposure(i) = 0.50 * DAE_i + 0.50 * SE_i
```

Then:

```text
RealizedExposure(i,m,t) =
  StructuralExposure(i) * CapabilityFit(i,m,t) / 100
```

Keep `OC` separate as an interpretive constraint, not as a direct penalty.

### 5. Compute realized occupation exposure

```text
RealizedOccupationExposure(m,t) =
  sum_i [ ImportanceWeight_i * RealizedExposure(i,m,t) ]
```

## Versioning Rules

- Never merge benchmark results across incompatible benchmark versions without a new `comparability_group`.
- Treat `osworld` and `osworld_verified` as different comparability groups.
- Treat `tau_bench`, `tau2_bench`, and `tau3_bench` as different comparability groups.
- Treat `swe_bench_verified` results from materially different evaluation scaffolds as separate variants.

## Monthly Update Rule

Each monthly snapshot should contain:

- the capability family list,
- the frozen benchmark matrix used that month,
- the frozen task matrix used that month,
- model registry entries for the models included,
- benchmark results with provenance,
- derived capability scores,
- task-level realized exposure,
- occupation-level realized exposure.

Do not overwrite prior months. Add a new snapshot for each month.

## Fetcher

The benchmark fetcher is:

- [fetch_benchmark_results.py](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/scripts/fetch_benchmark_results.py)

Fetcher config and inputs:

- [benchmark_fetch_registry.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/benchmark_fetch_registry.json)
- [model_aliases.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/input/model_aliases.csv)
- [manual_benchmark_results.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/input/manual_benchmark_results.csv)

Current fetch design:

- automated live adapters:
  - `gaia` via Hugging Face public results dataset
  - `terminal_bench_2` via the official leaderboard HTML
- manual-source adapters for now:
  - `bfcl_v4`
  - `webarena_verified`
  - `osworld_verified`
  - `tau3_bench`
  - `browsecomp`
  - `swe_bench_verified`

The fetcher writes:

- resolved results to [benchmark_results.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/input/benchmark_results.csv)
- raw fetched rows to `dashboard/output/fetch/<snapshot-month>/raw_source_rows.csv`
- unresolved source names to `dashboard/output/fetch/<snapshot-month>/unresolved_source_rows.csv`
- a source-by-source status log to `dashboard/output/fetch/<snapshot-month>/fetch_log.json`

Recommended monthly sequence:

1. Add canonical models to [models.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/input/models.csv).
2. Add known leaderboard name mappings to [model_aliases.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/input/model_aliases.csv).
3. Add manual rows for non-automated benchmarks to [manual_benchmark_results.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/input/manual_benchmark_results.csv).
4. Run the fetcher.
5. Review `unresolved_source_rows.csv` and add any new aliases.
6. Rerun the fetcher until the resolved coverage is acceptable.
7. Run the monthly snapshot generator.

Example fetch command:

```powershell
python llm_exposure_workflow/dashboard/scripts/fetch_benchmark_results.py `
  --snapshot-month 2026-04
```

## Runner

The monthly ingestion runner is:

- [run_monthly_dashboard_snapshot.py](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/scripts/run_monthly_dashboard_snapshot.py)

Default inputs:

- [models.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/input/models.csv)
- [benchmark_results.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/input/benchmark_results.csv)

Example inputs:

- [example_models.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/examples/example_models.csv)
- [example_benchmark_results.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/examples/example_benchmark_results.csv)

Example command:

```powershell
python llm_exposure_workflow/dashboard/scripts/run_monthly_dashboard_snapshot.py `
  --snapshot-month 2026-04 `
  --models llm_exposure_workflow/dashboard/examples/example_models.csv `
  --benchmark-results llm_exposure_workflow/dashboard/examples/example_benchmark_results.csv
```

Default output location:

- `llm_exposure_workflow/dashboard/output/<snapshot-month>/`

Generated files per month:

- `dashboard_snapshot.json`
- `snapshot_summary.json`
- `benchmark_results_normalized.csv`
- `capability_scores.csv`
- `task_realized_exposure.csv`
- `occupation_realized_exposure.csv`

## Interpretation Rule

This dashboard estimates exposure conditional on the currently observed public benchmark capability of a model family. It does not estimate certain automation, labor displacement, or replacement of human accountability.

Interpersonal project work such as negotiation, authority, and accountability remains only partially observed by public agentic benchmarks, so low benchmark coverage should be displayed explicitly.
