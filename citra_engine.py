"""Core inference module for the ArahKita prototype.

The module uses only Python's standard library so it can be imported directly
by a Streamlit app without installing an AI or machine-learning package.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from career_catalog import ACTIVITY_TO_PRIMARY, CAREER_CATALOG


BASE_DIR = Path(__file__).resolve().parent

PRIMARY_RECOMMENDATIONS = {
    "RecommendWorkNow": "Work Now",
    "RecommendWorkPreparation": "Internship or Skill Preparation",
    "RecommendMastersPreparation": "Master's Preparation",
    "RecommendScholarshipPreparation": "Scholarship Preparation",
    "RecommendCareerExploration": "Career Exploration",
}

GOAL_FACTS = {
    career.lower(): "Goal" + "".join(character for character in career if character.isalnum())
    for career in CAREER_CATALOG
}

RECOMMENDATION_CATEGORIES = {
    "RecommendWorkNow": {"Job"},
    "RecommendWorkPreparation": {"Job", "Internship", "Certification"},
    "RecommendMastersPreparation": {"Master's Program"},
    "RecommendScholarshipPreparation": {"Scholarship"},
    "RecommendCareerExploration": {"Job", "Internship", "Certification"},
}

PREFERRED_ACTIVITY_FACTS = {
    "mengolah data dan mencari pola": "PrefersDataAnalysis",
    "membuat model prediksi atau otomasi": "PrefersPredictiveModeling",
    "menganalisis data biologis atau genomik": "PrefersBioinformatics",
    "membangun aplikasi atau sistem digital": "PrefersSoftwareBuilding",
    "melakukan eksperimen di laboratorium": "PrefersResearchActivity",
    "mengelola riset klinis dan data pasien": "PrefersClinicalResearch",
    "memastikan mutu, keamanan, dan kepatuhan regulasi": "PrefersQualityRegulatory",
    "merancang produk atau layanan kesehatan": "PrefersHealthProduct",
    "menulis dan menjelaskan informasi sains": "PrefersScienceCommunication",
    # Tetap menerima label versi awal agar input lama tidak langsung rusak.
    "mengolah data dan membuat dashboard": "PrefersDataAnalysis",
    "membuat model prediksi dari data": "PrefersPredictiveModeling",
    "membangun aplikasi atau sistem": "PrefersSoftwareBuilding",
    "melakukan eksperimen dan riset": "PrefersResearchActivity",
}

SUGGESTED_CAREERS = {
    "SuggestedDataAnalyst": "Data Analyst",
    "SuggestedDataScientist": "Data Scientist",
    "SuggestedSoftwareIT": "Software/IT",
    "SuggestedResearcher": "Researcher",
    "SuggestedBioinformaticsAnalyst": "Bioinformatics Analyst",
    "SuggestedClinicalResearch": "Clinical Research Associate",
    "SuggestedQualityRegulatory": "Quality Assurance & Regulatory Affairs",
    "SuggestedHealthProduct": "Health Product / Business Analyst",
    "SuggestedScienceCommunication": "Medical Writer / Science Communicator",
}

PREPARATION_FOCUS = {
    "PreparationFocusSkill": {
        "value": "skill",
        "label": "Skill preparation",
    },
    "PreparationFocusInternship": {
        "value": "internship",
        "label": "Internship preparation",
    },
}


class InferenceError(RuntimeError):
    """Raised when the knowledge base produces an invalid final state."""


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_rules(path: str | Path | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load and minimally validate the forward-chaining knowledge base."""

    data = _read_json(Path(path) if path else BASE_DIR / "rules.json")
    rules = data.get("rules", [])
    if not rules:
        raise ValueError("rules.json does not contain any rules")

    rule_ids: set[str] = set()
    for rule in rules:
        required = {"id", "antecedents", "conclusions", "explanation"}
        missing = required - set(rule)
        if missing:
            raise ValueError(f"Rule is missing fields {sorted(missing)}: {rule}")
        if rule["id"] in rule_ids:
            raise ValueError(f"Duplicate rule id: {rule['id']}")
        if len(rule["conclusions"]) != 1:
            raise ValueError(
                f"{rule['id']} must have exactly one conclusion to remain a definite clause"
            )
        rule_ids.add(rule["id"])

    return data.get("metadata", {}), rules


