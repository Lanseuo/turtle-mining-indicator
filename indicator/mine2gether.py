import requests
import datetime

from .provider import Provider


class Mine2GetherProvider(Provider):
    """trtl.mine2gether.com"""

    def __init__(self, wallet_address):
        self.wallet_address = wallet_address

    def fetch_data(self):
        r1 = requests.get(
            "https://trtl.mine2gether.com/api/stats_address?address=" + self.wallet_address)
        r2 = requests.get("https://trtl.mine2gether.com/api/stats")
        return [r1.json(), r2.json()]
