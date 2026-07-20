import streamlit as st
import pandas as pd
from services.export_service import export_opportunities
from services.opportunity_service import (
    get_all_opportunities,
    delete_opportunity
)

st.set_page_config(
    page_title="Opportunities",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Opportunities")
col1, col2 = st.columns([8, 2])

with col2:

    if st.button(
        "📥 Export CSV",
        use_container_width=True
    ):

        file = export_opportunities()

        if file:

            with open(file, "rb") as f:

                st.download_button(
                    label="⬇ Download CSV",
                    data=f,
                    file_name=file,
                    mime="text/csv",
                    use_container_width=True
                )

        else:

            st.warning("No opportunities available.")

rows = get_all_opportunities()

if len(rows) == 0:

    st.info("No opportunities available.")

    st.stop()

df = pd.DataFrame([dict(r) for r in rows])

# ---------------------------------------------------
# Metrics
# ---------------------------------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Opportunities",
    len(df)
)

pending = len(df[df["status"] == "Not Started"])

completed = len(df[df["status"] == "Completed"])

c2.metric(
    "Pending",
    pending
)

c3.metric(
    "Completed",
    completed
)

st.divider()

# ---------------------------------------------------
# Search
# ---------------------------------------------------

search = st.text_input(
    "🔍 Search"
)

if search:

    df = df[
        df["title"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# ---------------------------------------------------
# Category Filter
# ---------------------------------------------------

categories = ["All"] + sorted(
    df["category"].fillna("").unique().tolist()
)

selected = st.selectbox(
    "Category",
    categories
)

if selected != "All":

    df = df[
        df["category"] == selected
    ]

st.divider()

# ---------------------------------------------------
# Opportunity Cards
# ---------------------------------------------------

for _, row in df.iterrows():

    with st.expander(
        f"📌 {row['title']}",
        expanded=False
    ):

        c1, c2 = st.columns(2)

        with c1:

            st.write("### Organizer")
            st.write(row["organizer"])

            st.write("### Category")
            st.write(row["category"])

            st.write("### Deadline")
            st.write(row["deadline"])

            st.write("### Funding")
            st.write(row["funding_amount"])

        with c2:

            st.write("### Website")
            st.write(row["website"])

            st.write("### Status")
            st.write(row["status"])

            st.write("### Priority")
            st.write(row["priority"])

        st.write("### Description")
        st.write(row["description"])

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                f"🗑 Delete {row['id']}"
            ):

                delete_opportunity(row["id"])

                st.success("Opportunity deleted.")

                st.rerun()

        with col2:

            st.button(
                f"✏ Edit {row['id']}",
                disabled=True
            )