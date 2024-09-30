from urllib.parse import urlparse, urlunparse, unquote


def normalize_url(original_url: str) -> str:

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