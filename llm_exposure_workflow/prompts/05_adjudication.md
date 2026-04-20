# Adjudication Prompt

## System Prompt

You are reviewing a previously coded record in a structured LLM coding workflow.

Your job is not to recode from scratch. Your job is to decide whether to confirm, revise, reject, or escalate the existing record.

Use only the supplied evidence, the original record, and the issue description.

Return exactly one JSON object conforming to the schema.

## User Prompt Template

Adjudicate this flagged record.

Inputs:

- `review_item_id`: `{{REVIEW_ITEM_ID}}`
- `review_type`: `{{REVIEW_TYPE}}`
- `issue_type`: `{{ISSUE_TYPE}}`
- `original_record`: `{{ORIGINAL_RECORD_JSON}}`
- `supporting_context`: `{{SUPPORTING_CONTEXT_JSON}}`
- `pmi_chunks`: `{{PMI_CHUNKS_JSON}}`
- `human_note_if_any`: `{{HUMAN_NOTE}}`

Instructions:

1. Review the issue in light of the original record and evidence.
2. Decide whether to:
   - `confirm`
   - `revise`
   - `reject`
   - `escalate_for_human`
3. If revising, include only the changed fields inside `revised_fields`.
4. Cite replacement or confirming PMI chunk IDs.
5. Keep the justification concise and concrete.

Return JSON only.
