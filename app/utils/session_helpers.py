def ensure_session_state():
    import streamlit as st
    defaults = {
        "current_prompt": "",
        "prompt_input": "",
        "history": [],  # for undo
        "is_enhanced": False,
        "last_image_bytes": None,
        "last_prompt_for_image": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def push_prompt_history(st_session, prompt: str):
    if "history" not in st_session or st_session.history is None:
        st_session.history = []
    st_session.history.append(prompt)
    if not st_session.get("current_prompt"):
        st_session.current_prompt = prompt

def undo_last_enhancement(st_session) -> str:
    if "history" not in st_session or not st_session.history:
        return st_session.get("prompt_input", "")
    last = st_session.history.pop()
    st_session.current_prompt = last
    if not st_session.history:
        st_session.current_prompt = ""
    return last