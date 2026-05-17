import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Business FAQ Chatbot", page_icon="")
st.title("Business FAQ Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Business Setup")
    business_name = st.text_input("Business Name", placeholder="e.g. Benjay Stores")
    business_info = st.text_area("Business Description", placeholder="what does your business do?")
    faqs = st.text_area("Your FAQs", placeholder="Q: What are your hours?\nA: We open 9am-6pm daily")
    st.caption("Fill the in to customize the chatbot for your business")

system_prompt = f"""You are a helpful customer support assistant for {business_name}.

About the business:
{business_info}

Known FAQs:
{faqs}

Answer the user's question based on the above information.
Be friendly, professional and concise.
If you don't know the answer, say so politely."""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages

        )
        reply = response.choices[0].message.content
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})



