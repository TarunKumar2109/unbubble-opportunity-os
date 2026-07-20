import streamlit as st

from services.pdf_service import extract_text_from_pdf
from services.gemini_service import extract_opportunity
from services.opportunity_service import save_opportunity
from components.review_card import render_review_card
from services.website_service import extract_text_from_website
from services.link_finder import find_opportunity_links

st.set_page_config(
    page_title="Opportunity Inbox",
    page_icon="📥",
    layout="wide"
)

st.title("📥 Opportunity Inbox")

st.markdown(
    """
Upload opportunities from different sources.

Nothing is saved until you click **Approve**.
"""
)

# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------

if "opportunity" not in st.session_state:
    st.session_state.opportunity = None

# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📄 PDF",
        "🖼 Image",
        "🌐 Website",
        "💼 LinkedIn",
        "📝 Paste Text"
    ]
)

# =========================================================
# PDF
# =========================================================

with tab1:

    uploaded_pdf = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if uploaded_pdf and st.session_state.opportunity is None:

        st.success(uploaded_pdf.name)

        if st.button(
            "🚀 Analyze PDF",
            type="primary",
            use_container_width=True
        ):

            with st.spinner("Reading PDF..."):

                text = extract_text_from_pdf(uploaded_pdf)

            with st.spinner("Analyzing with Gemini..."):

                st.session_state.opportunity = extract_opportunity(text)

# =========================================================
# WEBSITE
# =========================================================

with tab3:

    st.subheader("🌐 Website Opportunity Finder")

    website = st.text_input(
        "Website URL",
        placeholder="https://startupindia.gov.in"
    )

    if website and st.button(
        "🔎 Find Opportunities",
        type="primary",
        use_container_width=True
    ):

        try:

            with st.spinner("Finding opportunity pages..."):

                st.session_state.website_links = find_opportunity_links(
                    website
                )

            if len(st.session_state.website_links) == 0:

                st.warning(
                    "No opportunity pages found."
                )

        except Exception as e:

            st.error(str(e))

    # ---------------------------------------------
    # Show Opportunity Links
    # ---------------------------------------------

    if (
        "website_links" in st.session_state
        and len(st.session_state.website_links) > 0
    ):

        st.success(
            f"Found {len(st.session_state.website_links)} opportunity pages."
        )

        options = {}

        for i, link in enumerate(st.session_state.website_links):

            title = link["title"].strip()

            if title == "":
                title = f"Opportunity {i+1}"

            options[f"{i+1}. {title}"] = link["url"]

        selected = st.selectbox(
            "Choose an opportunity",
            list(options.keys())
        )

        if st.button(
            "🚀 Analyze Selected Opportunity",
            use_container_width=True
        ):

            selected_url = options[selected]

            try:

                with st.spinner("Reading webpage..."):

                    text = extract_text_from_website(
                        selected_url
                    )

                with st.spinner("Analyzing with Gemini..."):

                    st.session_state.opportunity = extract_opportunity(
                        text
                    )

                st.success(
                    "✅ Opportunity extracted successfully!"
                )

            except Exception as e:

                st.error(str(e))
# =========================================================
# PASTE TEXT
# =========================================================

with tab5:

    text = st.text_area(
        "Paste Opportunity",
        height=250
    )

    if text and st.session_state.opportunity is None:

        if st.button(
            "🚀 Analyze Text",
            use_container_width=True
        ):

            with st.spinner("Analyzing..."):

                st.session_state.opportunity = extract_opportunity(text)

# =========================================================
# IMAGE
# =========================================================

with tab2:

    from services.image_service import extract_text_from_image

    st.subheader("🖼 Upload Image")

    uploaded_image = st.file_uploader(
        "Choose Image",
        type=["png", "jpg", "jpeg"],
        key="image"
    )

    if uploaded_image and st.session_state.opportunity is None:

        st.image(uploaded_image, width=400)

        if st.button(
            "🚀 Analyze Image",
            type="primary",
            use_container_width=True
        ):

            with st.spinner("Extracting text from image..."):

                text = extract_text_from_image(uploaded_image)

            with st.spinner("Analyzing with Gemini..."):

                st.session_state.opportunity = extract_opportunity(text)

# =========================================================
# LINKEDIN
# =========================================================

with tab4:

    st.info("LinkedIn extraction will be added next.")

# =========================================================
# REVIEW PANEL
# =========================================================

if st.session_state.opportunity:

    opportunity = st.session_state.opportunity

    if opportunity.get("error", False):

        st.error("AI could not understand this opportunity.")

        st.code(
            opportunity.get(
                "raw_response",
                ""
            )
        )

    else:

        st.divider()

        st.subheader("🔍 Review Opportunity")

        edited_data, approve, reject = render_review_card(
            opportunity
        )

        c1, c2 = st.columns(2)

        with c1:

            if approve:

                save_opportunity(edited_data)

                st.session_state.opportunity = None

                st.success("✅ Opportunity Saved")

                st.balloons()

                st.rerun()

        with c2:

            if reject:

                st.session_state.opportunity = None

                st.warning("Opportunity discarded.")

                st.rerun()