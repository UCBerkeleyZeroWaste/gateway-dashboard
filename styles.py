import streamlit as st
from streamlit_js_eval import streamlit_js_eval


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
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    _apply_sidebar_menu_label()


def _apply_sidebar_menu_label():
    # The collapsed-sidebar toggle is a Material Symbols icon font glyph
    # ("keyboard_double_arrow_right") rendered inside the app's own
    # toolbar, not a separately-labeled control -- and its wrapper
    # data-testid (stIconMaterial) is shared by every icon in the app,
    # so it can't be targeted by a stable CSS selector alone. This finds
    # the icon by its actual text, walks up to its real <button>
    # ancestor, and adds a "Menu" label + green styling directly.
    #
    # Runs via streamlit_js_eval rather than components.html -- the two
    # create iframes with different sandbox permissions, and on
    # Streamlit Community Cloud the components.html version silently
    # failed to reach window.parent.document even though this exact
    # access pattern already works via streamlit_js_eval elsewhere in
    # this app (get_is_mobile in device.py). Reusing the mechanism
    # that's proven to work in production instead of the one that
    # isn't. A MutationObserver re-applies the label whenever Streamlit
    # re-renders the toolbar (e.g. sidebar collapse/expand), since the
    # button gets removed and recreated rather than just hidden.
    streamlit_js_eval(
        js_expressions="""
        (function() {
            function labelSidebarToggle() {
                const doc = window.parent.document;
                const icons = doc.querySelectorAll('span[data-testid="stIconMaterial"]');
                icons.forEach(function(icon) {
                    if (icon.textContent.trim() === 'keyboard_double_arrow_right') {
                        const btn = icon.closest('button');
                        if (btn && !btn.querySelector('.gw-menu-label')) {
                            btn.style.backgroundColor = '#3A8E3C';
                            btn.style.borderRadius = '0.4rem';
                            btn.style.padding = '0.35rem 0.7rem';
                            btn.style.display = 'flex';
                            btn.style.alignItems = 'center';
                            btn.style.gap = '0.35rem';
                            icon.style.color = '#FFFFFF';

                            const label = doc.createElement('span');
                            label.textContent = 'Menu';
                            label.className = 'gw-menu-label';
                            label.style.color = '#FFFFFF';
                            label.style.fontWeight = '600';
                            label.style.fontSize = '0.85rem';
                            label.style.fontFamily = 'inherit';
                            btn.appendChild(label);
                        }
                    }
                });
            }

            labelSidebarToggle();
            const observer = new MutationObserver(labelSidebarToggle);
            observer.observe(window.parent.document.body, {
                childList: true,
                subtree: true
            });

            return true;
        })()
        """,
        key="SIDEBAR_MENU_LABEL"
    )
