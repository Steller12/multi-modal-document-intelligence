from .ocr import run_ocr

def extract_images_with_ocr(doc, page):
    records = []

    for img in page.images:
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]

        ocr_text = run_ocr(image_bytes)

        if ocr_text and len(ocr_text.split()) > 20:
            records.append({
                "content": ocr_text,
                "modality": "image",
                "page": page.page_number,
                "source": "ocr"
            })

    return records
