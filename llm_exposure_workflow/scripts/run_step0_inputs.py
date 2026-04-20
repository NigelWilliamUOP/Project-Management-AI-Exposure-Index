from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(r"C:\Users\mrnig\Documents\codex\AI and Project Management jobs")
WORKFLOW = ROOT / "llm_exposure_workflow"
OUTPUT = WORKFLOW / "output"
OCCUPATION_DIR = ROOT / "Information Project Managers"


def load_csv(pattern: str) -> list[dict[str, str]]:
    file_path = next(OCCUPATION_DIR.glob(pattern))
    with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_tasks() -> list[dict[str, object]]:
    rows = load_csv("Tasks*.csv*")
    tasks = []
    for idx, row in enumerate(rows, start=1):
        tasks.append(
            {
                "task_id": f"T{idx:02d}",
                "onet_soc_code": "15-1299.09",
                "occupation_label": "Project Management Specialists / Information Project Managers",
                "onet_category": row["Category"],
                "onet_importance": int(row["Importance"]),
                "onet_task_text": row["Task"].strip(),
            }
        )
    return tasks


def normalize_simple_table(
    rows: list[dict[str, str]],
    record_prefix: str,
    name_key: str,
    description_key: str | None = None,
    importance_key: str | None = None,
) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []
    for idx, row in enumerate(rows, start=1):
        entry: dict[str, object] = {
            "record_id": f"{record_prefix}{idx:02d}",
            "label": row[name_key].strip(),
        }
        if description_key:
            entry["description"] = row[description_key].strip()
        if importance_key and row.get(importance_key):
            try:
                entry["importance"] = int(row[importance_key])
            except ValueError:
                entry["importance"] = row[importance_key]
        normalized.append(entry)
    return normalized


def build_linked_context(tasks: list[dict[str, object]]) -> list[dict[str, object]]:
    dwas = normalize_simple_table(
        load_csv("Detailed_Work_Activities*.csv*"),
        "DWA",
        "Detailed Work Activity",
    )
    skills = normalize_simple_table(
        load_csv("Skills*.csv*"),
        "SK",
        "Skill",
        "Skill Description",
        "Importance",
    )
    knowledge = normalize_simple_table(
        load_csv("Knowledge*.csv*"),
        "KN",
        "Knowledge",
        "Knowledge Description",
        "Importance",
    )
    work_activities = normalize_simple_table(
        load_csv("Work_Activities*.csv*"),
        "WA",
        "Work Activity",
        "Work Activity Description",
        "Importance",
    )

    # For this pilot we attach shared occupation-level context rather than forcing weak one-to-one links.
    shared_context = {
        "dwa_ids": [row["record_id"] for row in dwas[:18]],
        "skill_ids": [row["record_id"] for row in skills[:12]],
        "knowledge_ids": [row["record_id"] for row in knowledge[:12]],
        "work_activity_ids": [row["record_id"] for row in work_activities[:12]],
    }

    linked = []
    for task in tasks:
        linked.append(
            {
                "task_id": task["task_id"],
                "shared_context": shared_context,
            }
        )

    write_json(OUTPUT / "canonical_dwas.json", dwas)
    write_json(OUTPUT / "canonical_skills.json", skills)
    write_json(OUTPUT / "canonical_knowledge.json", knowledge)
    write_json(OUTPUT / "canonical_work_activities.json", work_activities)
    return linked


def main() -> None:
    tasks = normalize_tasks()
    links = build_linked_context(tasks)

    write_csv(
        OUTPUT / "canonical_tasks.csv",
        [
            "task_id",
            "onet_soc_code",
            "occupation_label",
            "onet_category",
            "onet_importance",
            "onet_task_text",
        ],
        tasks,
    )
    write_json(OUTPUT / "canonical_tasks.json", tasks)
    write_jsonl(OUTPUT / "canonical_tasks.jsonl", tasks)
    write_json(OUTPUT / "task_context_links.json", links)

    summary = {
        "occupation_code": "15-1299.09",
        "task_count": len(tasks),
        "dwa_count": 18,
        "skill_count": 35,
        "knowledge_count": 33,
        "work_activity_count": 41,
        "source_decision": "Duplicate occupation folders collapsed into one canonical pilot corpus.",
    }
    write_json(OUTPUT / "step0_summary.json", summary)


if __name__ == "__main__":
    main()