def load_templates(path: str | Path | None = None) -> dict[str, Any]:
    return _read_json(Path(path) if path else BASE_DIR / "recommendation_templates.json")


def load_opportunities(path: str | Path | None = None) -> list[dict[str, Any]]:
    data = _read_json(Path(path) if path else BASE_DIR / "qiara_opportunities.json")
    return data.get("opportunities", [])


def _normalized(value: Any) -> str:
    return str(value or "").strip().lower()


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    normalized = _normalized(value)
    if normalized in {"yes", "ya", "true", "1"}:
        return True
    if normalized in {"no", "tidak", "false", "0", "none", ""}:
        return False
    raise ValueError(f"Cannot interpret {value!r} as Yes/No")


def build_initial_facts(
    user_input: dict[str, Any], metadata: dict[str, Any]
) -> set[str]:
    """Convert explicit form answers into initial propositional facts."""

    facts: set[str] = set()

    education = _normalized(user_input.get("education_status"))
    if education == "final-year student":
        facts.add("IsFinalYearStudent")
    elif education == "fresh graduate":
        facts.add("IsFreshGraduate")
    else:
        raise ValueError("education_status must be 'Final-year student' or 'Fresh graduate'")

    major_group = _normalized(user_input.get("major_group"))
    if major_group in {"engineering", "science", "computing", "other stem"}:
        facts.add("HasSTEMBackground")

    career_goal_raw = str(user_input.get("career_goal", "")).strip()
    career_goal = career_goal_raw.lower()
    if career_goal in {"undecided", "belum yakin", ""}:
        facts.add("HasUnclearCareerGoal")
    elif career_goal in GOAL_FACTS:
        facts.update({"HasClearCareerGoal", GOAL_FACTS[career_goal]})
    else:
        raise ValueError("career_goal tidak ditemukan dalam katalog karier ArahKita")

    preferred_activity = _normalized(user_input.get("preferred_activity"))
    if preferred_activity in PREFERRED_ACTIVITY_FACTS:
        facts.add(PREFERRED_ACTIVITY_FACTS[preferred_activity])

    selected_skills = {
        str(skill).strip().lower() for skill in user_input.get("skills", [])
    }
    skill_pool = metadata.get("basic_skill_pool", [])
    recognized_skills = [
        skill for skill in skill_pool if skill.lower() in selected_skills
    ]
    for skill in recognized_skills:
        safe_name = skill.replace(" ", "").replace("/", "")
        facts.add(f"HasSkill_{safe_name}")

    threshold = int(metadata.get("basic_skill_threshold", 2))
    if len(recognized_skills) >= threshold:
        facts.add("HasBasicDataTechSkills")
    else:
        facts.add("LacksBasicDataTechSkills")

    if _as_bool(user_input.get("has_project", False)):
        facts.add("HasProjectExperience")

    if _as_bool(user_input.get("has_internship_or_work_experience", False)):
        facts.add("HasProfessionalExperience")
    else:
        facts.add("HasNoProfessionalExperience")

    certificate = _normalized(user_input.get("english_certificate"))
    if certificate not in {"", "none", "tidak ada"}:
        facts.add("HasEnglishCertificate")

    if _as_bool(user_input.get("needs_income_soon", False)):
        facts.add("NeedsIncomeSoon")
    else:
        facts.add("DoesNotNeedIncomeSoon")

    study = _normalized(user_input.get("wants_further_study"))
    if study in {"yes", "ya", "wants further study"}:
        facts.add("WantsFurtherStudy")
        funding = _normalized(user_input.get("needs_study_funding"))
        if funding in {"yes", "ya", "true", "1"}:
            facts.add("NeedsStudyFunding")
        elif funding in {"no", "tidak", "false", "0"}:
            facts.add("DoesNotNeedStudyFunding")
        else:
            raise ValueError(
                "needs_study_funding must be Yes or No when the user wants further study"
            )
    elif study in {"no", "tidak", "does not want further study"}:
        facts.add("DoesNotWantFurtherStudy")
    elif study in {"unsure", "belum yakin", "not sure"}:
        facts.add("IsUnsureAboutFurtherStudy")
    else:
        raise ValueError("wants_further_study must be Yes, No, or Unsure")

    return facts


