import os
from typing import Iterable, List, Dict
from ..core.config import settings

PROVIDER = os.getenv("LLM_PROVIDER", "openai")

prompt_tpl = (
    "You are an expert tutor. Answer the user's question using ONLY the given contexts. "
    "Cite sources as [#] with their titles. If unknown, say you don't know.\n\n"
    "Question: {q}\n\nContexts:\n{ctx}\n\nAnswer:"
)

def _format_ctx(contexts: List[Dict]):
    lines = []
    for i, c in enumerate(contexts, 1):
        title = c.get("title") or c.get("url")
        snippet = (c.get("content_text") or "")[:500]
        lines.append(f"[{i}] {title}\n{snippet}")
    return "\n\n".join(lines)


def stream_answer(q: str, contexts: List[Dict]) -> Iterable[str]:
    prompt = prompt_tpl.format(q=q, ctx=_format_ctx(contexts))
    if PROVIDER == "openai":
        import openai  # type: ignore
        openai.api_key = settings.OPENAI_API_KEY
        resp = openai.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role":"user","content": prompt}],
            stream=True,
            temperature=0.3,
        )
        for ev in resp:
            delta = ev.choices[0].delta.content or ""
            if delta:
                yield delta
    else:  # ollama fallback
        import requests, json
        url = f"{os.getenv('OLLAMA_HOST','http://ollama:11434')}/api/generate"
        with requests.post(url, json={"model": os.getenv("OLLAMA_MODEL","llama3.1:8b"), "prompt": prompt, "stream": True}, stream=True) as r:
            for line in r.iter_lines():
                if not line: continue
                try:
                    data = json.loads(line)
                    chunk = data.get("response", "")
                    if chunk:
                        yield chunk
                except Exception:
                    continue
