def split_text(
    text: str,
    chunk_size: int = 400,
    overlap: int = 50
):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        if chunk_text.strip():
            chunks.append(chunk_text)

        start = end - overlap

        if start < 0:
            start = 0

    return chunks


def chunk_records(records):
    chunked_records = []

    for record in records:
        modality = record["modality"]
        content = record["content"]

        if modality == "text":
            chunks = split_text(
                content,
                chunk_size=400,
                overlap=50
            )

            for chunk in chunks:
                new_record = record.copy()
                new_record["content"] = chunk
                chunked_records.append(new_record)

        elif modality == "image":
            chunks = split_text(
                content,
                chunk_size=200,
                overlap=30
            )

            for chunk in chunks:
                new_record = record.copy()
                new_record["content"] = chunk
                chunked_records.append(new_record)

        else:
            chunked_records.append(record)

    return chunked_records
