from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_pages(pages: list[dict], chunk_size: int = 500, chunk_overlap: int = 50) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    all_chunks = []

    for page_data in pages:
        raw_chunks = splitter.split_text(page_data["text"])

        for i, chunk_text in enumerate(raw_chunks):
            chunk_text = chunk_text.strip()
            if len(chunk_text) < 30:
                continue

            all_chunks.append({
                "chunk_id": f"{page_data['source']}_p{page_data['page']}_c{i}",
                "text": chunk_text,
                "page": page_data["page"],
                "source": page_data["source"]
            })

    print(f"Created {len(all_chunks)} chunks from {len(pages)} pages")
    return all_chunks


if __name__ == "__main__":
    fake_page = [{
        "page": 1,
        "text": (
            "NON-DISCLOSURE AGREEMENT\n\n"
            "This Agreement is entered as of Jan 1 2024, between Acme Corp "
            "and Beta Ltd.\n\n"
            "1. CONFIDENTIAL INFORMATION\n\n"
            "Confidential Information means any proprietary data not generally "
            "known to the public, in tangible or intangible form."
        ),
        "source": "test.pdf"
    }]

    chunks = chunk_pages(fake_page)
    for c in chunks:
        print(f"\n[{c['chunk_id']}]")
        print(c["text"])