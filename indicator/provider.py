import requests
import datetime


class Provider():
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address

    def fetch_data(self):
        r1 = requests.get(
            "https://trtl.mine2gether.com/api/stats_address?address=" + self.wallet_address)
        r2 = requests.get("https://trtl.mine2gether.com/api/stats")
        return [r1.json(), r2.json()]

    def data(self):
        d = self.fetch_data()

        balance = str(int(d[0]["stats"]["balance"]) / 100) + " TRTL"

        hashes = d[0]["stats"]["hashes"]

        hashrate = d[0]["stats"]["hashrate"] + "/s"

        last_share = str(datetime.datetime.now(
        ).replace(microsecond=0) - datetime.datetime.fromtimestamp(int(d[0]["stats"]["lastShare"])).replace(microsecond=0))

        if (d[1]["pool"]["hashrate"] > 1000):
            pool_hashrate = str(round(d[1]["pool"]["hashrate"] / 1000, 2)) + " KH/s"
        else:
            pool_hashrate = str(d[1]["pool"]["hashrate"]) + " H/s"

        pool_miners = str(d[1]["pool"]["miners"])

        pool_last_block_found = str(datetime.datetime.now(
        ).replace(microsecond=0) - datetime.datetime.fromtimestamp(int(str(str(d[1]["pool"]["lastBlockFound"])[:-3]))).replace(microsecond=0))

        return {
            "balance": balance,
            "hashes": hashes,
            "hashrate": hashrate,
            "last_share": last_share,
            "pool_hashrate": pool_hashrate,
            "pool_miners": pool_miners,
            "pool_last_block_found": pool_last_block_found
        }
