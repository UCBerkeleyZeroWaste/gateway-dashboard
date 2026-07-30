import streamlit as st

from styles import apply_global_style


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

MANUAL_URL = "app/static/Gateway_Zero_Waste_Operations_Manual.pdf"


# ======================================================
# PAGE INTRODUCTION
# ======================================================

st.title("Gateway Sustainability Systems")

st.write(
    "An interactive guide to the sustainability systems of UC Berkeley's Gateway, the College of Computing and Data Science. Gateway houses the first new college added to UC Berkeley for over 50 years, with construction reaching completion as of June 2026."
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

construction, purchasing, reuse, recovery, building = st.columns(5)


# ------------------------------------------------------
# CONSTRUCTION SYSTEMS
# ------------------------------------------------------

with construction:
    with st.container(border=True):

        st.image(
            "Images/Construction.jpg",
            use_container_width=True
        )

        st.markdown(
            """
            <div style="
                font-size: 1.15rem;
                font-weight: 700;
                line-height: 1.15;
                min-height: 2.8rem;
                margin-top: 0.8rem;
                margin-bottom: 0.55rem;
            ">
                Construction Systems
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                font-size: 0.92rem;
                line-height: 1.45;
                color: #6b6d75;
                min-height: 5.0rem;
                margin-bottom: 0.65rem;
            ">
                Reducing waste before the building even opened.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Explore →",
            key="construction_card",
            use_container_width=True
        ):
            st.switch_page("pages/1_Construction.py")


# ------------------------------------------------------
# CIRCULAR PURCHASING
# ------------------------------------------------------

with purchasing:
    with st.container(border=True):

        st.image(
            "Images/Circular_Purchasing.jpg",
            use_container_width=True
        )

        st.markdown(
            """
            <div style="
                font-size: 1.15rem;
                font-weight: 700;
                line-height: 1.15;
                min-height: 2.8rem;
                margin-top: 0.8rem;
                margin-bottom: 0.55rem;
            ">
                Circular Purchasing
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                font-size: 0.92rem;
                line-height: 1.45;
                color: #6b6d75;
                height: 5.0rem;
                margin-bottom: 0.65rem;
            ">
                Standardizing purchasing and refill systems to prevent waste.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Explore →",
            key="purchasing_card",
            use_container_width=True
        ):
            st.switch_page("pages/2_Circular_Purchasing.py")


# ------------------------------------------------------
# REUSE SYSTEMS
# ------------------------------------------------------

with reuse:
    with st.container(border=True):

        st.image(
            "Images/Reuse.jpg",
            use_container_width=True
        )

        st.markdown(
            """
            <div style="
                font-size: 1.15rem;
                font-weight: 700;
                line-height: 1.15;
                min-height: 2.8rem;
                margin-top: 0.8rem;
                margin-bottom: 0.55rem;
            ">
                Reuse Systems
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                font-size: 0.92rem;
                line-height: 1.45;
                color: #6b6d75;
                min-height: 5.0rem;
                margin-bottom: 0.65rem;
            ">
                Making reuse the easiest option every day.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Explore →",
            key="reuse_card",
            use_container_width=True
        ):
            st.switch_page("pages/3_Reuse.py")


# ------------------------------------------------------
# RECOVERY SYSTEMS
# ------------------------------------------------------

with recovery:
    with st.container(border=True):

        st.image(
            "Images/Recovery.jpg",
            use_container_width=True
        )

        st.markdown(
            """
            <div style="
                font-size: 1.15rem;
                font-weight: 700;
                line-height: 1.15;
                min-height: 2.8rem;
                margin-top: 0.8rem;
                margin-bottom: 0.55rem;
            ">
                Recovery Systems
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                font-size: 0.92rem;
                line-height: 1.45;
                color: #6b6d75;
                min-height: 5.0rem;
                margin-bottom: 0.65rem;
            ">
                Capturing materials that cannot be prevented or reused.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Explore →",
            key="recovery_card",
            use_container_width=True
        ):
            st.switch_page("pages/4_Recovery.py")


# ------------------------------------------------------
# BUILDING SYSTEMS
# ------------------------------------------------------

with building:
    with st.container(border=True):

        st.image(
            "Images/Building.jpg",
            use_container_width=True
        )

        st.markdown(
            """
            <div style="
                font-size: 1.15rem;
                font-weight: 700;
                line-height: 1.15;
                min-height: 2.8rem;
                margin-top: 0.8rem;
                margin-bottom: 0.55rem;
            ">
                Building Systems
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                font-size: 0.92rem;
                line-height: 1.45;
                color: #6b6d75;
                min-height: 5.0rem;
                margin-bottom: 0.65rem;
            ">
                Reducing resource use through efficient building systems.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Explore →",
            key="building_card",
            use_container_width=True
        ):
            st.switch_page("pages/5_Building_Systems.py")


# ======================================================
# GATEWAY AT A GLANCE
# Compact homepage highlights
# ======================================================

st.subheader("Gateway at a Glance")

metric_1, metric_2, metric_3, metric_4 = st.columns(
    4,
    gap="small"
)

with metric_1:
    st.metric(
        label="Global TRUE Pursuit",
        value="1st"
    )
    st.caption("C&D + Operations")

with metric_2:
    st.metric(
        label="Construction Diversion",
        value="92.1%"
    )
    st.caption("Materials diverted from landfill")

with metric_3:
    st.metric(
        label="Tons Recovered",
        value="7,945+"
    )
    st.caption("Earthwork excluded")

with metric_4:
    st.metric(
        label="Integrated Systems",
        value="5"
    )
    st.caption("Building-wide approach")


# ======================================================
# PROJECT RESOURCES
# ======================================================

st.divider()

st.header("Project Resources")

st.caption(
    "Access Gateway's core guidance, project documentation, and an expanding "
    "library of tools and resources."
)

manual, case_study, resource_library = st.columns(3)


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

# ------------------------------------------------------
# GATEWAY CASE STUDY
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

        if st.button(
            "Read Case Study →",
            key="case_study_resource",
            use_container_width=True
        ):
            # Update this path when the case study page is ready.
            st.switch_page("pages/7_Gateway_Case_Study.pdf")


# ------------------------------------------------------
# PROJECT RESOURCE LIBRARY
# ------------------------------------------------------

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