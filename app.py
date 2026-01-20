"""
Streamlit UI for translation chatbot.
Simplified workflow: Upload → Select Language → Translate → Display
"""
import streamlit as st
import base64
from backend.ocr import extract_text_from_image
from backend.pipeline import TranslationPipeline
from backend.db import init_db, save_message, get_chat_history, get_all_chat_ids, delete_chat
from frontend.ui_components import render_sidebar

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="Translation Chatbot",
    page_icon="🌍",
    layout="wide"
)

def encode_image(uploaded_file) -> str:
    """Convert uploaded file to base64 data URI."""
    bytes_data = uploaded_file.read()
    base64_image = base64.b64encode(bytes_data).decode("utf-8")
    mime_type = uploaded_file.type
    return f"data:{mime_type};base64,{base64_image}"


def main():
    """Main application logic."""
    st.title("🌍 Translation Chatbot")
    st.markdown("Upload an image with text, select a target language, and get instant translation!")
    
    # Initialize session state
    if "active_chat_id" not in st.session_state:
        st.session_state.active_chat_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image with text",
            type=["png", "jpg", "jpeg"],
            help="Upload an image containing text to translate"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", width="stretch")
    
    with col2:
        st.subheader("🎯 Translation Settings")
        target_lang = st.selectbox(
            "Target Language",
            ["Spanish", "French", "German", "Chinese", "Japanese", "Hindi", "Arabic"],
            help="Select the language to translate to"
        )
        
        translate_button = st.button("🚀 Translate", type="primary", width="stretch")
    
    # Translation workflow
    if uploaded_file and translate_button:
        with st.spinner("Processing..."):
            try:
                # Step 1: Encode image
                image_b64 = encode_image(uploaded_file)
                
                # Step 2: OCR Extraction
                st.info("🔍 Extracting text from image...")
                ocr_result = extract_text_from_image(image_b64)
                
                if not ocr_result["has_text"]:
                    st.error("❌ No text detected in the image. Please upload a different image.")
                    return
                
                extracted_text = ocr_result["raw_text"]
                
                # Step 3: Translation via Pipeline
                st.info(f"🌍 Translating to {target_lang}...")
                pipeline = TranslationPipeline()
                translation_result = pipeline.translate(extracted_text, target_lang)
                
                if not translation_result["success"]:
                    st.error(f"❌ Translation failed: {translation_result.get('error', 'Unknown error')}")
                    return
                
                # Step 4: Display Results
                st.success("✅ Translation Complete!")
                
                st.markdown("---")
                
                # Display extracted text
                st.markdown("### 📝 Extracted Text")
                st.info(extracted_text)
                
                # Display detected language
                st.markdown("### 🔍 Detected Language")
                st.write(translation_result.get("detected_language", "Processing..."))
                
                # Display translation
                st.markdown(f"### 🌍 Translation ({target_lang})")
                st.success(translation_result["translated_text"])
                
                # Save to database
                if st.session_state.active_chat_id:
                    user_message = f"Image uploaded for translation to {target_lang}"
                    assistant_message = (
                        f"**Extracted Text:**\n{extracted_text}\n\n"
                        f"**Translation ({target_lang}):**\n{translation_result['translated_text']}"
                    )
                    save_message(st.session_state.active_chat_id, "user", user_message)
                    save_message(st.session_state.active_chat_id, "assistant", assistant_message)
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.exception(e)


if __name__ == "__main__":
    main()
