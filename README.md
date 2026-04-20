# PMI-Grounded Agentic AI Exposure Dashboard for Project Management

This repository contains a workflow for estimating exposure of project-management work to agentic AI using:

- O*NET task data for `15-1299.09`,
- PMI-grounded task interdependence coding,
- a task graph and exposure index,
- and a monthly benchmark dashboard that maps public agentic model performance into realized project-management exposure.

## What Is Included

- the reproducible workflow in [`llm_exposure_workflow`](./llm_exposure_workflow),
- O*NET occupation input folders used for the pilot,
- prompt templates, schemas, scoring scripts, and dashboard scripts,
- benchmark fetch and snapshot tooling,
- and current generated dashboard artifacts.

## What Is Not Included

This public repository intentionally excludes:

- PMI standards and practice-guide PDFs,
- academic paper PDFs collected during the research process,
- and raw extracted PMI text generated from those PDFs.

Those materials remain local inputs only. The repository keeps the workflow, metadata, and derived analysis layer without redistributing copyrighted source files.

## Workflow Overview

The main workflow is documented in [`llm_exposure_workflow/README.md`](./llm_exposure_workflow/README.md).

High-level sequence:

1. Canonicalize O*NET inputs.
2. Chunk and tag PMI evidence locally.
3. Build task profiles, direct-exposure scores, dependency edges, and audit artifacts.
4. Compute task and occupation exposure scores.
5. Fetch benchmark results monthly.
6. Generate realized exposure snapshots by model and month.

## Dashboard Layer

The benchmark dashboard layer lives in [`llm_exposure_workflow/dashboard`](./llm_exposure_workflow/dashboard).

Key files:

- dashboard spec: [`llm_exposure_workflow/dashboard/README.md`](./llm_exposure_workflow/dashboard/README.md)
- fetch registry: [`llm_exposure_workflow/dashboard/benchmark_fetch_registry.json`](./llm_exposure_workflow/dashboard/benchmark_fetch_registry.json)
- fetcher: [`llm_exposure_workflow/dashboard/scripts/fetch_benchmark_results.py`](./llm_exposure_workflow/dashboard/scripts/fetch_benchmark_results.py)
- snapshot runner: [`llm_exposure_workflow/dashboard/scripts/run_monthly_dashboard_snapshot.py`](./llm_exposure_workflow/dashboard/scripts/run_monthly_dashboard_snapshot.py)

## Quick Start

### 1. Rebuild the PMI-grounded structural layer locally

Keep the PMI PDFs in a local `PMI Standards/` folder and run the workflow scripts under `llm_exposure_workflow/scripts`.

### 2. Update monthly benchmark coverage

Run:

```powershell
python llm_exposure_workflow/dashboard/scripts/fetch_benchmark_results.py --snapshot-month 2026-04
python llm_exposure_workflow/dashboard/scripts/run_monthly_dashboard_snapshot.py --snapshot-month 2026-04
```

### 3. Review outputs

- resolved benchmark rows: `llm_exposure_workflow/dashboard/input/benchmark_results.csv`
- fetch audit log: `llm_exposure_workflow/dashboard/output/fetch/<snapshot-month>/fetch_log.json`
- monthly snapshot: `llm_exposure_workflow/dashboard/output/<snapshot-month>/dashboard_snapshot.json`

## Notes

- The current benchmark fetcher automates the sources with stable live adapters and supports manual fallback for the rest.
- The first-pass model registry intentionally uses conservative exact alias matching.
- Public benchmark coverage is still weaker for high-judgment PM tasks like negotiation, authority, and accountability.
