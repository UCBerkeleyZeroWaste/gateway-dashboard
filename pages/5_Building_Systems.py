import base64
import textwrap
from pathlib import Path

import streamlit as st

from styles import apply_global_style


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Building Systems | Gateway Systems Dashboard",
    page_icon="\U0001F3E2",
    layout="wide"
)

apply_global_style()


# ======================================================
# HELPER FUNCTIONS
# Same set used on Reuse Systems / Recovery Systems.
# ======================================================

def render_html(content):
    """
    Render raw HTML safely. Markdown treats a blank line inside raw HTML
    as the end of that HTML block -- any indented markup after it then
    gets reinterpreted as a preformatted code block instead of being
    rendered. Stripping blank lines (harmless in HTML, which is
    whitespace-insensitive) prevents that entirely.
    """

    dedented = textwrap.dedent(content).strip()
    no_blank_lines = "\n".join(line for line in dedented.split("\n") if line.strip() != "")
    st.markdown(no_blank_lines, unsafe_allow_html=True)


# Page-specific compact styling -- same font and color palette used
# throughout the site (Arial, dark green #0B6E4F / #3F8F43, neutral
# grays). No additional colors or fonts are introduced anywhere below.
render_html(
    """
    <style>
    h1 { font-size: 2.25rem !important; margin-bottom: 0.35rem !important; }
    h2 { font-size: 1.55rem !important; margin-top: 1.15rem !important; margin-bottom: 0.35rem !important; }
    h3 { font-size: 1.08rem !important; margin-top: 0.1rem !important; margin-bottom: 0.3rem !important; }
    p, li, div[data-testid="stMarkdownContainer"] p { font-size: 0.92rem !important; line-height: 1.4 !important; }
    div[data-testid="stCaptionContainer"] p { font-size: 0.8rem !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] { padding: 0.85rem 0.9rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0.45rem; }
    </style>
    """
)


FIGURES_FOLDER = Path("Figures")


def get_base64_image(image_path):
    image_bytes = Path(image_path).read_bytes()
    return base64.b64encode(image_bytes).decode()


def coming_soon_card(icon, title, teaser, accent, key):
    """Lightweight preview card -- just an icon, a one-line teaser, and a
    'coming soon' chip. No fields to fill in yet since there's no real
    data behind this page."""

    render_html(f"""
    <style>
    div.st-key-{key} {{
        border: 1.5px solid {accent} !important;
        border-radius: 0.75rem !important;
    }}
    </style>
    """)

    with st.container(border=True, height=210, key=key):
        render_html(f"""
        <div style="text-align:center;">
            <div style="width:54px;height:54px;border-radius:50%;background:{accent}17;
                border:2px solid {accent};display:flex;align-items:center;justify-content:center;
                font-size:1.6rem;margin:0 auto 0.55rem auto;">{icon}</div>
            <div style="font-size:1.02rem;font-weight:700;color:#343743;margin-bottom:0.3rem;
                font-family:Arial, sans-serif;">{title}</div>
            <div style="font-size:0.8rem;color:#747B8D;line-height:1.4;margin-bottom:0.6rem;
                font-family:Arial, sans-serif;">{teaser}</div>
            <div style="display:inline-block;background:#F3F5F2;color:#747B8D;
                border:1px solid #D8DCE5;border-radius:999px;padding:0.2rem 0.7rem;
                font-size:0.7rem;font-weight:700;letter-spacing:0.02em;
                font-family:Arial, sans-serif;">\U0001F6A7 COMING SOON</div>
        </div>
        """)


# ======================================================
# PAGE HERO
# ======================================================

HERO_IMAGE_PATH = Path("images/gateway_building_systems_hero.jpg")

