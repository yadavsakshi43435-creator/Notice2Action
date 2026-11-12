import pymupdf


def extract_text_from_pdf(pdf_bytes):
    """
    Extract text from an uploaded PDF.
    """

    document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    extracted_pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        extracted_pages.append(
            f"\n--- Page {page_number} ---\n{text}"
        )

    document.close()

    return "\n".join(extracted_pages)