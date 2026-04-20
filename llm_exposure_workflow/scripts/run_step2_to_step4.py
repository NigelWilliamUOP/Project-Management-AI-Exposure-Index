from __future__ import annotations

import csv
import json
from pathlib import Path

import networkx as nx


ROOT = Path(r"C:\Users\mrnig\Documents\codex\AI and Project Management jobs")
WORKFLOW = ROOT / "llm_exposure_workflow"
OUTPUT = WORKFLOW / "output"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def evidence_definitions() -> dict[str, dict]:
    return {
        "program_p028_c11": {
            "summary": "Program managers manage dependencies and build an integrated framework across components and operations.",
            "domain_tags": ["strategic_alignment", "collaboration", "life_cycle_management"],
            "artifact_tags": ["program_management_plan", "roadmap"],
            "verb_tags": ["integrate", "coordinate", "manage", "align"],
            "evidence_strength": "core",
            "confidence": 0.92,
        },
        "program_p097_c42": {
            "summary": "Benefits identification develops a benefits register from the business case and strategic plan and uses it to measure and communicate delivery.",
            "domain_tags": ["benefits_management", "strategic_alignment", "reporting"],
            "artifact_tags": ["benefits_register", "business_case", "benefits_plan"],
            "verb_tags": ["identify", "measure", "communicate", "track"],
            "evidence_strength": "core",
            "confidence": 0.93,
        },
        "program_p115_c50": {
            "summary": "Program stakeholder engagement covers groups that benefit from or are disadvantaged by the program and internal support functions.",
            "domain_tags": ["stakeholder_engagement", "communications_management"],
            "artifact_tags": ["stakeholder_register", "communications_plan"],
            "verb_tags": ["identify", "categorize", "engage", "communicate"],
            "evidence_strength": "core",
            "confidence": 0.9,
        },
        "program_p142_c63": {
            "summary": "Collaboration should balance capabilities, capacity, pace, and sustainment needs across the program life cycle.",
            "domain_tags": ["collaboration", "life_cycle_management", "resource_management"],
            "artifact_tags": ["program_management_plan"],
            "verb_tags": ["balance", "collaborate", "sustain", "coordinate"],
            "evidence_strength": "core",
            "confidence": 0.89,
        },
        "portfolio_p025_c14": {
            "summary": "Portfolio managers identify business value, monitor risks and priorities, and resolve resource issues tied to strategic goals.",
            "domain_tags": ["portfolio_strategic_management", "value_management", "risk_management"],
            "artifact_tags": ["portfolio_management_plan", "roadmap", "performance_report"],
            "verb_tags": ["prioritize", "monitor", "measure", "improve"],
            "evidence_strength": "core",
            "confidence": 0.9,
        },
        "portfolio_p063_c38": {
            "summary": "Capacity management is critical and must balance portfolio value, risks, and execution needs.",
            "domain_tags": ["capacity_capability_management", "value_management", "risk_management"],
            "artifact_tags": ["portfolio_management_plan"],
            "verb_tags": ["balance", "allocate", "plan", "execute"],
            "evidence_strength": "core",
            "confidence": 0.9,
        },
        "portfolio_p095_c58": {
            "summary": "Value measurement depends on stakeholder buy-in and consistent, transparent execution to reach consensus.",
            "domain_tags": ["value_management", "stakeholder_engagement", "reporting"],
            "artifact_tags": ["performance_report", "benefits_plan"],
            "verb_tags": ["measure", "report", "align", "validate"],
            "evidence_strength": "supporting",
            "confidence": 0.87,
        },
        "requirements_pg_p032_c12": {
            "summary": "Requirements management planning initiation begins from project artifacts and stakeholder context and establishes how requirements work will be managed.",
            "domain_tags": ["requirements_management", "stakeholder_engagement", "business_analysis"],
            "artifact_tags": ["requirements_document", "project_management_plan", "stakeholder_register"],
            "verb_tags": ["gather", "plan", "trace", "manage"],
            "evidence_strength": "core",
            "confidence": 0.93,
        },
        "requirements_pg_p041_c17": {
            "summary": "Prototyping and iterative feedback progressively refine requirements through stakeholder evaluation and revision.",
            "domain_tags": ["requirements_management", "stakeholder_engagement", "agile_delivery"],
            "artifact_tags": ["requirements_document", "backlog"],
            "verb_tags": ["refine", "evaluate", "revise", "prototype"],
            "evidence_strength": "supporting",
            "confidence": 0.88,
        },
        "wbs_pg_p001_c01": {
            "summary": "The WBS is an essential planning artifact that organizes the total approved scope of the project.",
            "domain_tags": ["work_breakdown_management", "scope_schedule_cost_integration"],
            "artifact_tags": ["wbs", "wbs_dictionary"],
            "verb_tags": ["decompose", "organize", "scope", "plan"],
            "evidence_strength": "core",
            "confidence": 0.94,
        },
        "wbs_pg_p018_c06": {
            "summary": "The WBS provides an integrated mechanism across schedule, cost, risk, resource, technical, and performance management.",
            "domain_tags": ["work_breakdown_management", "scope_schedule_cost_integration", "risk_management", "resource_management"],
            "artifact_tags": ["wbs", "wbs_dictionary", "baseline"],
            "verb_tags": ["integrate", "structure", "link", "control"],
            "evidence_strength": "core",
            "confidence": 0.93,
        },
        "scheduling_pg_p069_c30": {
            "summary": "WBS elements should trace directly to schedule activities, and resource-loaded schedules support realistic coordination.",
            "domain_tags": ["scheduling_management", "resource_management", "work_breakdown_management"],
            "artifact_tags": ["schedule", "activity_list", "wbs", "baseline"],
            "verb_tags": ["sequence", "trace", "verify", "schedule"],
            "evidence_strength": "core",
            "confidence": 0.9,
        },
        "estimating_pg_p001_c01": {
            "summary": "Project estimating establishes early schedule and cost baselines and is refined as the project develops.",
            "domain_tags": ["estimating", "baseline_control", "scope_schedule_cost_integration"],
            "artifact_tags": ["estimate", "basis_of_estimate", "budget", "schedule"],
            "verb_tags": ["estimate", "baseline", "refine", "forecast"],
            "evidence_strength": "core",
            "confidence": 0.94,
        },
        "risk_practice_p031_c18": {
            "summary": "Risk strategy sets thresholds, assessment, response strategy, and governance and communication mechanisms.",
            "domain_tags": ["risk_management", "governance", "communications_management"],
            "artifact_tags": ["risk_register", "communications_plan"],
            "verb_tags": ["assess", "respond", "escalate", "govern"],
            "evidence_strength": "core",
            "confidence": 0.91,
        },
        "risk_practice_p059_c35": {
            "summary": "Plan Risk Management defines how risk processes will be executed and integrated with all other project activities.",
            "domain_tags": ["risk_management", "scope_schedule_cost_integration"],
            "artifact_tags": ["risk_register", "project_management_plan"],
            "verb_tags": ["plan", "integrate", "execute", "manage"],
            "evidence_strength": "core",
            "confidence": 0.92,
        },
        "risk_standard_p001_c01": {
            "summary": "Risk management is treated as a cross-level management standard spanning portfolios, programs, and projects.",
            "domain_tags": ["risk_management", "governance"],
            "artifact_tags": ["risk_register"],
            "verb_tags": ["define", "govern", "align", "manage"],
            "evidence_strength": "core",
            "confidence": 0.88,
        },
        "evm_p041_c24": {
            "summary": "The performance measurement baseline integrates scope, schedule, cost, quality, and related subsidiary planning inputs.",
            "domain_tags": ["scope_schedule_cost_integration", "baseline_control", "monitoring_control"],
            "artifact_tags": ["baseline", "project_management_plan", "budget", "schedule"],
            "verb_tags": ["integrate", "baseline", "measure", "plan"],
            "evidence_strength": "core",
            "confidence": 0.94,
        },
        "evm_p043_c25": {
            "summary": "Subsidiary plans need to address EVM methodology, including communications, resource, and risk implications.",
            "domain_tags": ["scope_schedule_cost_integration", "communications_management", "resource_management", "risk_management"],
            "artifact_tags": ["project_management_plan", "communications_plan", "risk_register", "budget", "schedule"],
            "verb_tags": ["tailor", "integrate", "plan", "control"],
            "evidence_strength": "supporting",
            "confidence": 0.9,
        },
        "evm_p033_c21": {
            "summary": "Performance information is used to monitor project status, explain variation, support decisions, and communicate performance.",
            "domain_tags": ["monitoring_control", "reporting", "communications_management"],
            "artifact_tags": ["performance_report", "baseline"],
            "verb_tags": ["monitor", "analyze", "decide", "communicate"],
            "evidence_strength": "core",
            "confidence": 0.93,
        },
        "evm_p108_c65": {
            "summary": "Project success depends heavily on effective communications and stakeholder management in reporting and control.",
            "domain_tags": ["communications_management", "stakeholder_engagement", "reporting"],
            "artifact_tags": ["communications_plan", "performance_report", "stakeholder_register"],
            "verb_tags": ["report", "communicate", "engage", "manage"],
            "evidence_strength": "core",
            "confidence": 0.9,
        },
        "agile_pg_p045_c16": {
            "summary": "Hybrid approaches combine methods to fit context and help justify value and ROI to sponsors.",
            "domain_tags": ["agile_delivery", "agile_planning", "stakeholder_engagement"],
            "artifact_tags": ["backlog", "roadmap", "business_case"],
            "verb_tags": ["adapt", "blend", "justify", "deliver"],
            "evidence_strength": "supporting",
            "confidence": 0.84,
        },
        "benefits_pg_p001_c01": {
            "summary": "Benefits realization links organizational strategy to project deliverables and expected outcomes.",
            "domain_tags": ["benefits_management", "value_management", "strategic_alignment"],
            "artifact_tags": ["benefits_plan", "benefits_register", "business_case"],
            "verb_tags": ["realize", "link", "deliver", "measure"],
            "evidence_strength": "core",
            "confidence": 0.92,
        },
        "ba_practice_p039_c24": {
            "summary": "Evaluation planning covers dependencies, roles, responsibilities, change considerations, and benefit metrics.",
            "domain_tags": ["business_analysis", "benefits_management", "change_control"],
            "artifact_tags": ["business_case", "benefits_plan", "requirements_document"],
            "verb_tags": ["evaluate", "measure", "analyze", "coordinate"],
            "evidence_strength": "supporting",
            "confidence": 0.87,
        },
    }


