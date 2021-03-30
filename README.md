# Postmaster

Send individual and bulk emails right from your applications or in a lightweight microservice.

## Requirements

### Python module

- Python 3.8

### Microservice

- Docker

## Creating templates

Postmaster uses the [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) template engine to quickly render HTML on-the-fly.
It supports the same syntax and features as Flask templates.

For email clients that don't support HTML, Postmaster will also automatically convert your templates into plain text.

For example:

```html
<p><b>Hello, {{ name }}</b></p>
<p>Your order is ready.</p>
<p>Sincerely, Aperture Science</p>
```

will render in plain text as:

```
**Hello, {{ name }}**

Your order is ready.

Sincerely, Aperture Science
```

## Using Postmaster as...

### a module

```python
import postmaster

client = postmaster.Client(
    username='noreply@aperturescience.com',
    password='emailPassword',
    smtp_host='smtp.gmail.com',
    default_from='Aperture Science <noreply@aperturescience.com>')

headers = postmaster.Headers(
    to_addr=['jane.doe@example.com'],
    subject='Your order receipt')

client.send_from_template(
    headers=headers,
    template='templates/order-receipt.html',
    jinja_env={'name': 'Jane'})

client.close()

```

### a microservice

```shell
git clone https://github.com/streamcord/postmaster.git
cd postmaster
docker build -t postmaster:latest .
docker run -d \
  -e POSTMASTER_TOKEN=$POSTMASTER_TOKEN \
  -v "$(pwd)"/templates:/app/templates:ro \
  -h postmaster \
  --name postmaster \
  postmaster:latest
```

Then, to send an email:

```python
import requests

POSTMASTER_TOKEN = 'your_token_here'

req = requests.post(
    'http://postmaster/emails/@new',
    headers={
        'Authorization': POSTMASTER_TOKEN
    },
    data={
        'bcc': False,
        'env': {
            'name': 'John'
        },
        'from': 'Aperture Science <noreply@aperturescience.com>',
        'subject': 'Hello, world!',
        'template': 'order-receipt.html',
        'to': ['john.doe@example.com']
   })

assert req.status_code == 204
```