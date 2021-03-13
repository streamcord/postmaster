import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import Resource
from jinja2 import Template


def build_from_template(source: str, ctx: dict = None) -> MIMEText:
    """
    Load a file and render its Jinja template.

    :param source: Path to the template file.
    :param ctx: Jinja context.
    :return: The resulting MIMEText.
    """

    ctx = ctx or {}

    with open(source, 'r') as f:
        html = f.read()
        template = Template(html)
        html = template.render(**ctx)

        return MIMEText(html, 'html')


def send_message(service: Resource, message: MIMEText) -> dict:
    """
    Send an email via the gmail API.

    :param service: The gmail API manager.
    :param message: The message content.
    :return: Information about the message sent.
    """

    raw = {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('utf-8')}
    from_addr = message['from'].split('<')[1].split('>')[0]

    message = service.users().messages().send(userId=from_addr, body=raw).execute()
    print(message['id'])
    return message
