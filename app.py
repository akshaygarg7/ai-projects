import streamlit as st

from src.agents.chat.main import invoke as chat


# 1. Page Configuration
st.set_page_config(page_title="Multi-Module Chatbot", page_icon="💬", layout="wide")
st.title("💬 Multi-Module Assistant")

# 2. Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Sidebar Configuration
st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown("Select a module method to process your chat prompts.")

# Map radio choices to your actual Python functions
module_mapping = {
    "chat": chat,
}

selected_mode = st.sidebar.radio(
    "Choose Agent:",
    options=list(module_mapping.keys())
)

# Optional sidebar button to clear chat
if st.sidebar.button("Clear Conversation History", type="primary"):
    st.session_state.messages = []
    st.rerun()

# 4. Display Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle New User Input
if user_prompt := st.chat_input("Type your message here..."):
    
    # Render user message instantly
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Save user message to history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Fetch the corresponding backend method dynamically based on the radio button
    active_method = module_mapping[selected_mode]
    
    # Generate response using the selected method
    with st.chat_message("assistant"):
        with st.spinner(f"Running {selected_mode}..."):
            response = active_method(user_prompt)
            st.markdown(response)
            
    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