if HERO_IMAGE_PATH.exists():
    hero_image = get_base64_image(HERO_IMAGE_PATH)

    render_html(
        f"""
        <style>
        .building-hero {{
            position: relative;
            width: 100%;
            min-height: 400px;
            border-radius: 22px;
            overflow: hidden;
            margin-bottom: 0.05rem;
            background-image:
                linear-gradient(90deg, rgba(5,18,14,0.88) 0%, rgba(5,18,14,0.62) 38%, rgba(5,18,14,0.15) 72%, rgba(5,18,14,0.05) 100%),
                url("data:image/jpeg;base64,{hero_image}");
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: flex-end;
        }}
        .building-hero-content {{ max-width: 750px; padding: 3rem; color: white; }}
        .building-hero h1 {{
            margin: 0; color: white; font-size: clamp(2.7rem, 6vw, 5rem);
            line-height: 0.95; font-weight: 750; letter-spacing: -0.04em;
        }}
        .building-hero-line {{ width: 210px; height: 3px; margin: 1.3rem 0; background: #3F8F43; border-radius: 999px; }}
        .building-hero p {{ margin: 0; max-width: 560px; color: rgba(255,255,255,0.92); font-size: 1.1rem; line-height: 1.55; }}
        @media (max-width: 700px) {{
            .building-hero {{ min-height: 330px; background-position: 60% center; }}
            .building-hero-content {{ padding: 2rem; }}
            .building-hero h1 {{ font-size: 2.8rem; }}
            .building-hero p {{ font-size: 1rem; }}
        }}
        </style>
        <div class="building-hero">
            <div class="building-hero-content">
                <h1>Building<br>Systems</h1>
                <div class="building-hero-line"></div>
                <p>Zero waste is one piece of a truly sustainable building. Here's where the rest of the story lives.</p>
            </div>
        </div>
        """
    )
else:
    st.title("Building Systems")
    st.write("Zero waste is one piece of a truly sustainable building. Here's where the rest of the story lives.")
    st.caption(
        "Add a hero photo at `images/gateway_building_systems_hero.jpg` "
        "to enable the full banner treatment used on other pages."
    )

st.markdown("<div style='height: 1.6rem;'></div>", unsafe_allow_html=True)


# ======================================================
# WHERE BUILDING SYSTEMS FITS IN
# ======================================================

st.write(
    "Construction, Circular Purchasing, Reuse, and Recovery cover how "
    "materials move through Gateway. This page is where the rest of "
    "the building's sustainability story will live -- how it uses "
    "energy, water, and air, and the systems working behind the "
    "scenes to keep all of it efficient."
)

st.divider()


# ======================================================
# WHAT'S COMING
# ======================================================

st.header("What's Coming")
st.write("A preview of what this page will cover once the data is in.")

CATEGORIES = [
    {
        "icon": "\U000026A1",
        "title": "Energy",
        "teaser": "Consumption, efficiency measures, and any on-site generation.",
        "accent": "#0B6E4F",
        "key": "energy_teaser_card"
    },
    {
        "icon": "\U0001F4A7",
        "title": "Water",
        "teaser": "Usage, fixtures, and any reclamation or reduction systems.",
        "accent": "#3F8F43",
        "key": "water_teaser_card"
    },
    {
        "icon": "\U0001F32C\U0000FE0F",
        "title": "Air Quality & Comfort",
        "teaser": "Ventilation, filtration, and indoor environmental quality.",
        "accent": "#3F8F43",
        "key": "air_quality_teaser_card"
    },
    {
        "icon": "\U0001F5A5\U0000FE0F",
        "title": "Smart Automation",
        "teaser": "Building automation and controls working behind the scenes.",
        "accent": "#0B6E4F",
        "key": "automation_teaser_card"
    },
]

teaser_cols = st.columns(4, gap="medium")

for col, category in zip(teaser_cols, CATEGORIES):
    with col:
        coming_soon_card(**category)

st.divider()


# ======================================================
# WORK IN PROGRESS BANNER
# ======================================================

render_html(
    """
    <div style="
        background: #F3F5F2;
        border: 1px solid #0B6E4F;
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        margin: 0.8rem 0;
        text-align: center;
    ">
        <div style="font-size: 1.8rem;margin-bottom: 0.4rem;">\U0001F6A7</div>
        <div style="color: #343743; font-size: 1rem; font-weight: 700;
            font-family: Arial, sans-serif;margin-bottom: 0.3rem;">
            This page is still under construction
        </div>
        <div style="color: #747B8D; font-size: 0.88rem; line-height: 1.4;
            max-width: 480px; margin: 0 auto; font-family: Arial, sans-serif;">
            Check back soon for real numbers on how
            Gateway performs beyond zero waste.
        </div>
    </div>
    """
)


# ======================================================
# CLOSING NOTE
# ======================================================

st.divider()

st.caption(
    "Gateway opened operationally in 2026. This page will be built out "
    "with real energy, water, and air quality data as it becomes "
    "available."
)