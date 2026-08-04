import streamlit as st
from streamlit_js_eval import streamlit_js_eval


def get_is_mobile():
    """
    Returns True/False for whether the viewport is mobile-width.

    Cached in st.session_state after the first successful detection --
    without this, every page navigation (Home -> Construction -> back
    to Home, etc.) would re-run the JS width check from scratch and
    re-trigger the loading skeleton, since each page load starts a
    fresh Streamlit script run. session_state persists across page
    navigation within the same browser session, so this only needs to
    resolve once.

    Returns None on the render before detection resolves (the very
    first page load of a session, before the cached value exists).
    Callers should render a loading skeleton and st.stop() when this
    returns None, then call it again on the automatic rerun that
    follows once streamlit_js_eval's real value comes back.

    Trade-off: since detection only runs once per session, resizing
    the browser or rotating a device mid-session won't update the
    cached value. Acceptable here since the goal is avoiding repeat
    skeleton flashes, not tracking live viewport changes.
    """
    if "is_mobile" in st.session_state:
        return st.session_state["is_mobile"]

    screen_width = streamlit_js_eval(js_expressions='window.parent.innerWidth', key='WIDTH')

    if screen_width is None:
        return None

    st.session_state["is_mobile"] = screen_width < 768
    return st.session_state["is_mobile"]