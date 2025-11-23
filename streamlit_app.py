import streamlit as st
import requests
import json

# Watson Orchestrate Configuration
ORCHESTRATE_API_KEY = "9BoWYXsiNAwF1V7ljv8nN5c8lxg7Dq4SFBy-8Axvc2jX"
ORCHESTRATE_URL = "https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/21192705-1d5a-4bfe-b8f5-11699516e970"

st.set_page_config(page_title="HR Agent", page_icon="🤖", layout="centered")

# Header
st.title("🤖 HR Agent")
st.markdown("Ask any question to the HR agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to send request to Watson Orchestrate
def send_to_orchestrate(user_message):
    headers = {
        "Authorization": f"Bearer {ORCHESTRATE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "text": user_message
        }
    }
    
    try:
        response = requests.post(
            f"{ORCHESTRATE_URL}/v1/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("output", {}).get("text", "Sorry, no response received")
        else:
            return f"API Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Connection Error: {str(e)}"

# Message input field
if prompt := st.chat_input("Write your question..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from Watson Orchestrate
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = send_to_orchestrate(prompt)
            st.markdown(response)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.markdown("""
    ### 📝 Information
    
    **Connected to:**
    - IBM Watson Orchestrate
    - Instance: watsonx-Hackathon
    
    **Example questions:**
    - What documents are needed for hiring?
    - How does onboarding work?
    - What is the vacation schedule?
    """)
    
    # Show message count
    st.caption(f"💬 Messages in chat: {len(st.session_state.messages)}")

# Footer
st.divider()
st.caption("🤖 HR Agent | Powered by IBM Watson Orchestrate")
