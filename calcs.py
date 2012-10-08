import math as m           

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

def valid_num(p,d,b,a,o):
  """Check each parameter to ensure it is within proper limits"""
  pValidate = ErrorCheck(p,'Phi',20,45)
  if not pValidate.numRange():
    raise pValidate
  dValidate = ErrorCheck(d,'Delta',0,30)
  if not dValidate.numRange():
    raise dValidate
  bValidate = ErrorCheck(b,'Beta',60,90)
  if not bValidate.numRange():
    raise bValidate
  aValidate = ErrorCheck(a,'Alpha',0,25)
  if not aValidate.numRange():
    raise aValidate
  oValidate = ErrorCheck(o,'OCR',0,5)
  if not oValidate.numRange():
    raise oValidate

           
def convert_to_rad(p,d,b,a):          
  """ Convert to radians for calculations"""
  p = m.radians(p)
  d = m.radians(d)
  b = m.radians(b)
  a = m.radians(a)
  return {'p':p, 'd':d, 'b':b, 'a':a}

def rankine_coeff(p,d,b,a):  
  """Calculation of Rankine Earth Pressure Coefficients
  Since Rankine theory only works for vertical walls, logical statement calculates Ka & Kp for vertical wall only."""
  
  if b == m.radians(90):
    Ka = round(m.cos(a)*((m.cos(a)-m.sqrt(pow(m.cos(a),2)-pow(m.cos(p),2)))/(m.cos(a)+m.sqrt(pow(m.cos(a),2)-pow(m.cos(p),2)))),2)
    Kp = round(m.cos(a)*((m.cos(a)+m.sqrt(pow(m.cos(a),2)-pow(m.cos(p),2)))/(m.cos(a)-m.sqrt(pow(m.cos(a),2)-pow(m.cos(p),2)))),2)
    error = None
  else:
    Ka = '-'
    Kp = '-'
    error = 'Rankine coefficients are only applicable for vertical walls.'
  return {'Ka':Ka, 'Kp':Kp, 'error':error}

def coulomb_coeff(p,d,b,a):    
  """Calculation of Coulomb's Earth Pressure Coefficients"""
  Kac = round(pow(m.sin(b+p),2)/((pow(m.sin(b),2)*m.sin(b-d))*pow(1+m.sqrt((m.sin(p+d)*m.sin(p-a))/(m.sin(b-d)*m.sin(a+b))),2)),2)
  Kpc= round(pow(m.sin(b-p),2)/((pow(m.sin(b),2)*m.sin(b+d))*pow(1-m.sqrt((m.sin(p+d)*m.sin(p+a))/(m.sin(b+d)*m.sin(a+b))),2)),2)
  return {'Kac':Kac, 'Kpc':Kpc}
 
def at_rest(p, o): 
  """Calculation of At-Rest Earth Pressure Coefficient"""
  Ko = round((1-m.sin(p))*pow(o,m.sin(p)),2)
  return {'Ko':Ko}


##prop = convert_to_rad(20,0,65,25)
##print rankine_coeff(prop['p'],prop['d'], prop['b'], prop['a'])
##print coulomb_coeff(prop['p'],prop['d'], prop['b'], prop['a'])
##print at_rest(prop['p'],1)
