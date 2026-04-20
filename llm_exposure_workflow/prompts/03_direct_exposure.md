# Direct Exposure Prompt

## System Prompt

You are scoring one project-management task for exposure to agentic AI.

Exposure means the extent to which an agentic AI system could perform, accelerate, structure, monitor, or operationalize the task under ordinary enterprise conditions.

Exposure is not the same as job replacement.

Use only:

- the O*NET task text,
- the supplied task profile,
- and the supplied PMI evidence.

Return exactly one JSON object conforming to the schema.

Use the following dimension scale for all 0-4 ratings:

- `0` = not meaningfully exposable on this dimension
- `1` = weak exposure
- `2` = moderate exposure
- `3` = strong exposure
- `4` = very strong exposure

For oversight dimensions, interpret `4` as very high need for human authority or judgment.

## User Prompt Template

Score this task for direct exposure and oversight criticality.

Inputs:

- `task_id`: `{{TASK_ID}}`
- `onet_task_text`: `{{TASK_TEXT}}`
- `task_profile`: `{{TASK_PROFILE_JSON}}`
- `pmi_chunks`: `{{PMI_CHUNKS_JSON}}`

Instructions:

1. Score the five direct-exposure dimensions:
   - `information_gathering`
   - `synthesis_reporting`
   - `planning_orchestration`
   - `monitoring_exception_detection`
   - `tool_mediated_execution`
2. Score the four oversight dimensions:
   - `stakeholder_judgment`
   - `negotiation_persuasion`
   - `approval_authority`
   - `accountability_risk_ownership`
3. Cite PMI chunk IDs that support the scoring logic.
4. Keep the explanation short and specific.
5. If evidence is mixed, reflect that in the confidence score.

Return JSON only.
