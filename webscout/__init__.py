from webscout.cli import config, print_banner
from webscout.webscout import WebScout

__version__ = '0.1'


def main():
    print_banner()
    ws = WebScout(config())
    ws.run()
