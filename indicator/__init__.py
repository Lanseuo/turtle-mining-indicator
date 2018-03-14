import gi
import os
import signal
import sys
import webbrowser

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3, GLib

from .mine2gether import Mine2GetherProvider
from .minetrtl import MineTRTL


try:
    provider = sys.argv[1]
    wallet_address = sys.argv[2]
except IndexError:
    print("Usage: indicator.py PROVIDER WALLETADDRESS")
    quit()

providers = ["mine2gether", "minetrtl"]
if provider not in providers:
    print("The provider '" + provider + "' is currently not supported. A list of all supported prodivers can be found on https://github.com/Lanseuo/turtle-mining-indicator. Create an issue and request support for your provider.")
    quit()


class Indicator():
    def __init__(self, provider, wallet_address):
        self.app = 'turtle-mining-indicator'
        self.indicator = AppIndicator3.Indicator.new(
            self.app,
            os.path.realpath(__file__)[:-21] + "icon.png",
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.menu = {}
        self.indicator.set_menu(self.create_menu())

        self.choose_provider(provider, wallet_address)

        self.update()
        GLib.timeout_add_seconds(300, self.update)

    def choose_provider(self, provider, wallet_address):
        if provider == "mine2gether":
            self.turtle = Mine2GetherProvider(wallet_address)
        elif provider == "minetrtl":
            self.turtle = MineTRTL(wallet_address)

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


Indicator(provider, wallet_address)
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
