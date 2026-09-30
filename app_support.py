"""Kontrak tampilan dan pembacaan data; tidak menjalankan inferensi AI."""
import json
from pathlib import Path

from career_catalog import CAREER_CATALOG, GOALS, SKILLS

ROOT = Path(__file__).resolve().parent


def read_json(path):
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)


def load_templates():
    return read_json(ROOT / "data" / "recommendation_templates.json")


def validate_result(result, templates, opportunity_ids):
    """Tolak hasil ambigu/tidak lengkap, jangan diam-diam membuat hasil pengganti."""
    if not isinstance(result, dict):
        raise ValueError("Engine harus mengembalikan dictionary.")
    titles = {v["title"] for v in templates.values() if isinstance(v, dict) and "title" in v}
    if result.get("primary_recommendation") not in titles:
        raise ValueError("primary_recommendation tidak sesuai lima judul template Qiara.")
    if result.get("recommended_career") not in CAREER_CATALOG:
        raise ValueError("recommended_career tidak ditemukan dalam katalog ArahKita.")
    rankings = result.get("career_rankings")
    if not isinstance(rankings, list) or len(rankings) != 4:
        raise ValueError("career_rankings harus berisi tepat empat arah karier.")
    ranked_careers = [item.get("career") for item in rankings if isinstance(item, dict)]
    if len(ranked_careers) != 4 or len(set(ranked_careers)) != 4:
        raise ValueError("Empat arah karier harus valid dan unik.")
    if any(career not in CAREER_CATALOG for career in ranked_careers):
        raise ValueError("career_rankings memuat karier yang tidak dikenal.")
    if any(
        not isinstance(item.get("match_score"), int) or not 0 <= item["match_score"] <= 100
        for item in rankings
    ):
        raise ValueError("Setiap ranking membutuhkan match_score 0–100.")
    if result["recommended_career"] != ranked_careers[0]:
        raise ValueError("recommended_career harus sama dengan peringkat pertama.")
    if result["primary_recommendation"] == "Internship or Skill Preparation":
        if result.get("preparation_focus") not in ("skill", "internship"):
            raise ValueError("Jalur persiapan membutuhkan preparation_focus: skill atau internship.")
    for field in (
        "reasons",
        "initial_facts",
        "derived_facts",
        "fired_rules",
        "matched_opportunity_ids",
        "missing_requirements",
        "next_steps",
        "supporting_actions",
    ):
        if not isinstance(result.get(field), list) or not all(isinstance(x, str) for x in result[field]):
            raise ValueError(f"{field} harus berupa list string, termasuk jika kosong.")
    unknown = set(result["matched_opportunity_ids"]) - set(opportunity_ids)
    if unknown:
        raise ValueError("ID opportunity tidak ditemukan: " + ", ".join(sorted(unknown)))
    matches = result.get("matched_opportunities")
    if not isinstance(matches, list) or not all(isinstance(item, dict) for item in matches):
        raise ValueError("matched_opportunities harus berupa list dictionary.")
    match_ids = [item.get("id") for item in matches]
    if match_ids != result["matched_opportunity_ids"]:
        raise ValueError("matched_opportunity_ids harus sama dan seurut dengan matched_opportunities.")
    trace = result.get("inference_trace")
    if not isinstance(trace, list) or not trace:
        raise ValueError("inference_trace harus berisi trace dari engine Citra.")
    for rule in trace:
        if not isinstance(rule, dict):
            raise ValueError("Setiap entry inference_trace harus berupa dictionary.")
        for key in ("rule_id", "conclusion", "explanation"):
            if not isinstance(rule.get(key), str) or not rule[key].strip():
                raise ValueError(f"Fired rule membutuhkan {key} berupa string.")
        if not isinstance(rule.get("antecedents"), list) or not all(isinstance(x, str) for x in rule["antecedents"]):
            raise ValueError("antecedents pada fired rule harus berupa list string.")
    if result["fired_rules"] != [rule["rule_id"] for rule in trace]:
        raise ValueError("fired_rules harus sama dan seurut dengan rule_id pada inference_trace.")
    if result.get("fixed_point_reached") is not True:
        raise ValueError("Engine harus mengonfirmasi fixed_point_reached = true.")
    return result


def display_template(result, templates):
    template = next(v for v in templates.values() if isinstance(v, dict) and v.get("title") == result["primary_recommendation"])
    focus = result.get("preparation_focus")
    variant_key = {"skill": "PreparationFocusSkill", "internship": "PreparationFocusInternship"}.get(focus)
    variant = template.get("variants", {}).get(variant_key, {})
    # Template Qiara tetap sumber isi. Langkah khusus engine ditampilkan terpisah.
    return template, variant.get("focus_label"), variant.get("next_steps", template.get("next_steps", []))


def combine_opportunities(paths):
    records, seen = [], set()
    for path in paths:
        payload = read_json(path)
        items = payload.get("opportunities") if isinstance(payload, dict) else payload
        if not isinstance(items, list):
            raise ValueError(f"{path}: perlu list atau object dengan opportunities.")
        for item in items:
            if not isinstance(item, dict) or not all(isinstance(item.get(k), str) and item[k] for k in ("id", "name", "category")):
                raise ValueError(f"{path}: opportunity harus memiliki id, name, category.")
            if item["id"] in seen:
                raise ValueError(f"ID opportunity duplikat: {item['id']}; perbaiki sebelum menggabungkan.")
            for field in ("target_goals", "required_skills", "required_documents"):
                if field in item and (not isinstance(item[field], list) or not all(isinstance(x, str) for x in item[field])):
                    raise ValueError(f"{item['id']}: {field} harus berupa list string.")
            seen.add(item["id"])
            records.append(item)
    return {"metadata": {"scope_note": "Dataset kurasi web; setiap peluang memiliki tautan sumber dan statusnya perlu diperiksa kembali."}, "opportunities": records}
