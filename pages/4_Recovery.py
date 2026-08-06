# pages/4_Recovery.py

import base64
import textwrap
from pathlib import Path
from urllib.parse import quote

import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from styles import apply_global_style
from paths import FIGURES_DIR, IMAGES_DIR


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Recovery Systems | Gateway Systems Dashboard",
    page_icon="\U0001F504",
    layout="wide"
)

apply_global_style()


# ======================================================
# DEVICE DETECTION
# Same technique as Home.py / Circular Purchasing / Reuse Systems --
# window.parent.innerWidth (not window.innerWidth, which would measure
# the component's own narrow iframe instead of the real browser
# window).
# ======================================================

screen_width = streamlit_js_eval(js_expressions='window.parent.innerWidth', key='WIDTH')
is_mobile = screen_width is not None and screen_width < 768


# ======================================================
# CONFIG
# Manual now lives as a Google Slides deck (not a hosted PDF) --
# MANUAL_URL points to the "present" view, and MANUAL_PAGE_SORTING is
# the Waste Sorting slide's actual Slides slide ID rather than a page
# number. Keep in sync with Reuse Systems / Circular Purchasing if the
# deck's slide order ever changes.
# ======================================================

MANUAL_URL = "https://docs.google.com/presentation/d/1j3IVyxEG0aGZXlMy2ydaw6Dh-32Yhf_N/present"
MANUAL_PAGE_SORTING = "p3"

# E-waste pickup requests go to Sarah at this address. Built into a
# mailto: link with a pre-filled subject on the E-Waste pathway card
# below (see the "action_label" / "action_url" args on that PATHWAYS
# entry) instead of just being printed as text in the tagline.
EWASTE_CONTACT_EMAIL = "specora@berkeley.edu"
EWASTE_MAILTO_SUBJECT = "E-Waste Pickup Request \u2014 Gateway"


# ======================================================
# HELPER FUNCTIONS
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


FIGURES_FOLDER = FIGURES_DIR


def show_media(filename, instructions, caption=None, bordered_placeholder=True):
    """Display an image if it exists; otherwise show a labeled placeholder."""

    file_path = FIGURES_FOLDER / filename

    if file_path.exists():
        st.image(str(file_path), caption=caption, use_container_width=True)
    else:
        placeholder = st.container(border=bordered_placeholder)
        with placeholder:
            st.info(
                f"**Visual placeholder**\n\n{instructions}\n\n"
                f"Save the finished file as:\n\n`Figures/{filename}`"
            )


def metric_placeholder(title, key=None, height=190):
    """A friendly 'not live yet' placeholder for the two metrics that
    need real operational data before they can be built."""

    with st.container(border=True, height=height, key=key):
        render_html(f"""
        <div style="text-align:center;padding-top:0.35rem;">
            <div style="width:50px;height:50px;border-radius:50%;background:#F3F5F2;
                border:2px solid #0B6E4F;color:#0B6E4F;display:flex;align-items:center;
                justify-content:center;font-weight:700;font-size:1.45rem;margin:0 auto 0.55rem auto;
                font-family:Arial, sans-serif;">?</div>
            <div style="font-weight:700;font-size:1rem;color:#343743;margin-bottom:0.3rem;
                font-family:Arial, sans-serif;">{title}</div>
            <div style="font-size:0.82rem;color:#747B8D;line-height:1.4;max-width:280px;
                margin:0 auto;font-family:Arial, sans-serif;">Will update with real data
                as we enter operations -- check back in to see your impact!</div>
        </div>
        """)


def mini_photo_spot(filename, label, height_px=100):
    """
    Small reference photo inside a pathway card -- what to actually look
    for at the physical bin/station. Rendered as a fixed-height,
    object-fit:cover <img> (not st.image) so its box size is always
    exactly height_px regardless of the source photo's dimensions --
    st.image sizes to its native aspect ratio, which is what was
    pushing into the tagline above it.
    """

    file_path = FIGURES_FOLDER / filename

    if file_path.exists():
        img_b64 = get_base64_image(file_path)
        ext = file_path.suffix.lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        render_html(f"""
        <div style="width:100%;height:{height_px}px;border-radius:10px;overflow:hidden;
            margin:0.55rem 0 0.6rem 0;">
            <img src="data:image/{mime};base64,{img_b64}"
                style="width:100%;height:100%;object-fit:cover;display:block;" />
        </div>
        """)
    else:
        render_html(f"""
        <div style="border:1px dashed #D8DCE5;border-radius:10px;height:{height_px}px;
            display:flex;align-items:center;justify-content:center;
            background:#FAFAFA;margin:0.55rem 0 0.6rem 0;">
            <div style="text-align:center;color:#9AA1B0;font-size:0.66rem;
                line-height:1.3;font-family:Arial, sans-serif;">
                \U0001F4F7<br>{label}
            </div>
        </div>
        """)


