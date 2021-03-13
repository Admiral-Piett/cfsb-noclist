import os
from typing import NamedTuple


class Settings(NamedTuple):
    noclist_domain: str = os.environ.get("NOCLIST_DOMAIN", "http://localhost:8888")
    noclist_auth_request_path: str = os.environ.get(
        "NOCLIST_AUTH_REQUEST_PATH", "/auth"
    )
    noclist_users_request_path: str = os.environ.get(
        "NOCLIST_USERS_REQUEST_PATH", "/users"
    )
    request_retry_threshold: int = int(os.environ.get("REQUEST_RETRY_THRESHOLD", 3))


settings = Settings()
