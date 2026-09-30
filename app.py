"""ArahKita: antarmuka Streamlit terintegrasi. Jalankan: streamlit run app.py."""

from html import escape

import streamlit as st

from app_support import GOALS, ROOT, SKILLS, read_json
from career_catalog import ACTIVITY_TO_PRIMARY, CAREER_CATALOG
from engine_adapter import assess


st.set_page_config(
    page_title="ArahKita • Temukan langkah setelah lulus",
    page_icon="🧭",
    layout="centered",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #1a2433;
        --navy: #10233f;
        --muted: #5c687a;
        --line: #d5dbe4;
        --blue: #315fb5;
        --blue-bright: #376fd5;
        --blue-dark: #214789;
        --teal: #147c73;
        --teal-soft: #dff1ee;
        --emerald: #287b55;
        --purple: #6655a8;
        --lavender: #e9e5f6;
        --sage: #e2ede3;
        --warm: #f5f4f0;
        --surface: #fffefa;
        --peach: #f7e6d8;
    }
    .stApp {
        background: var(--warm);
        color: var(--ink);
    }
    .block-container {max-width: 1060px; padding: 1.35rem 1.35rem 4rem;}
    #MainMenu, footer, [data-testid="stToolbar"] {display: none !important;}
    header[data-testid="stHeader"] {background: transparent;}
    h1, h2, h3 {color: var(--navy); letter-spacing: -.025em;}
    p {line-height: 1.62;}
    .topbar {display:flex;justify-content:space-between;align-items:center;gap:1rem;margin:0 0 1.15rem;}
    .brand {
        margin: 0;
        font-size: 1.85rem;
        line-height: 1;
        font-weight: 900;
        letter-spacing: -.05em;
        color: var(--navy);
    }
    .brand-dot {color:var(--blue-bright);}
    .nav-links {display:flex;align-items:center;gap:.25rem;}
    .nav-link {display:flex;align-items:center;gap:.32rem;padding:.45rem .62rem;border-radius:9px;color:#526074 !important;text-decoration:none !important;font-size:.75rem;font-weight:750;}
    .nav-link:hover {background:#e8ebf1;color:var(--navy) !important;}
    .nav-link svg {width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;}
    .nav-cta {margin-left:.2rem;background:var(--navy);color:white !important;}
    .nav-cta:hover {background:var(--blue-dark);color:white !important;}
    .hero {
        display:grid; grid-template-columns:minmax(0,1.55fr) minmax(250px,.75fr);
        gap:2rem; align-items:center; padding:2.65rem 2.75rem;
        background:linear-gradient(135deg,#10233f 0%,#193a5d 100%);
        border:1px solid #183451;border-radius:28px;color:white;
        box-shadow:0 18px 42px rgba(16,35,63,.18);position:relative;overflow:hidden;
    }
    .hero-label {
        display: inline-block; margin-bottom: .9rem; padding: .34rem .7rem;
        border-radius:999px;background:rgba(90,139,218,.24);color:#dce9ff;
        font-size:.7rem; font-weight:850; letter-spacing:.08em;
    }
    .hero h1 {
        max-width:680px;margin:0 0 .85rem;color:white;
        font-size:clamp(2.05rem,4.7vw,3.25rem); line-height:1.06;
    }
    .hero p {max-width:650px;margin:0;color:#d1dceb;font-size:1.02rem;}
    .hero-visual {display:grid; gap:.65rem;}
    .hero-mini {
        display:flex; align-items:center; gap:.7rem; padding:.78rem .9rem;
        border:1px solid rgba(255,255,255,.17);border-radius:14px;
        background:rgba(255,255,255,.09);color:#f4f7fb;font-size:.8rem;font-weight:750;
    }
    .hero-mini:nth-child(2) {margin-left:1.2rem;background:rgba(20,124,115,.23);}
    .hero-mini:nth-child(3) {margin-right:1.2rem;background:rgba(102,85,168,.23);}
    .mini-icon {width:28px;height:28px;display:grid;place-items:center;border-radius:9px;background:rgba(255,255,255,.14);color:#a8c7ff;}
    .hero-mini:nth-child(2) .mini-icon {color:#77ddd1;}
    .hero-mini:nth-child(3) .mini-icon {color:#c4b5fd;}
    .mini-icon svg,.line-icon svg {width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;}
    .trust-row {display:flex; flex-wrap:wrap; gap:.55rem; margin:1rem 0 1.8rem;}
    .trust-chip {
        padding:.43rem .72rem;background:var(--surface);border:1px solid #cfd6e0;
        border-radius:999px;color:#45546a;font-size:.77rem;font-weight:750;
    }
    .trust-chip:nth-child(1) {border-color:#aabde1;color:var(--blue-dark);}
    .trust-chip:nth-child(2) {border-color:#9fcac4;color:#126a63;}
    .trust-chip:nth-child(3) {border-color:#bbb0dc;color:#584795;}
    [data-testid="stVerticalBlockBorderWrapper"] {
        background:rgba(255,255,255,.97);border-color:#d1d8e2 !important;
        border-radius:22px !important;box-shadow:0 10px 28px rgba(31,45,68,.07);
    }
    [data-baseweb="select"] > div,
    [data-testid="stNumberInput"] input,
    [data-testid="stMultiSelect"] > div > div {border-radius: 12px !important;}
    [data-baseweb="select"] > div:focus-within,
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stMultiSelect"] > div > div:focus-within {border-color:var(--blue-bright) !important;box-shadow:0 0 0 2px rgba(55,111,213,.13) !important;}
    [data-baseweb="tag"] {background:#dfe7f6 !important;color:var(--blue-dark) !important;border-radius:999px !important;font-weight:750 !important;}
    div.stButton > button[kind="primary"] {
        width:100%; min-height:3rem; border:0; border-radius:13px;
        background:var(--blue-bright);color:white;font-weight:850;font-size:.96rem;
    }
    div.stButton > button[kind="primary"]:hover {background:var(--blue-dark);color:white;box-shadow:0 8px 18px rgba(49,95,181,.22);}
    div.stButton > button[kind="secondary"] {
        min-height:2.35rem; border:1px solid var(--line); border-radius:11px;
        background:var(--surface);color:var(--blue-dark);font-weight:750;font-size:.78rem;
    }
    [data-testid="stLinkButton"] a {border:0 !important;border-radius:11px !important;background:var(--navy) !important;color:white !important;font-weight:800 !important;}
    [data-testid="stLinkButton"] a:hover {background:var(--blue-dark) !important;color:white !important;}
    .form-intro {display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;margin-bottom:.75rem;}
    .form-intro h3 {margin:0 0 .2rem;font-size:1.3rem;}
    .form-intro p {margin:0;color:var(--muted);font-size:.84rem;}
    .progress-meta {display:flex;justify-content:space-between;align-items:center;margin:.7rem 0 .4rem;color:#34445b;font-size:.74rem;font-weight:800;}
    .progress-label {display:flex;align-items:center;gap:.4rem;}
    .progress-label svg {width:15px;height:15px;stroke:var(--teal);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
    .progress-track {height:8px;border-radius:999px;background:#dde3ea;overflow:hidden;margin-bottom:1.15rem;}
    .progress-fill {height:100%;border-radius:999px;background:linear-gradient(90deg,var(--teal),#25a294);transition:width .2s ease;}
    .form-section {display:flex;align-items:center;gap:.58rem;margin:1.25rem 0 .72rem;color:var(--navy);font-size:.94rem;font-weight:850;}
    .form-icon {display:grid;place-items:center;width:30px;height:30px;border-radius:9px;background:#e4eaf6;color:var(--blue-dark);}
    .form-icon svg {width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;}
    .form-section small {display:block;margin-bottom:.05rem;color:var(--muted);font-size:.6rem;font-weight:850;letter-spacing:.08em;}
    .result-wrap {margin-top: 2.45rem;}
    .dashboard-head {display:flex;justify-content:space-between;gap:1rem;align-items:flex-end;margin:2.5rem 0 .85rem;}
    .dashboard-head h2 {margin:0 0 .2rem;font-size:1.55rem;}
    .dashboard-head p {margin:0;color:var(--muted);font-size:.88rem;}
    .complete-pill {display:flex;align-items:center;gap:.35rem;padding:.45rem .72rem;border-radius:999px;background:var(--emerald);color:white;font-size:.7rem;font-weight:850;white-space:nowrap;}
    .complete-pill svg {width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
    .result-card {
        display:grid; grid-template-columns:68px 1fr auto; gap:1.15rem; align-items:center;
        padding:1.65rem;border-radius:22px;border:1px solid #cbd5e2;border-left:5px solid var(--blue-bright);
        background:var(--surface);box-shadow:0 14px 32px rgba(25,44,72,.09);
    }
    .result-icon {
        width:62px;height:62px;display:grid;place-items:center;
        border-radius:18px;background:var(--navy);color:#76d6c9;
    }
    .result-eyebrow {
        margin-bottom:.28rem;color:var(--blue-bright);font-size:.7rem;
        font-weight: 850; letter-spacing: .1em; text-transform: uppercase;
    }
    .result-card h2 {margin: 0 0 .35rem; font-size: 1.8rem;}
    .result-card p {margin:0;color:#626f80;font-size:.9rem;}
    .result-score {min-width:112px;padding:.75rem .8rem;border-radius:14px;background:#e5ecfa;text-align:center;}
    .result-score svg {width:16px;height:16px;margin-bottom:.2rem;stroke:var(--blue);fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;}
    .result-score strong {display:block;color:var(--blue-dark);font-size:1.4rem;}
    .result-score span {color:#4c5c75;font-size:.63rem;font-weight:800;}
    .section-title {display:flex;align-items:center;gap:.55rem;margin:2.1rem 0 .25rem;font-size:1.22rem;font-weight:850;color:var(--navy);}
    .section-icon {display:grid;place-items:center;width:32px;height:32px;border-radius:10px;background:var(--navy);color:white;}
    .section-icon svg {width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;}
    .section-copy {margin: 0 0 .85rem; color: var(--muted); font-size: .9rem;}
    .metric-grid {
        display: grid; grid-template-columns: repeat(4, minmax(0,1fr));
        gap: .7rem; margin: .8rem 0 1rem;
    }
    .metric-card {padding:.95rem;border:1px solid #d2d9e3;border-radius:14px;background:var(--surface);box-shadow:0 5px 14px rgba(32,45,66,.035);}
    .metric-card span {display:block; color: var(--muted); font-size: .72rem; margin-bottom: .25rem;}
    .metric-card strong {display:block; color: var(--ink); font-size: .95rem; line-height: 1.25;}
    .metric-icon {width:28px;height:28px;display:grid;place-items:center;margin-bottom:.55rem;border-radius:9px;background:#e4eaf6;color:var(--blue-dark);}
    .metric-icon svg {width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;}
    .metric-card:nth-child(2) .metric-icon {background:var(--teal-soft);color:var(--teal);}
    .metric-card:nth-child(3) .metric-icon {background:var(--lavender);color:var(--purple);}
    .metric-card:nth-child(4) .metric-icon {background:var(--sage);color:var(--emerald);}
    .career-grid {display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem;}
    .career-card {min-height:205px;padding:1.15rem;border:1px solid #d1d8e2;border-radius:18px;background:var(--surface);box-shadow:0 7px 18px rgba(35,48,69,.045);}
    .career-card.active {background:var(--navy);border:1.5px solid var(--navy);box-shadow:0 13px 28px rgba(16,35,63,.2);}
    .career-top {display:flex;justify-content:space-between;align-items:flex-start;gap:.8rem;}
    .career-heading {display:flex;gap:.7rem;align-items:flex-start;}
    .career-icon {width:38px;height:38px;display:grid;place-items:center;border-radius:12px;background:#e4eaf6;color:var(--blue-dark);flex:0 0 auto;}
    .career-card.active .career-icon {background:rgba(39,177,160,.18);color:#76d6c9;}
    .career-card strong {display:block;margin:.05rem 0 .2rem;color:var(--navy);line-height:1.25;}
    .career-rank {display:block;margin-bottom:.15rem;color:var(--blue-bright);font-size:.68rem;font-weight:850;letter-spacing:.04em;}
    .match-number {color:var(--purple);font-size:.92rem;font-weight:850;white-space:nowrap;}
    .career-desc {margin:.75rem 0 .45rem;color:#5f6c7d;font-size:.79rem;line-height:1.42;}
    .career-reason {font-size:.75rem;line-height:1.38;color:var(--muted);}
    .match-track {height:5px;margin:.7rem 0;border-radius:999px;background:#e8ebf0;overflow:hidden;}
    .match-fill {height:100%;border-radius:999px;background:var(--blue-bright);}
    .career-card.active .match-track {background:rgba(255,255,255,.15);}
    .career-card.active .match-fill {background:#42c4b4;}
    .tag-row {display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.75rem;}
    .skill-tag {padding:.28rem .5rem;border-radius:999px;background:#e5eaf3;color:#394e6e;font-size:.67rem;font-weight:750;}
    .career-card.active strong,.career-card.active .match-number {color:white;}
    .career-card.active .career-rank {color:#76d6c9;}
    .career-card.active .career-desc {color:#d7e1ed;}
    .career-card.active .career-reason {color:#b9c7d8;}
    .career-card.active .skill-tag {background:rgba(255,255,255,.12);color:#e5edf6;}
    .insight-grid {display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem;margin-top:.8rem;}
    .insight-card {padding:1.15rem;border:1px solid #d1d8e2;border-top:4px solid var(--teal);border-radius:17px;background:var(--surface);}
    .insight-card.growth {border-top-color:var(--purple);}
    .insight-card h4 {display:flex;align-items:center;gap:.45rem;margin:0 0 .65rem;color:var(--navy);font-size:.92rem;}
    .insight-title-icon {display:grid;place-items:center;width:26px;height:26px;border-radius:8px;background:var(--teal-soft);color:var(--teal);}
    .growth .insight-title-icon {background:var(--lavender);color:var(--purple);}
    .insight-title-icon svg {width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;}
    .insight-card p {margin:.38rem 0;color:var(--muted);font-size:.8rem;line-height:1.45;}
    .insight-dot {display:inline-block;width:7px;height:7px;margin-right:.45rem;border-radius:50%;background:var(--teal);}
    .insight-card.growth .insight-dot {background:#8b7bb0;}
    .priority-card {padding:1rem 1.05rem;border:1px solid var(--line);border-radius:16px;background:white;}
    .priority-card b {color: var(--ink);}
    .priority-card p {margin: .32rem 0 0; color: var(--muted); font-size: .86rem;}
    .plan-card {min-height:250px;padding:1.05rem;border:1px solid #d1d8e2;border-radius:17px;background:var(--surface);box-shadow:0 6px 16px rgba(32,45,66,.04);}
    .plan-number {
        width: 31px; height: 31px; display:grid; place-items:center; margin-bottom:.7rem;
        border-radius:9px;background:var(--blue-dark);color:white;font-weight:850;
    }
    .plan-card strong {display:block; margin-bottom:.55rem; color:var(--ink);}
    .plan-card p {margin:.35rem 0; color:var(--muted); font-size:.84rem; line-height:1.45;}
    .plan-card p b {color:#3d5650;}
    .opportunity-label {color:var(--teal);font-size:.7rem;font-weight:850;letter-spacing:.06em;}
    .opportunity-note {color:var(--muted); font-size:.86rem;}
    .soft-note {margin-top:.7rem; padding:.8rem 1rem; border-radius:13px; background:#fff7ec; color:#785438; font-size:.87rem;}
    .match-good {color:#3f7d70;font-weight:750;}
    .save-label {display:flex;align-items:center;gap:.42rem;margin:.9rem 0 .35rem;color:var(--navy);font-size:.8rem;font-weight:800;}
    .save-label svg {width:16px;height:16px;stroke:var(--purple);fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;}
    .filter-note {display:flex;align-items:center;gap:.42rem;margin:.35rem 0;color:#46566d;font-size:.78rem;font-weight:800;}
    .filter-note svg {width:15px;height:15px;stroke:var(--blue);fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;}
    .footer-note {margin-top:2.5rem; color:#7a8984; font-size:.78rem; text-align:center;}
    @media (max-width: 720px) {
        .block-container {padding:1rem .8rem 3rem;}
        .hero {grid-template-columns:1fr;padding:2rem 1.4rem;border-radius:22px;}
        .hero-visual {display:none;}
        .nav-link:not(.nav-cta) {display:none;}
        .result-card {grid-template-columns:1fr;padding:1.4rem;}
        .result-score {text-align:left;}
        .career-grid,.insight-grid {grid-template-columns:1fr;}
        .metric-grid {grid-template-columns:repeat(2,minmax(0,1fr));}
        .plan-card {min-height:auto;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


opportunities_path = ROOT / "opportunities.json"

if opportunities_path.exists():
    opportunities = read_json(opportunities_path)["opportunities"]
else:
    opportunities = []
opportunity_map = {item["id"]: item for item in opportunities}

EDUCATION_LABELS = {
    "Final-year student": "Mahasiswa tingkat akhir",
    "Fresh graduate": "Fresh graduate",
}
MAJOR_LABELS = {
    "Engineering": "Teknik",
    "Science": "Sains",
    "Computing": "Komputer / informatika",
    "Other STEM": "STEM lainnya",
}
GOAL_LABELS = {
    **{career: config["label"] for career, config in CAREER_CATALOG.items()},
    "Undecided": "Belum yakin",
}
INTEREST_TO_CAREER = ACTIVITY_TO_PRIMARY
CATEGORY_LABELS = {
    "Job": "Lowongan kerja",
    "Internship": "Magang",
    "Certification": "Program belajar",
    "Master's Program": "Program magister",
    "Scholarship": "Beasiswa",
}

SKILL_EXPLANATIONS = {
    "Excel": "Mengolah tabel, membersihkan data, dan membuat analisis awal.",
    "Python": "Mengotomasi proses, mengolah data, atau membangun logika aplikasi.",
    "SQL": "Mengambil, menggabungkan, dan memeriksa data dari database.",
    "Statistics": "Membaca pola dan membuat kesimpulan yang dapat dipertanggungjawabkan.",
    "Data Visualization": "Mengubah hasil analisis menjadi insight yang mudah dipahami.",
    "R": "Mengolah data statistik dan menjalankan analisis yang umum digunakan dalam riset.",
    "Machine Learning": "Membangun dan mengevaluasi model prediksi dari data.",
    "Bioinformatics": "Mengolah data biologis seperti sekuens, genomik, atau data omics.",
    "Laboratory Techniques": "Menjalankan prosedur laboratorium secara tepat dan terdokumentasi.",
    "Research Methodology": "Menyusun pertanyaan, desain, metode, dan interpretasi penelitian.",
    "Clinical Data Management": "Menjaga data studi klinis tetap lengkap, konsisten, dan dapat diaudit.",
    "Quality Management": "Memastikan proses dan hasil kerja mengikuti standar mutu.",
    "Regulatory Documentation": "Menyusun dan memeriksa dokumen sesuai ketentuan regulator.",
    "Scientific Writing": "Menjelaskan bukti ilmiah secara runtut, akurat, dan mudah ditinjau.",
    "Literature Review": "Mencari, menilai, dan merangkum sumber ilmiah yang relevan.",
    "Product Management": "Menerjemahkan kebutuhan user menjadi prioritas produk yang terukur.",
    "Git": "Mencatat perubahan kode dan berkolaborasi lewat version control.",
    "API Development": "Menghubungkan aplikasi dan data melalui layanan yang terstruktur.",
}
CAREER_PROFILES = CAREER_CATALOG

LINE_ICONS = {
    "data": '<svg viewBox="0 0 24 24"><path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/></svg>',
    "data_science": '<svg viewBox="0 0 24 24"><circle cx="6" cy="12" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="18" cy="18" r="2"/><path d="m8 11 8-4M8 13l8 4"/></svg>',
    "technology": '<svg viewBox="0 0 24 24"><path d="m8 9-4 3 4 3M16 9l4 3-4 3M14 5l-4 14"/></svg>',
    "research": '<svg viewBox="0 0 24 24"><path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3M8 15h8"/></svg>',
    "quality": '<svg viewBox="0 0 24 24"><path d="M12 3 5 6v5c0 4.5 2.7 8.2 7 10 4.3-1.8 7-5.5 7-10V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg>',
    "product": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m15 9-2 4-4 2 2-4 4-2Z"/></svg>',
    "communication": '<svg viewBox="0 0 24 24"><path d="M4 20h4l11-11-4-4L4 16v4ZM13 7l4 4"/><path d="M14 20h6"/></svg>',
}

UI_ICONS = {
    "profile": '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c1-5 4-7 8-7s7 2 8 7"/></svg>',
    "education": '<svg viewBox="0 0 24 24"><path d="m3 9 9-5 9 5-9 5-9-5Z"/><path d="M7 12v5c3 2 7 2 10 0v-5M21 9v6"/></svg>',
    "interest": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m15 9-2 4-4 2 2-4 4-2Z"/></svg>',
    "skills": '<svg viewBox="0 0 24 24"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M18.4 5.6l-2.8 2.8M8.4 15.6l-2.8 2.8"/><circle cx="12" cy="12" r="3"/></svg>',
    "priority": '<svg viewBox="0 0 24 24"><path d="M5 21V4M5 5h11l-2 4 2 4H5"/></svg>',
    "career": '<svg viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="12" rx="2"/><path d="M9 7V5h6v2M3 12h18M10 12v2h4v-2"/></svg>',
    "analytics": '<svg viewBox="0 0 24 24"><path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/></svg>',
    "strength": '<svg viewBox="0 0 24 24"><path d="m12 3 2.2 4.5 5 .7-3.6 3.5.9 5-4.5-2.4-4.5 2.4.9-5-3.6-3.5 5-.7L12 3Z"/></svg>',
    "growth": '<svg viewBox="0 0 24 24"><path d="M4 19 10 13l4 4 6-8"/><path d="M15 9h5v5"/></svg>',
    "roadmap": '<svg viewBox="0 0 24 24"><circle cx="5" cy="18" r="2"/><circle cx="19" cy="6" r="2"/><path d="M7 18h3c5 0 1-12 7-12"/></svg>',
    "bookmark": '<svg viewBox="0 0 24 24"><path d="M6 4h12v17l-6-4-6 4V4Z"/></svg>',
    "progress": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "filter": '<svg viewBox="0 0 24 24"><path d="M4 6h16M7 12h10M10 18h4"/></svg>',
    "opportunity": '<svg viewBox="0 0 24 24"><path d="M9 18h6M10 22h4M8 14c-1.2-1-2-2.6-2-4.4A6 6 0 0 1 18 9.6c0 1.8-.8 3.4-2 4.4-.7.6-1 1.2-1 2H9c0-.8-.3-1.4-1-2Z"/></svg>',
    "project": '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8 9h8M8 13h5M8 17h3"/></svg>',
    "experience": '<svg viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V4h6v3M3 12h18"/></svg>',
    "check": '<svg viewBox="0 0 24 24"><path d="m5 12 4 4L19 6"/></svg>',
    "start": '<svg viewBox="0 0 24 24"><path d="M5 12h14M14 7l5 5-5 5"/></svg>',
}


def career_icon(target):
    return LINE_ICONS[CAREER_PROFILES[target]["action_group"]]


def ui_icon(name):
    return UI_ICONS[name]


def render_section_heading(title, copy, icon_name, anchor=None):
    anchor_html = f' id="{anchor}"' if anchor else ""
    st.markdown(
        f'<div{anchor_html} class="section-title"><span class="section-icon">{ui_icon(icon_name)}</span>{escape(title)}</div>'
        f'<div class="section-copy">{escape(copy)}</div>',
        unsafe_allow_html=True,
    )

CAREER_ACTIONS = {
    "data": [
        ("Buat bukti analisis", "Gunakan satu dataset dan jawab satu masalah yang jelas.", "Data cleaning, SQL, insight, dan visualisasi.", "Notebook/dashboard + tiga insight."),
        ("Bungkus portfolio", "Susun cerita dari masalah, proses, sampai hasil.", "Cara berpikir dan kemampuan menjelaskan temuan.", "Satu halaman portfolio atau README."),
        ("Targetkan lamaran", "Bandingkan skill-mu dengan lowongan yang dipilih.", "Kecocokan pengalaman dan hasil project.", "CV satu halaman yang disesuaikan."),
    ],
    "data_science": [
        ("Bangun model dasar", "Pilih dataset dan buat baseline sebelum mencoba model lain.", "Pemilihan fitur, evaluasi, dan alasan memilih metrik.", "Notebook + perbandingan dua model."),
        ("Dokumentasikan eksperimen", "Catat asumsi, perubahan, dan hasil setiap percobaan.", "Scientific thinking, bukan hanya skor model.", "README eksperimen yang singkat."),
        ("Targetkan posisi junior", "Cari posisi yang menerima fresh graduate atau pengalaman project.", "Python, statistik, SQL, dan dampak model.", "CV dan portfolio yang diarahkan ke role."),
    ],
    "technology": [
        ("Bangun fitur kecil", "Buat aplikasi atau API dengan satu fungsi yang selesai.", "Struktur kode, alur data, dan penyelesaian masalah.", "Repository yang bisa dijalankan."),
        ("Rapikan repository", "Tambahkan README, contoh penggunaan, dan pengujian dasar.", "Kerapian kerja dan kemampuan handover.", "Repo dengan dokumentasi yang jelas."),
        ("Sesuaikan CV teknis", "Pilih role dan pakai kata kunci dari requirement-nya.", "Stack, kontribusi, dan hasil fitur.", "CV satu halaman + tautan GitHub."),
    ],
    "research": [
        ("Buat mini research note", "Pilih satu pertanyaan dan rangkum bukti dari beberapa sumber.", "Rumusan masalah, metode, dan ketelitian referensi.", "Ringkasan riset dua halaman."),
        ("Tunjukkan olah data", "Tambahkan analisis atau visualisasi pendukung.", "Kemampuan membaca bukti dan menarik kesimpulan.", "Tabel/grafik + interpretasi."),
        ("Siapkan profil riset", "Susun pengalaman lab, project, dan topik yang diminati.", "Relevansi akademik dan kemampuan dokumentasi.", "CV akademik + contoh tulisan."),
    ],
    "quality": [
        ("Petakan standar", "Pilih satu proses laboratorium atau produk lalu cari standar yang relevan.", "Ketelitian membaca SOP dan persyaratan.", "Matriks standar dan risiko."),
        ("Buat contoh dokumen", "Tulis checklist audit atau alur penanganan penyimpangan sederhana.", "Dokumentasi, konsistensi, dan pemahaman mutu.", "Satu contoh dokumen QA."),
        ("Targetkan industri", "Bandingkan kebutuhan QA dan regulatory di farmasi, alat kesehatan, atau lab.", "Kesesuaian pengetahuan dengan regulasi sektor.", "CV yang diarahkan ke satu industri."),
    ],
    "product": [
        ("Pilih masalah pengguna", "Temukan satu masalah nyata pada layanan atau produk kesehatan.", "Empati pengguna dan kemampuan memprioritaskan.", "Problem statement + user flow."),
        ("Uji solusi sederhana", "Buat wireframe atau simulasi proses lalu minta masukan.", "Pengambilan keputusan berbasis bukti.", "Prototype dan ringkasan feedback."),
        ("Buat portfolio kasus", "Jelaskan masalah, pilihan solusi, metrik, dan hasil pengujian.", "Cara berpikir produk dan komunikasi lintas tim.", "Satu product case study."),
    ],
    "communication": [
        ("Pilih topik medis", "Ubah satu artikel ilmiah menjadi penjelasan untuk pembaca umum.", "Akurasi, struktur, dan kemampuan menyederhanakan.", "Artikel populer 600–800 kata."),
        ("Tunjukkan sumber", "Susun referensi dan fact-check untuk setiap klaim penting.", "Literature review dan tanggung jawab ilmiah.", "Naskah dengan daftar referensi."),
        ("Bangun portfolio", "Buat dua format berbeda dari topik yang sama.", "Kemampuan menyesuaikan pesan dengan audiens.", "Artikel + carousel atau infografik."),
    ],
}

STUDY_ACTIONS = {
    "Master's Preparation": [
        ("Susun shortlist", "Bandingkan tiga program berdasarkan bidang dan kurikulum.", "Kecocokan akademik dengan tujuan karier.", "Tabel perbandingan tiga program."),
        ("Audit persyaratan", "Catat IPK, bahasa, dokumen, dan deadline tiap program.", "Kesiapan dan ketelitian aplikasi.", "Checklist persyaratan."),
        ("Siapkan narasi", "Hubungkan pengalaman kuliah dengan alasan memilih program.", "Arah studi yang konsisten dan spesifik.", "Draft statement of purpose."),
    ],
    "Scholarship Preparation": [
        ("Pilih skema pendanaan", "Bandingkan cakupan, syarat, dan timeline beasiswa.", "Kecocokan antara kebutuhan dan manfaat.", "Shortlist dua beasiswa."),
        ("Bangun bukti", "Kumpulkan capaian, project, dan kontribusi yang relevan.", "Dampak yang terukur, bukan daftar kegiatan.", "Bank bukti untuk esai."),
        ("Siapkan aplikasi", "Susun esai, rekomendasi, dan jadwal pengerjaan.", "Konsistensi tujuan studi dan rencana kontribusi.", "Timeline dan draft dokumen."),
    ],
}


def recommended_career(profile, result):
    if result.get("recommended_career"):
        return result["recommended_career"]
    if profile["career_goal"] != "Undecided":
        return profile["career_goal"]
    return INTEREST_TO_CAREER.get(profile.get("preferred_activity"), "Data Analyst")


def career_label(target):
    return CAREER_PROFILES[target]["label"]


def recommendation_copy(result, target):
    icon = career_icon(target)
    target_label = career_label(target)
    primary = result["primary_recommendation"]
    if primary == "Career Exploration":
        return icon, f"Eksplorasi dengan Fokus {target_label}", (
            f"Dari aktivitas dan bekalmu, {target_label} menjadi jalur pertama yang paling layak dicoba. "
            "Gunakan project kecil untuk memastikan kecocokannya sebelum berkomitmen lebih jauh."
        )
    if primary == "Internship or Skill Preparation":
        if result.get("preparation_focus") == "skill":
            return icon, f"Perkuat Skill untuk {target_label}", (
                "Arah kariermu sudah jelas, tetapi beberapa kemampuan inti masih belum terlihat di profil. "
                "Prioritaskan gap yang paling dekat dengan kebutuhan role."
            )
        return icon, f"Bangun Pengalaman sebagai {target_label}", (
            "Skill dasar sudah mulai terbentuk. Fokus berikutnya adalah mengubahnya menjadi bukti kerja "
            "melalui project, magang, atau pengalaman setara."
        )
    if primary == "Work Now":
        return icon, f"Mulai Melamar Posisi {target_label}", (
            "Tujuan, skill dasar, dan pengalaman awalmu sudah cukup untuk mulai menargetkan peluang yang relevan."
        )
    if primary == "Master's Preparation":
        return icon, f"Siapkan Studi Lanjut untuk Jalur {target_label}", (
            "Prioritasmu mendukung studi magister. Sekarang fokus pada kecocokan program, kesiapan bahasa, dan dokumen."
        )
    return icon, f"Siapkan Beasiswa untuk Jalur {target_label}", (
        "Kebutuhan pendanaan menjadi faktor utama. Pilih program dan beasiswa yang saling mendukung sejak awal."
    )


def render_career_map(rankings):
    render_section_heading(
        "Arah karier yang terbaca",
        "Empat jalur teratas berdasarkan tujuan, aktivitas, dan skillmu. Skor menunjukkan kecocokan aturan, bukan peluang diterima kerja.",
        "career",
        "hasil",
    )
    cards = []
    for item in rankings:
        career = item["career"]
        active = item["rank"] == 1
        config = CAREER_PROFILES[career]
        tags = "".join(
            f'<span class="skill-tag">{escape(skill)}</span>'
            for skill in config["skills"][:3]
        )
        score = int(item.get("match_score", 0))
        cards.append(
            f'<div class="career-card{" active" if active else ""}">'
            f'<div class="career-top"><div class="career-heading">'
            f'<div class="career-icon line-icon">{career_icon(career)}</div><div>'
            f'<span class="career-rank">#{item["rank"]} {"· PALING DISARANKAN" if active else ""}</span>'
            f'<strong>{escape(career_label(career))}</strong></div></div>'
            f'<div class="match-number">{score}/100</div></div>'
            f'<div class="match-track"><div class="match-fill" style="width:{score}%"></div></div>'
            f'<div class="career-desc">{escape(config["description"])}</div>'
            f'<div class="career-reason">{escape(item["reason"].capitalize())}.</div>'
            f'<div class="tag-row">{tags}</div></div>'
        )
    st.markdown('<div class="career-grid">' + "".join(cards) + "</div>", unsafe_allow_html=True)

    ranked_options = [item["career"] for item in rankings]
    if "saved_careers" in st.session_state:
        st.session_state["saved_careers"] = [
            career for career in st.session_state["saved_careers"] if career in ranked_options
        ]
    st.markdown(
        f'<div class="save-label">{ui_icon("bookmark")} Simpan karier untuk dibandingkan</div>',
        unsafe_allow_html=True,
    )
    with st.expander("Pilih dari Top 4"):
        st.multiselect(
            "Karier tersimpan",
            ranked_options,
            key="saved_careers",
            format_func=career_label,
            placeholder="Pilih karier dari Top 4",
            label_visibility="collapsed",
        )
        st.caption("Tersimpan selama sesi website ini dibuka.")


def render_profile_analysis(profile, target):
    core_skills = CAREER_PROFILES[target]["skills"]
    selected = set(profile["skills"])
    present = [skill for skill in core_skills if skill in selected]
    missing = [skill for skill in core_skills if skill not in selected]
    render_section_heading(
        "Analisis kesiapan profil",
        "Ringkasan ini membaca skill, bukti project, pengalaman, dan prioritasmu saat ini.",
        "analytics",
    )
    st.markdown(
        f"""
        <div class="metric-grid">
            <div class="metric-card"><div class="metric-icon">{ui_icon("career")}</div><span>Target utama</span><strong>{escape(career_label(target))}</strong></div>
            <div class="metric-card"><div class="metric-icon">{ui_icon("skills")}</div><span>Skill inti terdeteksi</span><strong>{len(present)} dari {len(core_skills)}</strong></div>
            <div class="metric-card"><div class="metric-icon">{ui_icon("project")}</div><span>Bukti project</span><strong>{"Sudah ada" if profile["has_project"] else "Belum ada"}</strong></div>
            <div class="metric-card"><div class="metric-icon">{ui_icon("experience")}</div><span>Pengalaman profesional</span><strong>{"Sudah ada" if profile["has_internship_or_work_experience"] else "Belum ada"}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    strength_items = []
    if present:
        strength_items.extend(f"Sudah memiliki {skill}" for skill in present[:3])
    if profile["has_project"]:
        strength_items.append("Punya project sebagai bukti penerapan")
    if profile["has_internship_or_work_experience"]:
        strength_items.append("Sudah memiliki pengalaman profesional awal")
    if not strength_items:
        strength_items.append("Punya latar belakang STEM sebagai fondasi belajar")

    strengths_html = "".join(
        f'<p><span class="insight-dot"></span>{escape(item)}</p>' for item in strength_items[:3]
    )
    if missing:
        growth_html = "".join(
            f'<p><span class="insight-dot"></span><b>{escape(skill)}</b> — {escape(SKILL_EXPLANATIONS[skill])}</p>'
            for skill in missing[:3]
        )
    else:
        growth_html = '<p><span class="insight-dot"></span>Perdalam penerapan skill lewat project yang lebih kuat.</p>'
    st.markdown(
        '<div class="insight-grid">'
        f'<div class="insight-card"><h4><span class="insight-title-icon">{ui_icon("strength")}</span>Kekuatan yang sudah terbaca</h4>{strengths_html}</div>'
        f'<div class="insight-card growth"><h4><span class="insight-title-icon">{ui_icon("growth")}</span>Skill yang paling layak dikembangkan</h4>{growth_html}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_action_plan(result, target):
    action_group = CAREER_PROFILES[target]["action_group"]
    plans = STUDY_ACTIONS.get(result["primary_recommendation"], CAREER_ACTIONS[action_group])
    render_section_heading(
        "Tiga langkah yang bisa dibawa pulang",
        "Bagian ini fokus pada eksekusi dan cara menunjukkan nilai profilmu.",
        "roadmap",
    )
    columns = st.columns(3)
    for index, (title, action, selling, output) in enumerate(plans, 1):
        with columns[index - 1]:
            st.markdown(
                f"""
                <div class="plan-card">
                    <div class="plan-number">{index}</div>
                    <strong>{escape(title)}</strong>
                    <p>{escape(action)}</p>
                    <p><b>Yang dijual:</b><br>{escape(selling)}</p>
                    <p><b>Output:</b><br>{escape(output)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def translate_requirement(value):
    translations = {
        "Completed bachelor degree": "Lulus sarjana",
        "Valid English proficiency certificate": "Sertifikat kemampuan bahasa Inggris",
    }
    if value.startswith("Minimum GPA "):
        return value.replace("Minimum GPA", "IPK minimum")
    if value.startswith("Skill: "):
        return value.replace("Skill: ", "Skill ")
    return translations.get(value, value)


def render_opportunity(item):
    category = CATEGORY_LABELS.get(item.get("category"), item.get("category", "Peluang"))
    missing = item.get("missing_requirements", [])
    with st.container(border=True):
        st.markdown(f'<div class="opportunity-label">{escape(category.upper())} · SUMBER WEB</div>', unsafe_allow_html=True)
        st.markdown(f"### {escape(item.get('name', 'Peluang'))}")
        st.markdown(f'<div class="opportunity-note">{escape(item.get("provider", ""))}</div>', unsafe_allow_html=True)
        if missing:
            readable = ", ".join(translate_requirement(value) for value in missing)
            st.markdown(
                f'<div class="soft-note"><strong>Gap yang terdeteksi:</strong> {escape(readable)}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<p class="match-good">✓ Tidak ada gap utama yang terdeteksi dari jawaban form</p>', unsafe_allow_html=True)
        with st.expander("Lihat ringkasan persyaratan"):
            if item.get("education_status_required"):
                st.write("**Pendidikan:** " + item["education_status_required"])
            if item.get("required_skills"):
                st.write("**Skill:** " + ", ".join(item["required_skills"]))
            if item.get("preferred_experience"):
                st.write("**Pengalaman:** " + item["preferred_experience"])
            if item.get("application_period"):
                st.write("**Status/periode:** " + item["application_period"])
            st.caption("Informasi dapat berubah. Periksa kembali status dan persyaratan lengkap pada halaman sumber.")
        url = item.get("source_url", "")
        if url.startswith("https://"):
            st.link_button("Buka halaman peluang ↗", url)


def render_result(result, profile):
    target = recommended_career(profile, result)
    icon, title, summary = recommendation_copy(result, target)
    top_score = result["career_rankings"][0].get("match_score", 0)
    st.markdown('<div class="result-wrap"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="dashboard-head"><div><h2>Profil kariermu sudah terbaca</h2>'
        '<p>Mulai dari arah utama, lalu bandingkan alternatif yang masih relevan.</p></div>'
        f'<div class="complete-pill">{ui_icon("check")} PROFIL SELESAI</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-icon line-icon">{icon}</div>
            <div>
                <div class="result-eyebrow">Rekomendasi utama</div>
                <h2>{escape(title)}</h2>
                <p>{escape(summary)}</p>
            </div>
            <div class="result-score">{ui_icon("analytics")}<strong>{top_score}/100</strong><span>SKOR KECOCOKAN</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_career_map(result["career_rankings"])
    render_profile_analysis(profile, target)
    render_action_plan(result, target)

    render_section_heading(
        "Peluang nyata untuk dieksplorasi",
        "Mulai dari ringkasannya, lalu buka detail hanya ketika dibutuhkan. Status peluang tetap perlu diperiksa di halaman sumber.",
        "opportunity",
        "peluang",
    )
    if not result["matched_opportunities"]:
        st.info("Belum ada peluang yang cocok pada daftar saat ini. Gunakan action plan di atas sambil mencari role serupa.")
        return
    matches = result["matched_opportunities"]
    available_categories = list(dict.fromkeys(match["category"] for match in matches))
    filter_options = ["Semua", *available_categories]
    if st.session_state.get("opportunity_filter") not in filter_options:
        st.session_state["opportunity_filter"] = "Semua"
    st.markdown(
        f'<div class="filter-note">{ui_icon("filter")} Filter berdasarkan jenis peluang</div>',
        unsafe_allow_html=True,
    )
    selected_category = st.selectbox(
        "Filter peluang",
        filter_options,
        key="opportunity_filter",
        format_func=lambda value: "Semua peluang" if value == "Semua" else CATEGORY_LABELS.get(value, value),
        label_visibility="collapsed",
    )
    filtered_matches = matches if selected_category == "Semua" else [
        match for match in matches if match["category"] == selected_category
    ]
    for match in filtered_matches:
        full_item = dict(opportunity_map.get(match["id"], {}))
        full_item.update(match)
        render_opportunity(full_item)


st.markdown(
    f"""
    <div class="topbar">
        <div class="brand">ArahKita<span class="brand-dot">.</span></div>
    </div>
    <div class="hero">
        <div>
            <span class="hero-label">MULAI DARI KONDISIMU SEKARANG</span>
            <h1>Arah karier nggak harus langsung sempurna.</h1>
            <p>Kenali pilihan yang paling dekat dengan minat dan bekalmu, lalu tentukan langkah kecil yang bisa dimulai sekarang.</p>
        </div>
        <div class="hero-visual">
            <div class="hero-mini"><span class="mini-icon"><svg viewBox="0 0 24 24"><path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/></svg></span>Kenali kekuatanmu</div>
            <div class="hero-mini"><span class="mini-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m15 9-2 4-4 2 2-4 4-2Z"/></svg></span>Bandingkan arah karier</div>
            <div class="hero-mini"><span class="mini-icon"><svg viewBox="0 0 24 24"><path d="m5 12 4 4L19 6"/><path d="M19 12a7 7 0 1 1-4-6.3"/></svg></span>Mulai langkah pertamamu</div>
        </div>
    </div>
    <div class="trust-row">
        <span class="trust-chip">Cek kesiapan</span>
        <span class="trust-chip">Temukan gap skill</span>
        <span class="trust-chip">Lihat peluang nyata</span>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown(
        '<div id="asesmen" class="form-intro"><div><h3>Ceritakan sedikit tentang dirimu</h3>'
        '<p>Jawabanmu digunakan untuk membaca kesiapan dan menyusun empat arah karier.</p></div></div>',
        unsafe_allow_html=True,
    )
    progress_slot = st.empty()

    st.markdown(
        f'<div class="form-section"><span class="form-icon">{ui_icon("education")}</span><div><small>TAHAP 1</small>Profil singkat</div></div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns(2)
    with left:
        education = st.selectbox(
            "Status pendidikan", list(EDUCATION_LABELS), index=None,
            placeholder="Pilih status pendidikan", format_func=EDUCATION_LABELS.get,
        )
        major = st.selectbox(
            "Kelompok program studi", list(MAJOR_LABELS), index=None,
            placeholder="Pilih kelompok program studi", format_func=MAJOR_LABELS.get,
        )
    with right:
        gpa = st.number_input(
            "IPK", min_value=0.0, max_value=4.0, value=None, step=0.01,
            format="%.2f", placeholder="Masukkan IPK",
        )

    st.markdown(
        f'<div class="form-section"><span class="form-icon">{ui_icon("interest")}</span><div><small>TAHAP 2</small>Arah dan minat</div></div>',
        unsafe_allow_html=True,
    )
    goal = st.selectbox(
        "Tujuan karier", GOALS, index=None,
        placeholder="Pilih tujuan atau belum yakin", format_func=GOAL_LABELS.get,
    )

    preferred_activity = None
    if goal == "Undecided":
        preferred_activity = st.selectbox(
            "Aktivitas yang paling menarik buat kamu",
            list(INTEREST_TO_CAREER), index=None, placeholder="Pilih satu aktivitas",
        )

    st.markdown(
        f'<div class="form-section"><span class="form-icon">{ui_icon("skills")}</span><div><small>TAHAP 3</small>Bekal yang sudah kamu punya</div></div>',
        unsafe_allow_html=True,
    )
    skills = st.multiselect("Skill", SKILLS, placeholder="Pilih semua yang sesuai")
    st.caption("Pilih skill yang sudah pernah kamu gunakan.")
    left, right = st.columns(2)
    with left:
        project = st.radio("Punya project kuliah/pribadi?", ["Ya", "Tidak"], index=None, horizontal=True)
    with right:
        experience = st.radio("Punya pengalaman magang/kerja?", ["Ya", "Tidak"], index=None, horizontal=True)
    english = st.selectbox(
        "Sertifikat bahasa Inggris", ["None", "TOEFL/IELTS available"], index=None,
        placeholder="Pilih kondisi saat ini",
        format_func=lambda value: "Belum punya" if value == "None" else "Sudah punya TOEFL/IELTS",
    )

    st.markdown(
        f'<div class="form-section"><span class="form-icon">{ui_icon("priority")}</span><div><small>TAHAP 4</small>Prioritasmu sekarang</div></div>',
        unsafe_allow_html=True,
    )
    income = st.radio("Perlu penghasilan dalam waktu dekat?", ["Ya", "Tidak"], index=None, horizontal=True)
    study = st.radio("Ingin melanjutkan studi?", ["Ya", "Tidak", "Belum yakin"], index=None, horizontal=True)
    funding = None
    if study == "Ya":
        funding = st.radio("Butuh pendanaan untuk studi?", ["Ya", "Tidak"], index=None, horizontal=True)

    progress_values = [education, major, gpa, goal, project, experience, english, income, study]
    if goal == "Undecided":
        progress_values.append(preferred_activity)
    if study == "Ya":
        progress_values.append(funding)
    completed = sum(value is not None for value in progress_values)
    total = len(progress_values)
    progress = round(completed / total * 100)
    progress_slot.markdown(
        f'<div class="progress-meta"><span class="progress-label">{ui_icon("progress")} Kelengkapan profil</span><span>{progress}%</span></div>'
        f'<div class="progress-track"><div class="progress-fill" style="width:{progress}%"></div></div>',
        unsafe_allow_html=True,
    )
    submitted = st.button("Temukan arah saya →", type="primary")

if submitted:
    required = [education, major, gpa, goal, project, experience, english, income, study]
    if goal == "Undecided":
        required.append(preferred_activity)
    if study == "Ya":
        required.append(funding)
    if any(value is None for value in required):
        st.error("Lengkapi semua pertanyaan terlebih dahulu supaya rekomendasinya tidak setengah-setengah.")
    else:
        profile = {
            "education_status": education,
            "major_group": major,
            "gpa": gpa,
            "career_goal": goal,
            "preferred_activity": preferred_activity,
            "skills": skills,
            "has_project": project == "Ya",
            "has_internship_or_work_experience": experience == "Ya",
            "english_certificate": english,
            "needs_income_soon": income == "Ya",
            "wants_further_study": study,
            "needs_study_funding": funding if study == "Ya" else "Tidak relevan",
        }
        try:
            st.session_state["assessment"] = assess(profile, opportunities)
            st.session_state["submitted_profile"] = profile
        except Exception as exc:
            st.error("Rekomendasi belum dapat dibuat. Coba periksa kembali jawabanmu.")
            with st.expander("Detail error untuk tim"):
                st.code(f"{type(exc).__name__}: {exc}", language=None)

if "assessment" in st.session_state and "submitted_profile" in st.session_state:
    render_result(st.session_state["assessment"], st.session_state["submitted_profile"])

st.markdown(
    """
    <div class="footer-note">
        ArahKita memberi panduan awal berdasarkan aturan forward chaining. Status peluang dan persyaratan akhir tetap mengikuti halaman sumber.
    </div>
    """,
    unsafe_allow_html=True,
)
