import fitz

class PDFPage:
    def __init__(self, page_number, text, images):
        self.page_number = page_number
        self.text = text
        self.images = images

def load_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text()
        images = page.get_images(full=True)

        pages.append(
            PDFPage(
                page_number=i + 1,
                text=text,
                images=images
            )
        )

    return pages
