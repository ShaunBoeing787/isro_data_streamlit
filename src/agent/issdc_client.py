import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


class ISSDCClient:

    LOGIN_URL = (
        "https://idp.issdc.gov.in/auth/realms/issdc/protocol/openid-connect/auth"
        "?response_type=code"
        "&client_id=al1-pradan-1"
        "&redirect_uri=https%3A%2F%2Fpradan1.issdc.gov.in%2Fal1%2Fprotected%2Fbrowse.xhtml"
        "&login=true"
        "&scope=openid"
    )

    def __init__(self):

        load_dotenv()

        self.username = os.getenv("ISSDC_USERNAME")
        self.password = os.getenv("ISSDC_PASSWORD")

        self.session = requests.Session()

    def login(self):

        print("Opening login page...")

        response = self.session.get(self.LOGIN_URL)

        if response.status_code != 200:
            raise Exception("Could not open login page")

        soup = BeautifulSoup(response.text, "html.parser")

        form = soup.find("form", {"id": "kc-form-login"})

        if form is None:
            raise Exception("Login form not found")

        action_url = form["action"]

        print("Found login form")

        payload = {
            "username": self.username,
            "password": self.password,
            "credentialId": ""
        }

        print("Submitting credentials...")

        login_response = self.session.post(
            action_url,
            data=payload,
            allow_redirects=True
        )

        final_url = login_response.url

        print("Final URL:")
        print(final_url)

        if "browse.xhtml" in final_url:
            print("Login successful")
            return True

        print("Login failed")
        return False


if __name__ == "__main__":

    client = ISSDCClient()

    success = client.login()

    print("SUCCESS =", success)