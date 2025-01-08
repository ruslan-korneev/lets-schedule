from urllib.parse import quote_plus

from src.modules.auth.google.utils import construct_url, destruct_url


def test_url_with_basic_parameters() -> None:
    base_url = "https://example.com/api"
    params = {"param1": "value1", "param2": "value2", "param3": "value3"}
    expected_url = "https://example.com/api?param1=value1&param2=value2&param3=value3"
    assert construct_url(base_url, params) == expected_url


def test_url_with_empty_parameters() -> None:
    base_url = "https://example.com/api"
    expected_url = "https://example.com/api"
    assert construct_url(base_url, {}) == expected_url


def test_url_with_existing_query() -> None:
    base_url = "https://example.com/api?existing_param=existing_value"
    params = {"param1": "value1"}
    expected_url = "https://example.com/api?param1=value1"
    assert construct_url(base_url, params) == expected_url


def test_url_with_special_characters() -> None:
    base_url = "https://example.com/api"
    params = {"param1": "value with spaces", "param2": "valúe&special=chars"}
    constructed_url = construct_url(base_url, params)
    assert quote_plus("value with spaces") in constructed_url
    assert "val%C3%BAe%26special%3Dchars" in constructed_url


def test_destruct_url() -> None:
    constructed_url = "https://example.com/api?param1=value1&param2=value2&param3=value3"
    expected_components = {
        "scheme": "https",
        "netloc": "example.com",
        "path": "/api",
        "query": {"param1": ["value1"], "param2": ["value2"], "param3": ["value3"]},
    }
    destructed_url = destruct_url(constructed_url)
    assert destructed_url.scheme == expected_components["scheme"]
    assert destructed_url.netloc == expected_components["netloc"]
    assert destructed_url.path == expected_components["path"]
    assert destructed_url.query == expected_components["query"]


def test_url_with_fragment() -> None:
    base_url = "https://example.com/page#section1"
    params = {"param": "value"}
    expected_url = "https://example.com/page?param=value#section1"
    assert construct_url(base_url, params) == expected_url


def test_destruct_url_with_fragment() -> None:
    constructed_url = "https://example.com/page?param=value#section1"
    expected_components = {
        "scheme": "https",
        "netloc": "example.com",
        "path": "/page",
        "query": {"param": ["value"]},
        "fragment": "section1",
    }
    destructed_url = destruct_url(constructed_url)
    assert destructed_url.scheme == expected_components["scheme"]
    assert destructed_url.netloc == expected_components["netloc"]
    assert destructed_url.path == expected_components["path"]
    assert destructed_url.query == expected_components["query"]
    assert destructed_url.fragment == expected_components["fragment"]
