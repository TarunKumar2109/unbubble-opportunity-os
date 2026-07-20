import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

from database.database import (
    initialize_database,
    DATABASE_PATH
)

# -------------------------------------------------
# Initialize Database
# -------------------------------------------------

initialize_database()

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="UnBubble Opportunity Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)



# -------------------------------------------------
# Database
# -------------------------------------------------

conn = sqlite3.connect(DATABASE_PATH)

df = pd.read_sql(
    "SELECT * FROM opportunities",
    conn
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.markdown("## 🚀 UnBubble")

st.sidebar.markdown(
    "Opportunity Intelligence"
)

st.sidebar.divider()

st.sidebar.success("✅ Database Connected")

# -------------------------------------------------
# Dashboard
# -------------------------------------------------

col1, col2 = st.columns([1, 6])

with col1:
    st.image("assets/logo.jpeg", width=100)

with col2:
    st.title("UnBubble Opportunity Intelligence")


st.caption(
    "AI-powered opportunity discovery and management platform"
)

st.divider()

# -------------------------------------------------
# Metrics
# -------------------------------------------------

total = len(df)

pending = (
    len(df[df["status"] == "Not Started"])
    if not df.empty else 0
)

completed = (
    len(df[df["status"] == "Completed"])
    if not df.empty else 0
)

funding = (
    len(
        df[
            df["category"]
            .fillna("")
            .str.contains(
                "grant|fund",
                case=False
            )
        ]
    )
    if not df.empty else 0
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "📋 Opportunities",
    total
)

c2.metric(
    "⏳ Pending",
    pending
)

c3.metric(
    "✅ Completed",
    completed
)

c4.metric(
    "💰 Grants/Funding",
    funding
)

st.divider()

# -------------------------------------------------
# Charts
# -------------------------------------------------

if not df.empty:

    left, right = st.columns(2)

    with left:

        st.subheader("Status Distribution")

        status_df = (
            df["status"]
            .value_counts()
            .reset_index()
        )

        status_df.columns = [
            "Status",
            "Count"
        ]

        fig = px.pie(
            status_df,
            names="Status",
            values="Count",
            hole=0.45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Categories")

        category_df = (
            df["category"]
            .fillna("Unknown")
            .value_counts()
            .head(10)
            .reset_index()
        )

        category_df.columns = [
            "Category",
            "Count"
        ]

        fig = px.bar(
            category_df,
            x="Category",
            y="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()
st.divider()

st.subheader("⚡ Quick Actions")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("📥 Add Opportunity", use_container_width=True):
        st.switch_page("pages/0_Opportunity_Inbox.py")

with c2:
    if st.button("📋 View Opportunities", use_container_width=True):
        st.switch_page("pages/2_Opportunities.py")

with c3:
    if st.button("✏ Edit Opportunity", use_container_width=True):
        st.switch_page("pages/3_Edit_Opportunity.py")

# -------------------------------------------------
# Latest Opportunities
# -------------------------------------------------

st.subheader("📌 Latest Opportunities")

if df.empty:

    st.info(
        "No opportunities available."
    )

else:

    latest = df.sort_values(
        "id",
        ascending=False
    ).head(10)

    st.dataframe(
        latest[
            [
                "title",
                "category",
                "deadline",
                "status",
                "priority"
            ]
        ],
        hide_index=True,
        use_container_width=True
    )

st.divider()

st.success("✅ System Ready")

st.caption(
    "Built with ❤️ using Streamlit • Gemini • SQLite"
)