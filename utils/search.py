import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import TAVILY_API_KEY

def search_web(query: str, max_results: int = 4) -> tuple[str, list[str]]:
    try:
        if not TAVILY_API_KEY or TAVILY_API_KEY == "YOUR_TAVILY_API_KEY_HERE":
            return _fallback_no_search(), []

        from tavily import TavilyClient
        client = TavilyClient(api_key=TAVILY_API_KEY)

        results = client.search(
            query=query,
            search_depth="basic",
            max_results=max_results,
            include_answer=True,
        )

        context_parts = []
        sources = []

        if results.get("answer"):
            context_parts.append(f"Quick Answer: {results['answer']}")

        for item in results.get("results", []):
            title   = item.get("title", "")
            content = item.get("content", "")
            url     = item.get("url", "")

            if content:
                context_parts.append(f"[{title}]\n{content}")
            if url:
                sources.append(url)

        context_text = "\n\n---\n\n".join(context_parts)
        return context_text, sources

    except ImportError:
        return "Web search is not available.", []
    except Exception as e:
        return f"Web search encountered an error: {str(e)}", []

def _fallback_no_search() -> str:
    return "No web search API key is configured. Answering from the built-in knowledge only."