def task_specs() -> dict[str, dict]:
    m = lambda source, domain, fit, chunk_ids: {
        "standard_source": source,
        "domain": domain,
        "fit_score": fit,
        "chunk_ids": chunk_ids,
    }
    return {
        "T01": {
            "functional_modes": ["coordination", "monitoring", "governance"],
            "pmi_domain_mappings": [
                m("evm", "scope_schedule_cost_integration", 4, ["evm_p041_c24", "evm_p043_c25"]),
                m("evm", "monitoring_control", 4, ["evm_p033_c21"]),
                m("program", "strategic_alignment", 2, ["program_p028_c11"]),
            ],
            "likely_inputs": ["approved project plan", "budget baseline", "schedule baseline", "WBS", "resource assignments"],
            "likely_outputs": ["execution decisions", "corrective actions", "updated performance signals"],
            "required_artifacts": ["project_management_plan", "budget", "schedule", "baseline", "wbs"],
            "confidence": 0.93,
            "justification": "Executing within budget, schedule, and scope is anchored in integrated baseline control and ongoing monitoring.",
        },
        "T02": {
            "functional_modes": ["coordination", "stakeholder_management", "risk_management"],
            "pmi_domain_mappings": [
                m("program", "collaboration", 4, ["program_p142_c63"]),
                m("program", "stakeholder_engagement", 3, ["program_p115_c50"]),
                m("risk_practice", "risk_management", 2, ["risk_practice_p031_c18"]),
            ],
            "likely_inputs": ["issue reports", "meeting signals", "stakeholder concerns"],
            "likely_outputs": ["resolved issues", "escalations", "recommended actions"],
            "required_artifacts": ["communications_plan", "risk_register", "performance_report"],
            "confidence": 0.9,
            "justification": "Problem resolution is collaboration-heavy and often routed through stakeholder and risk channels.",
        },
        "T03": {
            "functional_modes": ["monitoring", "reporting"],
            "pmi_domain_mappings": [
                m("scheduling_pg", "scheduling_management", 4, ["scheduling_pg_p069_c30"]),
                m("evm", "monitoring_control", 4, ["evm_p033_c21", "evm_p041_c24"]),
            ],
            "likely_inputs": ["schedule activities", "milestone definitions", "actual progress data"],
            "likely_outputs": ["milestone status", "variance visibility", "delivery alerts"],
            "required_artifacts": ["schedule", "baseline", "performance_report"],
            "confidence": 0.93,
            "justification": "Milestone tracking sits directly in scheduling and performance monitoring practice.",
        },
        "T04": {
            "functional_modes": ["quality_management", "reporting", "coordination"],
            "pmi_domain_mappings": [
                m("benefits_pg", "benefits_management", 2, ["benefits_pg_p001_c01"]),
                m("wbs_pg", "work_breakdown_management", 2, ["wbs_pg_p001_c01"]),
                m("evm", "reporting", 2, ["evm_p033_c21"]),
            ],
            "likely_inputs": ["accepted work outputs", "quality criteria", "delivery approvals"],
            "likely_outputs": ["submitted deliverables", "quality confirmation", "delivery status"],
            "required_artifacts": ["deliverable", "performance_report", "wbs"],
            "confidence": 0.82,
            "justification": "Deliverable submission depends on structured scope and performance reporting, with benefits realized through accepted outputs.",
        },
        "T05": {
            "functional_modes": ["stakeholder_management", "planning", "reporting"],
            "pmi_domain_mappings": [
                m("requirements_pg", "requirements_management", 4, ["requirements_pg_p032_c12", "requirements_pg_p041_c17"]),
                m("ba_practice", "business_analysis", 4, ["ba_practice_p039_c24"]),
                m("program", "stakeholder_engagement", 3, ["program_p115_c50"]),
            ],
            "likely_inputs": ["customer interviews", "survey data", "business drivers", "service issues"],
            "likely_outputs": ["priority statements", "refined requirements", "planning inputs"],
            "required_artifacts": ["requirements_document", "stakeholder_register", "business_case"],
            "confidence": 0.94,
            "justification": "This task is a direct requirements and stakeholder-needs activity that shapes later planning and scope definition.",
        },
        "T06": {
            "functional_modes": ["change_control", "governance", "planning"],
            "pmi_domain_mappings": [
                m("evm", "change_control", 4, ["evm_p043_c25", "evm_p041_c24"]),
                m("risk_practice", "risk_management", 3, ["risk_practice_p059_c35", "risk_practice_p031_c18"]),
                m("program", "governance", 3, ["program_p028_c11"]),
            ],
            "likely_inputs": ["change requests", "variance data", "risk findings", "stakeholder requests"],
            "likely_outputs": ["approved modifications", "revised plans", "updated controls"],
            "required_artifacts": ["change_request", "project_management_plan", "baseline", "risk_register"],
            "confidence": 0.93,
            "justification": "Plan modification is a governance and change-control function tightly linked to integrated baselines and risk planning.",
        },
        "T07": {
            "functional_modes": ["coordination", "communications_management"],
            "pmi_domain_mappings": [
                m("evm", "communications_management", 3, ["evm_p108_c65"]),
                m("program", "stakeholder_engagement", 3, ["program_p115_c50"]),
                m("program", "collaboration", 2, ["program_p142_c63"]),
            ],
            "likely_inputs": ["communication calendar", "stakeholder list", "agenda topics"],
            "likely_outputs": ["scheduled meetings", "meeting decisions", "issue clarifications"],
            "required_artifacts": ["communications_plan", "stakeholder_register"],
            "confidence": 0.88,
            "justification": "Meeting facilitation is an execution mechanism for communications and stakeholder engagement.",
        },
        "T08": {
            "functional_modes": ["coordination", "resource_management", "governance"],
            "pmi_domain_mappings": [
                m("program", "collaboration", 4, ["program_p142_c63"]),
                m("portfolio", "capacity_capability_management", 3, ["portfolio_p063_c38"]),
                m("program", "stakeholder_engagement", 2, ["program_p115_c50"]),
            ],
            "likely_inputs": ["staffing assignments", "project priorities", "work packages"],
            "likely_outputs": ["coordinated team activity", "work direction", "resource escalations"],
            "required_artifacts": ["project_management_plan", "wbs", "schedule"],
            "confidence": 0.89,
            "justification": "Directing personnel relies on collaborative control of capacity and coordinated execution.",
        },
        "T09": {
            "functional_modes": ["planning", "reporting", "budgeting"],
            "pmi_domain_mappings": [
                m("estimating_pg", "estimating", 4, ["estimating_pg_p001_c01"]),
                m("benefits_pg", "benefits_management", 3, ["benefits_pg_p001_c01"]),
                m("ba_practice", "business_analysis", 3, ["ba_practice_p039_c24"]),
                m("portfolio", "value_management", 3, ["portfolio_p095_c58"]),
            ],
            "likely_inputs": ["customer priorities", "requirements", "cost assumptions", "implementation constraints"],
            "likely_outputs": ["implementation plan", "ROI case", "cost-benefit analysis"],
            "required_artifacts": ["project_management_plan", "estimate", "business_case", "budget"],
            "confidence": 0.92,
            "justification": "Implementation planning with ROI is estimating-heavy and tied to benefits and value framing.",
        },
        "T10": {
            "functional_modes": ["planning", "resource_management", "budgeting"],
            "pmi_domain_mappings": [
                m("portfolio", "capacity_capability_management", 4, ["portfolio_p063_c38"]),
                m("scheduling_pg", "resource_management", 3, ["scheduling_pg_p069_c30"]),
                m("estimating_pg", "estimating", 2, ["estimating_pg_p001_c01"]),
            ],
            "likely_inputs": ["workload estimates", "WBS packages", "schedule logic", "available staffing"],
            "likely_outputs": ["resource gap list", "supplemental resource requests", "sourcing decisions"],
            "required_artifacts": ["wbs", "schedule", "budget", "project_management_plan"],
            "confidence": 0.92,
            "justification": "Resource need identification is a capacity-management activity informed by decomposition and scheduling realism.",
        },
        "T11": {
            "functional_modes": ["planning", "coordination", "budgeting"],
            "pmi_domain_mappings": [
                m("requirements_pg", "requirements_management", 3, ["requirements_pg_p032_c12"]),
                m("estimating_pg", "estimating", 3, ["estimating_pg_p001_c01"]),
                m("scheduling_pg", "scheduling_management", 3, ["scheduling_pg_p069_c30"]),
                m("risk_practice", "risk_management", 3, ["risk_practice_p059_c35"]),
                m("evm", "scope_schedule_cost_integration", 4, ["evm_p041_c24", "evm_p043_c25"]),
            ],
            "likely_inputs": ["customer needs", "technology constraints", "resource assumptions", "risk assessments"],
            "likely_outputs": ["integrated project plan", "funding/staffing plan", "control baselines"],
            "required_artifacts": ["project_management_plan", "schedule", "budget", "baseline", "risk_register", "requirements_document"],
            "confidence": 0.95,
            "justification": "This is the central integrated planning task that combines requirements, estimates, schedule, resources, and controls.",
        },
        "T12": {
            "functional_modes": ["risk_management", "planning", "reporting"],
            "pmi_domain_mappings": [
                m("risk_practice", "risk_management", 4, ["risk_practice_p031_c18", "risk_practice_p059_c35"]),
                m("risk_standard", "risk_management", 4, ["risk_standard_p001_c01"]),
            ],
            "likely_inputs": ["threats and opportunities", "project assumptions", "stakeholder concerns", "baseline data"],
            "likely_outputs": ["risk assessment", "response strategies", "risk escalation"],
            "required_artifacts": ["risk_register", "project_management_plan"],
            "confidence": 0.96,
            "justification": "This is the clearest direct risk-management task in the corpus.",
        },
        "T13": {
            "functional_modes": ["reporting", "monitoring", "communications_management"],
            "pmi_domain_mappings": [
                m("evm", "reporting", 4, ["evm_p033_c21", "evm_p108_c65"]),
                m("evm", "monitoring_control", 3, ["evm_p041_c24"]),
            ],
            "likely_inputs": ["performance data", "trend data", "milestone status", "budget status"],
            "likely_outputs": ["status report", "trend summary", "stakeholder communication"],
            "required_artifacts": ["performance_report", "baseline", "communications_plan"],
            "confidence": 0.95,
            "justification": "Status reporting directly matches EVM logic around performance data, variation analysis, and stakeholder communication.",
        },
        "T14": {
            "functional_modes": ["stakeholder_management", "resource_management", "planning"],
            "pmi_domain_mappings": [
                m("program", "stakeholder_engagement", 2, ["program_p115_c50"]),
                m("portfolio", "capacity_capability_management", 2, ["portfolio_p063_c38"]),
                m("risk_practice", "risk_management", 2, ["risk_practice_p031_c18"]),
            ],
            "likely_inputs": ["resource gaps", "requirements", "vendor capabilities", "commercial constraints"],
            "likely_outputs": ["vendor shortlist", "selection decision", "sourcing recommendation"],
            "required_artifacts": ["project_management_plan", "requirements_document", "budget"],
            "confidence": 0.77,
            "justification": "Procurement is only partially covered by the current PMI set, so this profile leans on stakeholder, capacity, and risk evidence rather than a dedicated procurement guide.",
        },
        "T15": {
            "functional_modes": ["budgeting", "planning", "monitoring"],
            "pmi_domain_mappings": [
                m("estimating_pg", "estimating", 4, ["estimating_pg_p001_c01"]),
                m("evm", "baseline_control", 3, ["evm_p041_c24"]),
                m("portfolio", "value_management", 2, ["portfolio_p095_c58"]),
            ],
            "likely_inputs": ["cost assumptions", "resource plans", "implementation plan", "historical spend"],
            "likely_outputs": ["annual budget", "budget updates", "spend constraints"],
            "required_artifacts": ["budget", "estimate", "baseline", "performance_report"],
            "confidence": 0.92,
            "justification": "Budget development and management are estimating-driven and tied to baseline and value measurement discipline.",
        },
        "T16": {
            "functional_modes": ["communications_management", "planning", "stakeholder_management"],
            "pmi_domain_mappings": [
                m("evm", "communications_management", 4, ["evm_p108_c65"]),
                m("program", "stakeholder_engagement", 4, ["program_p115_c50"]),
                m("requirements_pg", "requirements_management", 2, ["requirements_pg_p032_c12"]),
            ],
            "likely_inputs": ["stakeholder list", "reporting needs", "governance cadence", "project objectives"],
            "likely_outputs": ["communication plan", "communication routines", "engagement expectations"],
            "required_artifacts": ["communications_plan", "stakeholder_register", "performance_report"],
            "confidence": 0.94,
            "justification": "Communication planning formalizes how stakeholders will receive information and participate in project control.",
        },
        "T17": {
            "functional_modes": ["planning", "work_breakdown_management"],
            "pmi_domain_mappings": [
                m("wbs_pg", "work_breakdown_management", 4, ["wbs_pg_p001_c01", "wbs_pg_p018_c06"]),
                m("scheduling_pg", "scheduling_management", 3, ["scheduling_pg_p069_c30"]),
            ],
            "likely_inputs": ["scope definition", "requirements", "deliverable structure"],
            "likely_outputs": ["WBS", "work packages", "planning decomposition"],
            "required_artifacts": ["wbs", "wbs_dictionary", "schedule", "baseline"],
            "confidence": 0.96,
            "justification": "WBS development is a direct fit for the dedicated WBS practice standard and its integration into schedule and control.",
        },
        "T18": {
            "functional_modes": ["monitoring", "resource_management", "reporting"],
            "pmi_domain_mappings": [
                m("program", "collaboration", 3, ["program_p142_c63"]),
                m("portfolio", "capacity_capability_management", 2, ["portfolio_p063_c38"]),
                m("program", "stakeholder_engagement", 1, ["program_p115_c50"]),
            ],
            "likely_inputs": ["observed performance", "assigned responsibilities", "work outputs"],
            "likely_outputs": ["performance feedback", "development signals", "team adjustments"],
            "required_artifacts": ["performance_report", "project_management_plan"],
            "confidence": 0.78,
            "justification": "Team-performance feedback is relevant to coordination and capacity, but the current PMI source set covers it indirectly rather than with a dedicated people-management guide.",
        },
        "T19": {
            "functional_modes": ["resource_management", "planning", "stakeholder_management"],
            "pmi_domain_mappings": [
                m("portfolio", "capacity_capability_management", 3, ["portfolio_p063_c38"]),
                m("program", "collaboration", 2, ["program_p142_c63"]),
                m("program", "stakeholder_engagement", 2, ["program_p115_c50"]),
            ],
            "likely_inputs": ["resource shortages", "role needs", "candidate pools"],
            "likely_outputs": ["recruitment coordination", "selection recommendations", "staffing actions"],
            "required_artifacts": ["project_management_plan", "budget", "schedule"],
            "confidence": 0.82,
            "justification": "Recruitment is modeled here as a capacity and staffing response to project execution needs.",
        },
        "T20": {
            "functional_modes": ["resource_management", "governance", "planning"],
            "pmi_domain_mappings": [
                m("program", "collaboration", 3, ["program_p142_c63"]),
                m("portfolio", "capacity_capability_management", 3, ["portfolio_p063_c38"]),
                m("wbs_pg", "work_breakdown_management", 2, ["wbs_pg_p018_c06"]),
            ],
            "likely_inputs": ["staff availability", "work packages", "authority structure"],
            "likely_outputs": ["role assignments", "span-of-control decisions", "responsibility boundaries"],
            "required_artifacts": ["wbs", "project_management_plan", "schedule"],
            "confidence": 0.84,
            "justification": "Assignment of duties sits at the intersection of decomposition, capability management, and collaborative governance.",
        },
        "T21": {
            "functional_modes": ["stakeholder_management", "resource_management", "planning"],
            "pmi_domain_mappings": [
                m("program", "stakeholder_engagement", 4, ["program_p115_c50"]),
                m("portfolio", "value_management", 2, ["portfolio_p025_c14"]),
                m("risk_practice", "risk_management", 2, ["risk_practice_p031_c18"]),
            ],
            "likely_inputs": ["resource gaps", "supplier options", "budget constraints", "project priorities"],
            "likely_outputs": ["negotiated commitments", "resource agreements", "supplier concessions"],
            "required_artifacts": ["budget", "project_management_plan", "stakeholder_register"],
            "confidence": 0.79,
            "justification": "Negotiation is clearly stakeholder-facing but only partly formalized in the current PMI set, so the mapping is intentionally moderate-confidence.",
        },
    }


