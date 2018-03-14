import requests
import datetime


class Provider():
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address

    def fetch_data(self):
        return [{}, {}]

    def data(self):
        d = self.fetch_data()

        balance = str(int(d[0]["stats"]["balance"]) / 100) + " TRTL"

        hashes = d[0]["stats"]["hashes"]

        if d[0]["stats"].get("hashrate"):
            hashrate = d[0]["stats"].get("hashrate") + "/sec"
        else:
            hashrate = "0 H/sec"

        last_share = str(datetime.datetime.now(
        ).replace(microsecond=0) - datetime.datetime.fromtimestamp(int(d[0]["stats"]["lastShare"])).replace(microsecond=0))
        last_share += " ago"

        if (d[1]["pool"]["hashrate"] > 1000):
            pool_hashrate = str(round(d[1]["pool"]["hashrate"] / 1000, 2)) + " KH/sec"
        else:
            pool_hashrate = str(d[1]["pool"]["hashrate"]) + " H/sec"

        pool_miners = str(d[1]["pool"]["miners"])

        pool_last_block_found = str(datetime.datetime.now(
        ).replace(microsecond=0) - datetime.datetime.fromtimestamp(int(str(str(d[1]["pool"]["lastBlockFound"])[:-3]))).replace(microsecond=0))
        pool_last_block_found += " ago"

        return {
            "balance": balance,
            "hashes": hashes,
            "hashrate": hashrate,
            "last_share": last_share,
            "pool_hashrate": pool_hashrate,
            "pool_miners": pool_miners,
            "pool_last_block_found": pool_last_block_found
        }
