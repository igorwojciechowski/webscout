from webscout.cli import config
from webscout.webscout import WebScout


def main():
    ws = WebScout(config())
    ws.run()
