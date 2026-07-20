import streamlit as st
import sqlite3

from database.database import DATABASE_PATH

st.set_page_config(
    page_title="Edit Opportunity",
    page_icon="✏",
    layout="wide"
)

st.title("✏ Edit Opportunity")

conn = sqlite3.connect(DATABASE_PATH)
conn.row_factory = sqlite3.Row

rows = conn.execute(
    "SELECT id, title FROM opportunities ORDER BY id DESC"
).fetchall()

if len(rows) == 0:

    st.info("No opportunities available.")

    st.stop()

options = {
    f"{row['id']} - {row['title']}": row["id"]
    for row in rows
}

selected = st.selectbox(
    "Choose Opportunity",
    list(options.keys())
)

opportunity_id = options[selected]

data = conn.execute(
    "SELECT * FROM opportunities WHERE id=?",
    (opportunity_id,)
).fetchone()

title = st.text_input(
    "Title",
    value=data["title"]
)

organizer = st.text_input(
    "Organizer",
    value=data["organizer"]
)

category = st.text_input(
    "Category",
    value=data["category"]
)

deadline = st.text_input(
    "Deadline",
    value=data["deadline"]
)

website = st.text_input(
    "Website",
    value=data["website"]
)

status = st.selectbox(
    "Status",
    [
        "Not Started",
        "In Progress",
        "Completed"
    ],
    index=[
        "Not Started",
        "In Progress",
        "Completed"
    ].index(data["status"])
)

priority = st.selectbox(
    "Priority",
    [
        "Low",
        "Medium",
        "High"
    ],
    index=[
        "Low",
        "Medium",
        "High"
    ].index(data["priority"])
)

description = st.text_area(
    "Description",
    value=data["description"],
    height=200
)

if st.button(
    "💾 Update Opportunity",
    use_container_width=True,
    type="primary"
):

    conn.execute(
        """
        UPDATE opportunities
        SET
        title=?,
        organizer=?,
        category=?,
        deadline=?,
        website=?,
        status=?,
        priority=?,
        description=?
        WHERE id=?
        """,
        (
            title,
            organizer,
            category,
            deadline,
            website,
            status,
            priority,
            description,
            opportunity_id
        )
    )

    conn.commit()

    st.success("✅ Opportunity Updated")