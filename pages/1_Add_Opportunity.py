import sqlite3
import streamlit as st
from database.database import get_connection

st.set_page_config(page_title="Add Opportunity", page_icon="➕")

st.title("➕ Add New Opportunity")

with st.form("opportunity_form"):

    title = st.text_input("Opportunity Title *")

    organizer = st.text_input("Organizer")

    category = st.selectbox(
        "Category",
        [
            "Grant",
            "Hackathon",
            "Incubator",
            "Accelerator",
            "Competition",
            "Tender",
            "CSR",
            "Exhibition",
            "Award",
            "Other",
        ],
    )

    website = st.text_input("Website")

    deadline = st.date_input("Application Deadline")

    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"]
    )

    status = st.selectbox(
        "Application Status",
        [
            "Not Started",
            "In Progress",
            "Submitted",
            "Won",
            "Rejected",
        ],
    )

    funding = st.text_input("Funding Amount")

    location = st.text_input("Location")

    description = st.text_area("Description")

    notes = st.text_area("Internal Notes")

    submit = st.form_submit_button("💾 Save Opportunity")

if submit:

    if title.strip() == "":
        st.error("Opportunity title is required.")
    else:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO opportunities
            (
                title,
                organizer,
                category,
                description,
                website,
                deadline,
                status,
                priority,
                funding_amount,
                location,
                notes
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                organizer,
                category,
                description,
                website,
                str(deadline),
                status,
                priority,
                funding,
                location,
                notes,
            ),
        )

        conn.commit()
        conn.close()

        st.success("✅ Opportunity saved successfully!")