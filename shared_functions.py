from colorama import Style
from requests import Response
import json
import requests

def get_response(url: str, isencapsulated: bool = True) -> dict:
    """Gets the JSON response from the URL, and parses it as a dictionary.\n
    Optionally takes a boolean to determine whether the response is encapsulated in the `payload` key.\n
    If the bool is true (default -- since most responses are), then the contents of the `payload` key is returned.\n
    Otherwise, the full response is returned."""
    response: Response = requests.get(url)
    json_dict: dict = json.loads(response.text)
    if isencapsulated:
        # All info is encapsulated in the `payload` key for most responses
        return json_dict['payload']
    else:
        # But for the couple things that aren't encapsulated in the `payload` key, we can just pass False to the function
        return json_dict

class StyleApplyer:
    foreground: str
    style: str
    reset: str

    def __init__(self, foreground, style: str):
        self.foreground = foreground
        self.style = style
        self.reset = Style.RESET_ALL

    def Apply(self, val: str) -> str:
        return self.foreground + self.style + val + self.reset