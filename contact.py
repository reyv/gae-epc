import re
from google.appengine.api import mail
      
def contact_form(user, subject, message):
  emailTo = config.email_to
  emailFrom = config.email_from

  if re.match(r'\w+\.?\w+@\w+\.\w{2,3}', user):
    message = mail.EmailMessage(sender=emailFrom,subject='Geotech-Apps[EPC]: ' + subject)
    message.to = emailTo
    message.html = message + '<br /><br /> The sender is ' + user
    message.send()
    contact_form_msg = 'Thank you for contacting us.'
    self.generate('contact.html',{
                  'contact_form_msg':   contact_form_msg
    })
  else:
    contact_form_msg = 'You have input an invalid e-mail. Please retry.'
    self.generate('contact.html',{
                  'contact_form_msg':   contact_form_msg
                  })
