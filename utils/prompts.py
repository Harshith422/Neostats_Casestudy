from typing import List

def get_system_prompt(response_mode: str, difficulty: str, subject: str) -> str:
    mode_instruction = (
        "Give short, concise answers - maximum 3-4 sentences or 4 bullet points. "
        "Skip lengthy explanations."
        if response_mode == "Concise"
        else
        "Give detailed, thorough explanations. Use examples and "
        "step-by-step breakdowns to help the student understand."
    )

    level_instruction = {
        "Beginner":     "Use simple language. Avoid jargon.",
        "Intermediate": "Use standard academic language. Explain technical terms briefly.",
        "Advanced":     "Use precise technical language. Assume strong subject knowledge.",
    }.get(difficulty, "Use standard academic language.")

    return f"""
You are an intelligent, helpful, and highly accurate student learning assistant.
Your goal is to help the student understand concepts clearly, step-by-step.
Adapt your teaching style to the student's preferences.

Current Topic/Subject: {subject}
Response Depth: {response_mode}
Difficulty Level: {difficulty}

Always be encouraging and format your responses clearly using Markdown.

Response style: {mode_instruction}
Language level: {level_instruction}

Rules:
- If provided with study material context, base your answer on it first.
- If provided with web search results, summarize them clearly and cite sources.
- If you genuinely do not know something, say so honestly rather than guessing.
- Always stay on topic.
"""

def get_rag_prompt(query: str, context: str) -> str:
    return f"""The following is relevant content from the student's uploaded study material:

--- STUDY MATERIAL CONTEXT ---
{context}
--- END CONTEXT ---

Based on this study material, please answer the student's question:
{query}

Make sure your answer is grounded in the provided material. If something is not covered,
mention that and supplement with your own knowledge."""

def get_web_search_prompt(query: str, web_context: str, sources: List[str]) -> str:
    source_list = "\n".join(f"- {s}" for s in sources[:3]) if sources else "- No sources available"

    return f"""I searched the web and found the following information to help answer your question:

--- WEB SEARCH RESULTS ---
{web_context}
--- END WEB RESULTS ---

Sources:
{source_list}

Based on these search results, please answer the student's question:
{query}

Summarize the key points clearly and mention which source the information came from."""

def get_quiz_prompt(context: str, num_questions: int = 4) -> str:
    return f"""You are creating a short quiz based on this study material:

--- STUDY MATERIAL ---
{context[:3000]}  
--- END MATERIAL ---

Generate EXACTLY {num_questions} multiple-choice questions (MCQs) based on the material above.

Format each question like this:
Q1. [Question text]
   A) [Option]
   B) [Option]  
   C) [Option]
   D) [Option]
Answer: [Correct letter]
Explanation: [Brief reason why this is correct]

Make questions test understanding, not just memorization."""

def get_plain_prompt(query: str) -> str:
    return f"""Please answer the following student question using your knowledge:

{query}

Be helpful, accurate, and keep your response appropriate to the configured style."""
