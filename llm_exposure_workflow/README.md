# LLM Workflow Spec for a PMI-Grounded Agentic AI Exposure Index

## Purpose

This workflow operationalizes a fully LLM-coded pilot index for the O*NET occupation `15-1299.09` using:

- the 21 O*NET tasks in the project manager folders,
- the linked O*NET DWAs, skills, and knowledge items,
- PMI standards and practice guides in the `PMI Standards` folder,
- and a human audit step after LLM coding.

The workflow is designed so that all substantive coding is done by an LLM, while the human reviewer audits outputs rather than hand-coding from scratch.

## Scope and Assumptions

- Treat `Information Project Managers` and `Project Manager` as one canonical occupation corpus for this pilot because the local O*NET files are duplicates of the same `15-1299.09` bundle.
- Use the 21 O*NET tasks as the primary unit of analysis.
- Use PMI text as the normative source for interdependence, governance, artifacts, and management logic.
- Keep the existing field name `standard_source` for backward compatibility even when the source is a practice guide.
- Use academic literature to justify the measurement strategy, not to override the PMI-grounded graph.
- Interpret `exposure` as potential for agentic AI assistance or execution, not as realized displacement or job loss.

## Output Files

Recommended output files for one full run:

- `source_registry.json`
- `output/pmi_chunks.jsonl`
- `output/task_profiles.jsonl`
- `output/direct_exposure.jsonl`
- `output/task_dependencies.jsonl`
- `output/adjudications.jsonl`
- `output/task_scores.csv`
- `output/occupation_scores.json`
- `output/graph_edges.csv`

## Recommended Model Settings

- Temperature: `0`
- Top-p: `1`
- Max output tokens: high enough to return full JSON
- Response format: strict JSON when supported
- One record per call for dependency extraction if you want tighter control

## Workflow

### Step 0. Canonicalize the Inputs

Build one canonical task table with these fields:

- `task_id`: `T01` to `T21`
- `onet_task_text`
- `onet_importance`
- `onet_category`

Build supporting tables for:

- DWAs
- skills
- knowledge

Do not duplicate tasks across the two occupation folders.

### Step 1. Chunk and Tag PMI Evidence

Convert each PMI PDF into text and chunk into stable, reviewable units.

Use the canonical source registry:

- [source_registry.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/source_registry.json)
- [chunking_manifest.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/chunking_manifest.json)

The registry defines:

- stable `source_id` values,
- preferred filenames,
- duplicate handling,
- ingest order,
- and coverage hints for retrieval and prompt routing.

The chunking manifest defines:

- source inclusion for Step 1,
- chunking defaults,
- cleanup rules,
- output file targets,
- and exact duplicate-skip behavior.

Chunk rules:

- Preferred chunk size: 400 to 900 words
- Preserve section boundaries when possible
- Assign stable IDs such as:
  - `program_p064_c01`
  - `portfolio_p021_c02`
  - `evm_p017_c01`
  - `agile_pg_p042_c01`
  - `requirements_pg_p118_c01`
  - `wbs_pg_p077_c01`

Each chunk should then be LLM-tagged with:

- PMI domain tags
- artifact tags
- action verbs
- summary

Recommended `standard_source` IDs:

- `program`
- `portfolio`
- `evm`
- `agile_pg`
- `ba_practice`
- `benefits_pg`
- `estimating_pg`
- `scheduling_pg`
- `wbs_pg`
- `requirements_pg`
- `risk_practice`
- `risk_standard`

Use:

- [01_pmi_chunk_tagging.md](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/prompts/01_pmi_chunk_tagging.md)
- [pmi_evidence_chunk.schema.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/schemas/pmi_evidence_chunk.schema.json)

### Step 2. LLM Task Profiling

For each O*NET task, have the LLM map the task into PMI logic and project-work structure.

The model should identify:

- functional mode,
- likely PMI domain mappings,
- likely inputs,
- likely outputs,
- likely artifacts,
- likely upstream tasks,
- likely downstream tasks.

Use:

- [02_task_profile.md](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/prompts/02_task_profile.md)
- [task_profile.schema.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/schemas/task_profile.schema.json)

