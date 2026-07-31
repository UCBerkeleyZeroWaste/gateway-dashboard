import streamlit as st


def apply_global_style():
    st.markdown(
        """
        <style>

        /* Reduce unused space around the page */
        .block-container {
            max-width: 1500px;
            padding-top: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
            padding-bottom: 3rem;
        }

        /* Green sidebar */
        section[data-testid="stSidebar"] {
            background-color: #3A8E3C;
        }

        /* White sidebar text */
        section[data-testid="stSidebar"] * {
            color: #FFFFFF;
        }

        /* Style all Streamlit buttons */
        div[data-testid="stButton"] button {
            width: 100%;
            border-radius: 9px;
            font-weight: 600;
            padding: 0.45rem 0.6rem;
        }

        /* Slightly soften image corners */
        div[data-testid="stImage"] img {
            border-radius: 10px;
        }
        
        /* Active page in sidebar */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li[data-testid="stSidebarNavLink"] a[aria-current="page"] {
            background-color: rgba(255,255,255,0.18);
            border-radius: 10px;
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"] {
    padding: 0.8rem 0.9rem !important;

        </style>
        """,
        unsafe_allow_html=True
    )