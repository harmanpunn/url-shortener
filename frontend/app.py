import streamlit as st
import requests
from datetime import date, timedelta, time, datetime
from zoneinfo import ZoneInfo
from streamlit_js_eval import streamlit_js_eval
from utils import local_date_to_utc, utc_date_to_local, get_user_timezone, is_valid_url


API_URL = "http://localhost:8000/api/v1"

user_timezone = get_user_timezone()

st.title("URL Shortener")

tab1, tab2, tab3 = st.tabs(["Shorten URL", "Manage URLs", "Delete URL"])

with tab1:
    st.header("Shorten a URL")
    long_url = st.text_input("Enter the long URL:")
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


with tab2:
    st.header("View All Shortened URLs")

    # Option to get all URLs
    if st.button("Get All URLs"):
        response = requests.get(f"{API_URL}/urls")
        if response.status_code == 200:
            urls = response.json()
            
            # Prepare data for table
            if urls:
                import pandas as pd
                url_data = [
                    {
                        "Short URL": url['short_url'],
                        "Original URL": url['original_url'],
                        "Expiration Time": utc_date_to_local(url['expiration_time'], user_timezone).strftime('%Y-%m-%d %H:%M:%S')
                    }
                    for url in urls
                ]
                df = pd.DataFrame(url_data)
                st.dataframe(df)  # Display as a table
            else:
                st.info("No URLs available.")
        else:
            st.error("Error fetching URLs")

    st.subheader("Get Specific URL Metadata")
    short_url_input = st.text_input("Enter short URL (e.g., 0b7a59):")
    
    if st.button("Get URL Metadata"):
        if short_url_input:
            response = requests.get(f"{API_URL}/urls/{short_url_input}")
            
            if response.status_code == 200:
                url_data = response.json()
                st.write(f"Short URL: {url_data['short_url']}")
                st.write(f"Original URL: {url_data['original_url']}")

                # Convert expiration time to local time
                expiration_time_local = utc_date_to_local(url_data['expiration_time'], user_timezone)

                # st.write(f"Expiration Time: {url_data['expiration_time']}")
                st.write(f"Expiration Time: {expiration_time_local.strftime('%Y-%m-%d %H:%M:%S')}")
            elif response.status_code == 404:
                st.error("URL not found or expired")
            else:
                st.error("Error fetching URL metadata")
        else:
            st.error("Please enter a valid short URL")


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

