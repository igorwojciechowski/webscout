from argparse import ArgumentParser


class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    DEFAULT = '\033[0m'


class Icons:
    INFO = ''
    OK = ''
    ERROR = ''
    ARROW = '➡'


def config() -> (str, int):
    argparser = ArgumentParser()
    argparser.add_argument('-o', '--output', default='webscout_report')
    argparser.add_argument('-t', '--threads', default=5, type=int)
    args = argparser.parse_args()
    return args.output, args.threads


def info(msg: str):
    print(f"{Colors.BLUE}{Icons.INFO}{Colors.DEFAULT} {msg}")


def ok(msg: str):
    print(f"{Colors.GREEN}{Icons.OK}{Colors.DEFAULT} {msg}")


def error(msg: str):
    print(f"{Colors.RED}{Icons.ERROR} {msg}")


def req_info(url: str):
    info(f"Request {Icons.ARROW} {Colors.CYAN}{url}")


def req_ok(url: str, status_code: int):
    ok(f"Request {Icons.ARROW} {Colors.CYAN}{url} {Colors.DEFAULT}{Icons.ARROW} {color_status(status_code)}")


def req_error(url: str):
    error(f"Request {Icons.ARROW} {Colors.CYAN}{url} {Colors.RED}failed!")


def screenshot_info(url: str):
    info(f"Screenshot {Icons.ARROW} {Colors.CYAN}{url}")


def screenshot_ok(url: str):
    ok(f"Screenshot {Icons.ARROW} {Colors.CYAN}{url} {Colors.GREEN}ok")


def screenshot_error(url: str):
    error(f"Could not take screenshot for {Colors.CYAN}{url}")


def color_status(status: int):
    if status < 200:
        return f"{Colors.BLUE}{status}"
    if status < 300:
        return f"{Colors.GREEN}{status}"
    if status < 400:
        return f"{Colors.CYAN}{status}"
    if status < 500:
        return f"{Colors.YELLOW}{status}"
    return f"{Colors.RED}{status}"