def forward_chain(
    initial_facts: Iterable[str], rules: list[dict[str, Any]]
) -> tuple[set[str], list[dict[str, Any]]]:
    """Derive facts until a fixed point is reached.

    A trace entry is recorded only when a rule adds a genuinely new fact.
    New facts from one round are available to rules in the next round.
    """

    facts = set(initial_facts)
    trace: list[dict[str, Any]] = []
    iteration = 1

    while True:
        new_facts: set[str] = set()

        for rule in rules:
            antecedents = set(rule["antecedents"])
            conclusion = rule["conclusions"][0]
            if (
                antecedents.issubset(facts)
                and conclusion not in facts
                and conclusion not in new_facts
            ):
                new_facts.add(conclusion)
                trace.append(
                    {
                        "iteration": iteration,
                        "rule_id": rule["id"],
                        "antecedents": rule["antecedents"],
                        "conclusion": conclusion,
                        "explanation": rule["explanation"],
                    }
                )

        if not new_facts:
            break

        facts.update(new_facts)
        iteration += 1

    return facts, trace


def _select_primary_recommendation(final_facts: set[str]) -> tuple[str, str]:
    keys = [key for key in PRIMARY_RECOMMENDATIONS if key in final_facts]
    if len(keys) != 1:
        raise InferenceError(
            "Expected exactly one primary recommendation, "
            f"but found {len(keys)}: {keys}"
        )
    key = keys[0]
    return key, PRIMARY_RECOMMENDATIONS[key]


def _build_display_result(
    recommendation_key: str,
    final_facts: set[str],
    templates: dict[str, Any],
) -> dict[str, Any]:
    template = templates[recommendation_key]
    next_steps = list(template.get("next_steps", []))
    preparation_focus = None
    preparation_focus_label = None

    variants = template.get("variants", {})
    for variant_fact, variant in variants.items():
        if variant_fact in final_facts:
            focus = PREPARATION_FOCUS[variant_fact]
            preparation_focus = focus["value"]
            preparation_focus_label = variant.get("focus_label", focus["label"])
            next_steps = list(variant.get("next_steps", next_steps))
            break

    supporting_actions = [
        text
        for fact, text in templates.get("supporting_actions", {}).items()
        if fact in final_facts
    ]

    return {
        "title": template["title"],
        "summary": template["summary"],
        "preparation_focus": preparation_focus,
        "preparation_focus_label": preparation_focus_label,
        "next_steps": next_steps,
        "supporting_actions": supporting_actions,
        "limitation_note": template["limitation_note"],
    }


def _build_reasons(
    recommendation_key: str,
    final_facts: set[str],
    trace: list[dict[str, Any]],
) -> list[str]:
    """Return explanations from rules that lead to the displayed result.

    The backward walk is only used to select human-readable explanations. The
    recommendation itself is still produced exclusively by forward chaining.
    """

    targets = {recommendation_key}
    targets.update(fact for fact in PREPARATION_FOCUS if fact in final_facts)
    relevant_rule_ids: set[str] = set()
    changed = True

    while changed:
        changed = False
        for entry in reversed(trace):
            if entry["conclusion"] in targets and entry["rule_id"] not in relevant_rule_ids:
                relevant_rule_ids.add(entry["rule_id"])
                targets.update(entry["antecedents"])
                changed = True

    return [
        entry["explanation"]
        for entry in trace
        if entry["rule_id"] in relevant_rule_ids
    ]


