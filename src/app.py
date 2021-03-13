import json
import sys

from noclist_app.clients.noclist_client import NoclistClient


class NoclistRetriever:
    def __init__(self, noclist_client=None):
        # If we pass in an initialized client we can use it here (in our case a mocked out one for testing purposes)
        # or just create a new one by default.
        self.noclist_client: NoclistClient = noclist_client or NoclistClient()

    def main(self):
        print("GetNoclistStart", file=sys.stderr)

        # Authentication via noclist app
        auth_token = self.noclist_client.get_authentication_token()
        # Call for noclist users
        users_response_body = self.noclist_client.get_users(auth_token)

        # Split the response string on newline characters and turn into an array.
        users_list = users_response_body.split("\n")

        # Dump data array to json format and return via stdout
        print(json.dumps(users_list), file=sys.stdout)
        print("GetNoclistComplete", file=sys.stderr)


if __name__ == "__main__":
    nr = NoclistRetriever()
    nr.main()
