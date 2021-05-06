import os
import sys
import uuid

import requests
import re

from multiprocessing import pool as mpool
from selenium.webdriver import Chrome, ChromeOptions

import cli
from reporter import Reporter


class WebScout:

    def __init__(self, config) -> None:
        self.report_dir, self.threads = config
        self.urls = self.read_urls()
        self.data = []

    def run(self) -> None:
        self.create_report_directory(self.report_dir)
        pool = mpool.ThreadPool(self.threads)
        for url in self.urls:
            pool.apply_async(self.scout, args=(url,))
        pool.close()
        pool.join()
        Reporter.generate(self.report_dir, self.data)

    def scout(self, url: str):
        probe_data = self.probe(url)
        screenshot_data = self.take_screenshot(self.report_dir, url)
        self.data.append({
            **probe_data,
            'screenshot': screenshot_data
        })

    def probe(self, url: str) -> dict:
        cli.req_info(url)
        try:
            response = requests.get(self.create_url(url))
            cli.req_ok(url, response.status_code)
        except:
            cli.req_error(url)
        return {
            'url': url,
            'status_code': response.status_code,
            'headers': response.headers,
            'body': response
        }

    def take_screenshot(self, path: str, url: str) -> str:
        d = self.driver()
        cli.screenshot_info(url)
        try:
            d.get(url)
            filename = f"{uuid.uuid4()}.png"
            path = f"{path}/screenshots/{filename}"
            d.save_screenshot(path)
            cli.screenshot_ok(url)
        except:
            cli.screenshot_error(url)
        d.close()
        return filename

    @staticmethod
    def create_url(url: str) -> str:
        protocol = re.search('(https?)', url)
        domain = re.search('([A-z0-9-]*\.){1,}[a-z]{0,3}', url)
        port = re.search('(?<=:)([0-9]{1,5})', url)
        port = port.group(0) if port else ''
        if not domain:
            print('No domain!')
            sys.exit(1)
        domain = domain.group(0)
        if not protocol:
            protocol = 'https' if port == '443' else 'http'
        else:
            protocol = 'https' if port == '443' else protocol.group(0)
        if port == '443' or port == '80' or not port:
            return f"{protocol}://{domain}"
        return f"{protocol}://{domain}:{port}"

    @staticmethod
    def create_report_directory(path: str) -> None:
        if not os.path.exists(path):
            for _ in [
                f"{path}/",
                f"{path}/screenshots",
                f"{path}/responses"
            ]:
                os.makedirs(_)

    @staticmethod
    def read_urls() -> [str]:
        urls = []
        if not sys.stdin.isatty():
            for url in sys.stdin:
                urls.append(url.strip())
            return urls
        else:
            print("Stdin empty")
            sys.exit(1)

    @staticmethod
    def driver() -> Chrome:
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = Chrome(options=options)
        driver.set_window_size(1920, 1080)
        return driver
