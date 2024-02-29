"""Runs a web app server"""
from jinja2 import Environment, FileSystemLoader


def create_html():
    """Use Jinja2 to create an HTML page"""
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("base.html")
    content = template.render(title="Web App Server")
    print(content)


if __name__ == "__main__":
    create_html()
