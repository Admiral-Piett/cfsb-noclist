import sys

import requests

from noclist_app.clients import retry_wrapper
from hashlib import sha256
from noclist_app.settings import settings

AUTH_TOKEN_HEADER = "Badsec-Authentication-Token"
USERS_CHECKSUM_HEADER = "X-Request-Checksum"


def generate_request_checksum(token, request_path):
    plain_text = f"{token}{request_path}".encode("utf-8")
    return sha256(plain_text).hexdigest()


class NoclistClient:
    @retry_wrapper
    def get_authentication_token(self):
        print("GetAuthStart", file=sys.stderr)
        url = f"{settings.noclist_domain}{settings.noclist_auth_request_path}"
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPError(
                f"GetAuthFailure - HTTP ERROR - response_status_code: {response.status_code}, response_headers: {response.headers}"
            )
        auth_token = response.headers.get(AUTH_TOKEN_HEADER)
        if not auth_token:
            raise HTTPError(
                f"GetAuthFailure - INVALID HEADERS - response_status_code: {response.status_code}, response_headers: {response.headers}"
            )
        print(f"GetAuthSuccess - {auth_token}", file=sys.stderr)
        return auth_token

    @retry_wrapper
    def get_users(self, token):
        print("GetUsersStart", file=sys.stderr)
        request_checksum = generate_request_checksum(
            token, settings.noclist_users_request_path
        )

        headers = {USERS_CHECKSUM_HEADER: request_checksum}
        url = f"{settings.noclist_domain}{settings.noclist_users_request_path}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPError(
                f"GetUsersFailure - HTTP ERROR - response_status_code: {response.status_code}, response_body: {response.text}"
            )
        response_body = response.text
        if not response_body:
            raise HTTPError(
                f"GetUsersFailure - INVALID RESPONSE - response_status_code: {response.status_code}, response_body: {response.text}"
            )
        print(f"GetUsersSuccess - {response_body}", file=sys.stderr)
        return response_body


class HTTPError(Exception):
    pass
