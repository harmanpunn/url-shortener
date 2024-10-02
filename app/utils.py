from urllib.parse import urlparse, urlunparse, unquote
import re

def normalize_url(original_url: str) -> str:
    parsed_url = urlparse(original_url)

    # If no scheme is present, default to 'http'
    if not parsed_url.scheme:
        if original_url.startswith("www.") or re.match(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/.*)?$", original_url):
            original_url = "http://" + original_url
        else:
            original_url = "http://" + original_url  # Default to http if no scheme

        parsed_url = urlparse(original_url)

    decoded_path = unquote(parsed_url.path)
    decoded_query = unquote(parsed_url.query)

    normalized_url = urlunparse((
        parsed_url.scheme, 
        parsed_url.netloc.lower(), 
        decoded_path,
        parsed_url.params,
        decoded_query,  
        parsed_url.fragment
    ))

    return normalized_url