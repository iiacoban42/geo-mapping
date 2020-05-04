from unittest import TestCase
from nose.tools import assert_true, assert_false
from mock import Mock
import requests


class TestSimpleHTTPRequestHandler(TestCase):
    def test_get_request_response(self):
        mock_server = Mock()
        url = 'http://localhost:8000'
        # Send a request to the mock API server and store the response.
        response = mock_server.get(url)
        # Confirm that the request-response cycle completed successfully.
        assert_true(response.ok)

