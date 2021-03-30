from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html2text import HTML2Text
from jinja2 import Template

html_parser = HTML2Text()


def build_from_template(source: str, jinja_env: dict = None) -> MIMEMultipart:
    """
    Build an email from a Jinja template and create a MIMEMultipart containing the resulting HTML and alternative text.

    :param source: Path to the template file.
    :param jinja_env: Jinja context.
    :return: A MIMEMultipart containing the rendered message.
    """

    jinja_env = jinja_env or {}

    multipart = MIMEMultipart('alternative')

    with open(source, 'r') as f:
        html = f.read()

    template = Template(html)

    html = template.render(**jinja_env)
    html_mime = MIMEText(html, 'html')
    multipart.attach(html_mime)

    # generate alt text from HTML
    text = html_parser.handle(html)
    text_mime = MIMEText(text, 'text')
    multipart.attach(text_mime)

    return multipart
