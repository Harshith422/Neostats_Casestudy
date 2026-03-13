# LearnMate AI

LearnMate AI is an intelligent student learning assistant powered by Groq (Llama-3) and Tavily Web Search. It blends Retrieval-Augmented Generation (RAG) with real-time web search to provide direct, accurate answers from study materials or the internet.

## Prerequisites
- Python 3.9+ installed
- API Keys for Groq and Tavily (free tiers available)

## Installation

1. Clone or download this repository.
2. Open a terminal and navigate to the project directory:
   ```bash
   cd AI_UseCase
   ```

3. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure your API keys. Open the `.env` file in the root directory and paste your keys:
   ```env
   GROQ_API_KEY=your_groq_key_here
   TAVILY_API_KEY=your_tavily_key_here
   ```

## Running the Application

To start the LearnMate AI app locally, run the following command in your terminal:

```bash
python -m streamlit run app.py
```

The Streamlit server will start, and the application will automatically open in your default web browser (usually at `http://localhost:8501`).

## How to Use
1. **Upload Notes**: Use the sidebar to upload a PDF or TXT study file. The AI will read and index it.
2. **Select Subject**: Choose your subject from the dropdown.
3. **Adjust Mode & Level**: Toggle between 'Concise' and 'Detailed' modes, and set the difficulty level (Beginner/Intermediate/Advanced).
4. **Chat**: Ask questions! The AI will prioritize your uploaded notes. If it can't find the answer there, it will automatically search the web.
5. **Quiz**: Expand the "Quiz Me!" section to generate multiple-choice questions based on your notes.