def rank_careers(user_input: dict[str, Any]) -> list[dict[str, Any]]:
    """Urutkan empat arah karier dengan aturan skor yang mudah diaudit.

    Ranking ini melengkapi rekomendasi langkah dari forward chaining. Tidak ada
    prediksi probabilitas atau model black-box: skor hanya berasal dari tujuan,
    aktivitas yang diminati, dan irisan skill yang dipilih user.
    """

    explicit_goal = str(user_input.get("career_goal", "")).strip()
    if explicit_goal not in CAREER_CATALOG:
        explicit_goal = ""

    activity = str(user_input.get("preferred_activity", "")).strip()
    legacy_activity_map = {
        "Mengolah data dan membuat dashboard": "Data Analyst",
        "Membuat model prediksi dari data": "Data Scientist",
        "Membangun aplikasi atau sistem": "Software/IT",
        "Melakukan eksperimen dan riset": "Researcher",
    }
    activity_primary = ACTIVITY_TO_PRIMARY.get(activity) or legacy_activity_map.get(activity)
    selected_skills = {
        str(skill).strip() for skill in user_input.get("skills", []) if str(skill).strip()
    }

    scored: list[dict[str, Any]] = []
    for order, (career, config) in enumerate(CAREER_CATALOG.items()):
        score = 0
        match_score = 35
        signals: list[str] = []

        if explicit_goal:
            goal_config = CAREER_CATALOG[explicit_goal]
            if career == explicit_goal:
                score += 120
                match_score += 45
                signals.append("sesuai tujuan yang dipilih")
            elif career in goal_config["related"]:
                score += 48
                match_score += 25
                signals.append("masih satu rumpun dengan tujuan utama")
            elif explicit_goal in config["related"]:
                score += 30
                match_score += 18
                signals.append("memiliki jalur transisi yang dekat")
            elif set(config["opportunity_goals"]) & set(goal_config["opportunity_goals"]):
                score += 18
                match_score += 10
                signals.append("berbagi bidang kerja yang serupa")

        if activity_primary:
            activity_config = CAREER_CATALOG[activity_primary]
            if career == activity_primary:
                score += 90
                match_score += 40
                signals.append("paling sesuai dengan aktivitas yang diminati")
            elif career in activity_config["related"]:
                score += 38
                match_score += 22
                signals.append("aktivitasnya masih saling berkaitan")

        matched_skills = [skill for skill in config["skills"] if skill in selected_skills]
        if matched_skills:
            score += len(matched_skills) * 12
            match_score += round(20 * len(matched_skills) / len(config["skills"]))
            signals.append("didukung skill " + ", ".join(matched_skills[:2]))

        if user_input.get("has_project") and matched_skills:
            score += 4
            match_score += 2
        if user_input.get("has_internship_or_work_experience") and matched_skills:
            score += 4
            match_score += 3

        scored.append(
            {
                "career": career,
                "label": config["label"],
                "score": score,
                "match_score": min(match_score, 98),
                "reason": "; ".join(signals[:2]) or "opsi eksplorasi dengan skill yang masih dapat dikembangkan",
                "matched_skills": matched_skills,
                "_order": order,
            }
        )

    scored.sort(key=lambda item: (-item["score"], item["_order"]))
    top_four = scored[:4]
    for rank, item in enumerate(top_four, 1):
        item["rank"] = rank
        item.pop("_order")
    return top_four


