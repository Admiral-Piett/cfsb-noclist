import json
import sys
from unittest import TestCase
from unittest.mock import Mock, patch

from app import NoclistRetriever
from noclist_app.clients.noclist_client import NoclistClient


class NoclistRetrieverTests(TestCase):
    def setUp(self):
        self.noclist_client_mock: NoclistClient = Mock(spec=NoclistClient)
        self.noclist_client_mock.get_authentication_token.return_value = "12345"
        self.noclist_client_mock.get_users.return_value = "1111111111\n2222222222"

        self.noclist_retriver_app = NoclistRetriever(
            noclist_client=self.noclist_client_mock
        )

    @patch("app.sys", wraps=sys)
    def test__main_success(self, spy):
        self.noclist_retriver_app.main()

        self.noclist_client_mock.get_authentication_token.assert_called_once()
        self.noclist_client_mock.get_users.assert_called_once_with("12345")

        app_stdout_response = spy.stdout.mock_calls[0]
        self.assertEqual(
            json.dumps(["1111111111", "2222222222"]), app_stdout_response.args[0]
        )
