# Postmaster

A versatile email manager that uses the gmail API.

#### Why the gmail API?

Because Google Workspace security policies are excessive.

## Requirements
- Python 3.8 (or Docker, if running as a microservice)
- A gmail or Google Workspace account
- A Google OAuth application (and the `credentials.json` from it)

### How to set up an OAuth application

1. [Create a project and enable an API](https://developers.google.com/workspace/guides/create-project)
2. [Create credentials](https://developers.google.com/workspace/guides/create-credentials)
   - [Using OAuth 2.0 for Server to Server Applications](https://developers.google.com/identity/protocols/oauth2/service-account#python_2)

## Usage

### As a microservice

Running Postmaster as a microservice is recommended if you're using multiple applications to prevent API token conflicts.

```shell
git clone https://github.com/streamcord/postmaster.git
cd postmaster
docker build -t postmaster:latest .
docker run -d \
  -e POSTMASTER_TOKEN=$POSTMASTER_TOKEN \
  -v "$(pwd)"/templates:/app/templates:ro \
  -v "$(pwd)"/credentials.json:/app/credentials.json:ro \
  -v "$(pwd)"/token.json:/app/token.json \
  -h postmaster \
  --name postmaster \
  postmaster:latest
```

Then, to send an email:

```python3
import requests

POSTMASTER_TOKEN = 'your_token_here'

req = requests.post(
  'http://postmaster/emails/@new',
  headers={
    'Authorization': POSTMASTER_TOKEN
  },
  data={
    'from': 'ACME Corp <noreply@acme.com>',
    'subject': 'Hello, world!',
    'template': 'new_user.html',
    'to': 'johndoe@mee6.xyz'
  })

assert req.status_code == 204
```

### As a Python module

```python3
import postmaster

mailman = postmaster.create_service(
    credentials_file='credentials.json',
    token_file='token.json')

content = postmaster.message.build_from_template('templates/test.html')
content['from'] = 'John Doe <johndoe@example.com>'
content['to'] = 'janedoe@example.org'
content['subject'] = 'A love letter'

msg = postmaster.send_message(mailman, content)
print(msg)
```
