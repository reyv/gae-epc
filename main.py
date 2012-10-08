import os
import re
import webapp2
import jinja2
import config
import calcs

from google.appengine.api import mail

class BaseRequestHandler(webapp2.RequestHandler):
  """Supplies a common template generation function. generate() augments the template variables."""
  def generate(self, template_name, template_values={}):
    values = {}
    values.update(template_values)  
    path = os.path.join(os.path.dirname(__file__),'static/html/')
    jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(path),autoescape=True)
    template = jinja_environment.get_template(template_name)
    self.response.out.write(template.render(template_values))

class MainHandler(BaseRequestHandler):
    """Main Request Handler that renders main page"""
  
    def browserDetect(self, user_agent):
      """Very simple browser detection function."""
      if 'MSIE' in user_agent:
        return 'This web application is not supported by Internet Explorer browser. Please use either Google Chorme or Safari.'
      else:
        return ''

    def get(self):
        user_agent = os.environ.get('HTTP_USER_AGENT')
        browserError = self.browserDetect(user_agent)
        self.generate('index.html',{
                      'browserError':    browserError
            })
        
class Calculation(BaseRequestHandler):
    """Request Handler that processes form and performs server-side error handling."""
       
    def post(self):
        """Simple browser detection on results page"""
        user_agent = os.environ.get('HTTP_USER_AGENT')
        browserCheck = MainHandler()
        browserError = browserCheck.browserDetect(user_agent)
        
        try:        
            #Get soil/wall parameters (degrees)
            p_deg = int(self.request.get('friction'))
            d_deg = int(self.request.get('wall_friction'))
            b_deg = int(self.request.get('wall_inclination'))
            a_deg = int(self.request.get('backfill_angle'))
            o = int(self.request.get('ocr'))           

            #Actual calcs
            calcs.valid_num(p_deg,d_deg,b_deg,a_deg,o)
            prop = calcs.convert_to_rad(p_deg,d_deg,b_deg,a_deg)
            rankine = calcs.rankine_coeff(prop['p'],prop['d'], prop['b'], prop['a'])
            coulomb = calcs.coulomb_coeff(prop['p'],prop['d'], prop['b'], prop['a'])
            mk =  calcs.at_rest(prop['p'],o)

        except calcs.ErrorCheck, x:
            b_deg= 90
            a_deg= 15
            error = 'Incorrect Input. %s must be between %d and %d' %(x.paramName,x.Min, x.Max)
            #Render template with error messages. Beta & Alpha required to render Canvas drawing.
            self.generate('index.html',{
                'b_deg':    b_deg,
                'a_deg':    a_deg,
                'errors':   error
            })

        except ValueError, x:
            b_deg= 90
            a_deg= 15
            if 'math domain error' in x:
              error = 'Invalid input results in Math Domain Error. Retry.'
            else:
              error = 'Invalid input. Numbers only.'
            #Render template with error messages. Beta & Alpha required to render Canvas drawing.
            self.generate('index.html',{
                'b_deg':    b_deg,
                'a_deg':    a_deg,
                'errors':   error
            })

        else:
            #Render template for results 
            self.generate('index.html',{
                'Ka':       rankine['Ka'],
                'Kp':       rankine['Kp'],
                'Kac':      coulomb['Kac'],
                'Kpc':      coulomb['Kpc'],
                'Ko':       mk['Ko'],
                'p_deg':    p_deg,
                'd_deg':    d_deg,
                'b_deg':    b_deg,
                'a_deg':    a_deg,
                'o':        o,
                'browserError':   browserError,
                'errors':   rankine['error']
            })

class Contact(BaseRequestHandler):
    """Generates contact.html so directory structure is hidden from user."""
    def get(self):
        self.generate('contact.html',{})
        
    def post(self):
        emailTo = config.email_to
        emailFrom = config.email_from
        emailUser = self.request.get('email_from')
        emailSubject = self.request.get('email_subject')
        emailMessage = self.request.get('email_message')    

        if re.match(r'\w+\.?\w+@\w+\.\w{2,3}', emailUser):
          message = mail.EmailMessage(sender=emailFrom,subject='Geotech-Apps[EPC]: '+emailSubject)
          message.to = emailTo
          message.html = emailMessage + '<br /><br /> The sender is ' + emailUser
          message.send()
          Message = 'Thank you for contacting us.'
          self.generate('contact.html',{
                        'Message':   Message
          })
        else:
          Message = 'You have input an invalid e-mail. Please retry.'
	  self.generate('contact.html',{
                        'Message':   Message
          })
	  
class About(BaseRequestHandler):
    """Generates about.html."""
    def get(self):
        self.generate('about.html',{})
      
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/results', Calculation),
    ('/contact', Contact),
    ('/about', About)],
    debug=True)