def get_base64_image(image_path):
    image_bytes = Path(image_path).read_bytes()
    return base64.b64encode(image_bytes).decode()


def pathway_card(icon, title, tagline, chips, outcome, accent, key, photo_filename=None,
                  photo_label=None, height=450, action_label=None, action_url=None):
    """
    Scannable feature card: badge icon, title, one-line tagline, an
    optional small reference photo, an optional call-to-action button
    (e.g. a mailto: link), accepted items as pill chips, and a single
    short outcome line combining destination + benefit. Same
    colored-border technique (div.st-key-{key}) as the rest of the site.
    Fixed height so all cards in a row line up -- height is only passed
    on desktop (4-across); on mobile, cards stack full-width and don't
    need to match each other's height.

    action_label / action_url: when both are set, a real st.link_button
    is rendered between the photo and the chips, tinted to match this
    card's accent color the same way the chips already are (accent+"17"
    for the fill, plain accent for the border/text).
    """

    render_html(f"""
    <style>
    div.st-key-{key} {{
        border: 1.5px solid {accent} !important;
        border-radius: 0.75rem !important;
    }}
    div.st-key-{key} div[data-testid="stLinkButton"] a {{
        background-color: #EDEEF0 !important;
        border: 1px solid #9AA1B0 !important;
        color: #343743 !important;
        font-weight: 600 !important;
    }}
    </style>
    """)

    chip_html = "".join(
        f'<span style="display:inline-block;background:{accent}17;color:{accent};'
        f'border:1px solid {accent}55;border-radius:999px;padding:0.22rem 0.65rem;'
        f'font-size:0.74rem;font-weight:600;margin:0.15rem 0.2rem;'
        f'font-family:Arial, sans-serif;">{c}</span>'
        for c in chips
    )

    container_kwargs = {"border": True, "key": key}
    if height is not None:
        container_kwargs["height"] = height

    with st.container(**container_kwargs):
        render_html(f"""
        <div style="text-align:center;">
            <div style="width:54px;height:54px;border-radius:50%;background:{accent}17;
                border:2px solid {accent};display:flex;align-items:center;justify-content:center;
                font-size:1.6rem;margin:0 auto 0.55rem auto;">{icon}</div>
            <div style="font-size:1.02rem;font-weight:700;color:#343743;margin-bottom:0.25rem;
                font-family:Arial, sans-serif;">{title}</div>
            <div style="font-size:0.8rem;color:#747B8D;line-height:1.4;
                font-family:Arial, sans-serif;">{tagline}</div>
        </div>
        """)

        if photo_filename:
            mini_photo_spot(photo_filename, photo_label)

        if action_label and action_url:
            top_margin = "0.6rem" if not photo_filename else "0"
            render_html(f"""<div style="margin:{top_margin} 0 0 0;"></div>""")
            st.link_button(action_label, action_url, use_container_width=True)

        outcome_html = ""
        if outcome and outcome.strip():
            outcome_html = f"""
            <div style="font-size:0.76rem;color:#343743;line-height:1.4;
                font-family:Arial, sans-serif;border-top:1px solid #E4E7EC;padding-top:0.55rem;">
                &#8594; {outcome}
            </div>
            """

        render_html(f"""
        <div style="text-align:center;">
            <div style="margin:0.65rem 0 0.65rem 0;">{chip_html}</div>
            {outcome_html}
        </div>
        """)


# ======================================================
# PAGE HERO
# ======================================================

HERO_IMAGE_PATH = IMAGES_DIR / "gateway_recovery_hero.jpg"

