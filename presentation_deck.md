# LearnMate AI – Case Study Presentation Outline

*This document contains the exact content you should place into your 6-slide PowerPoint (PPT) presentation for the NeoStats AI Engineer Case Study.*

---

## Slide 1: Title Slide
**Title:** LearnMate AI – Your Intelligent Study Partner
**Subtitle:** NeoStats AI Engineer Case Study Submission
**Presenter:** [Your Name]
**Date:** [Today's Date]

---

## Slide 2: Use Case Objective
**Headline:** The Problem & Our Mission

**Bullet Points:**
- **The Challenge:** Students struggle to quickly extract key concepts from long, complex study materials (PDFs/TXTs) and spend too much time searching the web for clear explanations.
- **The Objective:** Build an intelligent, context-aware AI assistant that acts as a personalized tutor.
- **The Solution:** **LearnMate AI** — A dual-engine Retrieval-Augmented Generation (RAG) chatbot that perfectly blends a student's private study notes with real-time web knowledge.

---

## Slide 3: How I Approached the Problem
**Headline:** Architecture & Strategy

**Bullet Points:**
- **Zero Plagiarism / 100% Custom Architecture:** Built a modular Python backend from scratch without relying on code generation tools like Copilot.
- **Robustness First:** Integrated comprehensive `try/except` error handling across all modules so the app never crashes during a study session.
- **Secure Configuration:** Separated all API keys into a hidden `.env` file to strictly adhere to security best practices and prevent GitHub leaks.
- **Dynamic Fallback:** Used a fast LLM (Groq Llama-3) as the core engine, with an intelligent fallback to Tavily Search when local documents lack the answer.

---

## Slide 4: The Solution & Technical Stack
**Headline:** Under the Hood of LearnMate AI

**Bullet Points:**
- **Frontend UI:** Streamlit (Custom CSS for a clean, modern, dark-mode learning environment).
- **Core LLM Engine:** Groq (Llama-3-8B-Instant) for blazing-fast inference without rate limit crashes.
- **Vector Database (Memory):** FAISS + SentenceTransformers (`all-MiniLM-L6-v2`) for local RAG embedding.
- **Document Processing:** PyMuPDF (`fitz`) for highly accurate text extraction from PDFs.
- **Live Knowledge:** Tavily Search API to pull real-time educational data from the web.

---

## Slide 5: Features Implemented
**Headline:** Empowering the Student

**Bullet Points:**
- **Smart RAG Pipeline:** Upload any PDF/TXT notes; the AI prioritizes answering directly from your syllabus.
- **Automated Web Fallback:** If the answer isn't in your notes, the AI automatically searches the web and cites its sources.
- **Dynamic Response Modes:** Toggle between *Concise* (for quick revision before an exam) and *Detailed* (for deep, step-by-step learning).
- **Adaptive Difficulty:** Set explanations to *Beginner*, *Intermediate*, or *Advanced* to match your academic level.
- **"Quiz Me!" Generator:** Automatically generates multiple-choice questions (MCQs) from your uploaded notes to test your understanding.
- **Multi-Subject Session Memory:** Switch between subjects (Math, History, etc.) without losing chat history.

---

## Slide 6: Challenges Faced & Links
**Headline:** Development Hurdles & Final Product

**Challenges:**
- **LLM Rate Limits:** Initially faced severe rate-limiting and quota exhaustion (`429 RESOURCE_EXHAUSTED`) with Google Gemini's free tier. 
- **The Fix:** Completely decoupled the architecture from Gemini and pivoted exclusively to Groq's Llama-3, providing a much faster and more stable experience.
- **Context Injection:** Writing complex prompt templates that seamlessly blend RAG context, web sources, and the student's tone preferences into a single coherent prompt.

**Links:**
- **GitHub Repository:** [Insert your GitHub Repo Link Here]
- **Live Demo (Streamlit Cloud):** [Insert your Streamlit Cloud Link Here]
