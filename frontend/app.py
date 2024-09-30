import streamlit as st
import requests


API_URL = "http://localhost:8000/api/v1"

st.title("URL Shortener")

tab1, tab2, tab3 = st.tabs(["Shorten URL", "Manage URLs", "Delete URL"])

with tab1:
    st.header("Shorten a URL")
    long_url = st.text_input("Enter the long URL:")
    expiration_time = st.number_input("Expiration time (hours, optional):", min_value=0, value=0)
    
    if st.button("Shorten URL"):
        if not long_url:
            st.error("Please enter a valid long URL.")
        else:
            # Prepare data
            data = {"original_url": long_url}
            if expiration_time > 0:
                data["expiration_time"] = expiration_time

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
            for url_data in urls:
                st.write(f"Short URL: {url_data['short_url']}")
                st.write(f"Original URL: {url_data['original_url']}")
                st.write(f"Expiration Time: {url_data['expiration_time']}")
                st.write("---")
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
                st.write(f"Expiration Time: {url_data['expiration_time']}")
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

