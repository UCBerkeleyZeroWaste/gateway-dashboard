import streamlit as st

from styles import apply_global_style


# ======================================================
# PAGE CONFIGURATION
# This must be the first Streamlit command in the file.
# ======================================================

st.set_page_config(
    page_title="Gateway Resource Library",
    page_icon="♻️",
    layout="wide"
)

apply_global_style()


# ======================================================
# CONFIG — edit these
# ------------------------------------------------------
# The Manual now lives as a Google Slides deck (not a hosted PDF) --
# MANUAL_URL points to the "present" view, and each MANUAL_PAGE_*
# variable is that section's actual Slides slide ID rather than a page
# number. Keep these in sync with Reuse Systems, Recovery Systems, and
# Circular Purchasing if the deck's slide order ever changes.
#
# CASE_STUDY_URL is unchanged -- it's a separate document that hasn't
# been moved to Slides, so it's still pointed at the static-hosted PDF
# path. If that link is unreliable the same way the Manual's was,
# it likely needs the same static-serving fix (or its own move to
# Slides/Drive) separately.
# ======================================================

MANUAL_URL = "https://docs.google.com/presentation/d/1j3IVyxEG0aGZXlMy2ydaw6Dh-32Yhf_N/present"
CASE_STUDY_URL = "app/static/Gateway_Case_Study.pdf"
CATALOG_URL = "https://docs.google.com/spreadsheets/d/1A8FVGTV1aYEEU8FSmAIqXaVte6zZQoTVcCfQZ-hz0IU/edit?gid=1487214576#gid=1487214576"

# Slide IDs inside the Manual deck that each task card should jump to.
MANUAL_PAGE_KITCHEN = "g3f21e15226c_0_146"
MANUAL_PAGE_CATERING = "g3f21e15226c_0_206"
MANUAL_PAGE_EVENTS = "g3f21e15226c_0_249"
MANUAL_PAGE_CAFE = "g3f21e15226c_0_309"


# ======================================================
# PAGE INTRODUCTION
# ======================================================

st.title("Resource Library")

st.write(
    "Read the full Zero Waste Operations Manual, or jump straight to the "
    "section that matches what you're doing right now."
)


# ======================================================
# THE SOURCE DOCUMENTS
# ======================================================

st.header("The Source Documents")

st.caption(
    "The full picture, whenever you need it."
)

manual, case_study, catalog = st.columns(3)


# ------------------------------------------------------
# ZERO WASTE OPERATIONS MANUAL
# ------------------------------------------------------

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
                Full Guide
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
                The complete move-in guide — every policy, system, and
                sorting rule in one place.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "View Document →",
            MANUAL_URL,
            use_container_width=True
        )


# ------------------------------------------------------
# CASE STUDY
# ------------------------------------------------------

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
                Case Study
            </div>

            <div style="
                font-size: 0.92rem;
                line-height: 1.5;
                color: #6b6d75;
                min-height: 5.6rem;
                margin-bottom: 0.75rem;
            ">
                How Gateway became the first building in the world pursuing
                TRUE for both construction and operations.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "View Document →",
            CASE_STUDY_URL,
            use_container_width=True
        )


# ------------------------------------------------------
# APPROVED PRODUCTS CATALOG
# ------------------------------------------------------

with catalog:
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
                Quick Reference
            </div>

            <div style="
                font-size: 1.25rem;
                font-weight: 700;
                line-height: 1.2;
                color: #343743;
                min-height: 3rem;
                margin-bottom: 0.65rem;
            ">
                Approved Products Catalog
            </div>

            <div style="
                font-size: 0.92rem;
                line-height: 1.5;
                color: #6b6d75;
                min-height: 5.6rem;
                margin-bottom: 0.75rem;
            ">
                Look up what's already approved before you order anything new.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "View Document →",
            CATALOG_URL,
            use_container_width=True
        )


# ======================================================
# FIND WHAT YOU NEED
# ======================================================

