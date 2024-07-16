from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load gemeni pro model and get response
model = genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question, stream=True)
    return response

## initialize the streamlit app
st.set_page_config(page_title="Gemini Pro Chat", page_icon=":robot:")
st.header("Gemini Pro LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [] 

input=st.text_input("Input: ", key="input")
# Submit button
submit=st.button("Ask the question")

if submit and input:
    response=get_gemini_response(input)
    # Add user query and response to session chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is:")
    # As the Stream=True, we can get the response in chunks
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Gemini Pro", chunk.text))

st.subheader("Chat History")
for role,text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")