def direct_exposure_specs() -> dict[str, dict]:
    return {
        "T01": {"d": [2, 2, 3, 4, 3], "o": [4, 2, 3, 4], "c": 0.9, "j": "Execution management is highly monitorable and partially orchestrable, but still carries budget/scope accountability."},
        "T02": {"d": [3, 2, 2, 2, 2], "o": [4, 3, 2, 3], "c": 0.84, "j": "Agents can surface issues and options, but personnel problem resolution still depends on judgment and persuasion."},
        "T03": {"d": [3, 3, 2, 4, 3], "o": [2, 1, 1, 3], "c": 0.93, "j": "Milestone tracking is one of the most monitorable and reportable PM tasks."},
        "T04": {"d": [2, 3, 2, 2, 3], "o": [3, 2, 2, 3], "c": 0.83, "j": "Submission packaging and quality checks are agent-friendly, but final acceptance still needs human oversight."},
        "T05": {"d": [4, 3, 2, 1, 2], "o": [4, 3, 2, 3], "c": 0.89, "j": "Agents can collect and summarize customer signals, but priority interpretation remains highly human."},
        "T06": {"d": [3, 3, 4, 2, 2], "o": [4, 3, 4, 4], "c": 0.9, "j": "Plan modifications are structurally codifiable, but approval authority and accountability stay human."},
        "T07": {"d": [2, 2, 3, 1, 4], "o": [2, 2, 1, 2], "c": 0.92, "j": "Scheduling and meeting logistics are strongly tool-mediated and easy to automate."},
        "T08": {"d": [2, 2, 3, 3, 2], "o": [4, 3, 3, 4], "c": 0.86, "j": "Coordination support is feasible, but directing people remains a high-judgment management act."},
        "T09": {"d": [3, 4, 4, 2, 3], "o": [4, 2, 3, 3], "c": 0.9, "j": "Implementation planning and ROI analysis are highly exposable to analytic and drafting agents."},
        "T10": {"d": [3, 2, 3, 2, 3], "o": [3, 2, 2, 3], "c": 0.87, "j": "Resource need identification is estimable and pattern-friendly, but escalation choices still matter."},
        "T11": {"d": [3, 4, 4, 2, 3], "o": [4, 2, 3, 4], "c": 0.92, "j": "Integrated project planning is highly exposable to agentic drafting and synthesis, but ownership remains human."},
        "T12": {"d": [4, 3, 3, 3, 3], "o": [3, 2, 2, 4], "c": 0.91, "j": "Risk analysis and response suggestion are strongly exposable, while ultimate risk ownership stays human."},
        "T13": {"d": [3, 4, 2, 3, 4], "o": [2, 1, 1, 3], "c": 0.95, "j": "Status reporting is one of the strongest direct exposure cases in the corpus."},
        "T14": {"d": [3, 3, 2, 2, 3], "o": [4, 3, 3, 3], "c": 0.78, "j": "Vendors can be screened and compared by agents, but selection still has commercial and relational judgment."},
        "T15": {"d": [3, 4, 3, 3, 3], "o": [4, 2, 3, 4], "c": 0.9, "j": "Budget development and tracking are highly analytic, but spending authority remains human."},
        "T16": {"d": [3, 4, 4, 2, 3], "o": [3, 2, 2, 3], "c": 0.92, "j": "Communication planning is highly draftable and orchestrable by agents."},
        "T17": {"d": [2, 3, 4, 2, 3], "o": [3, 1, 2, 3], "c": 0.94, "j": "WBS development is structurally codifiable and strongly supported by decomposition tools."},
        "T18": {"d": [3, 3, 2, 3, 2], "o": [4, 3, 3, 4], "c": 0.79, "j": "Agents can surface performance signals, but feedback conversations and consequences remain human-intensive."},
        "T19": {"d": [3, 3, 2, 2, 3], "o": [4, 3, 2, 3], "c": 0.8, "j": "Recruitment coordination is partly automatable, but selection standards and fit remain human-sensitive."},
        "T20": {"d": [2, 2, 4, 2, 2], "o": [4, 3, 4, 4], "c": 0.82, "j": "Assignment logic can be optimized, but authority and accountability remain strongly human."},
        "T21": {"d": [3, 2, 3, 1, 1], "o": [4, 4, 3, 4], "c": 0.78, "j": "Agents can prep negotiation briefs, but the actual bargaining and commitment-making are low-direct, high-oversight work."},
    }


