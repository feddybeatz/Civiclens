import sys
from ai.retrieval import retrieve
from ai.ai_engine import ask_gemma

q = " ".join(sys.argv[1:])
passages = retrieve(q)
print("RETRIEVED:", [(p["document"], p["page"]) for p in passages])
r = ask_gemma(q, passages, passages[0]["document"] if passages else "")
for k in ("status", "document", "page", "answer", "excerpt", "limitations"):
    print(f"{k.upper()}: {r[k]}")
