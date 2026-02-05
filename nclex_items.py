import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# ✅ IMPORTANT: This should point to your real cases file
# If your file is named Cases.json (not .docx), use that instead.
CASES_PATH = BASE_DIR / "Cases.json"

OUT_PATH = BASE_DIR / "nclex_items.json"

TYPES_CYCLE = ["mcq", "sata", "ordered_response", "cloze", "matrix", "evolving_case"]

CLIENT_NEEDS = [
    "Physiological Integrity",
    "Safe and Effective Care Environment",
    "Health Promotion and Maintenance",
    "Psychosocial Integrity",
]


def load_case_ids() -> list[str]:
    """
    Expects Cases.json to be a LIST of 20 case objects like:
    [
      {"id": "adult_acs_01", "title": "...", ...},
      ...
    ]
    """
    if not CASES_PATH.exists():
        raise FileNotFoundError(
            f"Cannot find {CASES_PATH}. Put your real Cases.json in the same folder as this script."
        )

    raw = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    if not isinstance(raw, list):
        raise ValueError("Cases.json must be a JSON LIST (array) of case objects.")

    ids = []
    for c in raw:
        cid = c.get("id")
        if not cid:
            raise ValueError("A case in Cases.json is missing 'id'.")
        ids.append(cid)

    if len(ids) != 20:
        raise ValueError(f"Expected 20 cases in Cases.json, found {len(ids)}.")

    # keep order as in file
    return ids


def make_item(case_id: str, qnum: int, qtype: str) -> dict:
    qid = f"{case_id}-Q{qnum:02d}"
    client_need = CLIENT_NEEDS[(qnum - 1) % len(CLIENT_NEEDS)]
    stem_prefix = "Based on the patient scenario in this case,"

    base = {"id": qid, "type": qtype, "client_need": client_need}

    if qtype in ("mcq", "best_answer"):
        base.update(
            {
                "stem": f"{stem_prefix} what is the most appropriate NEXT nursing action?",
                "options": [
                    "Assess airway/breathing/circulation and obtain full vital signs",
                    "Implement immediate safety measures and call for help per protocol",
                    "Administer a medication without verifying orders/allergies",
                    "Delay care and recheck in 1 hour without reassessment",
                ],
                "correct": "Implement immediate safety measures and call for help per protocol",
                "rationale": "Prioritize safety/ABC, immediate stabilization, and timely escalation; avoid unsafe delays or unverified meds.",
            }
        )

    elif qtype == "sata":
        base.update(
            {
                "stem": f"{stem_prefix} which actions are appropriate to ensure patient safety? (Select all that apply.)",
                "options": [
                    "Verify patient identity and allergies before interventions",
                    "Initiate continuous monitoring and reassess frequently",
                    "Document baseline findings and trends",
                    "Change prescribed doses independently",
                    "Escalate concerns using SBAR when thresholds are met",
                ],
                "correct": [
                    "Verify patient identity and allergies before interventions",
                    "Initiate continuous monitoring and reassess frequently",
                    "Document baseline findings and trends",
                    "Escalate concerns using SBAR when thresholds are met",
                ],
                "rationale": "Safety actions include verification, monitoring, documentation, and escalation; independent dose changes are unsafe.",
            }
        )

    elif qtype == "ordered_response":
        base.update(
            {
                "stem": f"{stem_prefix} place the nursing actions in priority order (first → last).",
                "options": [
                    "Reassess and trend focused findings",
                    "Ensure safety/ABC and call for assistance if unstable",
                    "Prepare for provider notification with SBAR",
                    "Implement ordered interventions and evaluate response",
                ],
                "correct": [
                    "Ensure safety/ABC and call for assistance if unstable",
                    "Reassess and trend focused findings",
                    "Prepare for provider notification with SBAR",
                    "Implement ordered interventions and evaluate response",
                ],
                "rationale": "Start with safety/ABC, then focused reassessment and escalation prep; implement and evaluate interventions.",
            }
        )

    elif qtype == "cloze":
        base.update(
            {
                "stem": f"{stem_prefix} fill in the blank: The nurse should teach the patient to ________ to reduce recurrence/worsening.",
                "correct_text": "follow the care plan and report red-flag symptoms promptly",
                "acceptable": [
                    "follow the care plan and report red-flag symptoms promptly",
                    "adhere to the plan and report warning signs promptly",
                ],
                "rationale": "Clear return-precautions and adherence education reduces complications and supports maintenance.",
            }
        )

    elif qtype == "matrix":
        base.update(
            {
                "stem": f"{stem_prefix} for each finding, select whether it requires immediate escalation.",
                "rows": [
                    "New/worsening respiratory distress",
                    "Stable vital signs with mild discomfort",
                    "Acute change in level of consciousness",
                ],
                "cols": ["Escalate now", "Monitor/reassess"],
                "correct": {
                    "New/worsening respiratory distress": "Escalate now",
                    "Stable vital signs with mild discomfort": "Monitor/reassess",
                    "Acute change in level of consciousness": "Escalate now",
                },
                "rationale": "Escalate for acute deterioration or neuro/resp compromise; monitor if stable with low-risk symptoms.",
            }
        )

    elif qtype == "evolving_case":
        base.update(
            {
                "stem": f"{stem_prefix} answer as the case evolves through stages.",
                "stages": [
                    {
                        "stage": "Stage 1",
                        "update": "Initial assessment shows abnormal vitals requiring rapid reassessment.",
                        "question": {
                            "type": "mcq",
                            "stem": "What is the priority nursing focus now?",
                            "options": [
                                "Immediate ABC/safety assessment and escalation per protocol",
                                "Complete non-urgent documentation first",
                                "Wait for the next scheduled vital signs",
                                "Provide reassurance only",
                            ],
                            "correct": "Immediate ABC/safety assessment and escalation per protocol",
                        },
                    },
                    {
                        "stage": "Stage 2",
                        "update": "After first actions, the patient partially improves but one red flag remains.",
                        "question": {
                            "type": "sata",
                            "stem": "Which reassessment elements should be prioritized next? (Select all that apply.)",
                            "options": [
                                "Trend vitals and targeted assessment findings",
                                "Assess response to interventions and adverse effects",
                                "Update provider using SBAR with objective data",
                                "Stop monitoring to reduce alarms",
                                "Educate on safety precautions relevant to symptoms",
                            ],
                            "correct": [
                                "Trend vitals and targeted assessment findings",
                                "Assess response to interventions and adverse effects",
                                "Update provider using SBAR with objective data",
                                "Educate on safety precautions relevant to symptoms",
                            ],
                        },
                    },
                ],
                "rationale": "Evolving items test ongoing prioritization, reassessment, communication, and safety as new data appear.",
            }
        )

    else:
        raise ValueError(f"Unknown type: {qtype}")

    return base


def build_case(case_id: str, items_per_case: int = 30) -> dict:
    items = []
    for qnum in range(1, items_per_case + 1):
        qtype = TYPES_CYCLE[(qnum - 1) % len(TYPES_CYCLE)]
        items.append(make_item(case_id, qnum, qtype))
    return {"items": items}


def main():
    case_ids = load_case_ids()

    data = {"cases": {}}
    for cid in case_ids:
        data["cases"][cid] = build_case(cid, items_per_case=30)

    OUT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Wrote {OUT_PATH} with {len(case_ids) * 30} items total.")


if __name__ == "__main__":
    main()
