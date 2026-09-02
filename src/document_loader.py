from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF document.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(path)

    pages_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages_text.append(
            f"\n--- Page {page_number} ---\n{text}"
        )

    return "\n".join(pages_text)