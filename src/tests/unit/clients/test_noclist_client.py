from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch

import requests
from requests import Response

from noclist_app.clients.noclist_client import (
    NoclistClient,
    AUTH_TOKEN_HEADER,
    USERS_CHECKSUM_HEADER,
)

AUTH_TOKEN = "12345"
USERS_RESPONSE = "1111111111\n2222222222"
USERS_CHECKSUM = "c20acb14a3d3339b9e92daebb173e41379f9f2fad4aa6a6326a696bd90c67419"


class NoclistRetrieverTests(TestCase):
    def setUp(self):
        self.noclist_client = NoclistClient()

        # Here we create fake response objects to return from the request calls.
        self.auth_token_response = Response()
        self.auth_token_response.status_code = 200
        self.auth_token_response.headers = {AUTH_TOKEN_HEADER: AUTH_TOKEN}

        self.users_response = Response()
        self.users_response.status_code = 200
        # This is a little wonky to set a private attribute, but we need to set this this way so that the response
        # will be accurate to what the nocserver is expected to return.
        self.users_response._content = deepcopy(USERS_RESPONSE).encode("utf-8")

        # Create a mock for requests that we can re-build for all subsequent tests.
        self.requests_patcher = patch(
            "noclist_app.clients.noclist_client.requests", spec=requests
        )
        self.requests_mock = self.requests_patcher.start()

    def tearDown(self):
        self.requests_patcher.stop()

    def test__get_authentication_token_success(self):
        self.requests_mock.get.return_value = self.auth_token_response
        token = self.noclist_client.get_authentication_token()

        self.requests_mock.get.assert_called_once_with("http://localhost:8888/auth")
        self.assertEqual(AUTH_TOKEN, token)

    def test__get_authentication_token_400_causes_retry(self):
        failure_response = deepcopy(self.auth_token_response)
        failure_response.status_code = 400
        self.requests_mock.get.side_effect = [
            failure_response,
            self.auth_token_response,
        ]
        token = self.noclist_client.get_authentication_token()

        self.assertEqual(2, self.requests_mock.get.call_count)
        self.assertEqual(AUTH_TOKEN, token)

    def test__get_authentication_token_missing_token_in_header_causes_retry(self):
        failure_response = deepcopy(self.auth_token_response)
        failure_response.headers = {}
        self.requests_mock.get.side_effect = [
            failure_response,
            self.auth_token_response,
        ]
        token = self.noclist_client.get_authentication_token()

        self.assertEqual(2, self.requests_mock.get.call_count)
        self.assertEqual(AUTH_TOKEN, token)

    def test__get_authentication_token_exception_causes_retry(self):
        failure_response = deepcopy(self.auth_token_response)
        failure_response.status_code = 400
        self.requests_mock.get.side_effect = [
            failure_response,
            self.auth_token_response,
        ]
        token = self.noclist_client.get_authentication_token()

        self.assertEqual(2, self.requests_mock.get.call_count)
        self.assertEqual(AUTH_TOKEN, token)

    def test__get_authentication_token_retries_3_times_then_exits_app_code_1(self):
        self.requests_mock.get.side_effect = [Exception, Exception, Exception]
        with self.assertRaises(SystemExit) as exit_error:
            self.noclist_client.get_authentication_token()

        self.assertEqual(3, self.requests_mock.get.call_count)
        self.assertEqual(1, exit_error.exception.code)

    def test__get_users_success(self):
        self.requests_mock.get.return_value = self.users_response
        response = self.noclist_client.get_users(AUTH_TOKEN)

        self.requests_mock.get.assert_called_once_with(
            "http://localhost:8888/users",
            headers={USERS_CHECKSUM_HEADER: USERS_CHECKSUM},
        )
        self.assertEqual(USERS_RESPONSE, response)

    def test__get_users_400_causes_retry(self):
        failure_response = deepcopy(self.users_response)
        failure_response.status_code = 400
        self.requests_mock.get.side_effect = [failure_response, self.users_response]
        response = self.noclist_client.get_users(AUTH_TOKEN)

        self.assertEqual(2, self.requests_mock.get.call_count)
        self.assertEqual(USERS_RESPONSE, response)

    def test__get_users_500_causes_retry(self):
        failure_response = deepcopy(self.users_response)
        failure_response.status_code = 500
        self.requests_mock.get.side_effect = [failure_response, self.users_response]
        response = self.noclist_client.get_users(AUTH_TOKEN)

        self.assertEqual(2, self.requests_mock.get.call_count)
        self.assertEqual(USERS_RESPONSE, response)

    def test__get_users_missing_response_text_causes_retry(self):
        failure_response = deepcopy(self.users_response)
        failure_response._content = None
        self.requests_mock.get.side_effect = [failure_response, self.users_response]
        response = self.noclist_client.get_users(AUTH_TOKEN)

        self.assertEqual(2, self.requests_mock.get.call_count)
        self.assertEqual(USERS_RESPONSE, response)

    def test__get_users_exception_causes_retry(self):
        self.requests_mock.get.side_effect = [Exception, self.users_response]
        response = self.noclist_client.get_users(AUTH_TOKEN)

        self.assertEqual(2, self.requests_mock.get.call_count)
        self.assertEqual(USERS_RESPONSE, response)

    def test__get_users_retries_3_times_then_exits_app_code_1(self):
        self.requests_mock.get.side_effect = [Exception, Exception, Exception]
        with self.assertRaises(SystemExit) as exit_error:
            self.noclist_client.get_users(AUTH_TOKEN)

        self.assertEqual(3, self.requests_mock.get.call_count)
        self.assertEqual(1, exit_error.exception.code)
