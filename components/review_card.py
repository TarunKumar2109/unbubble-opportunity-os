import streamlit as st


def render_review_card(data: dict):
    """
    Display extracted opportunity information for user review.
    Returns the edited dictionary.
    """

    st.subheader("🔍 Review Extracted Opportunity")

    edited = {}

    edited["title"] = st.text_input(
        "Opportunity Title",
        value=data.get("title", "")
    )

    edited["organizer"] = st.text_input(
        "Organizer",
        value=data.get("organizer", "")
    )

    edited["category"] = st.text_input(
        "Category",
        value=data.get("category", "")
    )

    edited["deadline"] = st.text_input(
        "Deadline",
        value=data.get("deadline", "")
    )

    edited["website"] = st.text_input(
        "Website",
        value=data.get("website", "")
    )

    edited["funding_amount"] = st.text_input(
        "Funding Amount",
        value=data.get("funding_amount", "")
    )

    edited["eligibility"] = st.text_area(
        "Eligibility",
        value=data.get("eligibility", ""),
        height=80
    )

    edited["summary"] = st.text_area(
        "Summary",
        value=data.get("summary", ""),
        height=120
    )

    edited["description"] = st.text_area(
        "Description",
        value=data.get("description", ""),
        height=180
    )

    edited["relevance_score"] = st.slider(
        "Relevance Score",
        0,
        100,
        int(data.get("relevance_score", 0))
    )

    edited["confidence"] = st.slider(
        "Confidence",
        0,
        100,
        int(data.get("confidence", 0))
    )

    st.divider()

    col1, col2 = st.columns(2)

    approve = col1.button(
        "✅ Approve",
        type="primary",
        use_container_width=True
    )

    reject = col2.button(
        "❌ Reject",
        use_container_width=True
    )

    return edited, approve, reject