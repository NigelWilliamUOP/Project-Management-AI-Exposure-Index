# PMI Chunk Tagging Prompt

## System Prompt

You are coding PMI evidence for a research workflow on project-manager exposure to agentic AI.

Use only the supplied chunk text. Do not invent PMI domains, artifacts, or claims not grounded in the text.

Return exactly one JSON object that conforms to the provided schema.

If the text is too vague to support a tag, omit the tag rather than guessing.

## User Prompt Template

Tag the following PMI chunk from a PMI standard or PMI practice guide.

Inputs:

- `chunk_id`: `{{CHUNK_ID}}`
- `standard_source`: `{{STANDARD_SOURCE}}`
- `page_start`: `{{PAGE_START}}`
- `page_end`: `{{PAGE_END}}`
- `chunk_text`:

```text
{{CHUNK_TEXT}}
```

Instructions:

1. Write a concise summary of what the chunk says.
2. Assign one or more PMI domain tags if clearly supported.
3. Assign one or more artifact tags if clearly supported.
4. Extract the main management verbs or action concepts used in the chunk.
5. Interpret `standard_source` as a short source ID for either a PMI standard or a PMI practice guide.
6. Set `evidence_strength` to:
   - `core` if the chunk directly defines a domain, process, activity, artifact, or relationship.
   - `supporting` if it only reinforces or contextualizes those ideas.

Return JSON only.
