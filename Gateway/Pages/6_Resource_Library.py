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
# Fill in wherever the files actually end up hosted (relative "app/static/..."
# path if you set up static serving, or a direct hosted URL). Whatever you
# use, make sure it serves the raw PDF, not a preview wrapper, or the
# #page= jump on the task links below won't work.
# ======================================================

MANUAL_URL = "app/static/Gateway_Zero_Waste_Operations_Manual.pdf"
CASE_STUDY_URL = "app/static/Gateway_Case_Study.pdf"
CATALOG_URL = "https://docs.google.com/spreadsheets/d/1A8FVGTV1aYEEU8FSmAIqXaVte6zZQoTVcCfQZ-hz0IU/edit?gid=1487214576#gid=1487214576"

# Page numbers inside the Manual PDF that each task card should jump to.
# (Confirmed against the Manual TOC: Kitchen Reusables p.14, Catering
# Policies p.15, Event Guidelines p.16, Café Operations p.17.)
MANUAL_PAGE_KITCHEN = 14
MANUAL_PAGE_CATERING = 15
MANUAL_PAGE_EVENTS = 16
MANUAL_PAGE_CAFE = 17


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
            f"{MANUAL_URL}#page={MANUAL_PAGE_EVENTS}",
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
            f"{MANUAL_URL}#page={MANUAL_PAGE_KITCHEN}",
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
            f"{MANUAL_URL}#page={MANUAL_PAGE_CATERING}",
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
            f"{MANUAL_URL}#page={MANUAL_PAGE_CAFE}",
            use_container_width=True
        )


# ======================================================
# FOOTER NOTE
# ======================================================

st.write("")

st.caption(
    "Note: task-based links jump to a specific page inside the Manual PDF "
    "and work in most browsers' built-in PDF viewers. If a link opens the "
    "file from the beginning instead of jumping to the right page, it "
    "opened outside the native viewer — the file itself is unaffected."
)