def positive_edges() -> list[dict]:
    def e(source, target, relation, strength, confidence, evidence, justification):
        return {
            "source_task_id": source,
            "target_task_id": target,
            "relation_type": relation,
            "dependency_strength": strength,
            "evidence_chunk_ids": evidence,
            "confidence": confidence,
            "justification": justification,
        }

    return [
        e("T05", "T11", "informs", 4, 0.93, ["requirements_pg_p032_c12", "requirements_pg_p041_c17"], "Customer needs are a direct planning input."),
        e("T05", "T09", "informs", 3, 0.88, ["ba_practice_p039_c24", "benefits_pg_p001_c01"], "Need prioritization shapes implementation and ROI logic."),
        e("T05", "T16", "informs", 2, 0.8, ["program_p115_c50", "requirements_pg_p032_c12"], "Stakeholder needs inform communication planning."),
        e("T05", "T17", "informs", 3, 0.85, ["requirements_pg_p032_c12", "wbs_pg_p001_c01"], "Requirements and customer priorities shape scope decomposition."),
        e("T05", "T14", "informs", 2, 0.74, ["program_p115_c50", "ba_practice_p039_c24"], "Customer needs affect vendor criteria and sourcing options."),
        e("T09", "T11", "informs", 3, 0.87, ["estimating_pg_p001_c01", "benefits_pg_p001_c01"], "Implementation analyses feed the integrated plan."),
        e("T09", "T15", "informs", 3, 0.9, ["estimating_pg_p001_c01"], "Implementation planning creates budget assumptions."),
        e("T09", "T10", "informs", 3, 0.85, ["estimating_pg_p001_c01", "portfolio_p063_c38"], "Implementation design identifies resource needs."),
        e("T09", "T21", "informs", 2, 0.72, ["benefits_pg_p001_c01", "portfolio_p095_c58"], "Cost-benefit framing helps negotiation positions."),
        e("T10", "T19", "enables", 3, 0.88, ["portfolio_p063_c38"], "Identified staffing gaps trigger recruitment activity."),
        e("T10", "T14", "enables", 3, 0.86, ["portfolio_p063_c38"], "Non-staff resource gaps trigger vendor sourcing."),
        e("T10", "T15", "informs", 2, 0.83, ["estimating_pg_p001_c01", "portfolio_p063_c38"], "Resource need affects budget volume."),
        e("T10", "T21", "informs", 2, 0.79, ["portfolio_p063_c38"], "Identified resource gaps frame later negotiation."),
        e("T11", "T01", "enables", 4, 0.96, ["evm_p041_c24", "evm_p043_c25"], "Integrated planning enables controlled execution."),
        e("T11", "T03", "enables", 3, 0.9, ["scheduling_pg_p069_c30", "evm_p041_c24"], "Plan content defines what milestones and deliverables are tracked."),
        e("T11", "T06", "enables", 3, 0.86, ["evm_p043_c25", "risk_practice_p059_c35"], "A formal plan provides the object that later gets changed."),
        e("T11", "T07", "enables", 2, 0.76, ["evm_p108_c65", "program_p115_c50"], "Planned governance and stakeholder routines inform meeting cadence."),
        e("T11", "T15", "enables", 2, 0.81, ["estimating_pg_p001_c01", "evm_p041_c24"], "Integrated planning sharpens budget structure."),
        e("T11", "T16", "enables", 3, 0.88, ["evm_p108_c65", "requirements_pg_p032_c12"], "Communication planning depends on the integrated plan context."),
        e("T11", "T17", "enables", 3, 0.84, ["wbs_pg_p001_c01", "evm_p041_c24"], "Integrated planning and scope structure reinforce each other."),
        e("T12", "T11", "informs", 4, 0.94, ["risk_practice_p059_c35", "risk_practice_p031_c18"], "Risk strategy is integrated into the plan."),
        e("T12", "T01", "informs", 2, 0.8, ["risk_practice_p031_c18"], "Execution choices should reflect risk response strategy."),
        e("T12", "T06", "informs", 3, 0.88, ["risk_practice_p031_c18"], "Risk findings often trigger plan modifications."),
        e("T12", "T13", "informs", 3, 0.86, ["risk_practice_p059_c35", "evm_p108_c65"], "Risk posture should be visible in status reporting."),
        e("T12", "T21", "informs", 1, 0.7, ["risk_practice_p031_c18"], "Risk treatment sometimes shapes negotiating posture."),
        e("T15", "T01", "constrains", 3, 0.9, ["estimating_pg_p001_c01", "evm_p041_c24"], "Budget boundaries constrain how execution can proceed."),
        e("T15", "T13", "informs", 3, 0.89, ["evm_p033_c21"], "Budget status is a core reporting input."),
        e("T15", "T10", "constrains", 2, 0.78, ["portfolio_p063_c38", "estimating_pg_p001_c01"], "Available budget limits supplemental resource requests."),
        e("T16", "T07", "enables", 3, 0.91, ["evm_p108_c65"], "Meeting scheduling operationalizes the communication plan."),
        e("T16", "T13", "informs", 4, 0.93, ["evm_p108_c65", "evm_p033_c21"], "Status reporting follows planned communication pathways."),
        e("T16", "T02", "informs", 2, 0.76, ["program_p115_c50", "evm_p108_c65"], "Planned communication paths influence how issues are surfaced."),
        e("T17", "T01", "enables", 4, 0.95, ["wbs_pg_p001_c01", "wbs_pg_p018_c06"], "Execution requires defined work packages and scope structure."),
        e("T17", "T03", "enables", 3, 0.9, ["scheduling_pg_p069_c30"], "WBS elements trace to trackable schedule activities."),
        e("T17", "T10", "enables", 3, 0.88, ["wbs_pg_p018_c06", "portfolio_p063_c38"], "Decomposition clarifies what resources are needed."),
        e("T17", "T20", "enables", 3, 0.87, ["wbs_pg_p018_c06"], "Work breakdown informs responsibility assignment."),
        e("T19", "T20", "enables", 3, 0.85, ["portfolio_p063_c38"], "Recruitment fills roles that can then be assigned."),
        e("T19", "T08", "enables", 2, 0.77, ["portfolio_p063_c38"], "Recruitment supplies personnel for later coordination."),
        e("T14", "T21", "enables", 2, 0.73, ["program_p115_c50", "portfolio_p063_c38"], "Vendor review provides options and leverage for negotiation."),
        e("T14", "T01", "enables", 2, 0.74, ["portfolio_p063_c38"], "Selected vendors influence executable resource availability."),
        e("T14", "T10", "informs", 2, 0.71, ["portfolio_p063_c38"], "Vendor capability review refines resource-gap thinking."),
        e("T21", "T01", "enables", 3, 0.84, ["portfolio_p025_c14", "program_p115_c50"], "Negotiated resources and commitments unlock execution."),
        e("T21", "T10", "informs", 2, 0.72, ["portfolio_p063_c38"], "Negotiation outcomes refine resource needs and feasibility."),
        e("T07", "T02", "enables", 2, 0.75, ["evm_p108_c65"], "Meetings create the venue for issue identification and resolution."),
        e("T07", "T13", "enables", 2, 0.73, ["evm_p108_c65"], "Meetings produce updates that often feed formal status reports."),
        e("T02", "T06", "informs", 3, 0.89, ["risk_practice_p031_c18", "evm_p033_c21"], "Resolved and unresolved issues often trigger plan changes."),
        e("T02", "T13", "informs", 3, 0.87, ["evm_p033_c21"], "Issue trends are part of project status narratives."),
        e("T02", "T01", "informs", 2, 0.79, ["program_p142_c63"], "Problem resolution changes execution choices and pacing."),
        e("T03", "T13", "informs", 4, 0.95, ["evm_p033_c21", "evm_p108_c65"], "Milestone and deliverable status are core report inputs."),
        e("T03", "T06", "informs", 3, 0.88, ["evm_p033_c21"], "Tracking reveals slippage that can require plan updates."),
        e("T03", "T04", "enables", 3, 0.86, ["scheduling_pg_p069_c30"], "Deliverable submission typically follows milestone completion."),
        e("T08", "T01", "enables", 4, 0.91, ["program_p142_c63"], "Personnel coordination is a direct enabler of execution."),
        e("T08", "T18", "enables", 3, 0.82, ["program_p142_c63"], "Directed work creates the basis for later performance feedback."),
        e("T18", "T08", "informs", 2, 0.76, ["portfolio_p063_c38"], "Feedback informs how personnel are coordinated next."),
        e("T18", "T19", "informs", 2, 0.71, ["portfolio_p063_c38"], "Performance observations can imply a staffing or replacement need."),
        e("T20", "T08", "enables", 4, 0.89, ["wbs_pg_p018_c06", "portfolio_p063_c38"], "Assigned responsibilities operationalize coordination."),
        e("T20", "T01", "enables", 3, 0.87, ["wbs_pg_p018_c06"], "Execution depends on clear responsibility and authority."),
        e("T20", "T18", "informs", 2, 0.75, ["wbs_pg_p018_c06"], "Performance feedback depends on defined roles and expectations."),
        e("T06", "T11", "changes", 4, 0.95, ["evm_p043_c25"], "Plan changes flow back into the integrated plan itself."),
        e("T06", "T01", "changes", 3, 0.88, ["evm_p043_c25", "evm_p041_c24"], "Approved modifications alter execution conditions."),
        e("T06", "T03", "changes", 2, 0.8, ["evm_p043_c25"], "Plan changes can alter what milestones are monitored."),
        e("T01", "T03", "informs", 3, 0.85, ["evm_p033_c21"], "Actual execution progress is what milestone tracking reads."),
        e("T01", "T04", "enables", 3, 0.86, ["benefits_pg_p001_c01"], "Execution produces the work that can be submitted as deliverables."),
        e("T01", "T13", "informs", 3, 0.87, ["evm_p033_c21"], "Execution outcomes generate reportable status and trend data."),
        e("T01", "T06", "informs", 2, 0.79, ["evm_p033_c21"], "Execution variance can trigger change review."),
        e("T13", "T06", "informs", 3, 0.84, ["evm_p033_c21", "evm_p108_c65"], "Formal reports escalate issues and variances into change decisions."),
        e("T13", "T16", "communicates_with", 2, 0.76, ["evm_p108_c65"], "Status reporting and communication planning reinforce each other."),
        e("T04", "T13", "informs", 2, 0.78, ["benefits_pg_p001_c01", "evm_p033_c21"], "Delivered outputs affect status narratives and perceived progress."),
    ]


