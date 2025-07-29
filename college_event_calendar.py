import streamlit as st
import pandas as pd
from supabase import create_client, Client

# --- Connect to Supabase ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="📅 College Event Calendar", page_icon="📌")
st.title("📅 College Event Calendar (Cloud-Connected ✅)")

# --- Add New Event ---
with st.form("event_form"):
    title = st.text_input("Event Title")
    date = st.date_input("Event Date")
    desc = st.text_area("Description")
    submit = st.form_submit_button("➕ Add Event")

    if submit:
        if title.strip():
            response = supabase.table("events").insert({
                "title": title,
                "date": str(date),
                "description": desc
            }).execute()
            st.success("✅ Event added successfully!")
        else:
            st.warning("⚠ Title cannot be empty.")

st.divider()
st.subheader("📋 All Events")

# --- Display All Events ---
response = supabase.table("events").select("*").order("date", desc=False).execute()

if response.data:
    df = pd.DataFrame(response.data)
    df["date"] = pd.to_datetime(df["date"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No events yet. Add one above!")
