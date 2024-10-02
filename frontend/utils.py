from datetime import datetime, time
from zoneinfo import ZoneInfo
from streamlit_js_eval import streamlit_js_eval
import validators
import re
from urllib.parse import urlparse, urlunparse, unquote

def is_valid_url(url: str) -> bool:
    # Regex to check if the URL is a valid domain with optional path
    domain_with_path_regex = re.compile(
        r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/.*)?$"  # Matches 'google.com' and 'google.com/some-path'
    )
    
    parsed_url = urlparse(url)
    
    # If the URL has a valid scheme (http or https), it's valid
    if parsed_url.scheme in ['http', 'https']:
        return True
    
    # If the URL matches a domain with optional path, allow it
    if domain_with_path_regex.match(url):
        return True
    
    return False

'''
def is_valid_url(url):
    """
    Checks if a URL is valid.
    
    Parameters:
    url (str): The URL to check.
    
    Returns:
    bool: True if the URL is valid, False otherwise.
    """
    return validators.url(url)
'''

def get_user_timezone():
    """
    Retrieves the user's local timezone using JavaScript.
    
    Returns:
    str: The local timezone of the user.
    """
    return streamlit_js_eval(js_expressions="Intl.DateTimeFormat().resolvedOptions().timeZone", key="get_timezone")


def local_date_to_utc(date):
    """
    Converts a local date to a UTC datetime.
    
    Parameters:
    date (datetime.date): The local date to convert.
    
    Returns:
    str: The UTC datetime in ISO 8601 format.
    """
    local_datetime = datetime.combine(date, time.max)  # Sets the time to 23:59:59
    utc_datetime = local_datetime.astimezone(ZoneInfo("UTC"))
    return utc_datetime.isoformat()

def utc_date_to_local(date, local_tz_str):
    """
    Converts a UTC datetime to a local datetime in the specified timezone.
    
    Parameters:
    date (str): The UTC datetime in ISO 8601 format.
    local_tz_str (str): The local timezone as a string (e.g., "America/New_York").
    
    Returns:
    datetime: The local datetime in the specified timezone.
    """
    utc_datetime = datetime.fromisoformat(date).replace(tzinfo=ZoneInfo("UTC"))
    local_datetime = utc_datetime.astimezone(ZoneInfo(local_tz_str))
    return local_datetime