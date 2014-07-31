import numpy as np
import collections

class simulation:
  def __init__(self, tstep):
    self.stocks = {}
    self.flows = collections.OrderedDict()
    self.tstep = tstep

  def __getattr__(self,key):
    return self.stocks[key] if key in self.stocks else self.flows[key]['vals']

  def validate_key(self,key):  
    if key in self.stocks or key in self.flows:
      raise NameError("Variable " + key + " already defined.")  

  def init_stocks(self,icdict):
    for k,v in icdict.items():
      self.stock(k,v)

  def stock(self, key, IC):
    self.validate_key(key)
    self.stocks[key] = np.full((self.tstep,), IC) # init time series of stock

  def flow(self, key, f, start=None, end=None):
    self.validate_key(key)
    self.flows[key] = {'start': start, 'end': end, 'f': f, 'vals': np.zeros((self.tstep,))}

  def run(self):
    for t in xrange(1,self.tstep):
      for stock in self.stocks.itervalues(): # initialize stocks at prior values
        stock[t] = stock[t-1]

      for flow in self.flows.itervalues(): # calculate flows only once. distribute to stocks.
        flow['vals'][t-1] = flow['f'](t-1)
        if flow['start'] is not None:
          self.stocks[flow['start']][t] -= flow['vals'][t-1]
        if flow['end'] is not None:
          self.stocks[flow['end']][t] += flow['vals'][t-1]

    for flow in self.flows.itervalues(): # calculate flows at final timestep
        flow['vals'][self.tstep-1] = flow['f'](self.tstep-1)
