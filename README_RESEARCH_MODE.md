# ClinIQ Nurse / NurseReason (Commercial App File)

## Run
1. Create a fresh virtual environment (recommended)
2. Install requirements:
   - `pip install -r requirements.txt`
3. Put all required data files in the same folder as `app.py`
4. Run:
   - `streamlit run app.py`

## Required files (minimum to run)
- `app.py`  (main Streamlit app)
- `cases.json`
- `students.json`  (auto-created if missing, but recommended to include)
- `attempts_log.jsonl` (auto-created when students submit; can be empty)
- `attempts_policy.json`
- `admin_settings.json`
- `case_policy.json`
- `exam_access_policy.json`
- `nclex_policy.json`
- `nclex_items.json`
- `nclex_active_sets.json`  (auto-created if missing)
- `kpi_policy.json`

## Optional / safe to include
- `features.json` (feature flags; safe if missing)
- `autosave_drafts.jsonl` (created automatically; helps recovery)
- `backups/` folder (created automatically if backup_on_start enabled)
- `exports/` folder (created when exporting)

## Research Mode (Admin only)
This build adds a **Research Mode** toggle in the sidebar for admins. When enabled:
- Students are shown a **consent box** in the sidebar (if required).
- Extra analytics are recorded **only** when consent is given:
  - Answer-change behavior (first choice vs final choice, change count)
  - Section-level performance (Intake, A–E, SBAR, NCLEX)
  - Optional reflection (post-test)

Research records are written to:
- `research_log.jsonl` (separate from `attempts_log.jsonl`)

## NCLEX images
NCLEX item images are not displayed. You can also keep your data clean by using:
- `cleanup_nclex_items_images.py` (one-time cleaner)

## Export templates
- `research_export_template.csv` – suggested columns for buyers / IRB-style exports
- `research_export_template.sps` – SPSS import skeleton (edit paths as needed)
