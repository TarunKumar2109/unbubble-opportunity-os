import streamlit as st
from services.pdf_service import extract_text_from_pdf
st.set_page_config(
    page_title="Opportunity Inbox",
    page_icon="📥",
    layout="wide"
)

st.title("📥 Opportunity Inbox")

st.markdown(
    """
Upload or paste an opportunity from any source.

Nothing will be saved until you review and approve the extracted information.
"""
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 PDF",
    "🖼 Image",
    "🌐 Website",
    "💼 LinkedIn",
    "📝 Paste Text"
])

with tab1:

    st.subheader("📄 Upload PDF")

    uploaded_pdf = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
        key="pdf"
    )

    if uploaded_pdf is not None:

        st.success(f"Uploaded: {uploaded_pdf.name}")

        if st.button("Extract PDF"):

            with st.spinner("Extracting text..."):

                extracted_text = extract_text_from_pdf(uploaded_pdf)

            st.subheader("📑 Extracted Text")

            st.text_area(
                "Review before approval",
                extracted_text,
                height=400
            )

            st.success(
                "Extraction completed. Next we'll convert this into structured opportunity fields."
            )
with tab2:
    st.subheader("Upload Image")
    image = st.file_uploader(
        "Choose an Image",
        type=["png", "jpg", "jpeg"],
        key="image"
    )

    if image:
        st.image(image, width=400)
        st.info("OCR extraction will be added in the next step.")

with tab3:
    st.subheader("Paste Website URL")

    website = st.text_input(
        "Website URL",
        placeholder="https://example.com"
    )

    if st.button("Extract Website"):
        if website:
            st.success("Website received.")
            st.info("Website extraction will be added next.")
        else:
            st.warning("Please enter a website URL.")

with tab4:
    st.subheader("Paste LinkedIn Post URL")

    linkedin = st.text_input(
        "LinkedIn URL",
        placeholder="https://linkedin.com/..."
    )

    if st.button("Extract LinkedIn"):
        if linkedin:
            st.success("LinkedIn URL received.")
            st.info("LinkedIn extraction will be added next.")
        else:
            st.warning("Please enter a LinkedIn URL.")

with tab5:
    st.subheader("Paste Opportunity Text")

    text = st.text_area(
        "Paste complete opportunity details here",
        height=250
    )

    if st.button("Extract Text"):
        if text.strip():
            st.success("Text received.")
            st.info("AI extraction will be added next.")
        else:
            st.warning("Please paste some text.")