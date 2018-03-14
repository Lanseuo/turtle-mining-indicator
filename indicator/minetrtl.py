import requests
import datetime

from .provider import Provider


class MineTRTL(Provider):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address

    def fetch_data(self):
        r1 = requests.get(
            "http://159.65.171.69:8117/stats_address?address=" + self.wallet_address)
        r2 = requests.get("http://159.65.171.69:8117/live_stats")
        return [r1.json(), r2.json()]