if HERO_IMAGE_PATH.exists():
    hero_image = get_base64_image(HERO_IMAGE_PATH)

    render_html(
        f"""
        <style>
        .recovery-hero {{
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
        .recovery-hero-content {{ max-width: 750px; padding: 3rem; color: white; }}
        .recovery-hero h1 {{
            margin: 0; color: white; font-size: clamp(2.7rem, 6vw, 5rem);
            line-height: 0.95; font-weight: 750; letter-spacing: -0.04em;
        }}
        .recovery-hero-line {{ width: 210px; height: 3px; margin: 1.3rem 0; background: #3F8F43; border-radius: 999px; }}
        .recovery-hero p {{ margin: 0; max-width: 560px; color: rgba(255,255,255,0.92); font-size: 1.1rem; line-height: 1.55; }}
        @media (max-width: 700px) {{
            .recovery-hero {{ min-height: 330px; background-position: 60% center; }}
            .recovery-hero-content {{ padding: 2rem; }}
            .recovery-hero h1 {{ font-size: 2.8rem; }}
            .recovery-hero p {{ font-size: 1rem; }}
        }}
        </style>
        <div class="recovery-hero">
            <div class="recovery-hero-content">
                <h1>Recovery<br>Systems</h1>
                <div class="recovery-hero-line"></div>
                <p>Some materials can't be reused. We designed pathways so they still avoid landfill.</p>
            </div>
        </div>
        """
    )
else:
    st.title("Recovery Systems")
    st.write("Some materials can't be reused. We designed pathways so they still avoid landfill.")
    st.caption(
        "Add a hero photo at `Images/gateway_recovery_hero.jpg` "
        "to enable the full banner treatment used on other pages."
    )

st.markdown("<div style='height: 1.6rem;'></div>", unsafe_allow_html=True)


# ======================================================
# WHERE RECOVERY FITS IN
# Shortened on mobile -- desktop keeps the original paragraph exactly
# as before.
# ======================================================

if is_mobile:
    st.write(
        "Recovery is the last stop for what can't be reused -- "
        "batteries, e-waste, hard-to-recycle plastics, food scraps. "
        "Each one still has a designed path out of the building that "
        "isn't the landfill."
    )
else:
    st.write(
        "Reduce, reuse, and refill handle most of what moves through Gateway. "
        "Recovery is the last stop for what's left over -- the batteries, "
        "electronics, hard-to-recycle plastics, and food scraps that can't "
        "go through that loop again. Each one still has a specific, "
        "designed path out of the building that isn't the landfill."
    )

st.divider()


# ======================================================
# RECOVERY PATHWAYS
# Four cards across on desktop; stacked full-width on mobile. Asking
# st.columns for exactly 1 column on mobile matches Streamlit's own
# collapse-to-1 breakpoint behavior, so there's no conflict here the
# way there was with the 2-across metrics grid on Reuse Systems.
# ======================================================

st.header("Recovery Pathways")
st.write("Four streams, four ways to send materials where they belong.")

PATHWAYS = [
    {
        "icon": "\U0001F50B",
        "title": "Batteries",
        "tagline": "Drop them in the labeled bin at any ReUse Station.",
        "chips": ["AA/AAA", "9V", "Button-cell", "Rechargeable"],
        "outcome": "Certified recycler \u2014 recovers metals, keeps them out of groundwater",
        "accent": "#0B6E4F",
        "key": "battery_pathway_card",
        "photo_filename": "gateway_battery_bin.jpg",
        "photo_label": "Battery collection bin"
    },
    {
        "icon": "\U0000267B\U0000FE0F",
        "title": "Specialty Plastics",
        "tagline": "Drop hard-to-recycle plastics in the Recovery Bin.",
        "chips": ["Pen refill cartridges", "Worn-out markers", "Worn-out pens"],
        "outcome": "TerraCycle \u2014 diverts plastics standard recycling won't take",
        "accent": "#3F8F43",
        "key": "specialty_plastics_pathway_card",
        "photo_filename": "gateway_terracycle_bin.jpg",
        "photo_label": "TerraCycle collection bin"
    },
    {
        "icon": "\U0001F4BB",
        "title": "E-Waste",
        "tagline": "Hold onto old electronics until you have a small batch, then request a pickup.",
        "chips": ["Cables", "Chargers", "Electronics", "Old devices"],
        "outcome": "Certified recycler \u2014 keeps metals & hazmat out of landfill",
        "accent": "#0B6E4F",
        "key": "ewaste_pathway_card",
        "photo_filename": "gateway_ewaste_bin.jpg",
        "photo_label": "E-waste ready for pickup",
        "action_label": "Email for Pickup \u2192",
        "action_url": f"mailto:{EWASTE_CONTACT_EMAIL}?subject={quote(EWASTE_MAILTO_SUBJECT)}"
    },
    {
        "icon": "\U0001F331",
        "title": "Compost",
        "tagline": "Standard bins throughout the building \u2014 plus the Mill, a special one on the 5th floor.",
        "chips": ["Food scraps", "Approved compostable service ware", "Meat & bones", "Dairy", "Coffee gounds & filters", "Tea bags", "Napkins"],
        "outcome": "Compost stream / Mill's grounds \u2014 keeps food waste out of landfill, cuts methane",
        "accent": "#3F8F43",
        "key": "compost_pathway_card"
    },
]

