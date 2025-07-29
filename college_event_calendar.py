import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="College Event Calendar", page_icon="📅")

st.title("📅 College Event Calendar ")

# Initialize storage
if "events" not in st.session_state:
    st.session_state.events = []

# Form to add event
with st.form("add_event_form"):
    title = st.text_input("Event Title")
    date = st.date_input("Event Date")
    desc = st.text_area("Description")
    submit = st.form_submit_button("➕ Add Event")
    if submit:
        if title.strip():
            st.session_state.events.append({
                "Title": title,
                "Date": date.strftime("%Y-%m-%d"),
                "Description": desc
            })
            st.success("✅ Event added!")
        else:
            st.warning("⚠️ Title cannot be empty.")

st.divider()
st.subheader("📋 All Upcoming Events")

# Display all events
if st.session_state.events:
    df = pd.DataFrame(st.session_state.events)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    st.dataframe(df, use_container_width=True)

    # Delete section
    st.subheader("🗑️ Delete Event")
    selected_event = st.selectbox("Select event to delete:", [f"{row['Title']} - {row['Date'].date()}" for _, row in df.iterrows()])
    if st.button("Delete Selected Event"):
        index_to_delete = next((i for i, row in enumerate(df.iterrows()) if f"{row[1]['Title']} - {row[1]['Date'].date()}" == selected_event), None)
        if index_to_delete is not None:
            del st.session_state.events[index_to_delete]
            st.success("🗑️ Event deleted. Please refresh page.")

    # Search by Month
    st.subheader("🔍 Search Events by Month")
    month = st.selectbox("Select Month:", range(1, 13), format_func=lambda x: datetime(2023, x, 1).strftime('%B'))
    filtered = df[df["Date"].dt.month == month]
    if not filtered.empty:
        st.dataframe(filtered)
    else:
        st.info("No events found for selected month.")
else:
    st.info("No events to show yet.")
