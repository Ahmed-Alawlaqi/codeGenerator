import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF for PDFs

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def load_file(uploaded_file):
    """Reads uploaded file content (supports .txt and .pdf)"""
    text = ""
    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
    return text

def get_response(description, language):
    """Generates code and explanation using OpenAI"""
    prompt = f"""
    You are an expert programmer. Write a {language} program based on the following description:
    {description}

    Provide:
    1. Complete code.
    2. A simple step-by-step explanation.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use GPT-4o for best results
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

def main():
    # Page configuration
    st.set_page_config(page_title="Code Generator", page_icon="⌨️")

    st.title("💻 Code Generator")
    st.warning("Generate clean, optimized code snippets in multiple languages!")
    st.divider()

    # API Key check
    if not api_key:
        st.error("⚠️ API Key is missing. Please set it in your .env file.")
        st.stop()

    # Language selection
    lang_option = ["C++", "Python", "C", "C#", "Java", "JavaScript"]
    option = st.selectbox("Select programming language", lang_option)

    # File upload OR text input
    st.subheader("Provide your problem description")
    uploaded_file = st.file_uploader("Upload a .txt or .pdf file (optional)", type=["txt", "pdf"])
    user_input = st.text_area("Or enter your description manually", "Print Hello World...")

    if uploaded_file:
        user_input = load_file(uploaded_file)

    # Submit button
    if st.button("Generate Code"):
        if user_input.strip() == "":
            st.error("Please enter a description of the code or upload a file.")
        else:
            with st.spinner("Generating your code..."):
                response = get_response(user_input, option)
                st.subheader("✅ Generated Code & Explanation:")
                st.markdown(response)

    # Contact Section
    st.write("---")
    contact_form = """
<style>
form {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
    margin: auto;
    font-family: Arial, sans-serif;
}
input, textarea {
    width: 100%;
    padding: 10px;
    margin-top: 8px;
    margin-bottom: 16px;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-size: 14px;
}
button {
    background-color: #4CAF50;
    color: white;
    padding: 12px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    width: 100%;
}
button:hover {
    background-color: #45a049;
}
h3 {
    text-align: center;
    color: #333;
}
</style>

<form action="https://formsubmit.co/ahm.m.awlaqi@gmail.com" method="POST">
    <h3>Contact Me</h3>
    <input type="hidden" name="_captcha" value="false">
    <input type="text" name="name" placeholder="Your name" required>
    <input type="email" name="email" placeholder="Your email" required>
    <textarea name="message" placeholder="Your Suggestions or Comments..." rows="5" required></textarea>
    <button type="submit">Send Message</button>
</form>
"""

    st.markdown(contact_form, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
