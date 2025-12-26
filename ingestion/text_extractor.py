def extract_text(page):
    if not page.text.strip():
        return []

    return [{
        "content": page.text.strip(),
        "modality": "text",
        "page": page.page_number,
        "section": None,
        "source": "pdf_text"
    }]