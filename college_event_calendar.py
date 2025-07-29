import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Connect to Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="📅 College Event Calendar", page_icon="📌")
st.title("📅 College Event Calendar (Supabase Version)")

# --- Add new event ---
with st.form("event_form"):
    title = st.text_input("Event Title")
    date = st.date_input("Event Date")
    desc = st.text_area("Description")
    submit = st.form_submit_button("➕ Add Event")

    if submit:
        if title.strip():
            try:
                response = supabase.table("events").insert({
                    "title": title,
                    "date": str(date),
                    "description": desc
                }).execute()

                if response.data:
                    st.success("✅ Event added successfully!")
                else:
                    st.error(f"❌ Insert failed: {response.error.message if response.error else 'Unknown error'}")

            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
        else:
            st.warning("⚠ Title cannot be empty.")

st.divider()
st.subheader("📋 All Events")

# --- Display all events ---
try:
    response = supabase.table("events").select("*").order("date", desc=False).execute()
    if response.data:
        df = pd.DataFrame(response.data)
        df["date"] = pd.to_datetime(df["date"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No events found.")
except Exception as e:
    st.error(f"❌ Failed to load events: {e}")