def build_focus_chunks() -> list[dict]:
    chunk_lookup = {row["chunk_id"]: row for row in load_jsonl(OUTPUT / "pmi_chunks.jsonl")}
    focused = []
    for chunk_id, spec in evidence_definitions().items():
        row = chunk_lookup[chunk_id]
        focused.append(
            {
                "chunk_id": chunk_id,
                "standard_source": row["source_id"],
                "page_start": row["page_start"],
                "page_end": row["page_end"],
                "summary": spec["summary"],
                "domain_tags": spec["domain_tags"],
                "artifact_tags": spec["artifact_tags"],
                "verb_tags": spec["verb_tags"],
                "evidence_strength": spec["evidence_strength"],
                "confidence": spec["confidence"],
                "display_title": row["display_title"],
                "source_text_excerpt": " ".join(row["text"].split())[:500],
            }
        )
    focused.sort(key=lambda item: (item["standard_source"], item["page_start"], item["chunk_id"]))
    return focused


def build_task_profiles(tasks: list[dict], edge_rows: list[dict]) -> list[dict]:
    specs = task_specs()
    upstream: dict[str, set[str]] = {task["task_id"]: set() for task in tasks}
    downstream: dict[str, set[str]] = {task["task_id"]: set() for task in tasks}
    for edge in edge_rows:
        upstream[edge["target_task_id"]].add(edge["source_task_id"])
        downstream[edge["source_task_id"]].add(edge["target_task_id"])

    profiles = []
    task_text = {task["task_id"]: task["onet_task_text"] for task in tasks}
    task_importance = {task["task_id"]: task["onet_importance"] for task in tasks}
    for task_id, spec in specs.items():
        evidence_ids = []
        for mapping in spec["pmi_domain_mappings"]:
            evidence_ids.extend(mapping["chunk_ids"])
        profile = {
            "task_id": task_id,
            "onet_task_text": task_text[task_id],
            "onet_importance": task_importance[task_id],
            "functional_modes": spec["functional_modes"],
            "pmi_domain_mappings": spec["pmi_domain_mappings"],
            "likely_inputs": spec["likely_inputs"],
            "likely_outputs": spec["likely_outputs"],
            "required_artifacts": spec["required_artifacts"],
            "likely_upstream_task_ids": sorted(upstream[task_id]),
            "likely_downstream_task_ids": sorted(downstream[task_id]),
            "evidence_chunk_ids": sorted(set(evidence_ids)),
            "confidence": spec["confidence"],
            "justification": spec["justification"],
        }
        profiles.append(profile)
    return sorted(profiles, key=lambda item: item["task_id"])


