import streamlit as st
import aiohttp
import asyncio
from typing import Dict, Any

# Set page config to wide mode
st.set_page_config(layout="wide")


st.title("Multi-Model AI Chat Interface")

# Initialize session state for responses if they don't exist
if 'responses' not in st.session_state:
    st.session_state.responses = {
        'gpt': '',
        'gemini': '',
        'claude': ''
    }

# Create text input for user prompt
user_prompt = st.text_input("Enter your prompt:", key="prompt_input")

# Display responses in columns
col1, col2, col3 = st.columns(3)

# @st.cache_data
async def call_model_api(session: aiohttp.ClientSession, endpoint: str, prompt: str) -> Dict[str, Any]:
    """Make async API call to model endpoint"""
    try:
        async with session.post(
            f"http://localhost:8000/{endpoint}",
            json={"prompt": prompt}
        ) as response:
            return await response.json()
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

async def get_all_responses(prompt: str):
    """Get responses from all models concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [
            call_model_api(session, "gpt", prompt),
            call_model_api(session, "gemini", prompt),
            call_model_api(session, "claude", prompt)
        ]
        responses = await asyncio.gather(*tasks)
        
        # Update session state with responses
        st.session_state.responses['gpt'] = responses[0].get('response', 'Error getting response')
        with col1:
            st.subheader("GPT Response")
            st.write(st.session_state.responses['gpt'])
        
        st.session_state.responses['gemini'] = responses[1].get('response', 'Error getting response')
        with col2:
            st.subheader("Gemini Response")
            st.write(st.session_state.responses['gemini'])

        st.session_state.responses['claude'] = responses[2].get('response', 'Error getting response')
        with col3:
            st.subheader("Claude Response")
            st.write(st.session_state.responses['claude'])

# Button to trigger the API calls
if st.button("Generate Responses") and user_prompt:
    # Run async calls using asyncio
    asyncio.run(get_all_responses(user_prompt))


# with col1:
#     st.subheader("GPT Response")
#     st.write(st.session_state.responses['gpt'])

# with col2:
#     st.subheader("Gemini Response")
#     st.write(st.session_state.responses['gemini'])

# with col3:
#     st.subheader("Claude Response")
#     st.write(st.session_state.responses['claude'])
