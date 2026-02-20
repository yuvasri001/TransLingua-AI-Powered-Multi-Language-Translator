import streamlit as st
try:
    import google.generativeai as genai
except Exception:
    genai = None
    st.error("Missing 'google-generative-ai' package. Install it with: pip install google-generative-ai")
    st.stop()

# NOTE: Do not hardcode API keys. Allow end-users to paste their key in the sidebar
# and keep it only in the Streamlit session state.
def init_model_with_key(key: str):
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-2.5-flash")

# Sidebar: accept API key from end user (kept only in session)
st.sidebar.header("Google API Key")
key_input = st.sidebar.text_input("Paste Google API Key (keeps in session only)", type="password")
if st.sidebar.button("Set API Key"):
    if key_input and key_input.strip():
        st.session_state["api_key"] = key_input.strip()
        try:
            st.session_state["model"] = init_model_with_key(st.session_state["api_key"])
            st.sidebar.success("API key set (stored in session for this run)")
        except Exception as e:
            st.sidebar.error(f"Failed to initialize model with provided key: {e}")
    else:
        st.sidebar.warning("Please paste a non-empty API key before clicking Set API Key.")

# Try to initialize model if API key already in session (e.g., on rerun)
model = None
if "model" in st.session_state:
    model = st.session_state["model"]
elif "api_key" in st.session_state:
    try:
        st.session_state["model"] = init_model_with_key(st.session_state["api_key"])
        model = st.session_state["model"]
    except Exception:
        model = None

# Translation function
def translate_text(model_obj, text, source_language, target_language):
    if model_obj is None:
        raise RuntimeError("API key not configured. Paste your Google API key in the sidebar and click 'Set API Key'.")
    prompt = f"Translate the following text from {source_language} to {target_language}: {text}"
    try:
        response = model_obj.generate_content(prompt)
        return response.text
    except Exception as e:
        raise

# Streamlit UI
st.set_page_config(page_title="AI-Powered Language Translator", page_icon="🌍")
st.header("🌍 AI-Powered Language Translator")

text = st.text_area("📝 Enter text to translate:")
source_language = st.selectbox(
    "🌐 Select source language:",
    ["English", "Telugu", "Hindi", "Spanish", "French", "German", "Chinese"]
)

target_language = st.selectbox(
    "🎯 Select target language:",
    ["English", "Telugu", "Hindi", "Spanish", "French", "German", "Chinese"]
)

if st.button("🔁 Translate"):
    if not text:
        st.warning("⚠️ Please enter text to translate")
    else:
        if model is None:
            st.error("No API key configured. Paste your Google API key in the sidebar and click 'Set API Key'.")
        else:
            try:
                translated_text = translate_text(model, text, source_language, target_language)
                st.subheader("📘 Translated Text:")
                st.write(translated_text)
            except Exception as e:
                st.error(f"Translation failed: {e}")
