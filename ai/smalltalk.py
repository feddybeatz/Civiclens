"""Instant replies for greetings, thanks and help. Returns None if not smalltalk,
so the normal pipeline handles the message. Never states facts about budgets."""
import re

GREET = {"hi", "hello", "hey", "good morning", "good afternoon", "good evening",
         "habari", "hujambo", "jambo", "mambo", "sasa", "niaje", "salaam", "shikamoo"}
THANKS = {"thanks", "thank you", "thanks a lot", "thank you very much",
          "asante", "asante sana", "shukran"}
HELP = {"help", "what can you do", "how does this work", "who are you",
        "what is this", "msaada", "unaweza kufanya nini"}

HELP_TEXT = ("I answer questions about Kenyan government budget documents and, where "
             "recorded, parliamentary votes. Every answer shows the document, page and "
             "source. If the records don't answer, I'll say so instead of guessing. "
             "Try: \"How much was allocated to health in 2026/27?\"")

def _norm(t):
    t = re.sub(r"[^\w\s]", "", t.lower()).strip()
    return re.sub(r"\s+", " ", t)

def reply(text):
    n = _norm(text)
    if n in GREET:
        return "Hello! / Habari! Ask me about the budget documents. " + HELP_TEXT
    if n in THANKS:
        return "You're welcome! / Karibu! Ask another question any time."
    if n in HELP:
        return HELP_TEXT
    return None

def smalltalk(text):
    """Name used by ui/chat.py."""
    return reply(text)
