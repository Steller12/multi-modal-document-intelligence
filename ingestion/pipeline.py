import fitz
from .pdf_loader import load_pdf
from .text_extractor import extract_text
from .table_extractor import extract_tables
from .image_extractor import extract_images_with_ocr

def ingest_document(pdf_path):
    documents = []

    pages = load_pdf(pdf_path)
    doc = fitz.open(pdf_path)

    for page in pages:
        # Text
        documents.extend(extract_text(page))

        # Tables
        documents.extend(extract_tables(pdf_path, page.page_number))

        # Images + OCR
        documents.extend(extract_images_with_ocr(doc, page))

    return documents
