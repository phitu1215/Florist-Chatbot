import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os

st.title("🌸 Flora - Your Friendly Florist Assistant")

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Fast & cheap; or "llama-4-scout-..." for better quality
    temperature=0.7,
    max_tokens=500,
)

# System prompt tailored for florist
system_prompt = """You are Flora, a warm, knowledgeable, and enthusiastic florist assistant at "Bloom Haven" flower shop.
You help customers with:
- Bouquet & arrangement recommendations
- Occasion ideas (birthday, anniversary, sympathy, wedding, etc.)
- Pricing, delivery, care instructions
- Seasonal flowers and availability
- Personalized suggestions based on budget, colors, preferences

Be friendly, professional, and helpful. Suggest upsells tastefully. If unsure about stock, say you'll check with the team."""

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about flowers, bouquets, or arrangements..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        messages = [SystemMessage(content=system_prompt)] + \
                   [HumanMessage(content=m["content"]) if m["role"] == "user" else SystemMessage(content=m["content"]) 
                    for m in st.session_state.messages]
        
        response = llm.invoke(messages)
        st.markdown(response.content)
    
    st.session_state.messages.append({"role": "assistant", "content": response.content})