def build_direct_exposure() -> list[dict]:
    specs = direct_exposure_specs()
    rows = []
    for task_id, spec in specs.items():
        rows.append(
            {
                "task_id": task_id,
                "direct_dimensions": {
                    "information_gathering": spec["d"][0],
                    "synthesis_reporting": spec["d"][1],
                    "planning_orchestration": spec["d"][2],
                    "monitoring_exception_detection": spec["d"][3],
                    "tool_mediated_execution": spec["d"][4],
                },
                "oversight_dimensions": {
                    "stakeholder_judgment": spec["o"][0],
                    "negotiation_persuasion": spec["o"][1],
                    "approval_authority": spec["o"][2],
                    "accountability_risk_ownership": spec["o"][3],
                },
                "evidence_chunk_ids": sorted(set(task_specs()[task_id]["evidence_chunk_ids"] if "evidence_chunk_ids" in task_specs()[task_id] else [])) or sorted(
                    set(
                        chunk_id
                        for mapping in task_specs()[task_id]["pmi_domain_mappings"]
                        for chunk_id in mapping["chunk_ids"]
                    )
                ),
                "confidence": spec["c"],
                "justification": spec["j"],
            }
        )
    return sorted(rows, key=lambda item: item["task_id"])


def build_adjudications() -> list[dict]:
    return [
        {
            "review_item_id": "task_profile_T14",
            "review_type": "task_profile",
            "issue_type": "low_confidence",
            "decision": "confirm",
            "revised_fields": {},
            "replacement_evidence_chunk_ids": ["program_p115_c50", "portfolio_p063_c38", "risk_practice_p031_c18"],
            "confidence": 0.8,
            "justification": "Dedicated procurement guidance is absent, but the stakeholder-capacity-risk framing is sufficient for a pilot profile.",
        },
        {
            "review_item_id": "task_profile_T18",
            "review_type": "task_profile",
            "issue_type": "low_confidence",
            "decision": "confirm",
            "revised_fields": {},
            "replacement_evidence_chunk_ids": ["program_p142_c63", "portfolio_p063_c38"],
            "confidence": 0.78,
            "justification": "Performance feedback is indirectly covered through collaboration and capability management, which is acceptable for the present corpus.",
        },
        {
            "review_item_id": "direct_exposure_T21",
            "review_type": "direct_exposure",
            "issue_type": "inconsistent_score",
            "decision": "revise",
            "revised_fields": {"direct_dimensions.tool_mediated_execution": 1},
            "replacement_evidence_chunk_ids": ["program_p115_c50", "portfolio_p025_c14"],
            "confidence": 0.83,
            "justification": "Negotiation preparation is tool-assisted, but the negotiation act itself is less directly executable than initially estimated.",
        },
        {
            "review_item_id": "task_dependency_T05_T16",
            "review_type": "task_dependency",
            "issue_type": "weak_rationale",
            "decision": "confirm",
            "revised_fields": {},
            "replacement_evidence_chunk_ids": ["program_p115_c50", "requirements_pg_p032_c12"],
            "confidence": 0.79,
            "justification": "Customer and stakeholder needs legitimately shape what communication must be planned.",
        },
        {
            "review_item_id": "task_dependency_T14_T21",
            "review_type": "task_dependency",
            "issue_type": "inconsistent_score",
            "decision": "revise",
            "revised_fields": {"dependency_strength": 2},
            "replacement_evidence_chunk_ids": ["program_p115_c50", "portfolio_p063_c38"],
            "confidence": 0.77,
            "justification": "Vendor review prepares negotiation but does not fully determine the bargaining outcome, so moderate strength fits better than strong.",
        },
        {
            "review_item_id": "task_dependency_T18_T19",
            "review_type": "task_dependency",
            "issue_type": "low_confidence",
            "decision": "confirm",
            "revised_fields": {},
            "replacement_evidence_chunk_ids": ["portfolio_p063_c38"],
            "confidence": 0.73,
            "justification": "Observed underperformance can legitimately create a staffing or recruitment signal even if the dependency is weak.",
        },
    ]


