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


def info(msg: str) -> None:
    print(f"{Colors.BLUE}{Icons.INFO}{Colors.DEFAULT} {msg}{Colors.DEFAULT}")


def ok(msg: str) -> None:
    print(f"{Colors.GREEN}{Icons.OK}{Colors.DEFAULT} {msg}{Colors.DEFAULT}")


def error(msg: str) -> None:
    print(f"{Colors.RED}{Icons.ERROR} {msg}{Colors.DEFAULT}")


def color_status_code(status_code: int):
    if status_code < 200:
        return f"{Colors.BLUE}{status_code}"
    if status_code < 300:
        return f"{Colors.GREEN}{status_code}"
    if status_code < 400:
        return f"{Colors.CYAN}{status_code}"
    if status_code < 500:
        return f"{Colors.YELLOW}{status_code}"
    return f"{Colors.RED}{status_code}"
