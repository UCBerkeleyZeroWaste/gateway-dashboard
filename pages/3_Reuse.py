import base64
import textwrap
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from styles import apply_global_style


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Reuse Systems | Gateway Systems Dashboard",
    page_icon="\U0000267B\U0000FE0F",
    layout="wide"
)

apply_global_style()


# ======================================================
# CONFIG
# Same manual/catalog URLs and page numbers used on the Resource
# Library and Circular Purchasing pages -- keep these in sync if the
# file locations or manual page layout change.
# ======================================================

MANUAL_URL = "app/static/Gateway_Zero_Waste_Operations_Manual.pdf"
CATALOG_URL = "https://docs.google.com/spreadsheets/d/1A8FVGTV1aYEEU8FSmAIqXaVte6zZQoTVcCfQZ-hz0IU/edit?gid=1487214576#gid=1487214576"
MANUAL_PAGE_KITCHEN = 14
MANUAL_PAGE_CAFE = 17


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
    to recolor a bordered container's border -- splitting a raw <div>
    open/close tag across two separate st.markdown calls does NOT work,
    since each st.markdown(unsafe_allow_html=True) call renders its own
    isolated HTML fragment; an unclosed <div> gets auto-closed at the end
    of that single call instead of wrapping later elements.
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
    no axes. active_indices: a set/list of step indices this page covers.
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

HERO_IMAGE_PATH = Path("images/gateway_reuse_hero.jpg")

if HERO_IMAGE_PATH.exists():
    hero_image = get_base64_image(HERO_IMAGE_PATH)

    render_html(
        f"""
        <style>
        .reuse-hero {{
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
        .reuse-hero-content {{ max-width: 750px; padding: 3rem; color: white; }}
        .reuse-hero h1 {{
            margin: 0; color: white; font-size: clamp(2.7rem, 6vw, 5rem);
            line-height: 0.95; font-weight: 750; letter-spacing: -0.04em;
        }}
        .reuse-hero-line {{ width: 210px; height: 3px; margin: 1.3rem 0; background: #3F8F43; border-radius: 999px; }}
        .reuse-hero p {{ margin: 0; max-width: 560px; color: rgba(255,255,255,0.92); font-size: 1.1rem; line-height: 1.55; }}
        @media (max-width: 700px) {{
            .reuse-hero {{ min-height: 330px; background-position: 60% center; }}
            .reuse-hero-content {{ padding: 2rem; }}
            .reuse-hero h1 {{ font-size: 2.8rem; }}
            .reuse-hero p {{ font-size: 1rem; }}
        }}
        </style>
        <div class="reuse-hero">
            <div class="reuse-hero-content">
                <h1>Reuse<br>Systems</h1>
                <div class="reuse-hero-line"></div>
                <p>Everything you need to keep supplies in circulation was already handed to you at move-in.</p>
            </div>
        </div>
        """
    )
else:
    st.title("Reuse Systems")
    st.write("Everything you need to keep supplies in circulation was already handed to you at move-in.")
    st.caption(
        "Add a hero photo at `images/gateway_reuse_hero.jpg` "
        "to enable the full banner treatment used on other pages."
    )

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)


# ======================================================
# WHERE REUSE FITS IN
# ======================================================

st.header("Where Reuse Fits In")

st.write("Supplies move through Gateway in a sequence, not a straight line to the trash.")


# ======================================================
# 3-STEP OVERVIEW -- moved to the very top of the page so
# the reuse -> refill -> reorder sequence is immediately
# visible on arrival, before any other content.
# ======================================================

step_indicator(["Reuse", "Refill", "Reorder"], active_indices={0, 1})

st.caption(
    "You are here. Step 3 -- ordering more once supplies actually run out "
    "-- is covered on the Circular Purchasing page."
)


# ======================================================
# WHY THIS MATTERS
# ======================================================

st.write(
    "Reuse works best when it's the easy option, not the responsible one. "
    "Gateway's Starter Kits and ReUse Stations exist so that keeping "
    "supplies in circulation takes less effort than ordering something "
    "new -- no extra trip, no extra decision, just the default path."
)

st.divider()

# ======================================================
# GATEWAY STARTER KITS
# ======================================================

st.header("Gateway Starter Kits")

st.write("Your introduction to Gateway's Circular Office Supply System -- provided to every department at move-in.")

kit_metric_1, kit_metric_2, kit_metric_3, kit_metric_4, kit_metric_5 = st.columns(5)

with kit_metric_1:
    compact_metric(value="1,308", label="B2P Refillable Pens", note="Planned starter kit quantity")

with kit_metric_2:
    compact_metric(value="100", label="Refillable Whiteboard Markers", note="Planned starter kit quantity")

