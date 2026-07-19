import pdfplumber


def extract_text_from_pdf(uploaded_file):
    """
    Extract all text from an uploaded PDF file.

    Parameters:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        str: Extracted text
    """

    extracted_text = ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:
                    extracted_text += text + "\n\n"

        return extracted_text.strip()

    except Exception as e:

        return f"ERROR: {str(e)}"