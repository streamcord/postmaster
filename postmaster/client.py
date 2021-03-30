import smtplib
from .errors import *
from .headers import Headers
from .message import build_from_template


class Client:

    def __init__(self, *, username: str, password: str, smtp_host: str, smtp_port: int = 587, default_from: str = None):
        """
        Initialize a Postmaster client and connect to the SMTP server.

        :param username: Email to log in with.
        :param password: Password to log in with.
        :param smtp_host: SMTP host server.
        :param smtp_port: SMTP host server port.
        :param default_from: Default email `from` address. Example: `John Doe <john.doe@example.com>`
        """

        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._default_from = default_from

        self.smtp = smtplib.SMTP(smtp_host, smtp_port)
        self.smtp.starttls()

        self.smtp.login(username, password)

    def close(self):
        """Close connection to the SMTP server."""
        self.smtp.quit()

    def send_from_template(self, *, headers: Headers, template: str, jinja_env: dict = None, from_addr: str = None):

        from_addr = from_addr or self._default_from
        if not from_addr:
            raise InvalidSenderError('A from address must be specified if no `default_from` was configured')

        content = build_from_template(template, jinja_env)

        # Add subject, to, and from to the message content
        headers.attach(content, from_addr)

        print(headers.to_addr)
        return self.smtp.send_message(content, from_addr, headers.to_addr)
