# Postmaster

Easily send emails via the gmail API.

## Requirements
- Python 3.8
- A gmail or Google Workspace account
- A Google OAuth application (and the `credentials.json` from it)

## Examples

```python3
import postmaster

mailman = postmaster.create_service()

content = postmaster.message.build_from_template('templates/test.html')
content['from'] = 'John Doe <johndoe@example.com>'
content['to'] = 'janedoe@example.org'
content['subject'] = 'A love letter'

msg = postmaster.send_message(mailman, content)
print(msg)
```