pathway_cols = st.columns(1 if is_mobile else 4, gap="medium")

for i, pathway in enumerate(PATHWAYS):
    with pathway_cols[i % len(pathway_cols)]:
        pathway_card(height=None if is_mobile else 450, **pathway)

st.divider()


# ======================================================
# MEET THE MILL
# Photo + text side by side on desktop, stacked on mobile.
# ======================================================

st.header("Meet the Mill")

mill_cols = st.columns(1 if is_mobile else 2, gap="large")
mill_photo_col = mill_cols[0]
mill_text_col = mill_cols[0] if is_mobile else mill_cols[1]

with mill_photo_col:
    show_media(
        "gateway_mill.jpg",
        instructions="Photo of the Mill itself in the 1st floor social kitchen -- the physical unit, ideally mid-use or freshly installed.",
        caption="The Mill, 1st floor social kitchen."
    )

with mill_text_col:
    st.write(
        "Most recovery pathways are a labeled bin. The Mill is the "
        "exception -- an on-site food recycler that dries and grinds "
        "scraps overnight into nutrient-dense grounds, right in the "
        "1st floor social kitchen. It's the one pathway occupants can "
        "actually watch do its job."
    )
    st.metric(label="Volume Reduction", value="~80%")
    st.caption("Grounds go to UC Berkeley's vermicomposting program, which also feeds Gateway's gardens.")
    st.caption("Want one for your own social kitchen? Departments can purchase a Mill directly.")

st.divider()


# ======================================================
# RECOVERY IN NUMBERS
# Fully visible on both mobile and desktop -- stacks instead of
# sitting side by side.
# ======================================================

st.header("Recovery in Numbers")

num_cols = st.columns(1 if is_mobile else 2, gap="large")
weight_col = num_cols[0]
diversion_col = num_cols[0] if is_mobile else num_cols[1]

with weight_col:
    metric_placeholder(title="Weight Collected", key="weight_collected_placeholder")

with diversion_col:
    metric_placeholder(title="Diversion Over Time", key="diversion_over_time_placeholder")

st.divider()


# ======================================================
# RESOURCES
# Fully visible on both mobile and desktop.
# ======================================================

st.header("Resources")

render_html(
    f"""
    <div style="
        background: #F3F5F2;
        border: 1px solid #0B6E4F;
        border-radius: 14px;
        padding: 1rem 1.3rem;
        margin: 0.8rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    ">
        <div style="font-size: 1.4rem;">\U0001F9ED</div>
        <div style="flex: 1; min-width: 220px; color: #343743; font-size: 0.92rem; line-height: 1.4;">
            Not sure which bin something goes in? The <strong>Waste Sorting</strong>
            section of the Zero Waste Operations Manual breaks down what goes where.
        </div>
    </div>
    """
)

st.link_button("View Sorting Guide", f"{MANUAL_URL}#slide=id.{MANUAL_PAGE_SORTING}", use_container_width=True)


# ======================================================
# CLOSING NOTE
# ======================================================

st.divider()

st.caption(
    "Gateway opened operationally in 2026. This page will be updated with real "
    "weight and diversion data as it becomes available."
    )