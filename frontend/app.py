import streamlit as st
import requests
from datetime import date, timedelta, time, datetime
from zoneinfo import ZoneInfo
from streamlit_js_eval import streamlit_js_eval
from utils import local_date_to_utc, utc_date_to_local, get_user_timezone, is_valid_url
import pyperclip
import math
import os

API_URL = "http://localhost:8000/api/v1"

user_timezone = get_user_timezone()

st.title("URL Shortener")

tab1, tab2, tab3 = st.tabs(["Shorten URL", "Manage URLs", "Delete URL"])

with tab1:
    st.header("Shorten a URL")
    long_url = st.text_input("Your long URL:")
    default_expiration_date = date.today() + timedelta(days=365)

    
    # Commented this because we changed the expiration to be set as date instead of days.

    # expiration_time = st.number_input(
    #     "Expiration time (days, default: 365 days):",
    #     min_value=1,  # Minimum value should be at least 1 day
    #     value=365,    # Default to 365 days
    #     help="Specify the number of days after which the URL will expire. The default is 365 days."
    # )
    


    expiration_time = st.date_input(
        "Expiration date (default: 1 year from today):",
        value=default_expiration_date,
        min_value=date.today() + timedelta(days=1),
        help="Specify the date on which the URL will expire. Default is set to 1 year from today."
    )   

    st.write(f"The URL will expire on {expiration_time}.")   
   
    if st.button("Shorten URL"):
        if not long_url:
            st.error("Please enter a valid long URL.")
        elif not is_valid_url(long_url):
            st.error("Please enter a valid URL with the correct format (e.g., https://www.example.com).")
        else:
            # Prepare data
            data = {"original_url": long_url}

            # Convert expiration time to utc
            expiration_time_utc = local_date_to_utc(expiration_time)

            expiration_timestamp = expiration_time_utc
            data["expiration_time"] = expiration_timestamp

            # Call the API
            response = requests.post(f"{API_URL}/shorten", json=data)

            if response.status_code == 200:
                short_url = response.json().get("short_url")
                st.success(f"Short URL: {short_url}")
            else:
                st.error("Error shortening URL")


# Number of items per page for pagination
ITEMS_PER_PAGE = 5

# Function to get URLs from API
def get_urls():
    response = requests.get(f"{API_URL}/urls")
    if response.status_code == 200:
        return response.json()
    return []

# Pagination function to slice the data for the current page
def paginate_data(data, page, items_per_page):
    start = page * items_per_page
    end = start + items_per_page
    return data[start:end]



with tab2:
    st.subheader("Your shortened URLs")

    # Current page for pagination (maintained across re-renders)
    if "current_page" not in st.session_state:
        st.session_state.current_page = 0

    # Fetch the URLs from the API
    urls = get_urls()
    
    if urls:
        # Pagination setup
        total_pages = math.ceil(len(urls) / ITEMS_PER_PAGE)
        
        # Get URLs for the current page
        current_page_urls = paginate_data(urls, st.session_state.current_page, ITEMS_PER_PAGE)

        for url in current_page_urls:
            # Convert expiration time to local time
            expiration_time_local = utc_date_to_local(url['expiration_time'], user_timezone)

            # Creating a unique key for each URL
            key = url['short_url']

            with st.container(border=True):
                # Custom HTML/CSS for Short URL and Original URL
                st.markdown(
                    f"""
                    <div style="padding: 10px; border-radius: 5px;">
                        <p style="font-size:20px; font-weight:bold; color:#333;">
                            <a href="{url['short_url']}" style="text-decoration:none; color:#333;">{url['short_url']}</a>
                        </p>
                        <p style="font-size:14px; color:gray;">
                            <a href="{url['original_url']}" style="color:gray;">{url['original_url']}</a>
                        </p>
                        <p>Expires on: {expiration_time_local.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    """, unsafe_allow_html=True
                )

                col1, col2 = st.columns([1,1], gap="small")

                copy_button = col1.button("Copy to clipboard", key=f"copy_{key}", type="secondary", use_container_width=True)
                delete_button = col2.button("Delete", key=f"delete_{key}", type="primary", use_container_width=True)

                # Copy to clipboard action
                if copy_button:
                    pyperclip.copy(url['short_url'])
                    st.toast(f"Copied to clipboard: {url['short_url']}", icon='😍')

                # Delete action
                if delete_button:
                    # Send a DELETE request to the API to delete the URL
                    response = requests.delete(f"{API_URL}/{url['short_url_key']}")
                    if response.status_code == 200:
                        st.toast(f"Short URL {url['short_url']} deleted successfully.")
                        # Refresh the list of URLs by re-fetching the data
                        urls = get_urls()

                        # Update the UI
                        st.rerun()

                    else:
                        st.error(f"Error deleting URL {url['short_url']}. It might not exist or could not be deleted.")

        # Pagination controls
        col1, col2 = st.columns(2)

        if col1.button("Previous", disabled=(st.session_state.current_page == 0)):
            st.session_state.current_page -= 1

        if col2.button("Next", disabled=(st.session_state.current_page >= total_pages - 1)):
            st.session_state.current_page += 1

        st.write(f"Page {st.session_state.current_page + 1} of {total_pages}")

    else:
        st.info("No URLs available.")


with tab3:
    st.header("Delete a Shortened URL")
    short_url_to_delete = st.text_input("Enter the short URL to delete (e.g., 0b7a59):")
    
    if st.button("Delete URL"):
        if not short_url_to_delete:
            st.error("Please enter a short URL to delete.")
        else:
            response = requests.delete(f"{API_URL}/{short_url_to_delete}")
            if response.status_code == 200:
                st.success("Short URL deleted successfully")
            else:
                st.error("Error deleting URL. It might not exist.")

