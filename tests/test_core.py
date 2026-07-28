"""Tests standard tap features using the built-in SDK tests library.

Copyright (c) 2026 Meltano.
"""

import requests
from singer_sdk.testing import get_tap_test_class

from tap_adp.client import ADPPaginator
from tap_adp.tap import TapADP

SAMPLE_CONFIG = {
    "client_id": "test",
    "client_secret": "test",
    "cert_public": "test",
    "cert_private": "test",
}


TestTapADP = get_tap_test_class(
    TapADP,
    config=SAMPLE_CONFIG,
    include_tap_tests=False,
    include_stream_tests=False,
    include_stream_attribute_tests=False,
)


class TestADPPaginator:
    """Test ADP paginator."""

    def test_get_next(self) -> None:
        """Test get next."""
        paginator = ADPPaginator(start_value=0, page_size=100)
        response = requests.Response()
        response.status_code = 200
        response._content = b'{"foo": "bar"}'  # ruff: ignore[private-member-access]

        paginator.advance(response)
        assert paginator.current_value == 100  # ruff: ignore[magic-value-comparison]

        paginator.advance(response)
        assert paginator.current_value == 200  # ruff: ignore[magic-value-comparison]

    def test_has_more(self) -> None:
        """Test has more."""
        paginator = ADPPaginator(start_value=0, page_size=100)
        response = requests.Response()
        response.status_code = 200
        response._content = b'{"next": 100}'  # ruff: ignore[private-member-access]
        assert paginator.has_more(response)

    def test_has_more_no_content(self) -> None:
        """Test has more no content."""
        paginator = ADPPaginator(start_value=0, page_size=100)
        response = requests.Response()
        response.status_code = 204
        assert not paginator.has_more(response)