def full_dependency_matrix(tasks: list[dict], sparse_edges: list[dict]) -> list[dict]:
    sparse_lookup = {
        (edge["source_task_id"], edge["target_task_id"]): edge
        for edge in sparse_edges
    }
    task_ids = [task["task_id"] for task in tasks]
    rows = []
    for source_id in task_ids:
        for target_id in task_ids:
            if source_id == target_id:
                continue
            edge = sparse_lookup.get((source_id, target_id))
            if edge:
                rows.append(edge)
            else:
                rows.append(
                    {
                        "source_task_id": source_id,
                        "target_task_id": target_id,
                        "relation_type": "none",
                        "dependency_strength": 0,
                        "evidence_chunk_ids": [],
                        "confidence": 0.68,
                        "justification": "No material PMI-grounded dependency was retained for this directed pair in the sparse graph.",
                    }
                )
    return rows


def compute_scores(tasks: list[dict], exposure_rows: list[dict], sparse_edges: list[dict]) -> tuple[list[dict], dict]:
    importance_map = {task["task_id"]: task["onet_importance"] for task in tasks}
    task_text_map = {task["task_id"]: task["onet_task_text"] for task in tasks}
    total_importance = sum(importance_map.values())

    exposure_lookup = {}
    for row in exposure_rows:
        direct = row["direct_dimensions"]
        oversight = row["oversight_dimensions"]
        dae = 100 * sum(direct.values()) / 20
        oc = 100 * sum(oversight.values()) / 16
        exposure_lookup[row["task_id"]] = {
            "DAE": round(dae, 2),
            "OC": round(oc, 2),
            **direct,
            **oversight,
        }

    graph = nx.DiGraph()
    for task in tasks:
        graph.add_node(task["task_id"])
    for edge in sparse_edges:
        weight = (edge["dependency_strength"] / 4) * edge["confidence"]
        graph.add_edge(
            edge["source_task_id"],
            edge["target_task_id"],
            weight=weight,
            distance=1 / (weight + 0.001),
            relation=edge["relation_type"],
        )

    out_strength = {node: 0.0 for node in graph.nodes}
    in_strength = {node: 0.0 for node in graph.nodes}
    for u, v, data in graph.edges(data=True):
        out_strength[u] += data["weight"]
        in_strength[v] += data["weight"]

    def normalize(values: dict[str, float]) -> dict[str, float]:
        max_val = max(values.values()) if values else 0
        if max_val == 0:
            return {k: 0.0 for k in values}
        return {k: v / max_val for k, v in values.items()}

    sout = normalize(out_strength)
    sin = normalize(in_strength)
    bet = nx.betweenness_centrality(graph, weight="distance", normalized=True)
    pagerank = nx.pagerank(graph, weight="weight")
    pr_min = min(pagerank.values()) if pagerank else 0
    pr_max = max(pagerank.values()) if pagerank else 0
    if pr_max == pr_min:
        pr_norm = {node: 0.0 for node in graph.nodes}
    else:
        pr_norm = {node: (score - pr_min) / (pr_max - pr_min) for node, score in pagerank.items()}

    task_score_rows = []
    for task in tasks:
        task_id = task["task_id"]
        ic = 100 * ((0.30 * sout[task_id]) + (0.30 * sin[task_id]) + (0.20 * bet[task_id]) + (0.20 * pr_norm[task_id]))
        se = (exposure_lookup[task_id]["DAE"] * ic) / 100
        weight = importance_map[task_id] / total_importance
        task_score_rows.append(
            {
                "task_id": task_id,
                "onet_task_text": task_text_map[task_id],
                "onet_importance": importance_map[task_id],
                "importance_weight": round(weight, 6),
                "DAE": round(exposure_lookup[task_id]["DAE"], 2),
                "OC": round(exposure_lookup[task_id]["OC"], 2),
                "IC": round(ic, 2),
                "SE": round(se, 2),
                "information_gathering": exposure_lookup[task_id]["information_gathering"],
                "synthesis_reporting": exposure_lookup[task_id]["synthesis_reporting"],
                "planning_orchestration": exposure_lookup[task_id]["planning_orchestration"],
                "monitoring_exception_detection": exposure_lookup[task_id]["monitoring_exception_detection"],
                "tool_mediated_execution": exposure_lookup[task_id]["tool_mediated_execution"],
                "stakeholder_judgment": exposure_lookup[task_id]["stakeholder_judgment"],
                "negotiation_persuasion": exposure_lookup[task_id]["negotiation_persuasion"],
                "approval_authority": exposure_lookup[task_id]["approval_authority"],
                "accountability_risk_ownership": exposure_lookup[task_id]["accountability_risk_ownership"],
            }
        )

    occupation = {
        "occupation_code": "15-1299.09",
        "occupation_label": "Project Management Specialists / Information Project Managers",
        "Occupation_DAE": round(sum(row["importance_weight"] * row["DAE"] for row in task_score_rows), 2),
        "Occupation_OC": round(sum(row["importance_weight"] * row["OC"] for row in task_score_rows), 2),
        "Occupation_IC": round(sum(row["importance_weight"] * row["IC"] for row in task_score_rows), 2),
        "Occupation_SE": round(sum(row["importance_weight"] * row["SE"] for row in task_score_rows), 2),
    }
    occupation["Composite_Impact"] = round(
        0.35 * occupation["Occupation_DAE"]
        + 0.35 * occupation["Occupation_SE"]
        + 0.20 * occupation["Occupation_IC"]
        + 0.10 * (100 - occupation["Occupation_OC"]),
        2,
    )
    return task_score_rows, occupation


