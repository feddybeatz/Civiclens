from ai.retrieval import retrieve
from ai.ai_engine import ask_gemma

q = "What is the Mwananchi Guide about?"
passages = retrieve(q)
for p in passages:
    print(p["document"], "page", p["page"])
print(ask_gemma(q, passages, passages[0]["document"] if passages else ""))
