from webscout.cli import config
from webscout.webscout import WebScout

__version__ = '0.1'


def main():
    ws = WebScout(config())
    ws.run()
