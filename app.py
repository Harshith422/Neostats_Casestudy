import streamlit as st
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from models.llm import get_llm
from utils.rag import process_uploaded_file, get_rag_context
from utils.search import search_web
from utils.prompts import (
    get_system_prompt,
    get_rag_prompt,
    get_web_search_prompt,
    get_quiz_prompt,
    get_plain_prompt,
)
from config.config import APP_TITLE, APP_SUBTITLE, MAX_MESSAGES

st.set_page_config(
    page_title=f"{APP_TITLE} - Study Partner",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #f0f0f0; }
    [data-testid="stSidebar"] { background: rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.1); }
    .learnmate-header { text-align: center; padding: 1.5rem 0 0.5rem 0; }
    .learnmate-header h1 {
        font-size: 2.6rem; font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .learnmate-header p { color: #94a3b8; font-size: 1rem; margin-top: 0.3rem; }
    .status-banner { background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 10px; padding: 0.6rem 1rem; color: #c4b5fd; margin-bottom: 0.8rem; }
    .web-banner { background: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.3); border-radius: 10px; padding: 0.6rem 1rem; color: #6ee7b7; margin-bottom: 0.8rem; }
    [data-testid="stChatMessage"] { background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; margin-bottom: 0.5rem; padding: 0.5rem; }
    .stButton > button { background: linear-gradient(90deg, #7c3aed, #4f46e5); color: white; border: none; border-radius: 8px; font-weight: 600; }
    .quiz-box { background: rgba(167, 139, 250, 0.08); border: 1px solid rgba(167, 139, 250, 0.3); border-radius: 12px; padding: 1.2rem; margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

def init_session():
    defaults = {
        "messages":        {},
        "faiss_index":     {},
        "doc_chunks":      {},
        "doc_loaded":      {},
        "current_subject": "General",
        "response_mode":   "Detailed",
        "difficulty":      "Intermediate",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

def render_sidebar():
    with st.sidebar:
        st.markdown(f"## {APP_TITLE}")
        st.markdown(f"*{APP_SUBTITLE}*")
        st.divider()

        st.markdown("### Subject")
        subjects = ["General", "Mathematics", "Physics", "Chemistry", "Biology", "History", "Computer Science", "Economics", "Custom"]
        subject = st.selectbox("Choose your subject:", subjects, index=subjects.index(st.session_state.current_subject) if st.session_state.current_subject in subjects else 0, label_visibility="collapsed")
        st.session_state.current_subject = subject

        for d in ["messages", "faiss_index", "doc_chunks", "doc_loaded"]:
            if subject not in st.session_state[d]:
                st.session_state[d][subject] = ([] if d == "messages" else False if d == "doc_loaded" else None)

        st.divider()

        st.markdown("### Upload Study Material")
        uploaded = st.file_uploader("Upload PDF or TXT notes", type=["pdf", "txt"], key=f"upload_{subject}", help="Upload notes to provide context.")

        if uploaded:
            with st.spinner("Processing documents..."):
                try:
                    index, chunks, _ = process_uploaded_file(uploaded)
                    st.session_state.faiss_index[subject] = index
                    st.session_state.doc_chunks[subject]  = chunks
                    st.session_state.doc_loaded[subject]  = True
                    st.success(f"Indexed {len(chunks)} sections.")
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")

        if st.session_state.doc_loaded.get(subject):
            chunk_count = len(st.session_state.doc_chunks.get(subject, []))
            st.markdown(f'<div class="status-banner"><b>{chunk_count} sections</b> imported</div>', unsafe_allow_html=True)

        st.divider()

        st.markdown("### Response Mode")
        mode = st.radio("Response style:", ["Concise", "Detailed"], index=0 if st.session_state.response_mode == "Concise" else 1, horizontal=True, label_visibility="collapsed")
        st.session_state.response_mode = mode

        st.divider()

        st.markdown("### Difficulty Level")
        difficulty = st.select_slider("Explanation level:", options=["Beginner", "Intermediate", "Advanced"], value=st.session_state.difficulty, label_visibility="collapsed")
        st.session_state.difficulty = difficulty

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.messages[subject] = []
                st.rerun()
        with col2:
            if st.button("Remove Notes", use_container_width=True):
                st.session_state.faiss_index[subject] = None
                st.session_state.doc_chunks[subject]  = None
                st.session_state.doc_loaded[subject]  = False
                st.rerun()

def render_quiz_section(subject: str, llm):
    st.markdown("---")
    with st.expander("Quiz Me! - Test your knowledge", expanded=False):
        if not st.session_state.doc_loaded.get(subject):
            st.info("Upload study material first to generate a quiz.")
            return

        col1, col2 = st.columns([2, 1])
        with col1:
            num_q = st.slider("Number of questions:", 2, 8, 4, key="quiz_num")
        with col2:
            generate = st.button("Create Quiz", use_container_width=True, key="gen_quiz")

        if generate:
            with st.spinner("Generating quiz..."):
                try:
                    chunks = st.session_state.doc_chunks[subject]
                    sample_text = " ".join(chunks[:10])
                    system_prompt = get_system_prompt(st.session_state.response_mode, st.session_state.difficulty, subject)
                    quiz_prompt = get_quiz_prompt(sample_text, num_q)
                    messages = [SystemMessage(content=system_prompt), HumanMessage(content=quiz_prompt)]
                    response = llm.invoke(messages)
                    st.markdown(f'<div class="quiz-box">\n\n{response.content}\n\n</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Quiz error: {str(e)}")

def get_response(query: str, subject: str, llm) -> tuple[str, str]:
    system_prompt = get_system_prompt(st.session_state.response_mode, st.session_state.difficulty, subject)
    history = st.session_state.messages.get(subject, [])

    formatted = [SystemMessage(content=system_prompt)]
    for msg in history[-(MAX_MESSAGES):]:
        if msg["role"] == "user":
            formatted.append(HumanMessage(content=msg["content"]))
        else:
            formatted.append(AIMessage(content=msg["content"]))

    source_label = "Knowledge Base"

    try:
        rag_used = False
        if st.session_state.doc_loaded.get(subject) and st.session_state.faiss_index.get(subject):
            context, found = get_rag_context(query, st.session_state.faiss_index[subject], st.session_state.doc_chunks[subject])
            if found and context:
                formatted.append(HumanMessage(content=get_rag_prompt(query, context)))
                response = llm.invoke(formatted)
                return response.content, "Study Notes (RAG)"
            rag_used = True

        web_trigger = (rag_used or not st.session_state.doc_loaded.get(subject) or any(kw in query.lower() for kw in ["search", "latest", "recent", "news"]))

        if web_trigger:
            web_context, sources = search_web(query)
            if web_context and "not available" not in web_context:
                formatted.append(HumanMessage(content=get_web_search_prompt(query, web_context, sources)))
                response = llm.invoke(formatted)
                source_lbl = "Web Search"
                if sources:
                    source_lbl += f" - {sources[0]}"
                return response.content, source_lbl

        formatted.append(HumanMessage(content=get_plain_prompt(query)))
        response = llm.invoke(formatted)
        return response.content, source_label

    except Exception as e:
        return f"Error encountered: {str(e)}", "System Error"

def render_chat(subject: str, llm):
    st.markdown(f"""
    <div class="learnmate-header">
        <h1>LearnMate AI</h1>
        <p>{APP_SUBTITLE} | Subject: <b>{subject}</b> | Mode: <b>{st.session_state.response_mode}</b> | Level: <b>{st.session_state.difficulty}</b></p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.doc_loaded.get(subject):
        st.markdown('<div class="status-banner">Study notes active. Answers will prioritize uploaded material.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="web-banner">No notes uploaded. Providing general answers or web context.</div>', unsafe_allow_html=True)

    render_quiz_section(subject, llm)
    st.markdown("---")

    for msg in st.session_state.messages.get(subject, []):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("source"):
                st.caption(msg["source"])

    user_input = st.chat_input(f"Ask about {subject}...", key=f"chat_{subject}")

    if user_input:
        if subject not in st.session_state.messages:
            st.session_state.messages[subject] = []
        st.session_state.messages[subject].append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:
                    answer, source = get_response(user_input, subject, llm)
                    st.markdown(answer)
                    st.caption(source)
                    st.session_state.messages[subject].append({"role": "assistant", "content": answer, "source": source})
                except Exception as e:
                    err = f"Execution Error: {str(e)}"
                    st.error(err)
                    st.session_state.messages[subject].append({"role": "assistant", "content": err, "source": ""})

def main():
    render_sidebar()
    subject = st.session_state.current_subject

    if "llm" not in st.session_state:
        try:
            st.session_state.llm = get_llm()
        except Exception as e:
            st.error(f"Cannot initialize AI model: {str(e)}")
            st.stop()

    render_chat(subject, st.session_state.llm)

if __name__ == "__main__":
    main()