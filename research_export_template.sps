* SPSS import template for research_export.csv (edit the FILE= path).
GET DATA
  /TYPE=TXT
  /FILE="research_export.csv"
  /DELCASE=LINE
  /DELIMITERS=","
  /QUALIFIER='"'
  /ARRANGEMENT=DELIMITED
  /FIRSTCASE=2
  /VARIABLES=
    timestamp A40
    event A20
    mode A20
    timer_minutes A20
    timer_expired F1.0
    caseId A60
    caseTitle A200
    system A60
    setting A60
    duration_sec F8.0
    student_token A40
    intake_score F8.0
    A_score F8.0
    B_score F8.0
    C_score F8.0
    D_score F8.0
    SBAR_score F8.0
    NCLEX_score F8.0
    NCLEX_total F8.0
    answer_changes_total F8.0
    reflection_text A500
  .
EXECUTE.
