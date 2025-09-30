from google import genai
from google.genai import types
import streamlit as st
import os

# --- 1. Configuration and Initialization ---

# Use Streamlit secrets for your API key
try:
    # This automatically looks for the key in st.secrets["GEMINI_API_KEY"]
    client = genai.Client()
    MODEL = "gemini-2.5-flash"
except Exception:
    st.error("Gemini client failed to initialize. Please ensure your API key is set in Streamlit Secrets.")
    st.stop()

# Define the persona instructions (based on your screenshot)
PERSONA_INSTRUCTIONS = (
    "You are an Urban Fantasy RPG Game Master. Your responses should be creative, "
    "engaging, and guide the user through a fantasy story. Keep your responses concise."
)

def initialize_chat_session():
    """Initializes a new Gemini chat object with the persona instructions."""
    if "chat_session" not in st.session_state:
        # Configuration to pass the system instruction
        config = types.GenerateContentConfig(
            system_instruction=PERSONA_INSTRUCTIONS
        )
        # Create and store the actual Gemini Chat object
        st.session_state.chat_session = client.chats.create(
            model=MODEL,
            config=config
        )

# Call the initialization function
initialize_chat_session()
chat_session = st.session_state.chat_session


# --- 2. Sidebar Content (Memory Display) ---

with st.sidebar:
    st.title("Conversation History")
    
    # Button to start a new chat (clears the session state key)
    if st.button("Start New Adventure", use_container_width=True):
        st.session_state.pop("chat_session", None)
        st.rerun()

    st.markdown("---")
    st.subheader("Last Turns")
    
    # Access and display the history from the Gemini Chat object
    try:
        chat_history = chat_session.get_history()
        
        # Display each message in the sidebar
        for message in chat_history:
            # Safely get the text content
            text_part = next((p.text for p in message.parts if p.text), "...")
            
            # Truncate for cleaner sidebar display
            display_text = text_part.split('\n')[0][:45].strip() + "..."
            
            role_emoji = "👤" if message.role == "user" else "🤖"
            st.markdown(f"**{role_emoji} {message.role.capitalize()}:** {display_text}")
            
    except Exception as e:
        # This should no longer fire, but good for safety
        st.error(f"Error loading history: {e}")


# --- 3. Main Chat Area ---

st.title("Urban Fantasy RPG (Urban Dungeon)")

# Display app image and caption (based on your screenshot)
st.image("Lucifer.png", caption="Welcome to my domain. (Art by me!)") 

st.markdown("---")

# Display all messages from history on the main page
for message in chat_session.get_history():
    role = "user" if message.role == "user" else "assistant"
    # The message history is a list of parts, we only care about text for display
    text_part = next((p.text for p in message.parts if p.text), "")
    
    if text_part:
        with st.chat_message(role):
            st.markdown(text_part)

# Handle New Input
if prompt := st.chat_input("What do you do next, adventurer?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send message via the chat object (this maintains the memory!)
    try:
        with st.spinner("The GM is thinking..."):
            response = chat_session.send_message(prompt)

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
        # Rerunning ensures the sidebar updates immediately
        st.rerun()
            
    except Exception as e:
        st.error(f"An error occurred: {e}")