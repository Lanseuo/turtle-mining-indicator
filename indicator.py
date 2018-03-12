#!/usr/bin/env python3
import signal
import gi
import webbrowser
import requests
import threading
import datetime
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib

import os

WALLET = ""
ICON = os.path.realpath(__file__)[:-12] + "icon.png"


class TurtleMining():
    def __init__(self):
        pass

    def fetch_data(self):
        r1 = requests.get("https://trtl.mine2gether.com/api/stats_address?address=" + WALLET)
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


class Indicator():
    def __init__(self):
        self.turtle = TurtleMining()

        self.app = 'turtle-mining-indicator'
        self.menu = {}
        self.indicator = AppIndicator3.Indicator.new(
            self.app, ICON,
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label("Starting TurtleMining Indicator ...", self.app)
        self.update()
        GLib.timeout_add_seconds(300, self.update)

    def update(self):
        try:
            data = self.turtle.data()
            print("Updated Data")
            print(data)
            self.indicator.set_label("Pending Balance: " + data["balance"], self.app)
            self.menu["hashrate"].set_label("Hash Rate: " + data["hashrate"])
            self.menu["hashes"].set_label("Hashes: " + data["hashes"])
            self.menu["last_share"].set_label("Last Share: " + data["last_share"])
            self.menu["pool_hashrate"].set_label("Pool Hash Rate: " + data["pool_hashrate"])
            self.menu["pool_miners"].set_label("Pool Miners: " + data["pool_miners"])
            self.menu["pool_last_block_found"].set_label(
                "Pool Last Block Found: " + data["pool_last_block_found"])
        except Exception as e:
            self.indicator.set_label("An error occured", self.app)
            print(e)
        return True

    def on_update(self, source):
        self.update()

    def create_menu(self):
        menu = Gtk.Menu()

        # Hash Rate
        self.menu["hashrate"] = Gtk.MenuItem("Hash Rate")
        menu.append(self.menu["hashrate"])

        # Hash Rate
        self.menu["hashes"] = Gtk.MenuItem("Hashes")
        menu.append(self.menu["hashes"])

        # Last Share
        self.menu["last_share"] = Gtk.MenuItem("Last Share")
        menu.append(self.menu["last_share"])

        # Seperator
        menu_sep1 = Gtk.SeparatorMenuItem()
        menu.append(menu_sep1)

        # Pool Hash Rate
        self.menu["pool_hashrate"] = Gtk.MenuItem("Pool Hash Rate")
        menu.append(self.menu["pool_hashrate"])

        # Pool Miners
        self.menu["pool_miners"] = Gtk.MenuItem("Pool Miners")
        menu.append(self.menu["pool_miners"])

        # Pool Last Block Found
        self.menu["pool_last_block_found"] = Gtk.MenuItem("Pool Last Block Found")
        menu.append(self.menu["pool_last_block_found"])

        # Seperator
        menu_sep2 = Gtk.SeparatorMenuItem()
        menu.append(menu_sep2)

        # Update
        self.menu["update"] = Gtk.MenuItem("Update")
        self.menu["update"].connect("activate", self.on_update)
        menu.append(self.menu["update"])

        # Open
        self.menu["open"] = Gtk.MenuItem("Open")
        self.menu["open"].connect("activate", self.open)
        menu.append(self.menu["open"])

        # Quit
        self.menu["quit"] = Gtk.MenuItem('Quit')
        self.menu["quit"].connect('activate', self.stop)
        menu.append(self.menu["quit"])

        menu.show_all()
        return menu

    def open(self, source):
        webbrowser.open_new("https://trtl.mine2gether.com")

    def stop(self, source):
        Gtk.main_quit()


Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
