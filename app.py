import streamlit as st
import openai
from datetime import datetime

def generate_linkedin_content(topic, industry, expertise_areas=None, personal_story=None):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a LinkedIn content expert specializing in creating engaging, professional posts."},
                {"role": "user", "content": f"""
                Create a LinkedIn post about:
                Topic: {topic}
                Industry: {industry}
                Expertise: {expertise_areas if expertise_areas else 'General'}
                Personal Story: {personal_story if personal_story else 'None'}
                
                Include:
                1. Engaging hook
                2. Main insights
                3. Data points or examples
                4. Call to action
                5. 3-5 relevant hashtags
                """}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="LinkedIn Content Generator", layout="wide")

st.title("LinkedIn Content Generator")

# Sidebar for API key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Get your API key from https://platform.openai.com/api-keys")
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("""
    1. Enter your OpenAI API key
    2. Fill in the topic and industry
    3. Optionally add expertise areas and personal story
    4. Click Generate Content
    5. Copy and paste to LinkedIn!
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Details")
    topic = st.text_input("Topic", placeholder="e.g., Impact of AI on Healthcare")
    industry = st.text_input("Industry", placeholder="e.g., Healthcare Technology")
    expertise = st.text_input("Expertise Areas (optional)", placeholder="e.g., Machine Learning, Data Science")
    story = st.text_area("Personal Story (optional)", placeholder="Share a relevant experience...")
    
    if st.button("Generate Content", type="primary"):
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar")
        elif not topic or not industry:
            st.error("Please enter both topic and industry")
        else:
            with st.spinner("Generating content..."):
                openai.api_key = api_key
                content = generate_linkedin_content(topic, industry, expertise, story)
                st.session_state.content = content

with col2:
    st.subheader("Generated Content")
    if 'content' in st.session_state:
        st.text_area("Your LinkedIn Post", st.session_state.content, height=400)
        st.download_button(
            label="Download Content",
            data=st.session_state.content,
            file_name=f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Your LinkedIn Content Assistant")