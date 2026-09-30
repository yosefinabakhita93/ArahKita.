"""Titik sambung UI Malikha ke forward-chaining engine Citra."""
from app_support import ROOT, load_templates, validate_result


def assess(profile, opportunities):
    try:
        from citra_engine import generate_recommendation
    except ModuleNotFoundError as exc:
        if exc.name == "citra_engine":
            raise RuntimeError("Engine Citra belum dipasang. Gunakan Pratinjau tampilan untuk memeriksa desain.") from exc
        raise RuntimeError(f"Dependensi engine belum tersedia: {exc.name}") from exc
    except ImportError as exc:
        raise RuntimeError("Fungsi generate_recommendation tidak ditemukan pada citra_engine.py.") from exc
    result = generate_recommendation(
        profile,
        rules_path=ROOT / "data" / "rules.json",
        templates_path=ROOT / "data" / "recommendation_templates.json",
        opportunities_path=ROOT / "data" / "opportunities.json",
    )
    return validate_result(result, load_templates(), [row["id"] for row in opportunities])
