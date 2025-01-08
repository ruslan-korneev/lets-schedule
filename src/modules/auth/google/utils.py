from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from src.modules.auth.google.dto import URLComponentsDTO


def construct_url(base_url: str, params: dict[str, Any]) -> str:
    """Constructs a URL from a base URL and a dictionary of parameters."""
    parsed_url = urlparse(base_url)
    query_string = urlencode(params)
    return urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, query_string, parsed_url.fragment)
    )


def destruct_url(url: str) -> URLComponentsDTO:
    """Destructs a URL into its components."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return URLComponentsDTO(
        scheme=parsed_url.scheme,
        netloc=parsed_url.netloc,
        path=parsed_url.path,
        params=parsed_url.params,
        query=query_params,
        fragment=parsed_url.fragment,
    )
