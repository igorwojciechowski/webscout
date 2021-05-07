import os

from jinja2 import Environment, FileSystemLoader

from webscout import cli


class Reporter:

    @staticmethod
    def generate(output: str, data: list) -> None:
        cli.info(f'Generating report...')
        loader = FileSystemLoader(searchpath='./templates')
        env = Environment(loader=loader)
        template = env.get_template('report.html.j2')
        filename = os.path.abspath(f"{output}/webscout.html")
        with open(filename, 'w') as report:
            report.write(template.render(data=data))
        cli.ok(f'Report saved to: {filename}')