with kit_metric_3:
    compact_metric(value="~55,000", label="Paper Clips", note="Estimated from a ~2 ft\u00b3 bulk container")

with kit_metric_4:
    compact_metric(value="50+", label="Binders", note="Condition varies")

with kit_metric_5:
    compact_metric(value="Multiple boxes", label="Organizational Supplies", note="File organizers, Avery labels, staples, accordion folders")

# ------------------------------------------------------
# Refillable Writing System (1/3 width) next to the
# plastic prevented/recovered chart (2/3 width), so the
# card and its supporting data sit side by side instead
# of stacked.
# ------------------------------------------------------

writing_col, chart_col = st.columns([1, 2], gap="large")

with writing_col:
    bullet_card(
        title="Refillable Writing System",
        bullets=[
            "Pilot B2P refillable pens",
            "Refillable whiteboard markers",
            "Refill both at the Refill Hub in any ReUse Station"
        ]
    )

with chart_col:
    plastic_years = ["2026", "2027", "2028"]
    prevented_kg = [37.916, 75.832, 113.748]
    recovered_kg = [8.448, 16.896, 25.344]
    total_kg = [p + r for p, r in zip(prevented_kg, recovered_kg)]

    plastic_fig = go.Figure()

    plastic_fig.add_trace(go.Bar(
        x=plastic_years,
        y=prevented_kg,
        name="Prevented",
        marker=dict(color="#0B6E4F"),
        text=[f"{v:.1f} kg" for v in prevented_kg],
        textposition="inside",
        textfont=dict(family="Arial, sans-serif", size=11, color="white"),
        hovertemplate="<b>%{x}</b><br>%{y:.1f} kg prevented<extra></extra>"
    ))

    plastic_fig.add_trace(go.Bar(
        x=plastic_years,
        y=recovered_kg,
        name="Recovered via TerraCycle",
        marker=dict(color="#3F8F43"),
        text=[f"{v:.1f} kg" for v in recovered_kg],
        textposition="inside",
        textfont=dict(family="Arial, sans-serif", size=11, color="white"),
        hovertemplate="<b>%{x}</b><br>%{y:.1f} kg recovered via TerraCycle<extra></extra>"
    ))

    for x_val, total in zip(plastic_years, total_kg):
        plastic_fig.add_annotation(
            x=x_val, y=total, text=f"{total:.1f} kg", showarrow=False,
            yshift=12, font=dict(family="Arial, sans-serif", size=11, color="#343743")
        )

    plastic_fig.update_layout(
        barmode="stack",
        title=dict(
            text="<b>Projected Plastic Prevented and Recovered</b><br><span style='font-size:11px;color:#747B8D;'>Cumulative, based on planned starter kit quantities</span>",
            x=0, xanchor="left", y=0.94, yanchor="top",
            font=dict(family="Arial, sans-serif", size=15, color="#343743")
        ),
        height=280,
        margin=dict(l=40, r=15, t=64, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", color="#343743"),
        legend=dict(orientation="h", y=-0.18, x=0, font=dict(size=10))
    )

    plastic_fig.update_yaxes(title=None, showgrid=True, gridcolor="rgba(116,123,141,0.13)", showline=False, zeroline=False, fixedrange=True)
    plastic_fig.update_xaxes(title=None, showgrid=False, showline=False, ticks="", fixedrange=True)

    st.plotly_chart(plastic_fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})

st.caption(
    "Estimated from planned pen and marker quantities, refill frequency, and "
    "plastic per disposable equivalent. The small "
    "amount of residual plastic left over from each refill isn't landfilled "
    "either, it's caught by Gateway's TerraCycle specialty recycling bin."
)


st.caption(
    "Worn-out pens, markers, and mechanical pencils don't go in the trash either. "
    "Drop them at the Recovery Bin in any ReUse Station."
)


# ======================================================
# REUSE STATIONS
# ======================================================

st.header("ReUse Stations")

st.write("Shared refill and redistribution infrastructure, found on every floor.")

# ------------------------------------------------------
# Photo (portrait -- crop to 2:3) next to the Refill Hub
# and Shared Stock cards stacked on top of each other,
# rather than a full-width photo above two side-by-side
# cards.
# ------------------------------------------------------

station_photo_col, station_cards_col = st.columns(2, gap="large")

with station_photo_col:
    show_media(
        "gateway_reuse_station.png",
        instructions="Photo of an actual ReUse Station -- the physical stand or shelf holding the Refill Hub and shared stock. Crop to a 2:3 portrait ratio.",
        caption="A ReUse Station on one of Gateway's floors."
    )

