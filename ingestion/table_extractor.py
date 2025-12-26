import camelot

def extract_tables(pdf_path, page_number):
    records = []

    try:
        tables = camelot.read_pdf(pdf_path, pages=str(page_number))

        for table in tables:
            if table.df.shape[0] > 1 and table.df.shape[1] > 1:
                records.append({
                    "content": table.df.to_string(index=False),
                    "modality": "table",
                    "page": page_number,
                    "source": "pdf_table"
                })
    except Exception:
        pass

    return records
