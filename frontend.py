import streamlit as st
from app import query_rag

st.set_page_config(page_title="SQL Assistant", page_icon="🧠", layout="centered")

st.title("🧠 SQL Assistant (RAG POC)")
st.markdown(
    """
    This is a simple proof-of-concept SQL assistant that reads `.docx` documentation
    and generates SQL queries using OpenAI and LangChain.
    """
)

query = st.text_input("Enter your SQL-related question:")

if st.button("Generate SQL"):
    if query.strip():
        with st.spinner("Thinking..."):
            try:
                response = query_rag(query)
                st.markdown("### 💬 Response")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")

st.markdown("---")
st.caption("Built with LangChain, Streamlit, and OpenAI.")
