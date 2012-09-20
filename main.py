import os, webapp2, jinja2, re, config
import math as m
from google.appengine.api import mail

errors = []

class BaseRequestHandler(webapp2.RequestHandler):
  #Supplies a common template generation function. generate() augments the template variables.
  def generate(self, template_name, template_values={}):
    values = {}
    values.update(template_values)  
    path = os.path.join(os.path.dirname(__file__),'static/html/')
    jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(path),autoescape=True)
    template = jinja_environment.get_template(template_name)
    self.response.out.write(template.render(template_values))

class ErrorCheck(Exception):
    """A user-defined exception class"""
    def __init__(self, param, paramName, Min, Max):
        Exception.__init__(self)
        self.param = param
        self.paramName = paramName
        self.Min = Min
        self.Max = Max
    
    def numRange(self):
        """Determines whether the input values are within tolerable limits"""
        if self.param < self.Min:
            return False
        elif self.param > self.Max:
            return False
        else:
            return True  

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

    def erase(self,errors):     
        del errors[0:len(errors)]
        
    def post(self):
        self.erase(errors)        #clears erase list for each instance the app is run.

        #Simple browser detection on results page
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
            #Check each parameter to ensure it is within proper limits
            pValidate = ErrorCheck(p_deg,'Phi',20,45)
            if not pValidate.numRange():
                raise pValidate
            dValidate = ErrorCheck(d_deg,'Delta',0,30)
            if not dValidate.numRange():
                raise dValidate
            bValidate = ErrorCheck(b_deg,'Beta',60,90)
            if not bValidate.numRange():
                raise bValidate
            aValidate = ErrorCheck(a_deg,'Alpha',0,25)
            if not aValidate.numRange():
                raise aValidate
            oValidate = ErrorCheck(o,'OCR',0,5)
            if not oValidate.numRange():
                raise oValidate
            # Convert to radians for calculations
            p = m.radians(p_deg)
            d = m.radians(d_deg)
            b = m.radians(b_deg)
            a = m.radians(a_deg)
            #Calculation of Rankine Earth Pressure Coefficients
            #Since Rankine theory only works for vertical walls, logical statement calculates Ka & Kp for vertical wall only.
            if b == m.radians(90):
                Ka = round(m.cos(a)*((m.cos(a)-m.sqrt(pow(m.cos(a),2)-pow(m.cos(p),2)))/(m.cos(a)+m.sqrt(pow(m.cos(a),2)-pow(m.cos(p),2)))),2)
                Kp = round(m.cos(a)*((m.cos(a)+m.sqrt(pow(m.cos(a),2)-pow(m.cos(p),2)))/(m.cos(a)-m.sqrt(pow(m.cos(a),2)-pow(m.cos(p),2)))),2)
            else:
                Ka = "-"
                Kp = "-"
                errors.append('Rankine coefficients are only applicable for vertical walls.')
            #Calculation of Coulomb's Earth Pressure Coefficients
            Kac = round(pow(m.sin(b+p),2)/((pow(m.sin(b),2)*m.sin(b-d))*pow(1+m.sqrt((m.sin(p+d)*m.sin(p-a))/(m.sin(b-d)*m.sin(a+b))),2)),2)
            Kpc= round(pow(m.sin(b-p),2)/((pow(m.sin(b),2)*m.sin(b+d))*pow(1-m.sqrt((m.sin(p+d)*m.sin(p+a))/(m.sin(b+d)*m.sin(a+b))),2)),2)
            Kac1 = str(Kac)
            Kpc1 = str(Kpc)
            #Calculation of At-Rest Earth Pressure Coefficient
            Ko = round((1-m.sin(p))*pow(o,m.sin(p)),2)
              
        except (TypeError, ValueError, ZeroDivisionError):
            self.erase(errors)
            b_deg= 90
            a_deg= 15
            errors.append('Invalid Input. Please Retry.')
            #Render template with error messages. Beta & Alpha required to render Canvas drawing.
            self.generate('index.html',{
                'b_deg':    b_deg,
                'a_deg':    a_deg,
                'errors':   errors
            })
        except ErrorCheck, x:
            self.erase(errors)
            b_deg= 90
            a_deg= 15
            errors.append('Incorrect Input. %s must be between %d and %d' %(x.paramName,x.Min, x.Max))
            #Render template with error messages. Beta & Alpha required to render Canvas drawing.
            self.generate('index.html',{
                'b_deg':    b_deg,
                'a_deg':    a_deg,
                'errors':   errors
            })
        else:
            #Render template for results 
            self.generate('index.html',{
                'Ka':       Ka,
                'Kp':       Kp,
                'Ko':       Ko,
                'Kac1':     Kac1,
                'Kpc1':     Kpc1,
                'p_deg':    p_deg,
                'd_deg':    d_deg,
                'b_deg':    b_deg,
                'a_deg':    a_deg,
                'o':        o,
                'browserError':        browserError,
                'errors':   errors
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
