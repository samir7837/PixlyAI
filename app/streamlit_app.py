import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import os
from io import BytesIO

import streamlit as st
from PIL import Image
from dotenv import load_dotenv


load_dotenv()


from app.services.pollinations import generate_image_bytes
from app.services.enhancer import enhance_prompt
from app.utils.downloader import prepare_image_download_bytes
from app.utils.session_helpers import ensure_session_state, push_prompt_history, undo_last_enhancement


def _style():
    st.markdown(
        """
        <style>
        .btn-row {margin-top: 8px; margin-bottom: 8px;}
        .small-muted {color: #6c757d; font-size: 0.95em;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def _display_image_bytes_safely(image_bytes):
    
    try:
        img = Image.open(BytesIO(image_bytes))
        try:
            st.image(img, use_container_width=True)
        except TypeError:
            try:
                st.image(img, use_column_width=True)
            except Exception:
                st.image(img)
    except Exception:
        try:
            st.image(image_bytes)
        except Exception:
            st.warning("Could not display generated content as an image.")



def _improve_callback():
    original = st.session_state.get("prompt_input", "")
    if not original or not original.strip():
        st.session_state["_improve_error"] = "Please enter a short description to improve first."
        return

    try:
        enhanced = enhance_prompt(original)
    except Exception as e:
        st.session_state["_improve_error"] = f"Enhancer failed: {e}"
        return

    if not enhanced or enhanced.strip() == original.strip():
        st.session_state["_improve_info"] = "Enhancer did not change your description."
        return

    
    push_prompt_history(st.session_state, original)
    
    st.session_state["prompt_input"] = enhanced
    st.session_state["current_prompt"] = enhanced
    st.session_state["is_enhanced"] = True
    st.session_state["_improve_info"] = "Description improved."



def _undo_callback():
   
    undone = undo_last_enhancement(st.session_state)
    
    st.session_state["prompt_input"] = undone
    st.session_state["current_prompt"] = undone
    st.session_state["is_enhanced"] = False
   
    st.session_state["_undo_info"] = "Reverted to previous description."


def main():
    st.set_page_config(page_title="PixlyAI ⭐", layout="centered")
    _style()

    ensure_session_state()

    st.title("PixlyAI ⭐")
    st.write("Describe what you want, click Improve to make it better, then Create image.")

   
    if "prompt_input" not in st.session_state:
        st.session_state["prompt_input"] = st.session_state.get("current_prompt", "")

    
    st.text_area(
        "Describe what you want (e.g., 'a black cat sitting on a windowsill at sunrise')",
        value=st.session_state.get("prompt_input", ""),
        placeholder="Type a short description of the image you want",
        height=140,
        key="prompt_input",
    )

   
    if st.session_state.get("_improve_error"):
        st.error(st.session_state.get("_improve_error"))
        del st.session_state["_improve_error"]

    if st.session_state.get("_improve_info"):
      
        st.info(st.session_state.get("_improve_info"))
        del st.session_state["_improve_info"]

    if st.session_state.get("_undo_info"):
    
        st.success(st.session_state.get("_undo_info"))
        del st.session_state["_undo_info"]

   
    cols = st.columns([1, 1, 1])
    with cols[0]:

        st.button("🎨 Improve description", key="enhance_btn", on_click=_improve_callback)
    with cols[1]:
        if st.button("🖼️ Create image", key="imagine_btn"):
            prompt_to_use = st.session_state.get("prompt_input", "").strip()
            if not prompt_to_use:
                st.warning("Please type a description before creating an image.")
            else:
                with st.spinner("Creating image..."):
                    try:
                        image_bytes = generate_image_bytes(prompt_to_use)
                        st.session_state.last_image_bytes = image_bytes
                        st.session_state.last_prompt_for_image = prompt_to_use
                    except Exception as e:
                        st.error(f"Image creation failed: {e}")
    with cols[2]:
        
        st.button("↶ Undo improvement", key="undo_enhance_btn", on_click=_undo_callback)

    
    if st.session_state.get("last_image_bytes"):
        st.subheader("Your image")
        _display_image_bytes_safely(st.session_state["last_image_bytes"])

        rr, dd = st.columns([1, 1])
        with rr:
            if st.button("🔁 Create another", key="remagine_btn"):
                prompt_to_use = st.session_state.get("last_prompt_for_image") or st.session_state.get("prompt_input", "")
                if not prompt_to_use:
                    st.warning("No prompt available to regenerate.")
                else:
                    with st.spinner("Creating another image..."):
                        try:
                            new_bytes = generate_image_bytes(prompt_to_use)
                            st.session_state.last_image_bytes = new_bytes
                            st.session_state.last_prompt_for_image = prompt_to_use
                        except Exception as e:
                            st.error(f"Failed to create another image: {e}")
        with dd:
            download_bytes, filename = prepare_image_download_bytes(
                st.session_state.last_image_bytes, st.session_state.get("last_prompt_for_image", "")
            )
            st.download_button(label="⬇️ Download image", data=download_bytes, file_name=filename, mime="image/png")

    
    st.markdown("")
    st.markdown(
        "<div class='small-muted'>Tips: Describe the main subject first, then a few details about style, mood or lighting. "
        "Example: 'a portrait of a fox in neon city, cinematic lighting, film grain'.</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()