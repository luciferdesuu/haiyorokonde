import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

persona_instructions = """
You are a storyteller whose task is to guide the user in their journey 
throughout a cyberpunk city that combines both magic and tech in 
tandem to each other. Offer help to the user in cryptic ways similar 
to a game of Dungeons and Dragons. Provide choices to the user throughout
the interaction. Ask the user for their identity before beginning the session.
"""



def get_gemini_response(prompt, persona_instructions):
    full_prompt = f"{persona_instructions}\n\nUser: {prompt}\nAssistant:"
    response = model.generate_content(full_prompt)
    return response.text

def main():
    st.title("Urban Fantasy RPG (better title pending)")
    st.image("lucifer.png", caption= "Welcome to my domain.")

    with st.sidebar:
        st.title("Options")
        st.radio("Genre", ["Horror", "Thriller", "Slice of Life"], index = 0)
        if st.button("Start New Chat", use_container_width=True):
            st.session_state.pop("chat_session", None)
            st.session_state.pop("messages", None)
            st.rerun()
        st.markdown("---")
        st.subheader("Current Session Memory")

    


        user_emoji = "💀"
        robot_img = "lucifer.png"

    
    initialize_session_state()

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar=robot_img):
                st.write(f"{message['content']}")
        else:
             with st.chat_message("user", avatar=user_emoji):
                st.write(f"{message['content']}")

    # Chat input
    if prompt := st.chat_input("Chat with the Storyteller."):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get Gemini response
        response = get_gemini_response(prompt, persona_instructions)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
