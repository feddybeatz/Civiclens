"""ILLUSTRATIVE data so the interface can be built before the real pipeline.

Everything here is fictional. Replace it with verified data from real
documents (Phase 3 onwards) and delete this file when it is no longer used.
"""

NOTE = ("Illustrative sample county budget. All figures and excerpts are "
        "fictional, not government evidence.")

DOCUMENT = {
    "name": "Sample County Budget 2025-26.pdf",
    "pages": 64,
    "year": "FY 2025/26",
}

TOTAL_BUDGET_B = 12.0

# Billions of KSh. All values sum to 12.0.
ALLOCATIONS = [
    {"sector": "Health", "amount_b": 3.6, "share": 30, "page": 18},
    {"sector": "Education", "amount_b": 2.4, "share": 20, "page": 18},
    {"sector": "Roads & transport", "amount_b": 1.8, "share": 15, "page": 18},
    {"sector": "Administration", "amount_b": 1.8, "share": 15, "page": 18},
    {"sector": "Water & sanitation", "amount_b": 1.2, "share": 10, "page": 18},
    {"sector": "Agriculture", "amount_b": 1.2, "share": 10, "page": 18},
]

SPLIT = [("Recurrent", 7.2, 60), ("Development", 4.8, 40)]

SUGGESTED = [
    "How much was allocated to health?",
    "Which sector has the largest share?",
    "How is development spending split?",
    "Are ward-level projects listed?",
]

GAPS = [
    {
        "kind": "Unclear allocation",
        "title": "Road maintenance by ward",
        "text": "The budget lists KSh 240 million for road maintenance, but does not explain how it is distributed across wards.",
        "excerpt": "Road maintenance: KSh 240,000,000.",
        "meta": "Page 32 · included in the KSh 1.8B roads allocation",
        "note": "A missing breakdown is a prompt for clarification, not evidence of misuse.",
    },
    {
        "kind": "Missing project details",
        "title": "Mtoni dispensary",
        "text": "The project is named, but the entry does not include a cost, completion date or contractor.",
        "excerpt": "Planned health project: Mtoni dispensary.",
        "meta": "Page 41 · project list",
        "note": "Details may be available in a separate procurement or implementation document.",
    },
]

QUESTIONS = [
    {
        "tag": "Clarify the allocation",
        "text": "How is the KSh 240 million for road maintenance distributed across wards, and which criteria guide that distribution?",
        "meta": "Road maintenance · page 32",
    },
    {
        "tag": "Ask for project details",
        "text": "Could the county share the planned cost, timeline and procurement reference for the Mtoni dispensary?",
        "meta": "Health projects · page 41",
    },
    {
        "tag": "Track delivery",
        "text": "Where can residents find expenditure and implementation reports to compare actual progress with these allocations?",
        "meta": "Follow-up request · not answered in this budget",
    },
]
