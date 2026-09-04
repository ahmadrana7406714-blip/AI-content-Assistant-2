import os
import streamlit as st
from groq import Groq

# Set page title and icon
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags for any platform in seconds.")

# Sidebar for API Key input (allows user or deployed environment key)
groq_api_key = st.sidebar.text_input(
    "Groq API Key", 
    type="password", 
    value=os.environ.get("GROQ_API_KEY", ""),
    help="Get a free key at https://console.groq.com/keys"
)

# Input Controls
col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox(
        "Platform", 
        ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "TikTok"]
    )
    content_type = st.selectbox(
        "Content Type", 
        ["Educational Post", "Promotional / Sales", "Storytelling", "Quick Tip", "Industry News"]
    )
    tone = st.selectbox(
        "Tone", 
        ["Professional", "Casual & Friendly", "Energetic & Hype", "Witty & Humor", "Informative"]
    )

with col2:
    topic = st.text_input("Topic / Main Subject", placeholder="e.g., Remote Work Productivity")
    target_audience = st.text_input("Target Audience", placeholder="e.g., Software Engineers, Marketers")

# Additional context or instructions
extra_context = st.text_area("Extra Details / Constraints (Optional)", placeholder="e.g., Mention our tool 'FlowApp', keep under 200 words.")

# Generation Logic
if st.button("🚀 Generate Content", type="primary", use_container_width=True):
    if not groq_api_key:
        st.error("Please enter a valid Groq API Key in the sidebar or setup Streamlit Secrets.")
    elif not topic or not target_audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=groq_api_key)

            # Constructing a structured prompt
            prompt = f"""
            You are an expert social media copywriter. Generate a complete post based on these requirements:
            
            - Platform: {platform}
            - Content Type: {content_type}
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}
            - Additional Notes: {extra_context if extra_context else 'None'}
            
            Structure the output clearly into 3 sections:
            1. **Main Post Content / Caption** (Tailored for {platform}'s optimal format and formatting options like line breaks)
            2. **Call to Action (CTA)**
            3. **Relevant Hashtags** (5-10 strategic hashtags)
            """

            with st.spinner("Generating content using Groq..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": "You are a professional social media content assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )

            generated_text = response.choices[0].message.content

            st.success("Content Generated Successfully!")
            st.markdown("---")
            st.markdown(generated_text)
            
            # Download option for generated content
            st.download_button(
                label="📥 Download Content as Text",
                data=generated_text,
                file_name=f"{platform.lower().replace(' ', '_')}_post.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
