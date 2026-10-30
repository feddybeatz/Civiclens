import json
import pathlib

import fitz  # pymupdf

PDF_DIR = pathlib.Path("data/pdfs")
OUT = pathlib.Path("data/index/pages.json")

# Optional: data/sources.json maps filename -> official URL, e.g.
# {"mwananchi-guide-2024-25.pdf": "https://..."}
src_file = pathlib.Path("data/sources.json")
sources = json.loads(src_file.read_text()) if src_file.exists() else {}

records = []
for pdf in sorted(PDF_DIR.glob("*.pdf")):
    doc = fitz.open(pdf)
    kept = 0
    for i, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            kept += 1
            records.append({
                "document": pdf.name,
                "page": i,
                "text": text,
                "source_url": sources.get(pdf.name),
            })
    print(f"{pdf.name}: {kept} of {len(doc)} pages have text")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(records))
print(f"Total: {len(records)} pages indexed")
