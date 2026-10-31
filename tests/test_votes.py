from ai import votes, votes_answer as va
from ai.votes_parser import parse_division

# SYNTHETIC data with invented names, only to test code paths. Not real Hansard.
SAMPLE = """AYES (3)
1. Test Member One    2. Test Member Two
3. Test Member Three
NOES (2)
1. Test Member Four
2. Test Member Five
The Speaker: The Ayes have it.
"""

def db(tmp_path):
    con = votes.connect(str(tmp_path / "v.db"))
    r = parse_division(SAMPLE)
    mem = [(n, "ayes") for n in r["ayes"]] + [(n, "noes") for n in r["noes"]]
    votes.add_division(con, "Sample Elections Bill", "Third Reading", "2026-01-01",
                       "recorded", 3, 2, 10, "x.pdf", "http://x", "live streaming", mem)
    votes.add_division(con, "Sample Voice Bill", "Second Reading", "2026-02-01",
                       "voice", page=5, aliases="voice sample")
    votes.add_division(con, "Mismatch Bill", "Third Reading", "2026-03-01", "recorded",
                       3, 5, 7, "y.pdf", "", "mismatch", [("Test Member Six", "noes")])
    return con

def test_parser():
    r = parse_division(SAMPLE)
    assert r["noes"] == ["Test Member Four", "Test Member Five"]
    assert len(r["ayes"]) == 3 and r["totals"] == {"ayes": 3, "noes": 2}

def test_known_division_exact_list(tmp_path):
    out = va.answer("list MPs who voted no on the live streaming bill in 2026", db(tmp_path))
    assert "- Test Member Four" in out and "- Test Member Five" in out
    assert "Test Member One" not in out and "page 10" in out

def test_voice_vote(tmp_path):
    out = va.answer("who voted no on the sample voice bill", db(tmp_path))
    assert "no individual votes were recorded" in out

def test_unknown_bill(tmp_path):
    assert va.answer("who voted no on the zebra protection bill", db(tmp_path)) == va.NOT_FOUND

def test_totals_mismatch_flagged(tmp_path):
    out = va.answer("who voted no on the mismatch bill", db(tmp_path))
    assert "may be incomplete" in out

def test_budget_question_not_routed():
    assert not va.is_vote_question("How much was allocated to health in 2026/27?")
