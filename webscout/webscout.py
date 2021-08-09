import os
import sys
import uuid

import requests
import re

from multiprocessing import pool as mpool

from requests import Response
from selenium.webdriver import Chrome, ChromeOptions

from webscout.reporter import Reporter
from webscout import cli


class WebScout:

    def __init__(self, config) -> None:
        self.report_dir, self.threads, self.timeout = config
        self.urls = self.read_urls()
        self.data = []

    def driver(self) -> Chrome:
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = Chrome(options=options)
        driver.set_window_size(1920, 1080)
        driver.set_page_load_timeout(self.timeout)
        return driver

    def run(self) -> None:
        self.create_report_directory(self.report_dir)
        pool = mpool.ThreadPool(self.threads)
        for url in self.urls:
            pool.apply_async(self.scout, args=(url,))
        pool.close()
        pool.join()
        Reporter.generate(self.report_dir, self.data)

    def scout(self, url: str) -> None:
        probe_data = self.probe(url)
        screenshot_file = self.take_screenshot(url)
        self.data.append({
            **probe_data,
            'screenshot': screenshot_file
        })

    def probe(self, url: str) -> dict:
        cli.info(f'Probing url: {url}...')
        try:
            response = requests.get(self.prepare_url(url), timeout=self.timeout)
            cli.ok(f'Status code for {url}: {cli.color_status_code(response.status_code)}')
        except:
            cli.error(f'{url} request failed')
        filename = os.path.abspath(f'{self.report_dir}/responses/{uuid.uuid4()}.http')
        with open(filename, 'w') as f:
            f.write(self.parse_response(response))
        cli.ok(f'Response from {url} saved to {os.path.basename(filename)}')
        return {
            'url': url,
            'status_code': response.status_code,
            'headers': response.headers,
            'body': response
        }

    def take_screenshot(self, url: str) -> str:
        d = self.driver()
        cli.info(f'Taking screenshot of {url}...')
        try:
            d.get(self.prepare_url(url))
            filename = f"{uuid.uuid4()}.png"
            path = os.path.abspath(f"{self.report_dir}/screenshots/{filename}")
            d.save_screenshot(path)
            cli.ok(f'Screenshot for {url} successfully saved to {os.path.basename(filename)}')
        except:
            cli.error(f'Screenshot of {url} failed')
        d.close()
        return filename

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
    def create_report_directory(path: str) -> None:
        if not os.path.exists(path):
            for directory in [
                f"{path}/",
                f"{path}/screenshots",
                f"{path}/responses"
            ]:
                os.makedirs(directory)

    @staticmethod
    def prepare_url(url: str) -> str:
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
    def parse_response(response: Response) -> str:
        headers = '\r\n'.join(f'{k}: {v}' for k, v in response.headers.items())
        body = response.text
        return f"HTTP/1.1 {response.status_code} {response.reason}\nHost: {response.url}\n{headers}\n{body}\n"
