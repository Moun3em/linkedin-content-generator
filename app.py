import streamlit as st
import webbrowser
from services.openai_service import OpenAIService
from services.canva_service import CanvaService
from services.google_service import GoogleDocsService
from datetime import datetime
import asyncio

# Page config
st.set_page_config(page_title="LinkedIn Content Generator", layout="wide")

# Initialize services
if 'services' not in st.session_state:
    st.session_state.services = {
        'openai': OpenAIService(),
        'canva': CanvaService(),
        'google': GoogleDocsService()
    }

# Sidebar
with st.sidebar:
    st.title("Content Settings")
    
    # API Keys section
    st.header("API Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    # Help section
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("""
    1. Enter your API key
    2. Fill in content details
    3. Generate content
    4. Create visuals with Canva
    5. Check grammar
    6. Save to Google Docs
    """)

# Main content area
st.title("LinkedIn Content Generator")

# Input form
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Content Details")
    topic = st.text_input("Topic", placeholder="e.g., AI in Healthcare")
    industry = st.text_input("Industry", placeholder="e.g., Healthcare Technology")
    expertise = st.text_input("Areas of Expertise (optional)")
    story = st.text_area("Personal Story (optional)")
    
    if st.button("Generate Content", type="primary"):
        if not api_key:
            st.error("Please enter your OpenAI API key")
        elif not topic or not industry:
            st.error("Please enter both topic and industry")
        else:
            with st.spinner("Generating content..."):
                result = asyncio.run(st.session_state.services['openai'].generate_content(
                    topic=topic,
                    industry=industry,
                    expertise=expertise,
                    story=story
                ))
                
                if result["status"] == "success":
                    st.session_state.generated_content = result["content"]
                    # Generate Canva image
                    image_result = asyncio.run(st.session_state.services['canva'].generate_image(
                        topic=topic,
                        industry=industry
                    ))
                    if 'error' not in image_result:
                        st.session_state.image_url = image_result.get('url')
                else:
                    st.error(f"Error: {result['content']}")

with col2:
    st.subheader("Generated Content")
    if "generated_content" in st.session_state:
        content = st.session_state.generated_content
        st.text_area("Your LinkedIn Post", content, height=300)
        
        # Image preview
        if "image_url" in st.session_state:
            st.image(st.session_state.image_url, caption="Generated Visual")
        
        # Action buttons
        col3, col4, col5 = st.columns(3)
        
        with col3:
            if st.button("Check Grammar"):
                # Open Grammarly in new tab
                webbrowser.open("https://app.grammarly.com/")
        
        with col4:
            if st.button("Edit in Canva"):
                if "image_url" in st.session_state:
                    webbrowser.open(st.session_state.image_url)
                else:
                    st.warning("Generate content first to create visuals")
        
        with col5:
            if st.button("Save to Google Docs"):
                with st.spinner("Saving to Google Docs..."):
                    doc_url = asyncio.run(st.session_state.services['google'].create_document(
                        content=content,
                        topic=topic
                    ))
                    if not doc_url.startswith("Error"):
                        st.success(f"Saved! [Open Document]({doc_url})")
                    else:
                        st.error(doc_url)
        
        # Download button
        st.download_button(
            label="Download Content",
            data=content,
            file_name=f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Your LinkedIn Content Assistant")