### Step 3. LLM Direct Exposure Coding

For each task, the model scores five direct-exposure dimensions and four oversight dimensions.

Direct exposure dimensions:

- `information_gathering`
- `synthesis_reporting`
- `planning_orchestration`
- `monitoring_exception_detection`
- `tool_mediated_execution`

Oversight dimensions:

- `stakeholder_judgment`
- `negotiation_persuasion`
- `approval_authority`
- `accountability_risk_ownership`

Use:

- [03_direct_exposure.md](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/prompts/03_direct_exposure.md)
- [direct_exposure.schema.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/schemas/direct_exposure.schema.json)

### Step 4. LLM Pairwise Dependency Coding

For every ordered task pair `(A, B)`, ask whether Task A materially affects Task B.

Recommended relation types:

- `depends_on`
- `enables`
- `informs`
- `constrains`
- `monitors`
- `changes`
- `communicates_with`
- `none`

Recommended strength scale:

- `0` = no meaningful dependency
- `1` = weak contextual relationship
- `2` = moderate functional relationship
- `3` = strong operational relationship
- `4` = critical gating relationship

Use:

- [04_task_pair_dependency.md](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/prompts/04_task_pair_dependency.md)
- [task_pair_dependency.schema.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/schemas/task_pair_dependency.schema.json)

### Step 5. LLM Adjudication Pass

Run a fifth pass only on problematic records:

- confidence below `0.75`,
- missing PMI evidence IDs,
- contradictions across earlier passes,
- strong edges involving high-importance tasks,
- or reviewer-flagged records.

Use:

- [05_adjudication.md](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/prompts/05_adjudication.md)
- [adjudication.schema.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/schemas/adjudication.schema.json)

### Step 6. Build the Graph

Graph nodes:

- `Task`
- `DWA`
- `Skill`
- `Knowledge`
- `PMI_Domain`
- `PMI_Artifact`

Graph edges:

- `requires`
- `produces`
- `informs`
- `monitors`
- `changes`
- `constrains`
- `depends_on`
- `communicates_with`

For the task-to-task graph used in scoring, use only the directed dependency edges from Step 4.

### Step 7. Compute the Four Index Components

All final component scores are on a `0-100` scale.

## Exact Formulas

### Notation

For task `t`:

- `IG_t` = information gathering score, `0-4`
- `SR_t` = synthesis/reporting score, `0-4`
- `PO_t` = planning/orchestration score, `0-4`
- `MD_t` = monitoring/exception detection score, `0-4`
- `TE_t` = tool-mediated execution score, `0-4`

- `SJ_t` = stakeholder judgment score, `0-4`
- `NP_t` = negotiation/persuasion score, `0-4`
- `AA_t` = approval authority score, `0-4`
- `AR_t` = accountability/risk ownership score, `0-4`

For directed edge from task `i` to task `j`:

- `strength_ij` = dependency strength, `0-4`
- `confidence_ij` = LLM confidence, `0-1`

For task importance:

- `I_t` = O*NET importance score
- `w_t = I_t / sum(I_k for all tasks k)`

### 1. Direct Agentic Exposure

Direct Agentic Exposure for task `t`:

`DAE_t = 100 * (IG_t + SR_t + PO_t + MD_t + TE_t) / 20`

This is equivalent to the average of the five direct-exposure dimensions, rescaled from `0-4` to `0-100`.

### 2. Oversight Criticality

Oversight Criticality for task `t`:

`OC_t = 100 * (SJ_t + NP_t + AA_t + AR_t) / 16`

This is equivalent to the average of the four oversight dimensions, rescaled from `0-4` to `0-100`.

### 3. Interdependence Centrality

First define the weighted edge value:

`A_ij = (strength_ij / 4) * confidence_ij`

So every directed edge weight lies in `[0, 1]`.

Then compute:

- out-strength: `OUT_i = sum(A_ij for all j != i)`
- in-strength: `IN_i = sum(A_ji for all j != i)`

Normalize them:

