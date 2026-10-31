# CivicLens

**Where Did Our Money Go?** CivicLens lets Kenyan citizens ask questions about government budget documents in plain language and get answers that can be checked against the official source.

Every answer shows the document, the page, and the exact sentence it came from. If the documents don't answer the question, CivicLens says so instead of guessing.

## How it works

```
official PDFs -> ingest.py -> data/index/pages.json   (offline, run when documents change)

question -> retrieve() -> top pages -> ask_gemma() -> citation check -> answer + evidence
            (BM25)                     (Gemma API)     (word-for-word)
```

1. **Ingest** extracts text from each PDF, page by page, into `data/index/pages.json`.
2. **Retrieve** scores pages against the question with BM25 and returns the top few.
3. **Ask Gemma** sends only the question and those few pages to the model, which replies with JSON: answer, status, cited passage number, and an excerpt.
4. **Validate** checks that the cited passage exists and that the excerpt appears word for word in it. If the check fails, the answer is discarded.
5. **The UI** (Streamlit) shows the answer, the document, the page, the excerpt, and the limitations.

Answer statuses: `supported`, `partial`, `no_evidence`, `error`.

## Safety design

- Only the question and the retrieved passages are sent to Google. The full PDFs stay on the machine.
- Document text is treated as untrusted data. The prompt tells the model to ignore any instructions inside it.
- Valid JSON is not trusted. The cited excerpt must appear word for word in the cited passage.
- The model never writes the document or page itself. It cites a passage number, and the app looks up the document and page from that passage.
- An allocation is described as a plan, not actual spending. A missing detail is never presented as wrongdoing.
- Internal errors are never shown to users. They are logged to the terminal instead.

## Project structure

```
Civiclens/
  app.py                 Streamlit entry point and navigation
  config.py              Settings read from .env
  ingest.py              PDFs -> data/index/pages.json
  ai/
    ai_engine.py         Prompt, model call, JSON parsing, citation validation
    retrieval.py         BM25 page retrieval
  ui/
    chat.py              Budget Assistant page (real pipeline)
    dashboard.py, insights.py, participation.py, about.py   (still use sample data)
    components.py, styles.py, sample_data.py
  data/
    pdfs/                PDFs with extractable text (indexed)
    scanned/             Scanned PDFs waiting for OCR (not indexed)
    index/pages.json     Generated page index
    sources.json         Optional: filename -> official URL
```

## Setup

```bash
cd ~/projects/Civiclens
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install pymupdf rank-bm25 requests
```

Create `.env` in the project root:

```
GEMINI_API_KEY=your-key-here
GEMMA_MODEL=gemma-4-26b-a4b-it
```

`config.py` also sets `REQUEST_TIMEOUT_MS = 120000` (milliseconds). Never commit `.env`.

## Adding documents

1. Download PDFs from official sources (below) into `data/pdfs/` and give them short names, such as `mwananchi-guide-2024-25.pdf`.
2. Run `python ingest.py`. It prints one line per PDF, for example `16 of 16 pages have text`.
3. Move any PDF with far fewer text pages than total pages (a scan) into `data/scanned/`.
4. Restart the app. The index is loaded at startup.

To link answers back to the official document, add entries to `data/sources.json`:

```json
{"mwananchi-guide-2024-25.pdf": "https://official-url-of-the-document"}
```

Re-run `python ingest.py`. The UI then shows an "Open official document" button.

### Official sources

- Bajeti Yetu portal: https://bajetiyetu.treasury.go.ke/ (individual documents are public; the full document list requires a login, so download documents one at a time)
- National Treasury budget books: https://www.treasury.go.ke/budget-books
- Parliament budget documents: https://parliament.go.ke/2026-2027-budget-documents
- Commission on Revenue Allocation: https://cra.go.ke/

The Bajeti Yetu `robots.txt` blocks nothing. Keep downloads gentle anyway: one request at a time, with a pause, and a clear User-Agent.

## Running

```bash
streamlit run app.py
```

Open **Budget Assistant**. A question takes roughly 10 to 20 seconds.

## Testing without the UI

```bash
python test_engine.py                                   # fixed passage, expects supported + no_evidence
python test_questions.py How much is allocated to education?
```

Always check the cited excerpt against the real PDF page. That is the test that matters.

## Known limitations

- **Scanned PDFs** (for example the 2022 Budget Circular and the 2019-2020 Supplementary Appropriation Act) have no text layer and are not indexed. They need OCR.
- **Swahili questions** retrieve nothing, because BM25 matches English words only. The app declines instead of guessing. Fix: translate the question to English before retrieval.
- **Tables** can extract as scrambled text, so some answers fail the word-for-word check. That is the safe outcome.
- **Page numbers** are PDF page indexes, which can differ from the numbers printed on the page.
- **Sample data:** the Dashboard, Insights and Participation pages still show the sample county, not real data.
- **Model reliability:** `gemma-4-31b-it` returned HTTP 500 errors during testing, so the default is `gemma-4-26b-a4b-it`. `gemini-2.5-flash` is no longer available to new keys.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| "We couldn't generate an answer." | Check the terminal for the logged traceback |
| `module 'config' has no attribute ...` | Missing setting in `config.py` |
| `No module named 'ai.retrieval'` | File missing, or `ai/__init__.py` missing |
| Request times out | Model slow or overloaded; check with a raw `curl` call, then retry or switch model |
| HTTP 404 on a model | Model retired; list models with the `/v1beta/models` endpoint |
| Answers don't change after adding PDFs | Re-run `ingest.py` and restart Streamlit |

## Next steps

1. Check the first real answers in the UI against the PDFs.
2. Fill in `data/sources.json` with official URLs.
3. Add more text-based documents (national and county budgets).
4. Translate Swahili questions before retrieval.
5. OCR the scanned documents.
6. Replace the sample data on the other pages with figures extracted from the documents.
7. Optional: a `sync.py` script that downloads documents listed in a `data/manifest.json`.

