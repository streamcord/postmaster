import postmaster

srv = postmaster.create_service()

mime = postmaster.message.build_from_template('templates/test.html')
mime['from'] = 'Streamcord <noreply@streamcord.io>'
mime['to'] = 'r3aper.ow@gmail.com'
mime['subject'] = 'Notification failed to send in Streamcord Dev'

msg = postmaster.send_message(srv, mime)
print(msg)