with station_cards_col:
    bullet_card(
        title="Refill Hub Contents",
        bullets=[
            "Pilot G2 pen ink refills",
            "Whiteboard marker refill cartridges"
        ]
    )
    bullet_card(
        title="Shared Stock Contents",
        bullets=[
            "Reusable organization materials -- file organizers, dividers, binders",
            "Paper clips and approved redistribution items"
        ]
    )

bullet_card(
    title="What ReUse Stations Are For",
    bullets=[
        "Donate usable office supplies and collect shared materials.",
        "Access refill stock for Gateway's reusable writing supplies.",
        "Reduce duplicate purchasing across departments.",
        "Not a dumping space -- items placed here should be usable, not discarded."
    ]
)

render_html(
    """
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
        <div style="font-size: 1.4rem;">\U0001F50E</div>
        <div style="flex: 1; min-width: 220px; color: #343743; font-size: 0.92rem; line-height: 1.4;">
            Want to check what's currently stocked in a ReUse Station? The
            <strong>Approved Products Catalog</strong> stays current with real inventory.
        </div>
    </div>
    """
)

st.link_button("View Catalog", CATALOG_URL, use_container_width=True)

st.divider()

# ======================================================
# OUR REUSABLES
# ======================================================

st.header("Our Reusables")

st.write(
    "Gateway's social kitchens are stocked with real dishware, not "
    "disposables -- glasses, plates, flatware, and mugs that get washed "
    "and used again instead of thrown away after one round."
)

reusables_photo_col, reusables_list_col = st.columns(2, gap="large")

with reusables_photo_col:
    show_media(
        "gateway_reusables_set.jpg",
        instructions=(
            "Photo of Gateway's reusable kitchenware set -- glasses, plates, "
            "bowls, flatware, serving platters, and mugs, ideally styled "
            "together to show off the full set."
        ),
        caption="Gateway's reusable kitchenware set."
    )

with reusables_list_col:
    bullet_card(
        title="What's In the Set",
        bullets=[
            "Tall glasses (90) and short glasses (90)",
            "Plates (210), salad plates (210), and bowls (210)",
            "Forks (256), knives (128), and spoons (256)",
            "Serving platters (36) and mugs (216)"
        ],
        metric="425,500",
        metric_label="Disposable Items Avoided Per Year"
    )

st.caption(
    f"Need more for a department or event? The [Approved Products "
    f"Catalog]({CATALOG_URL}) lists where to reorder the same reusable "
    f"kitchenware."
)

st.divider()

# ======================================================
# WHERE ELSE REUSE SHOWS UP
# Cards link straight to the source (the manual, via page anchor) --
# not to the Resource Library -- so this stays a two-click path, not
# three. The Resource Library still carries the same entries for
# anyone who lands there directly via the sidebar/homepage.
# ======================================================

st.header("Where Else Reuse Shows Up")

st.write(
    "Reuse extends into kitchens and caf\u00e9s too."
)

moment_1, moment_2 = st.columns(2, gap="large")

with moment_1:
    bordered_link_card(
        title="Kitchen Reusables",
        description="The reuse-first system for Gateway's social kitchens -- reusable dishware, utensils, and cleaning stations.",
        button_label="Read Kitchen Reusables \u2192",
        button_url=f"{MANUAL_URL}#page={MANUAL_PAGE_KITCHEN}",
        accent="#0B6E4F",
        key="kitchen_reusables_card"
    )

with moment_2:
    bordered_link_card(
        title="Caf\u00e9 Operations",
        description="How Dispatch Goods -- Gateway's reusable takeout system -- works: borrow, use, return, reuse.",
        button_label="Read Caf\u00e9 Operations \u2192",
        button_url=f"{MANUAL_URL}#page={MANUAL_PAGE_CAFE}",
        accent="#3F8F43",
        key="cafe_operations_card"
    )


# ======================================================
# PROJECT RESOURCES
# Removed entirely on this page, same reasoning as Circular
# Purchasing. Catalog already has a specific, working callout above
# ("check what's stocked") plus a reorder link under Our Reusables --
# a generic footer card added nothing. Nobody arriving here needs the
# full manual either: Starter Kits and ReUse Stations content is
# already written directly on this page, and Kitchen Reusables /
# Caf\u00e9 Operations now link straight to their specific manual pages.
# The full manual stays reachable from the homepage and sidebar for
# anyone who wants the whole document.
# ======================================================


# ======================================================
# CLOSING NOTE
# ======================================================

st.divider()

st.caption(
    "Gateway opened operationally in 2026. Update this page with photos "
    "and real usage details as ReUse Stations become fully stocked."
)