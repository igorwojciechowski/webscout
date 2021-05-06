from cli import config
from webscout import  WebScout



if __name__ == '__main__':
    ws = WebScout(config())
    ws.run()