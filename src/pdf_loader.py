import fitz
from pathlib import Path


def load_pdf(pdf_path: str) -> list[dict]:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"Can't find: {pdf_path}")

    doc = fitz.open(pdf_path)
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        if text:
            pages.append({
                "page": page_num + 1,
                "text": text,
                "source": path.name
            })

    doc.close()
    print(f"Loaded {len(pages)} pages with text from '{path.name}'")
    return pages


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pdf_loader.py MyFile.pdf")
        sys.exit(1)

    result = load_pdf(sys.argv[1])
    print(f"\nFirst page preview:\n{result[0]['text'][:300]}")