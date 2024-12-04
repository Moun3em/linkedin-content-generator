import streamlit as st
from services.openai_service import OpenAIService
import asyncio
from datetime import datetime

# Page config
st.set_page_config(
    page_title="LinkedIn Content Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
if 'openai_service' not in st.session_state:
    st.session_state.openai_service = OpenAIService()

# Sidebar
with st.sidebar:
    st.title("Content Settings")
    st.markdown("""Configure your content generation settings here.""")
    
    # API Configuration section
    st.header("API Configuration")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key"
    )

# Main content area
st.title("LinkedIn Content Generator")

# Input form
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Content Details")
    
    topic = st.text_input(
        "Topic",
        placeholder="e.g., The Future of AI in Healthcare"
    )
    
    industry = st.text_input(
        "Industry",
        placeholder="e.g., Healthcare Technology"
    )
    
    expertise = st.text_input(
        "Areas of Expertise (optional)",
        placeholder="e.g., Machine Learning, Data Science"
    )
    
    story = st.text_area(
        "Personal Story (optional)",
        placeholder="Share a relevant experience or insight..."
    )
    
    if st.button("Generate Content", type="primary"):
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar")
        elif not topic or not industry:
            st.error("Please enter both topic and industry")
        else:
            with st.spinner("Generating your LinkedIn content..."):
                result = asyncio.run(
                    st.session_state.openai_service.generate_content(
                        topic=topic,
                        industry=industry,
                        expertise=expertise,
                        story=story
                    )
                )
                
                if result["status"] == "success":
                    st.session_state.generated_content = result["content"]
                else:
                    st.error(f"Error generating content: {result['content']}")

with col2:
    st.subheader("Generated Content")
    if "generated_content" in st.session_state:
        content = st.session_state.generated_content
        st.text_area(
            "Your LinkedIn Post",
            content,
            height=400
        )
        
        # Download button
        st.download_button(
            label="Download Content",
            data=content,
            file_name=f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
        
        # Future integration buttons
        col3, col4, col5 = st.columns(3)
        with col3:
            st.button("Check Grammar", disabled=True)
        with col4:
            st.button("Generate Image", disabled=True)
        with col5:
            st.button("Save to Drive", disabled=True)

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ by Your LinkedIn Content Assistant"
)