- `SOUT_i = OUT_i / max(OUT_k)`
- `SIN_i = IN_i / max(IN_k)`

If the denominator is `0`, set the normalized term to `0`.

Compute weighted betweenness centrality `B_i` on the directed graph using edge distance:

`distance_ij = 1 / (A_ij + 0.001)`

Normalize weighted betweenness to `[0,1]`.

Compute weighted PageRank `PR_i` on the directed graph using `A_ij` as the edge weight.

Min-max normalize PageRank:

`P_i = (PR_i - min(PR_k)) / (max(PR_k) - min(PR_k))`

If the denominator is `0`, set `P_i = 0`.

Then define Interdependence Centrality:

`IC_i = 100 * (0.30 * SOUT_i + 0.30 * SIN_i + 0.20 * B_i + 0.20 * P_i)`

### 4. Spillover Exposure

Spillover Exposure captures the joint condition that a task is both directly exposed and structurally central:

`SE_t = (DAE_t * IC_t) / 100`

This keeps the scale in `0-100`.

## Occupation-Level Aggregation

Aggregate each task-level component using O*NET importance weights:

- `Occupation_DAE = sum(w_t * DAE_t)`
- `Occupation_OC = sum(w_t * OC_t)`
- `Occupation_IC = sum(w_t * IC_t)`
- `Occupation_SE = sum(w_t * SE_t)`

These four occupation-level values are the main pilot outputs.

## Optional Composite Score

If you want one headline number later, use this only as a reporting convenience, not as the primary analytic result:

`Composite_Impact = 0.35 * Occupation_DAE + 0.35 * Occupation_SE + 0.20 * Occupation_IC + 0.10 * (100 - Occupation_OC)`

Keep the four components visible even when you report the composite.

## Audit Protocol

The human reviewer should always inspect:

- all 21 task profiles,
- all 21 direct exposure records,
- all task pairs with `strength >= 3`,
- all records with confidence below `0.75`,
- all records with fewer than 2 evidence chunk IDs,
- all adjudication decisions marked `revise` or `escalate_for_human`.

Recommended audit columns:

- `record_id`
- `accept_or_reject`
- `reason`
- `prompt_change_needed`
- `weight_change_needed`
- `notes`

## Decision Rules

- If a task has weak evidence but the model is confident, human review wins.
- If task profile and direct exposure conflict, rerun the exposure pass using the revised task profile.
- If dependency extraction returns many reciprocal strong edges, review those pairs first for graph inflation.
- If more than 15% of records are rejected in audit, freeze the run, revise the prompt, and rerun the full pass.

## Prompt and Schema Files

Prompts:

- [01_pmi_chunk_tagging.md](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/prompts/01_pmi_chunk_tagging.md)
- [02_task_profile.md](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/prompts/02_task_profile.md)
- [03_direct_exposure.md](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/prompts/03_direct_exposure.md)
- [04_task_pair_dependency.md](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/prompts/04_task_pair_dependency.md)
- [05_adjudication.md](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/prompts/05_adjudication.md)

Schemas:

- [dashboard_snapshot.schema.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/dashboard_snapshot.schema.json)

## Dashboard Layer

The monthly dashboard layer lives in:

- [dashboard/README.md](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/README.md)
- [benchmark_capability_matrix.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/benchmark_capability_matrix.csv)
- [task_capability_matrix.csv](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/dashboard/task_capability_matrix.csv)

These files define:

- the normalized monthly snapshot schema,
- the benchmark-to-capability mapping used to derive model capability scores,
- and the task-to-capability mapping used to convert model capability into realized PM exposure.

- [pmi_evidence_chunk.schema.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/schemas/pmi_evidence_chunk.schema.json)
- [task_profile.schema.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/schemas/task_profile.schema.json)
- [direct_exposure.schema.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/schemas/direct_exposure.schema.json)
- [task_pair_dependency.schema.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/schemas/task_pair_dependency.schema.json)
- [adjudication.schema.json](/C:/Users/mrnig/Documents/codex/AI%20and%20Project%20Management%20jobs/llm_exposure_workflow/schemas/adjudication.schema.json)
