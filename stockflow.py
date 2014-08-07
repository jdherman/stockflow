import numpy as np
from scipy.integrate import odeint

class simulation:
  def __init__(self, t):
    self.t = t
    self.ix = {}
    self.flows = {}
    self.current = []
    self.done = False
    self.results = None

  def __getattr__(self,key):
    if not self.done: return self.current[self.ix[key]]
    else: return self.results[:,self.ix[key]]

  def __validate_key(self,key):  
    if key in self.ix: raise NameError("Variable " + key + " already defined.")  

  def __new_state_var(self, key, IC):
    self.__validate_key(key)
    self.current.append(IC)
    self.ix[key] = len(self.current)-1

  def stocks(self,icdict):
    for k,v in icdict.items():
      self.__new_state_var(k,v)

  def flow(self, key, f, start=None, end=None):
    self.__new_state_var(key,f(0))
    s = self.ix[start] if start is not None else None
    e = self.ix[end] if end is not None else None
    self.flows[key] = {'f': f, 'start': s, 'end': e}

  def xdot(self,y,t):
    self.current = y
    d = np.zeros((len(y),))
    for k,f in self.flows.iteritems(): # calculate flows only once. distribute to stocks.
        i = self.ix[k]
        ft = f['f'](t)
        d[i] =  ft - self.current[i]
        if f['start'] is not None: d[f['start']] -= ft
        if f['end'] is not None: d[f['end']] += ft
    return d

  def run(self):
    self.done = False
    self.results = odeint(self.xdot, self.current, self.t)
    self.done = True
    self.current = self.results[0,:] # restore initial conditions
