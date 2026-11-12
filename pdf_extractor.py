
import pymupdf

def extract_text_from_pdf(pdf_bytes):

    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    try:
        if document.page_count == 0:
            return ""

        extracted_pages = []

        for page_number, page in enumerate(
            document, start=1
        ):
            text = page.get_text("text").strip()

            if text:
                extracted_pages.append(
                    f"\n--- Page {page_number} ---\n{text}"
                )

        return "\n".join(extracted_pages)

    finally:
        document.close()