# Project Management AI Exposure Index

This repository packages a research workflow and public dashboard for estimating how exposed project-management work is to agentic AI.

The project combines four layers:

- O*NET task data for occupation `15-1299.09` (`Project Management Specialists / Information Project Managers`)
- PMI-grounded evidence coding and task interdependence mapping
- a structural exposure index at the task and occupation level
- a monthly benchmark layer that converts public agentic AI results into realized exposure estimates by model

## Why This Repo Exists

Most AI exposure measures flatten work into isolated tasks. Project management is different: tasks are tightly coupled through plans, dependencies, reporting, governance, and change control.

This workflow treats exposure as both:

- `structural exposure`: how exposed a PM task is in principle, given its information-processing content and its position in the task network
- `realized exposure`: how much of that structural exposure is currently reachable by a specific model, based on public benchmark evidence

That split makes the dashboard updateable as new models and new benchmarks appear.

## Public Repo Contents

- reproducible workflow docs in [`llm_exposure_workflow`](./llm_exposure_workflow)
- prompt templates, JSON schemas, and scoring scripts
- O*NET pilot inputs used for the first occupation build
- dashboard ingestion, benchmark fetching, and monthly snapshot tooling
- a GitHub Pages-ready comparison site in [`docs`](./docs)
- generated benchmark and dashboard artifacts that can be audited directly

## Intentionally Excluded

This public repository does not redistribute:

- PMI standards or practice-guide PDFs
- academic paper PDFs collected during the research process
- raw extracted PMI text derived from copyrighted PDFs

Those materials remain local inputs only. The public repo includes the workflow, schemas, prompts, and derived outputs without republishing source documents.

## Current Pilot Scope

- Occupation: `15-1299.09`
- Task base: 21 O*NET tasks
- Structural layer: LLM-coded with human audit
- Benchmark layer: monthly snapshots from public agentic AI benchmarks
- Current example snapshot: `2026-04`

## Repository Map

- [`llm_exposure_workflow/README.md`](./llm_exposure_workflow/README.md): end-to-end exposure workflow
- [`llm_exposure_workflow/dashboard/README.md`](./llm_exposure_workflow/dashboard/README.md): monthly benchmark dashboard specification
- [`llm_exposure_workflow/dashboard/scripts/fetch_benchmark_results.py`](./llm_exposure_workflow/dashboard/scripts/fetch_benchmark_results.py): benchmark ingestion
- [`llm_exposure_workflow/dashboard/scripts/run_monthly_dashboard_snapshot.py`](./llm_exposure_workflow/dashboard/scripts/run_monthly_dashboard_snapshot.py): snapshot builder
- [`llm_exposure_workflow/dashboard/scripts/build_comparison_site.py`](./llm_exposure_workflow/dashboard/scripts/build_comparison_site.py): static comparison page data builder
- [`docs/index.html`](./docs/index.html): public comparison table page

## Quick Start

### 1. Build or refresh the structural PM layer

Keep the PMI source PDFs local in `PMI Standards/`, then run the workflow under [`llm_exposure_workflow/scripts`](./llm_exposure_workflow/scripts).

### 2. Refresh the monthly benchmark snapshot

```powershell
python llm_exposure_workflow/dashboard/scripts/fetch_benchmark_results.py --snapshot-month 2026-04
python llm_exposure_workflow/dashboard/scripts/run_monthly_dashboard_snapshot.py --snapshot-month 2026-04
```

### 3. Rebuild the public comparison page data

```powershell
python llm_exposure_workflow/dashboard/scripts/build_comparison_site.py --snapshot-month 2026-04
```

This updates the site data under [`docs/data`](./docs/data).

## Comparison Page

The repository includes a static comparison page that ranks models by realized project-management exposure and shows coverage metadata side by side.

- page source: [`docs/index.html`](./docs/index.html)
- generated data: [`docs/data/latest-comparison.json`](./docs/data/latest-comparison.json)
- downloadable table: [`docs/data/latest-comparison.csv`](./docs/data/latest-comparison.csv)
- frontier model page: [`docs/frontier-models.html`](./docs/frontier-models.html)
- frontier model data: [`docs/data/frontier-models.json`](./docs/data/frontier-models.json)
- deploy workflow: [`.github/workflows/deploy-pages.yml`](./.github/workflows/deploy-pages.yml)

The repository now includes a GitHub Pages deployment workflow. If GitHub Pages is enabled in the repository settings, pushes to `main` can publish the comparison page as a lightweight public dashboard.

## Notes For Readers

- Public benchmark coverage remains partial. A model can look weaker simply because it has fewer benchmark results in the current snapshot.
- Oversight criticality is intentionally kept separate from exposure. A task can be highly exposed while still requiring human approval or accountability.
- The current public model registry is conservative and keeps many benchmark-specific systems separate rather than collapsing them into a single vendor taxonomy.

## License

Code, schemas, prompts, and generated public artifacts in this repository are released under the [`MIT License`](./LICENSE), except for third-party source materials that are intentionally excluded from version control.