def match_opportunities(
    user_input: dict[str, Any],
    recommendation_key: str,
    opportunities: list[dict[str, Any]],
    recommended_career: str | None = None,
) -> list[dict[str, Any]]:
    """Perform transparent requirement matching on the curated web dataset.

    This is deliberately separate from the forward-chaining inference engine.
    It does not predict acceptance probability.
    """

    allowed_categories = RECOMMENDATION_CATEGORIES[recommendation_key]
    if not allowed_categories:
        return []

    career_goal = recommended_career or str(user_input.get("career_goal", "")).strip()
    accepted_goal_labels = {career_goal}
    if career_goal in CAREER_CATALOG:
        accepted_goal_labels.update(CAREER_CATALOG[career_goal]["opportunity_goals"])
    education = str(user_input.get("education_status", "")).strip()
    gpa = float(user_input.get("gpa", 0) or 0)
    if not 0 <= gpa <= 4:
        raise ValueError("gpa must be between 0.00 and 4.00")
    has_english = _normalized(user_input.get("english_certificate")) not in {
        "",
        "none",
        "tidak ada",
    }
    selected_skills = {
        str(skill).strip().lower() for skill in user_input.get("skills", [])
    }

    matches: list[dict[str, Any]] = []
    for opportunity in opportunities:
        if opportunity.get("category") not in allowed_categories:
            continue
        target_goals = opportunity.get("target_goals", [])
        if target_goals and not accepted_goal_labels.intersection(target_goals):
            continue

        missing: list[str] = []
        manual_checks: list[str] = []

        minimum_gpa = opportunity.get("minimum_gpa")
        if minimum_gpa is not None and gpa < float(minimum_gpa):
            missing.append(f"Minimum GPA {minimum_gpa}")

        for required_skill in opportunity.get("required_skills", []):
            if required_skill.lower() not in selected_skills:
                missing.append(f"Skill: {required_skill}")

        if opportunity.get("category") in {"Master's Program", "Scholarship"}:
            if education == "Final-year student":
                missing.append("Completed bachelor degree")
            if not has_english:
                missing.append("Valid English proficiency certificate")

        if opportunity.get("accepted_major_groups"):
            manual_checks.append("Check detailed major eligibility on the official page")

        for requirement in opportunity.get("other_requirements", []):
            manual_checks.append(requirement)

        matches.append(
            {
                "id": opportunity["id"],
                "name": opportunity["name"],
                "provider": opportunity["provider"],
                "category": opportunity["category"],
                "status": "Potential match" if not missing else "Preparation needed",
                "missing_requirements": missing,
                "manual_checks": manual_checks,
                "application_period": opportunity.get("application_period"),
                "source_url": opportunity.get("source_url"),
            }
        )

    return matches


def generate_recommendation(
    user_input: dict[str, Any],
    *,
    rules_path: str | Path | None = None,
    templates_path: str | Path | None = None,
    opportunities_path: str | Path | None = None,
) -> dict[str, Any]:
    """Run the complete Citra pipeline and return a Streamlit-friendly dict."""

    metadata, rules = load_rules(rules_path)
    templates = load_templates(templates_path)
    opportunities = load_opportunities(opportunities_path)

    initial_facts = build_initial_facts(user_input, metadata)
    final_facts, trace = forward_chain(initial_facts, rules)
    recommendation_key, recommendation_title = _select_primary_recommendation(final_facts)
    career_rankings = rank_careers(user_input)
    recommended_career = career_rankings[0]["career"]
    display = _build_display_result(recommendation_key, final_facts, templates)
    matched_opportunities = match_opportunities(
        user_input, recommendation_key, opportunities, recommended_career
    )
    missing_requirements = list(
        dict.fromkeys(
            requirement
            for opportunity in matched_opportunities
            for requirement in opportunity["missing_requirements"]
        )
    )

    return {
        "primary_recommendation_key": recommendation_key,
        "primary_recommendation": recommendation_title,
        "recommended_career": recommended_career,
        "career_rankings": career_rankings,
        "preparation_focus": display["preparation_focus"],
        "preparation_focus_label": display["preparation_focus_label"],
        "summary": display["summary"],
        "reasons": _build_reasons(recommendation_key, final_facts, trace),
        "next_steps": display["next_steps"],
        "supporting_actions": display["supporting_actions"],
        "limitation_note": display["limitation_note"],
        "initial_facts": sorted(initial_facts),
        "derived_facts": sorted(final_facts - initial_facts),
        "final_facts": sorted(final_facts),
        "fired_rules": [entry["rule_id"] for entry in trace],
        "inference_trace": trace,
        "matched_opportunity_ids": [
            opportunity["id"] for opportunity in matched_opportunities
        ],
        "matched_opportunities": matched_opportunities,
        "missing_requirements": missing_requirements,
        "fixed_point_reached": True,
    }
