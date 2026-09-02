import streamlit as st

from styles import apply_global_style
from paths import IMAGES_DIR
from device import get_is_mobile


# ======================================================
# PAGE CONFIGURATION
# This must be the first Streamlit command in the file.
# ======================================================

st.set_page_config(
    page_title="Gateway Sustainability Systems",
    page_icon="♻️",
    layout="wide"
)

apply_global_style()

# Manual now lives as a Google Slides deck -- same URL used on
# 6_Resource_Library.py. Keep these in sync if the deck ever moves.
MANUAL_URL = "https://docs.google.com/presentation/d/1j3IVyxEG0aGZXlMy2ydaw6Dh-32Yhf_N/present"

# The two greens already used across the site (hero accents, pathway
# cards, cross-link borders). Reused here instead of introducing any
# new color.
GREEN_DARK = "#0B6E4F"
GREEN_MID = "#3F8F43"
GREEN_TINT = "#E8F3EC"  # light tint of GREEN_DARK, for button fills


# ======================================================
# DEVICE DETECTION
# Reports the real browser viewport width back into Python. Uses
# window.parent.innerWidth (not window.innerWidth) since the JS runs
# inside the component's own iframe -- window.innerWidth alone would
# measure that narrow iframe, not the actual browser window. Returns
# None for one render on first load, then Streamlit reruns
# automatically once the real value comes back -- so is_mobile settles
# to a correct True/False right after.
# ======================================================

screen_width = get_is_mobile()

