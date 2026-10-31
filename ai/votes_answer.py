"""Answers 'who voted no/yes on X' from the votes table, by code. No model, no guessing."""
import re
from ai import votes

_TOPIC = re.compile(r"\b(mp|mps|member|members|senator|senators|bill|hansard|parliament|assembly|division)\b", re.I)
_VOTE = re.compile(r"\b(voted|vote|votes|ayes|noes|against|division)\b", re.I)
_NOES = re.compile(r"\b(voted (no|against)|noes|nays?|against|opposed)\b", re.I)
_AYES = re.compile(r"\b(voted (yes|aye|for)|ayes|in favou?r|supported)\b", re.I)

NOT_FOUND = ("I couldn't find a matching vote record. I won't guess. Try the bill's official "
             "title, or check the Hansard archive: "
             "https://parliament.go.ke/the-national-assembly/house-business/hansard")

def is_vote_question(q):
    return bool(_VOTE.search(q) and _TOPIC.search(q))

def direction(q):
    if _NOES.search(q):
        return "noes"
    if _AYES.search(q):
        return "ayes"
    return None

def _source(d):
    bits = [f"Hansard {d['hansard_file']}" if d["hansard_file"] else "Hansard"]
    if d["page"]:
        bits.append(f"page {d['page']}")
    s = ", ".join(bits)
    return s + (f" - {d['source_url']}" if d["source_url"] else "")

def answer(question, con):
    side = direction(question)
    if side is None:
        return "Do you want the MPs who voted Aye (yes) or No (noes)?"
    divs = votes.search_divisions(con, question)
    if not divs:
        return NOT_FOUND
    if len(divs) > 1:
        lines = [f"{i+1}. {d['bill']} - {d['stage']} ({d['date']})" for i, d in enumerate(divs)]
        return "More than one record matches. Which do you mean?\n" + "\n".join(lines)
    d = divs[0]
    head = f"{d['bill']} - {d['stage']}, {d['date']}."
    if d["dtype"] == "voice":
        return (head + " This question was decided by voice vote, so no individual votes "
                "were recorded.\nSource: " + _source(d))
    if d["dtype"] == "unknown":
        return (head + " A record exists, but individual votes could not be read from it. "
                "See the source.\nSource: " + _source(d))
    names = votes.members(con, d["id"], side)
    label = "No (noes)" if side == "noes" else "Aye (yes)"
    total = d["noes_total"] if side == "noes" else d["ayes_total"]
    out = [head, f"Recorded totals: Ayes {d['ayes_total']}, Noes {d['noes_total']}.",
           f"Members recorded as {label} ({len(names)}):"]
    out += [f"- {n}" for n in names]
    if total is not None and total != len(names):
        out.append(f"Note: Hansard's total is {total} but {len(names)} names could be read. "
                   "The list may be incomplete. Check the source page.")
    out.append("Source: " + _source(d))
    return "\n".join(out)