def build_audit_workbook(
    tasks: list[dict],
    profiles: list[dict],
    exposures: list[dict],
    full_edges: list[dict],
    adjudications: list[dict],
    task_scores: list[dict],
) -> tuple[list[dict], dict]:
    task_text_map = {task["task_id"]: task["onet_task_text"] for task in tasks}
    score_map = {row["task_id"]: row for row in task_scores}
    audit_rows: list[dict] = []

    def base_row(
        record_id: str,
        record_type: str,
        confidence: float | str,
        evidence_count: int,
        review_reasons: list[str],
        priority_rank: int,
        **extra: object,
    ) -> dict:
        priority_label = "high" if priority_rank == 1 else "medium" if priority_rank == 2 else "standard"
        row = {
            "record_id": record_id,
            "record_type": record_type,
            "priority_label": priority_label,
            "task_id": "",
            "source_task_id": "",
            "target_task_id": "",
            "onet_task_text": "",
            "target_task_text": "",
            "relation_type": "",
            "dependency_strength": "",
            "confidence": confidence,
            "evidence_count": evidence_count,
            "review_reason": "|".join(review_reasons),
            "DAE": "",
            "OC": "",
            "IC": "",
            "SE": "",
            "accept_or_reject": "",
            "reason": "",
            "prompt_change_needed": "",
            "weight_change_needed": "",
            "notes": "",
            "_priority_rank": priority_rank,
        }
        row.update(extra)
        return row

    for row in profiles:
        reasons = ["all_task_profiles"]
        if row["confidence"] < 0.75:
            reasons.append("low_confidence")
        if len(row["evidence_chunk_ids"]) < 2:
            reasons.append("thin_evidence")
        scores = score_map[row["task_id"]]
        priority = 1 if "low_confidence" in reasons or "thin_evidence" in reasons else 3
        audit_rows.append(
            base_row(
                record_id=f"task_profile_{row['task_id']}",
                record_type="task_profile",
                confidence=row["confidence"],
                evidence_count=len(row["evidence_chunk_ids"]),
                review_reasons=reasons,
                priority_rank=priority,
                task_id=row["task_id"],
                onet_task_text=row["onet_task_text"],
                DAE=scores["DAE"],
                OC=scores["OC"],
                IC=scores["IC"],
                SE=scores["SE"],
            )
        )

    for row in exposures:
        reasons = ["all_direct_exposure"]
        if row["confidence"] < 0.75:
            reasons.append("low_confidence")
        if len(row["evidence_chunk_ids"]) < 2:
            reasons.append("thin_evidence")
        scores = score_map[row["task_id"]]
        priority = 1 if "low_confidence" in reasons or "thin_evidence" in reasons else 3
        audit_rows.append(
            base_row(
                record_id=f"direct_exposure_{row['task_id']}",
                record_type="direct_exposure",
                confidence=row["confidence"],
                evidence_count=len(row["evidence_chunk_ids"]),
                review_reasons=reasons,
                priority_rank=priority,
                task_id=row["task_id"],
                onet_task_text=task_text_map[row["task_id"]],
                DAE=scores["DAE"],
                OC=scores["OC"],
                IC=scores["IC"],
                SE=scores["SE"],
            )
        )

    for row in full_edges:
        reasons = []
        if row["dependency_strength"] >= 3:
            reasons.append("strong_edge")
        if row["confidence"] < 0.75:
            reasons.append("low_confidence")
        if len(row["evidence_chunk_ids"]) < 2:
            reasons.append("thin_evidence")
        if not reasons:
            continue
        priority = 1 if "strong_edge" in reasons else 2
        scores = score_map[row["source_task_id"]]
        audit_rows.append(
            base_row(
                record_id=f"dependency_{row['source_task_id']}_{row['target_task_id']}",
                record_type="task_dependency",
                confidence=row["confidence"],
                evidence_count=len(row["evidence_chunk_ids"]),
                review_reasons=reasons,
                priority_rank=priority,
                task_id=row["source_task_id"],
                source_task_id=row["source_task_id"],
                target_task_id=row["target_task_id"],
                onet_task_text=task_text_map[row["source_task_id"]],
                target_task_text=task_text_map[row["target_task_id"]],
                relation_type=row["relation_type"],
                dependency_strength=row["dependency_strength"],
                DAE=scores["DAE"],
                OC=scores["OC"],
                IC=scores["IC"],
                SE=scores["SE"],
            )
        )

    for row in adjudications:
        if row["decision"] not in {"revise", "escalate_for_human"}:
            continue
        task_id = ""
        item_parts = row["review_item_id"].split("_")
        if row["review_type"] in {"task_profile", "direct_exposure"} and item_parts:
            task_id = item_parts[-1]
        elif row["review_type"] == "task_dependency" and len(item_parts) >= 4:
            task_id = item_parts[-2]
        scores = score_map.get(task_id, {})
        audit_rows.append(
            base_row(
                record_id=f"adjudication_{row['review_item_id']}",
                record_type="adjudication",
                confidence=row["confidence"],
                evidence_count=len(row["replacement_evidence_chunk_ids"]),
                review_reasons=[f"adjudication_{row['decision']}"],
                priority_rank=1,
                task_id=task_id,
                onet_task_text=task_text_map.get(task_id, ""),
                DAE=scores.get("DAE", ""),
                OC=scores.get("OC", ""),
                IC=scores.get("IC", ""),
                SE=scores.get("SE", ""),
                notes=row["justification"],
            )
        )

    audit_rows.sort(
        key=lambda row: (
            row["_priority_rank"],
            row["record_type"],
            row["task_id"],
            row["target_task_id"],
            row["record_id"],
        )
    )
    for row in audit_rows:
        row.pop("_priority_rank", None)

    reason_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    for row in audit_rows:
        type_counts[row["record_type"]] = type_counts.get(row["record_type"], 0) + 1
        for reason in row["review_reason"].split("|"):
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

    summary = {
        "audit_record_count": len(audit_rows),
        "record_type_counts": type_counts,
        "review_reason_counts": reason_counts,
    }
    return audit_rows, summary


def main() -> None:
    tasks = load_json(OUTPUT / "canonical_tasks.json")

    focus_chunks = build_focus_chunks()
    write_jsonl(OUTPUT / "pmi_focus_chunks_tagged.jsonl", focus_chunks)

    sparse_edges = positive_edges()
    profiles = build_task_profiles(tasks, sparse_edges)
    exposures = build_direct_exposure()

    # Apply adjudicated revision to T21 direct exposure before scoring/export.
    for row in exposures:
        if row["task_id"] == "T21":
            row["direct_dimensions"]["tool_mediated_execution"] = 1

    adjudications = build_adjudications()
    full_edges = full_dependency_matrix(tasks, sparse_edges)
    task_scores, occupation_scores = compute_scores(tasks, exposures, sparse_edges)
    audit_rows, audit_summary = build_audit_workbook(tasks, profiles, exposures, full_edges, adjudications, task_scores)

    graph_edges = []
    for edge in sparse_edges:
        weight = round((edge["dependency_strength"] / 4) * edge["confidence"], 4)
        graph_edges.append(
            {
                "source_task_id": edge["source_task_id"],
                "target_task_id": edge["target_task_id"],
                "relation_type": edge["relation_type"],
                "dependency_strength": edge["dependency_strength"],
                "confidence": edge["confidence"],
                "weight": weight,
                "evidence_chunk_ids": "|".join(edge["evidence_chunk_ids"]),
                "justification": edge["justification"],
            }
        )

    write_jsonl(OUTPUT / "task_profiles.jsonl", profiles)
    write_jsonl(OUTPUT / "direct_exposure.jsonl", exposures)
    write_jsonl(OUTPUT / "task_dependencies.jsonl", full_edges)
    write_jsonl(OUTPUT / "adjudications.jsonl", adjudications)
    write_csv(
        OUTPUT / "graph_edges.csv",
        [
            "source_task_id",
            "target_task_id",
            "relation_type",
            "dependency_strength",
            "confidence",
            "weight",
            "evidence_chunk_ids",
            "justification",
        ],
        graph_edges,
    )
    write_csv(
        OUTPUT / "task_scores.csv",
        [
            "task_id",
            "onet_task_text",
            "onet_importance",
            "importance_weight",
            "DAE",
            "OC",
            "IC",
            "SE",
            "information_gathering",
            "synthesis_reporting",
            "planning_orchestration",
            "monitoring_exception_detection",
            "tool_mediated_execution",
            "stakeholder_judgment",
            "negotiation_persuasion",
            "approval_authority",
            "accountability_risk_ownership",
        ],
        task_scores,
    )
    write_csv(
        OUTPUT / "audit_workbook.csv",
        [
            "record_id",
            "record_type",
            "priority_label",
            "task_id",
            "source_task_id",
            "target_task_id",
            "onet_task_text",
            "target_task_text",
            "relation_type",
            "dependency_strength",
            "confidence",
            "evidence_count",
            "review_reason",
            "DAE",
            "OC",
            "IC",
            "SE",
            "accept_or_reject",
            "reason",
            "prompt_change_needed",
            "weight_change_needed",
            "notes",
        ],
        audit_rows,
    )
    write_json(OUTPUT / "occupation_scores.json", occupation_scores)
    write_json(OUTPUT / "audit_summary.json", audit_summary)

    run_summary = {
        "focus_chunk_count": len(focus_chunks),
        "task_profile_count": len(profiles),
        "direct_exposure_count": len(exposures),
        "positive_edge_count": len(sparse_edges),
        "full_dependency_pair_count": len(full_edges),
        "adjudication_count": len(adjudications),
        "audit_record_count": len(audit_rows),
        "composite_impact": occupation_scores["Composite_Impact"],
    }
    write_json(OUTPUT / "step2_to_step4_summary.json", run_summary)


if __name__ == "__main__":
    main()