if screen_width is None:
    # None only on the very first render of a session, before the
    # cached value exists (see device.py) -- this is what was causing
    # the desktop layout to flash before snapping to mobile. Rendering
    # a neutral skeleton and stopping here means nothing layout-
    # specific paints before the real value resolves and Streamlit
    # auto-reruns. On every later page navigation this session, the
    # cached value returns immediately and this branch is skipped
    # entirely -- no repeat skeleton flashes.
    st.markdown(
        """
        <style>
        @keyframes gw-pulse {
            0% { opacity: 0.5; }
            50% { opacity: 0.85; }
            100% { opacity: 0.5; }
        }
        .gw-skeleton {
            background-color: #E4E7EC;
            border-radius: 10px;
            animation: gw-pulse 1.3s ease-in-out infinite;
        }
        </style>
        <div class="gw-skeleton" style="height:170px;width:100%;margin-bottom:1.4rem;"></div>
        <div class="gw-skeleton" style="height:2.1rem;width:65%;margin-bottom:0.7rem;"></div>
        <div class="gw-skeleton" style="height:1rem;width:90%;margin-bottom:0.4rem;"></div>
        <div class="gw-skeleton" style="height:1rem;width:55%;margin-bottom:2rem;"></div>
        <div class="gw-skeleton" style="height:88px;width:100%;margin-bottom:0.8rem;"></div>
        <div class="gw-skeleton" style="height:88px;width:100%;margin-bottom:0.8rem;"></div>
        <div class="gw-skeleton" style="height:88px;width:100%;margin-bottom:0.8rem;"></div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

is_mobile = screen_width


# ======================================================
# MOBILE BUTTON STYLING
# Light green fill for every mobile "Open" button -- reuses the same
# div.st-key-{key} CSS-targeting technique already used throughout the
# site (bullet_card, pathway_card, etc.) rather than introducing a new
# pattern.
#
# st.button renders a real <button> element, but st.link_button renders
# an <a> styled to look like one -- so the two need slightly different
# CSS selectors. target="button" for st.button, target="a" for
# st.link_button. st.link_button also doesn't accept a key= argument
# directly, so link buttons get wrapped in their own st.container(key=...)
# instead, and the CSS targets that container's key.
# ======================================================

def style_mobile_button(key, target="button"):
    st.markdown(
        f"""
        <style>
        div.st-key-{key} {target} {{
            background-color: {GREEN_TINT} !important;
            border: 1px solid {GREEN_DARK} !important;
            color: {GREEN_DARK} !important;
            font-weight: 600 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ======================================================
# MOBILE CARD SPACING
# Collapses the default vertical-block gap Streamlit applies between
# stacked elements inside a container -- the columns row, the arrow,
# and the button all had ~1rem of flex gap between them by default,
# which is what made the cards read as too spacious on mobile. This
# overrides that gap directly rather than fighting it with margins on
# the inner markdown.
# ======================================================

def style_mobile_card_spacing(key):
    st.markdown(
        f"""
        <style>
        div.st-key-{key} [data-testid="stVerticalBlock"] {{
            gap: 0.35rem !important;
        }}
        div.st-key-{key} div[data-testid="stElementContainer"] {{
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ======================================================
# SYSTEM CARD DATA
# One source of truth for both the mobile and desktop layouts, so
# titles/teasers/images only need to be edited in one place.
# ======================================================

SYSTEMS = [
    {
        "title": "Construction Systems",
        "teaser_short": "How we built it right",
        "teaser_long": "Reducing waste before the building even opened.",
        "image": "Construction.jpg",
        "page": "pages/1_Construction.py",
        "key": "construction"
    },
    {
        "title": "Circular Purchasing",
        "teaser_short": "Reorder the right way",
        "teaser_long": "Standardizing purchasing and refill systems to prevent waste.",
        "image": "Circular_Purchasing.jpg",
        "page": "pages/2_Circular_Purchasing.py",
        "key": "purchasing"
    },
    {
        "title": "Reuse Systems",
        "teaser_short": "Stations, refill, reorder",
        "teaser_long": "Making reuse the easiest option every day.",
        "image": "Reuse.jpg",
        "page": "pages/3_Reuse.py",
        "key": "reuse"
    },
    {
        "title": "Recovery Systems",
        "teaser_short": "Batteries, e-waste, compost",
        "teaser_long": "Capturing materials that cannot be prevented or reused.",
        "image": "Recovery.jpg",
        "page": "pages/4_Recovery.py",
        "key": "recovery"
    },
    {
        "title": "Building Systems",
        "teaser_short": "Energy, water, air quality",
        "teaser_long": "Reducing resource use through efficient building systems.",
        "image": "Building.jpg",
        "page": "pages/5_Building_Systems.py",
        "key": "building"
    },
]


# ======================================================
# MOBILE HERO IMAGE
# Small, fixed-height banner shown only on mobile, right above the
# page title. object-fit: cover keeps it compact and consistent
# regardless of the source photo's aspect ratio, cropping rather than
# squishing it. Adjust the height below if it still feels too thin
# once you see it live.
# ======================================================

if is_mobile:
    st.markdown(
        """
        <style>
        /* Break the hero out of Streamlit's default content padding so
        the photo runs edge-to-edge, and zero out the default gap
        Streamlit puts between elements inside this container -- same
        technique used on the system cards below. Title card and photo
        are both children of ONE container now (not two separate ones)
        so the negative margin pulling the title up actually holds. */
        div.st-key-home_hero {
            margin-left: -1rem !important;
            margin-right: -1rem !important;
            width: calc(100% + 2rem) !important;
        }
        div.st-key-home_hero div[data-testid="stElementContainer"] {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }
        div.st-key-home_hero img {
            height: 170px !important;
            width: 100% !important;
            object-fit: cover !important;
            display: block !important;
            border-radius: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.container(key="home_hero"):
        st.image(
            str(IMAGES_DIR / "Home_Hero.jpg"),
            use_container_width=True
        )
        # Title + intro built as one HTML block (not st.title/st.write)
        # so it's a single element sitting directly under the image in
        # this same container -- that's what makes the overlap hold.
        # border-radius left at 0 for now: rounding the top corners
        # only looks right if the page background matches this card's
        # white exactly, otherwise the rounded gap reveals whatever's
        # behind it (that's what caused the green sliver).
        st.markdown(
            """
            <div style="
                position: relative;
                z-index: 2;
                background-color: #FFFFFF;
                margin-top: -1.75rem;
                padding: 1.1rem 0 0.25rem 0;
            ">
                <div style="font-size:2.25rem;font-weight:800;line-height:1.15;color:#111417;margin-bottom:0.6rem;">
                    Gateway Sustainability Systems
                </div>
                <div style="font-size:1rem;color:#31333F;line-height:1.5;">
                    The first building in the world pursuing TRUE Zero Waste Certification for both construction and operations.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ======================================================
# PAGE INTRODUCTION (desktop only)
# On mobile, the title and intro sentence are rendered inside
# home_hero above so they can overlap the photo. Desktop has no hero
# image and keeps the original st.title/st.write.
# ======================================================

if not is_mobile:
    st.title("Gateway Sustainability Systems")
    st.write(
        "An interactive guide to the sustainability systems of the Barbara and Gerson Bakar Gateway, home of the UC Berkeley College of Computing, Data Science, and Society. Gateway houses the first new college added to UC Berkeley for over 50 years, with construction reaching completion as of June 2026."
        " Gateway is the first building in the world to pursue TRUE Zero Waste Certification for both construction and operations."
    )


# ======================================================
# EXPLORE GATEWAY'S SYSTEMS
# ======================================================

st.header("Explore Gateway")

st.caption(
    "Learn how materials, purchasing, reuse, recovery, and building operations "
    "work together to support Gateway's zero waste goals."
)

if is_mobile:

    # --------------------------------------------------
    # MOBILE -- compact tappable list. Title, one-line teaser, tap
    # anywhere on the row to open the page. No hero photos or long
    # descriptions here -- those still live on each system's own page.
    # A left-border accent alternates between the site's two greens so
    # rows aren't visually identical blocks, and the "Explore" button
    # uses a light green fill to bring back color the compact list
    # lost when the hero photos were dropped.
    # --------------------------------------------------

    for i, system in enumerate(SYSTEMS):
        accent = GREEN_DARK if i % 2 == 0 else GREEN_MID
        card_key = f"{system['key']}_mobile_card"
        button_key = f"{system['key']}_mobile_button"

        st.markdown(
            f"""
            <style>
            div.st-key-{card_key} {{
                border-left: 4px solid {accent} !important;
                border-radius: 0.5rem !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        style_mobile_card_spacing(card_key)

        with st.container(border=True, key=card_key):
            # Subtitle and arrow now share one flex row instead of a
            # separate st.columns row -- the columns split was adding
            # its own layout overhead on top of the vertical-block gap,
            # which is what left that empty chunk of space above the
            # button. Single markdown call, single element-container.
            st.markdown(
                f"""
                <div style="font-size:0.95rem;font-weight:700;color:#343743;margin-bottom:0.15rem;">
                    {system['title']}
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-size:0.82rem;color:#747B8D;">
                        {system['teaser_short']}
                    </div>
                    <div style="color:#343743;font-size:0.95rem;">→</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            style_mobile_button(button_key, target="button")

            if st.button(
                "Explore",
                key=button_key,
                use_container_width=True
            ):
                st.switch_page(system["page"])

else:

    # --------------------------------------------------
    # DESKTOP -- unchanged full card layout, hero photo + title +
    # description + button, five across.
    # --------------------------------------------------

    columns = st.columns(5)

    for column, system in zip(columns, SYSTEMS):
        with column:
            with st.container(border=True):

                st.image(
                    str(IMAGES_DIR / system["image"]),
                    use_container_width=True
                )

                st.markdown(
                    f"""
                    <div style="
                        font-size: 1.15rem;
                        font-weight: 700;
                        line-height: 1.15;
                        min-height: 2.8rem;
                        margin-top: 0.8rem;
                        margin-bottom: 0.55rem;
                    ">
                        {system['title']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div style="
                        font-size: 0.92rem;
                        line-height: 1.45;
                        color: #6b6d75;
                        min-height: 5.0rem;
                        margin-bottom: 0.65rem;
                    ">
                        {system['teaser_long']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "Explore →",
                    key=f"{system['key']}_card",
                    use_container_width=True
                ):
                    st.switch_page(system["page"])


# ======================================================
# GATEWAY AT A GLANCE
# Compact homepage highlights. 2 columns on mobile so metric labels
# stay readable instead of squeezing four across a narrow screen.
# ======================================================

st.subheader("Gateway at a Glance")

METRICS = [
    ("Global TRUE Pursuit", "1st", "C&D + Operations"),
    ("Construction Diversion", "92.1%", "Materials diverted from landfill"),
    ("Tons Recovered", "7,945+", "Earthwork excluded"),
    ("Integrated Systems", "5", "Building-wide approach"),
]

if is_mobile:
    # st.columns collapses to a single stacked column below Streamlit's
    # mobile breakpoint no matter what count is passed in -- that's why
    # this was rendering as one full-width list instead of 2x2. A raw
    # CSS grid doesn't have that breakpoint behavior, so it holds a true
    # 2x2 layout regardless of viewport width.
    #
    # Built with NO blank lines between the per-metric blocks -- same
    # markdown HTML-block bug hit before: a blank line inside raw HTML
    # ends markdown's HTML recognition early, so everything after gets
    # reinterpreted as a code block instead of rendered markup.
    metric_blocks = []
    for label, value, note in METRICS:
        metric_blocks.append(
            f'<div><div style="font-size:0.85rem;color:#31333F;margin-bottom:0.1rem;">{label}</div>'
            f'<div style="font-size:1.9rem;font-weight:600;line-height:1.2;color:#111417;">{value}</div>'
            f'<div style="font-size:0.8rem;color:#747B8D;margin-top:0.1rem;">{note}</div></div>'
        )
    metrics_html = (
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:1.4rem 1rem;'>"
        + "".join(metric_blocks)
        + "</div>"
    )
    st.markdown(metrics_html, unsafe_allow_html=True)
else:
    metric_columns = st.columns(4, gap="small")
    for i, (label, value, note) in enumerate(METRICS):
        with metric_columns[i % len(metric_columns)]:
            st.metric(label=label, value=value)
            st.caption(note)


# ======================================================
# PROJECT RESOURCES
# ======================================================

st.divider()

st.header("Project Resources")

st.caption(
    "Access Gateway's core guidance, project documentation, and an expanding "
    "library of tools and resources."
)

if is_mobile:

    # --------------------------------------------------
    # MOBILE -- same compact row pattern as the system cards above,
    # including the alternating green left-border accent and the light
    # green button fill.
    # --------------------------------------------------

    RESOURCES = [
        {
            "title": "Zero Waste Operations Manual",
            "teaser": "Policies, procedures, and operating guidance",
            "action": "link",
            "url": MANUAL_URL,
            "key": "manual_mobile"
        },
        {
            "title": "Gateway Case Study",
            "teaser": "Implementation process and outcomes",
            "action": "page",
            "page": "pages/6_Resource_Library.py",
            "key": "case_study_mobile"
        },
        {
            "title": "Resource Library",
            "teaser": "Task-based guides and the product catalog",
            "action": "page",
            "page": "pages/6_Resource_Library.py",
            "key": "resource_library_mobile"
        },
    ]

    NEUTRAL_BORDER = "#D8DCE5"

    for i, resource in enumerate(RESOURCES):
        card_key = f"{resource['key']}_card"
        button_key = f"{resource['key']}_button"

        st.markdown(
            f"""
            <style>
            div.st-key-{card_key} {{
                border-left: 4px solid {NEUTRAL_BORDER} !important;
                border-radius: 0.5rem !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        style_mobile_card_spacing(card_key)

        with st.container(border=True, key=card_key):
            st.markdown(
                f"""
                <div style="font-size:0.95rem;font-weight:700;color:#343743;margin-bottom:0.15rem;">
                    {resource['title']}
                </div>
                <div style="font-size:0.82rem;color:#747B8D;margin-bottom:0.5rem;">
                    {resource['teaser']}
                </div>
                """,
                unsafe_allow_html=True
            )

            if resource["action"] == "link":
                # st.link_button doesn't accept a key= argument, so it's
                # wrapped in its own container(key=...) and styled as an
                # <a> element instead of a <button>.
                style_mobile_button(button_key, target="a")
                with st.container(key=button_key):
                    st.link_button("Open →", resource["url"], use_container_width=True)
            else:
                style_mobile_button(button_key, target="button")
                if st.button("Open →", key=button_key, use_container_width=True):
                    st.switch_page(resource["page"])

else:

    # --------------------------------------------------
    # DESKTOP -- unchanged 3-column resource cards.
    # --------------------------------------------------

    manual, case_study, resource_library = st.columns(3)

    with manual:
        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    font-size: 0.78rem;
                    font-weight: 700;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                    color: #747B8D;
                    margin-bottom: 0.65rem;
                ">
                    Implementation
                </div>
                <div style="
                    font-size: 1.25rem;
                    font-weight: 700;
                    line-height: 1.2;
                    color: #343743;
                    min-height: 3rem;
                    margin-bottom: 0.65rem;
                ">
                    Zero Waste Operations Manual
                </div>
                <div style="
                    font-size: 0.92rem;
                    line-height: 1.5;
                    color: #6b6d75;
                    min-height: 5.6rem;
                    margin-bottom: 0.75rem;
                ">
                    Explore the policies, procedures, signage, purchasing standards,
                    and operating guidance used to support Gateway's zero waste systems.
                </div>
                """,
                unsafe_allow_html=True
            )

            st.link_button(
                "Open Manual →",
                MANUAL_URL,
                use_container_width=True
            )

    with case_study:
        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    font-size: 0.78rem;
                    font-weight: 700;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                    color: #747B8D;
                    margin-bottom: 0.65rem;
                ">
                    Project Story
                </div>

                <div style="
                    font-size: 1.25rem;
                    font-weight: 700;
                    line-height: 1.2;
                    color: #343743;
                    min-height: 3rem;
                    margin-bottom: 0.65rem;
                ">
                    Gateway Case Study
                </div>

                <div style="
                    font-size: 0.92rem;
                    line-height: 1.5;
                    color: #6b6d75;
                    min-height: 5.6rem;
                    margin-bottom: 0.75rem;
                ">
                    Follow Gateway's implementation process, major outcomes, lessons
                    learned, and approach to TRUE Zero Waste certification.
                </div>
                """,
                unsafe_allow_html=True
            )

            # The case study itself lives on the Resource Library page
            # (it's a Google Slides deck, not a page file, so it can't be
            # a direct st.switch_page target).
            if st.button(
                "Read Case Study →",
                key="case_study_resource",
                use_container_width=True
            ):
                st.switch_page("pages/6_Resource_Library.py")

    with resource_library:
        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    font-size: 0.78rem;
                    font-weight: 700;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                    color: #747B8D;
                    margin-bottom: 0.65rem;
                ">
                    Tools & Updates
                </div>

                <div style="
                    font-size: 1.25rem;
                    font-weight: 700;
                    line-height: 1.2;
                    color: #343743;
                    min-height: 3rem;
                    margin-bottom: 0.65rem;
                ">
                    Resource Library
                </div>

                <div style="
                    font-size: 0.92rem;
                    line-height: 1.5;
                    color: #6b6d75;
                    min-height: 5.6rem;
                    margin-bottom: 0.75rem;
                ">
                    Task-based guides, the Approved Products Catalog, and training materials as they're added.
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Browse Resources →",
                key="resource_library",
                use_container_width=True
            ):
                # This page can become the expandable menu for all future resources.
                st.switch_page("pages/6_Resource_Library.py")