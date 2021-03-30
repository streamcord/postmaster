from email.mime.multipart import MIMEMultipart


class Headers:

    def __init__(self, *, to_addr: list, subject, bcc: bool = True):
        """
        Generate MIME headers for an email.

        :param to_addr: A list of addresses to send the email to.
        :param subject: The email's subject.
        :param bcc: Whether or not recipients should see each others' emails in the `To` list.
        """

        self.to_addr = to_addr
        self.subject = subject
        self.bcc = bcc

    def attach(self, multipart: MIMEMultipart, from_addr: str):

        multipart['From'] = from_addr
        multipart['Subject'] = self.subject
        if not self.bcc:
            multipart['To'] = ','.join(self.to_addr)
