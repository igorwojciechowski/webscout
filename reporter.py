from jinja2 import Environment, FileSystemLoader


class Reporter:

    @staticmethod
    def generate(output: str, data: list) -> None:
        loader = FileSystemLoader(searchpath='./templates')
        env = Environment(loader=loader)
        template = env.get_template('report.html.j2')
        filename = f"{output}/webscout.html"
        with open(filename, 'w') as report:
            report.write(template.render(data=data))
