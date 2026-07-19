import streamlit as st
from database.database import initialize_database

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
# Sidebar
# -------------------------------------------------
st.sidebar.title("🚀 UnBubble")
st.sidebar.markdown("### Opportunity Intelligence")
st.sidebar.divider()

st.sidebar.success("✅ Database Connected")

# -------------------------------------------------
# Main Dashboard
# -------------------------------------------------
st.title("🚀 UnBubble Opportunity Intelligence")

st.write(
    """
Welcome to **UnBubble Opportunity Intelligence**.

This platform helps manage:

- 🏆 Hackathons
- 💰 Grants
- 🌱 Sustainability Programs
- 🏢 Incubators
- 🤝 Partnerships
- 📅 Deadlines
- 📝 Tasks
- 👥 Team Assignments
"""
)

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Opportunities", "0")
col2.metric("Upcoming Deadlines", "0")
col3.metric("Pending Tasks", "0")
col4.metric("Applications Submitted", "0")

st.divider()

st.success("🎉 Database initialized successfully!")

st.info(
    "Next step: We'll build the Add Opportunity page where every opportunity will be saved permanently."
)