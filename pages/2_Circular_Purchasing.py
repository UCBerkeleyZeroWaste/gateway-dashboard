import base64
import textwrap
from pathlib import Path

import streamlit as st

from styles import apply_global_style


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Circular Purchasing | Gateway Systems Dashboard",
    page_icon="\U0001F6D2",
    layout="wide"
)

apply_global_style()


# ======================================================
# CONFIG
# Manual now lives as a Google Slides deck (not a hosted PDF) --
# MANUAL_URL points to the "present" view, and each page-number
# variable is that section's actual Slides slide ID rather than a
# page number. Keep these in sync with Reuse Systems and Recovery
# Systems if the deck's slide order ever changes.
# ======================================================

MANUAL_URL = "https://docs.google.com/presentation/d/1j3IVyxEG0aGZXlMy2ydaw6Dh-32Yhf_N/present"
MANUAL_PAGE_CATERING = "g3f21e15226c_0_206"
MANUAL_PAGE_EVENTS = "g3f21e15226c_0_249"


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
    div[data-testid="stCaptionContainer"] p { font-size: 0.78rem !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] { padding: 0.72rem 0.82rem !important; }
    div[data-testid="stMetricValue"] { font-size: 1.45rem !important; }
    div[data-testid="stMetricLabel"] { font-size: 0.78rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0.65rem; }
    details summary p { font-size: 0.9rem !important; }
    </style>
    """
)


FIGURES_FOLDER = Path("Figures")


def show_media(filename, instructions, caption=None, title=None, bordered_placeholder=True):
    """Display an image if it exists; otherwise show a labeled placeholder."""

    file_path = FIGURES_FOLDER / filename

    if file_path.exists():
        st.image(str(file_path), caption=caption, use_container_width=True)
    else:
        placeholder = st.container(border=bordered_placeholder)
        with placeholder:
            if title:
                st.subheader(title)
            st.info(
                f"**Visual placeholder**\n\n{instructions}\n\n"
                f"Save the finished file as:\n\n`Figures/{filename}`"
            )


def bullet_card(title, bullets, metric=None, metric_label=None, height=None, accent=None, key=None):
    """
    accent + key: when both are set, the card border is recolored via CSS
    targeting the container's stable `st-key-<key>` class (added by
    Streamlit when a container is given a key). This is the correct way
    to recolor a bordered container's border, since the container still
    actually wraps its children -- unlike splitting a raw <div> open/close
    tag across two separate st.markdown calls, which does NOT work:
    each st.markdown(unsafe_allow_html=True) call renders its own isolated
    HTML fragment, so an unclosed <div> gets auto-closed by the browser at
    the end of that single call instead of wrapping later elements.
    """

    container_kwargs = {"border": True}
    if height is not None:
        container_kwargs["height"] = height
    if key is not None:
        container_kwargs["key"] = key

    if accent and key:
        render_html(f"""
        <style>
        div.st-key-{key} {{
            border: 1.5px solid {accent} !important;
            border-radius: 0.75rem !important;
        }}
        </style>
        """)

    with st.container(**container_kwargs):
        st.subheader(title)
        if metric:
            st.metric(label=metric_label or "", value=metric)
        for bullet in bullets:
            st.markdown(f"- {bullet}")


def numbered_card(title, items, caption=None, height=None, accent=None, key=None, link_label=None, link_url=None):
    """Same shape as bullet_card, but for ordered action steps."""

    container_kwargs = {"border": True}
    if height is not None:
        container_kwargs["height"] = height
    if key is not None:
        container_kwargs["key"] = key

    if accent and key:
        render_html(f"""
        <style>
        div.st-key-{key} {{
            border: 1.5px solid {accent} !important;
            border-radius: 0.75rem !important;
        }}
        </style>
        """)

    with st.container(**container_kwargs):
        st.subheader(title)
        for i, item in enumerate(items, start=1):
            st.markdown(f"{i}. {item}")
        if caption:
            st.caption(caption)
        if link_label and link_url:
            st.link_button(link_label, link_url, use_container_width=True)


def bordered_link_card(title, description, button_label, button_url=None, button_key=None, accent=None, key=None, height=170):
    """
    Same shape as the plain st.container(border=True) info cards used for
    cross-link ("Where Else X Shows Up") sections, but with a colored
    border via the same key-based CSS technique as bullet_card/numbered_card.

    Pass button_url to render a real, working st.link_button. Omitting it
    falls back to a disabled placeholder button (button_key required in
    that case) -- useful while a destination isn't hosted/ready yet.
    """

    container_kwargs = {"border": True, "height": height}
    if key is not None:
        container_kwargs["key"] = key

    if accent and key:
        render_html(f"""
        <style>
        div.st-key-{key} {{
            border: 1.5px solid {accent} !important;
            border-radius: 0.75rem !important;
        }}
        </style>
        """)

    with st.container(**container_kwargs):
        st.subheader(title)
        st.write(description)
        if button_url:
            st.link_button(button_label, button_url, use_container_width=True)
        else:
            st.button(button_label, key=button_key, use_container_width=True, disabled=True)


def compact_metric(value, label, note=None):
    st.metric(label=label, value=value)
    if note:
        st.caption(note)


def get_base64_image(image_path):
    image_bytes = Path(image_path).read_bytes()
    return base64.b64encode(image_bytes).decode()


def step_indicator(steps, active_indices):
    """
    Simple numbered-step visual -- circles connected by a line, no chart,
    no axes. Replaces the earlier funnel chart, which had the same label
    appearing twice (once as an axis category, once as bar text).
    active_indices: a set/list of step indices this page covers.
    """

    parts = []
    for i, label in enumerate(steps):
        is_active = i in active_indices
        circle_bg = "#0B6E4F" if is_active else "#F3F5F2"
        circle_border = "#0B6E4F" if is_active else "#D8DCE5"
        circle_color = "white" if is_active else "#747B8D"
        text_color = "#0B6E4F" if is_active else "#747B8D"
        text_weight = "700" if is_active else "600"
        parts.append(f"""
        <div style="display:flex;flex-direction:column;align-items:center;flex:1;">
            <div style="width:52px;height:52px;border-radius:50%;background:{circle_bg};
                border:2px solid {circle_border};color:{circle_color};display:flex;
                align-items:center;justify-content:center;font-weight:700;font-size:1.1rem;
                font-family:Arial, sans-serif;">{i + 1}</div>
            <div style="margin-top:0.5rem;font-size:0.85rem;color:{text_color};
                font-weight:{text_weight};font-family:Arial, sans-serif;">{label}</div>
        </div>
        """)
        if i < len(steps) - 1:
            parts.append('<div style="flex:1;height:2px;background:#D8DCE5;margin-bottom:1.9rem;"></div>')

    render_html(
        f"""
        <div style="display:flex;align-items:flex-start;justify-content:center;
            gap:0;margin:1rem 0 0.6rem 0;">
            {''.join(parts)}
        </div>
        """
    )


# ======================================================
# PAGE HERO
# ======================================================

HERO_IMAGE_PATH = Path("images/gateway_circular_purchasing_hero.jpg")

if HERO_IMAGE_PATH.exists():
    hero_image = get_base64_image(HERO_IMAGE_PATH)

    render_html(
        f"""
        <style>
        .purchasing-hero {{
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
        .purchasing-hero-content {{ max-width: 750px; padding: 3rem; color: white; }}
        .purchasing-hero h1 {{
            margin: 0; color: white; font-size: clamp(2.7rem, 6vw, 5rem);
            line-height: 0.95; font-weight: 750; letter-spacing: -0.04em;
        }}
        .purchasing-hero-line {{ width: 210px; height: 3px; margin: 1.3rem 0; background: #3F8F43; border-radius: 999px; }}
        .purchasing-hero p {{ margin: 0; max-width: 560px; color: rgba(255,255,255,0.92); font-size: 1.1rem; line-height: 1.55; }}
        @media (max-width: 700px) {{
            .purchasing-hero {{ min-height: 330px; background-position: 60% center; }}
            .purchasing-hero-content {{ padding: 2rem; }}
            .purchasing-hero h1 {{ font-size: 2.8rem; }}
            .purchasing-hero p {{ font-size: 1rem; }}
        }}
        </style>
        <div class="purchasing-hero">
            <div class="purchasing-hero-content">
                <h1>Circular<br>Purchasing</h1>
                <div class="purchasing-hero-line"></div>
                <p>Check first. Refill first. Order last -- and make it count.</p>
            </div>
        </div>
        """
    )
else:
    st.title("Circular Purchasing")
    st.write("Check first. Refill first. Order last -- and make it count.")
    st.caption(
        "Add a hero photo at `images/gateway_circular_purchasing_hero.jpg` "
        "to enable the full banner treatment used on other pages."
    )

st.markdown("<div style=\'height: 2rem;\'></div>", unsafe_allow_html=True)

# ======================================================
# WHY THIS MATTERS
# ======================================================

st.markdown(
    "Purchasing is where a lot of waste gets decided before it ever exists. "
    "Packaging, delivery trips, and duplicate orders all get locked in the "
    "moment something is bought. What departments choose to order is one of "
    "the few places that number gets easier or harder before anything "
    "reaches a bin."
)

render_html(
    """
    <div style="
        background: #0B6E4F;
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin: 0.5rem 0 1.3rem 0;
        display: flex;
        align-items: center;
        gap: 1.8rem;
        flex-wrap: wrap;
        font-family: Arial, sans-serif;
    ">
        <div style="
            font-size: 3.4rem;
            font-weight: 800;
            line-height: 1;
            color: white;
            letter-spacing: -0.02em;
        ">90%+</div>
        <div style="
            max-width: 480px;
            color: rgba(255,255,255,0.92);
            font-size: 1rem;
            line-height: 1.5;
        ">
            is Gateway\'s landfill diversion target. Every order placed on this
            page either moves the building toward it or away from it.
        </div>
    </div>
    """
)


# ======================================================
# WHERE PURCHASING FITS IN
# ======================================================

st.header("Where Purchasing Fits In")

st.write(
    "Purchasing is the last step in a longer sequence -- reuse and refill "
    "come first, and this page picks up once supplies actually run out."
)

step_indicator(["Reuse", "Refill", "Reorder"], active_indices={2})

st.caption(
    "You are here. Steps 1 & 2 -- reusing starter supplies and refilling "
    "them at the Refill Hub -- are covered on the Reuse Systems page."
)

numbered_card(
    title="Before You Order Anything",
    items=[
        "Check the ReUse Stations, routine supplies are often already there.",
        "Try the Refill Hub before buying something new.",
        "Still need it? That\'s what the rest of this page covers."
    ]
)

st.divider()

# ======================================================
# PURCHASING PATHWAYS
# ======================================================

st.header("Purchasing Pathways")

st.write("Two ways to order, depending on what you need.")

stockroom_col, bearbuy_col = st.columns(2, gap="large")

with stockroom_col:
    numbered_card(
        title="Standard Purchasing -- Gateway Stockroom",
        items=[
            "Set up an account by emailing the Stanley Hall storeroom team to get registered.",
            "Once set up, reorder directly -- no BearBUY purchase order needed."
        ],
        caption=(
            "The Stockroom is the Avantor Storeroom in Stanley Hall, open to "
            "all campus research labs. It also carries office supplies "
            "through Gateway\'s partnership with Blaisdell\'s, including EPP "
            "options at a bulk discount."
        ),
        height=280,
        accent="#0B6E4F",
        key="stockroom_card",
        link_label="Email the Storeroom",
        link_url="mailto:stanley.stockroom@avantorsciences.com"
    )

with bearbuy_col:
    numbered_card(
        title="Specialty Purchasing -- BearBUY",
        items=[
            "Log into BearBUY, UC Berkeley\'s procurement marketplace.",
            "Look for Blaisdell\'s storefront first -- Gateway\'s preferred vendor, with EPP items filterable."
        ],
        caption="Use this only when the Stockroom doesn\'t carry what you need.",
        height=280,
        accent="#3F8F43",
        key="bearbuy_card",
        link_label="Go to BearBUY",
        link_url="https://supplychain.berkeley.edu/bearbuy"
    )

with st.container(border=True):
    st.subheader("Not Sure Which One?")
    st.write(
        "The Gateway Approved Products Catalog shows which pathway applies "
        "to a specific item, along with vendor and catalog numbers. It\'s "
        "also kept current with what\'s actually stocked in the ReUse "
        "Stations, so it doubles as a quick way to check availability "
        "before you buy anything at all."
    )
    st.link_button(
        "View Catalog",
        "https://docs.google.com/spreadsheets/d/1A8FVGTV1aYEEU8FSmAIqXaVte6zZQoTVcCfQZ-hz0IU/edit?gid=1487214576#gid=1487214576",
        use_container_width=True
    )
st.divider()

# ======================================================
# WHERE ELSE PURCHASING SHOWS UP
# Cards link straight to the source (the manual, via slide anchor) --
# not to the Resource Library -- so this stays a two-click path, not
# three. The Resource Library still carries the same entries for
# anyone who lands there directly via the sidebar/homepage.
# ======================================================

st.header("Where Else Purchasing Shows Up")

st.write(
    "Catering and events are where good purchasing habits are easiest to "
    "abandon, a single delivery of disposable cups and trays can undo a "
    "whole department\'s worth of careful ordering."
)



moment_1, moment_2 = st.columns(2, gap="large")

with moment_1:
    bordered_link_card(
        title="Catering Policies",
        description="Ordering in bulk, requesting reusable serviceware, and minimizing packaging when food is catered.",
        button_label="Read Catering Policies \u2192",
        button_url=f"{MANUAL_URL}#slide=id.{MANUAL_PAGE_CATERING}",
        accent="#0B6E4F",
        key="catering_policies_card"
    )

with moment_2:
    bordered_link_card(
        title="Event Guidelines",
        description="What to order for giveaways, decor, and signage -- and what to avoid.",
        button_label="Read Event Guidelines \u2192",
        button_url=f"{MANUAL_URL}#slide=id.{MANUAL_PAGE_EVENTS}",
        accent="#3F8F43",
        key="event_guidelines_card"
    )


render_html(
    """
    <div style="display:flex;flex-direction:column;gap:0.6rem;margin:0.6rem 0 1.2rem 0;">
        <div style="background:#F3F5F2;border-left:4px solid #0B6E4F;
            border-radius:10px;padding:0.85rem 1.3rem;">
            <div style="font-weight:700;color:#0B6E4F;font-size:0.95rem;margin-bottom:0.35rem;">
                \u2713 Looks Like This
            </div>
            <ul style="margin:0;padding-left:1.2rem;font-size:0.88rem;color:#343743;line-height:1.55;">
                <li>Reusable serviceware prioritized -- see Dispatch Goods</li>
                <li>Approved compostables when necessary</li>
                <li>Bulk ordering from approved vendors -- see the Gateway Approved Products Catalog</li>
            </ul>
        </div>
        <div style="background:#F3F5F2;border-left:4px solid #747B8D;
            border-radius:10px;padding:0.85rem 1.3rem;">
            <div style="font-weight:700;color:#747B8D;font-size:0.95rem;margin-bottom:0.35rem;">
                \u2715 Not This
            </div>
            <ul style="margin:0;padding-left:1.2rem;font-size:0.88rem;color:#343743;line-height:1.55;">
                <li>Single-use plastic cups, plates, utensils, and trays piling up in the bin before the event\'s even over.</li>
            </ul>
        </div>
    </div>
    """
)

st.divider()

# ======================================================
# HOW WE ACHIEVE CIRCULAR PURCHASING
# ======================================================

st.header("How We Achieve Circular Purchasing")

st.write(
    "These are standard TRUE Zero Waste purchasing practices -- not unique "
    "to Gateway, but core to how the whole program works."
)

standard_1, standard_2 = st.columns(2, gap="large")

with standard_1:
    bullet_card(
        title="Recycled Content",
        bullets=[
            "Office paper: \u226530% post-consumer recycled content.",
            "Janitorial paper products (towels, tissue): \u226520% post-consumer recycled content.",
            "Sustainably produced paper and wood products preferred."
        ]
    )

with standard_2:
    bullet_card(
        title="What We Prioritize",
        bullets=[
            "Durable and reusable goods over disposable ones.",
            "Used, refurbished, or remanufactured goods when available.",
            "Approved vendors only."
        ]
    )

st.divider()

# ======================================================
# Have any questions or product requests?
# ======================================================

st.header("Can\'t Find What You Need, or Just Have a Question?")

with st.container(border=True):
    st.write("Submit a request for a product we don\'t carry, or ask us anything about how Circular Purchasing works and we will follow up.")
    st.link_button(
        "Ask or Request",
        "https://docs.google.com/forms/d/e/1FAIpQLSd6228-0VySoiQXMYRLDfUz7obqbrjYKIy6qmNrcVp3NFGGow/viewform?usp=publish-editor",
        use_container_width=True
    )


# ======================================================
# PROJECT RESOURCES
# Removed entirely on this page. The Catalog is already covered above
# by "Not Sure Which One?" and the "Looks Like This" checklist, and
# nobody arriving here mid-purchasing-task needs the full manual --
# Pathways, Catalog, and Catering/Event Guidelines already cover what
# this page is for. The full manual stays reachable from the homepage
# and sidebar for anyone who actually wants the whole document.
# ======================================================

# ======================================================
# CLOSING NOTE
# ======================================================

st.divider()

st.caption(
    "Gateway opened operationally in 2026, so purchasing figures reflect "
    "program design rather than measured performance data. Update this "
    "page with real purchasing metrics as they become available."
)
