import os
import openai
import streamlit as st


openai.api_key = st.secrets["api_key"]



def load_file():
    text = ""
    data_dir = os.path.join(os.getcwd(),"data")
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(data_dir,filename),"r") as f:
                text += f.read()
    return text


def get_response(text,option):
    prompt = f"""
        You are expert of coding.You'll be given a coding problem. You will code the problem
        with '''' {option} '''' language, with simple explain of the processe.
        text: '''' {text}''''
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content']



def main():
    #page configration
    st.set_page_config(
        page_title="codeGenrator",
        page_icon="⌨️",
        
    )

    #Header
    st.title("Code Generator")
    st.warning("Our app empowers you to generate clean, optimized code snippets with just a few clicks ")
    st.divider()
    
    #check if the user want to upload a text or pdf file
    lang_option=["C++","Python","C","C#","Java","JavaScript"]
    option = st.selectbox("Select programming language",lang_option)

    #Create a text area for the user to input text
    if option:
        user_input = st.text_area("Description of the code to generate","Print Hello world...")

        #Create a submit button 
        if st.button("Submit") and user_input != "":
            #call get_response function and print the response
            response = get_response(user_input,option)
            # st.subheader("Code:")
            st.markdown(f">{response}")
        else:
            st.error("Please Enter Text.")

    #---contact----
    with st.container():
        st.write("---")
        st.subheader("Contact With Me")
        st.write("##")
        contact_form = """
        <form action="https://formsubmit.co/ahm.m.awlaqi@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" Placeholder = "Your name" required>
            <input type="email" name="email" Placeholder = "Your email" required>
            <textarea name="message" placeholder="Your Suggestions or Comments..."></textarea>
            <button type="submit">Send</button>
        </form>
        """
        st.markdown(contact_form,unsafe_allow_html=True)
        st.divider()
        st.write("[Twitter](https://twitter.com/AhmedAwlaqi)")


if __name__ == "__main__":
    main()