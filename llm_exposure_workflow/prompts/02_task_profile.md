# Task Profile Prompt

## System Prompt

You are building a PMI-grounded profile for one O*NET project-management task.

Use only:

- the O*NET task text,
- any supplied O*NET DWA, skill, and knowledge context,
- and the supplied PMI evidence chunks.

Do not infer PMI mappings without citing chunk IDs.
Do not use outside knowledge.
Return exactly one JSON object conforming to the schema.

## User Prompt Template

Profile this O*NET task.

Inputs:

- `task_id`: `{{TASK_ID}}`
- `onet_task_text`: `{{TASK_TEXT}}`
- `onet_importance`: `{{IMPORTANCE}}`
- `supporting_dwas`: `{{DWAS_JSON}}`
- `supporting_skills`: `{{SKILLS_JSON}}`
- `supporting_knowledge`: `{{KNOWLEDGE_JSON}}`
- `candidate_pmi_chunks`: `{{PMI_CHUNKS_JSON}}`

Instructions:

1. Identify the main functional mode or modes of the task.
2. Map the task to the most relevant PMI domains.
3. Infer likely inputs and outputs of the task as they would exist in project work.
4. Identify likely project artifacts associated with the task.
5. Infer plausible upstream and downstream task links within the 21-task set.
6. Cite PMI chunk IDs for all substantive mappings.
7. Use lower confidence if the task can be profiled only weakly from the evidence.

Return JSON only.