st.divider()

st.header("Find What You Need")

st.caption(
    "Jump straight to the section that matches your situation."
)

events, kitchen = st.columns(2)


# ------------------------------------------------------
# EVENT GUIDELINES
# ------------------------------------------------------

with events:
    with st.container(border=True):

        st.markdown(
            """
            <div style="
                font-size: 1.15rem;
                font-weight: 700;
                line-height: 1.2;
                color: #343743;
                min-height: 2.8rem;
                margin-bottom: 0.65rem;
            ">
                Event Guidelines
            </div>

            <div style="
                font-size: 0.92rem;
                line-height: 1.5;
                color: #6b6d75;
                min-height: 3.5rem;
                margin-bottom: 0.75rem;
            ">
                Waste stations, giveaways, decor — what every Gateway event
                needs to include.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "Jump to This Section →",
            f"{MANUAL_URL}#slide=id.{MANUAL_PAGE_EVENTS}",
            use_container_width=True
        )


# ------------------------------------------------------
# KITCHEN REUSABLES
# ------------------------------------------------------

with kitchen:
    with st.container(border=True):

        st.markdown(
            """
            <div style="
                font-size: 1.15rem;
                font-weight: 700;
                line-height: 1.2;
                color: #343743;
                min-height: 2.8rem;
                margin-bottom: 0.65rem;
            ">
                Kitchen Reusables
            </div>

            <div style="
                font-size: 0.92rem;
                line-height: 1.5;
                color: #6b6d75;
                min-height: 3.5rem;
                margin-bottom: 0.75rem;
            ">
                How the reuse-first dishware system works, and what to do
                when it's not feasible.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "Jump to This Section →",
            f"{MANUAL_URL}#slide=id.{MANUAL_PAGE_KITCHEN}",
            use_container_width=True
        )

st.write("")

catering, cafe = st.columns(2)


# ------------------------------------------------------
# CATERING POLICIES
# ------------------------------------------------------

with catering:
    with st.container(border=True):

        st.markdown(
            """
            <div style="
                font-size: 1.15rem;
                font-weight: 700;
                line-height: 1.2;
                color: #343743;
                min-height: 2.8rem;
                margin-bottom: 0.65rem;
            ">
                Catering Policies
            </div>

            <div style="
                font-size: 0.92rem;
                line-height: 1.5;
                color: #6b6d75;
                min-height: 3.5rem;
                margin-bottom: 0.75rem;
            ">
                Required serviceware, approved materials, and what's
                off-limits.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "Jump to This Section →",
            f"{MANUAL_URL}#slide=id.{MANUAL_PAGE_CATERING}",
            use_container_width=True
        )


# ------------------------------------------------------
# CAFÉ OPERATIONS
# ------------------------------------------------------

with cafe:
    with st.container(border=True):

        st.markdown(
            """
            <div style="
                font-size: 1.15rem;
                font-weight: 700;
                line-height: 1.2;
                color: #343743;
                min-height: 2.8rem;
                margin-bottom: 0.65rem;
            ">
                Café Operations
            </div>

            <div style="
                font-size: 0.92rem;
                line-height: 1.5;
                color: #6b6d75;
                min-height: 3.5rem;
                margin-bottom: 0.75rem;
            ">
                Dispatch Goods, returns, and how to sort café waste
                correctly.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "Jump to This Section →",
            f"{MANUAL_URL}#slide=id.{MANUAL_PAGE_CAFE}",
            use_container_width=True
        )


# ======================================================
# FOOTER NOTE
# ======================================================

st.write("")

st.caption(
    "Note: task-based links jump to a specific slide inside the Manual "
    "Google Slides deck. If a link opens the deck from the beginning "
    "instead of jumping to the right slide, the slide ID may be out of "
    "date -- re-copy it from that slide's address bar in Slides and "
    "update the corresponding MANUAL_PAGE_* variable above."
)
