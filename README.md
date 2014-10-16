## stockflow
### System dynamics in Python 

Lightweight data structures for readable, maintainable models. Stocks are nouns and flows connect them. Wrapper around `scipy.integrate.odeint`, which is a wrapper around the Fortran library `odepack` using `lsoda`. The goal of this project is to provide an easy interface for describing stock/flow systems that will set up the ODEs automatically and solve them.

Requires [NumPy](http://www.numpy.org/) and [SciPy](http://www.scipy.org/)

#### How to use

__Create simulation__
```python
from stockflow import simulation
import numpy as np

tmax = 100
dt = 0.01
t = np.arange(0,tmax,dt)
s = simulation(t)
```

__Create stocks__
```python
# define names of states and their initial conditions
s.stocks({'A': 0, 'B': 10, 'C': 20})
```

__Define flows and their functions__
```python
# The flow called 'Q' moves (stuff) from stock 'A' to stock 'B'. 
# Function f(t) is evaluated at each timestep.
s.flow('Q', start='A', end='B', f=lambda t: k*s.A - l*s.B)

# Flow 'P' starts outside the control volume (None) and ends at C. 
s.flow('P', start=None, end='C', f=lambda t: m*s.C if s.B > 2 else 0)
# etc.
```
Forcing flows that originate outside the system (control volume) will have `start='None'`. Flows that originate inside the system but leave will have `end='None'`. Flow functions `f` can depend on any stocks or flows that already exist, or will exist at runtime.

Flow functions can also depend on `t`, as will usually be the case with forcing functions. This can either be continuous (e.g. `sin(t)`) or discrete (`P[t]`). *If you are using discrete flow functions, run the model with `s.run(discrete=True)`*.

__Define parameters (global constants)__
```python
k = 0.2; l = 0.7; m = 1.2
```

__Run simulation and look at time series of stocks/flows__
```python
s.run() # use discrete=True for discrete flow functions
# now access/plot any of s.A, s.B, s.C, s.Q, s.P, which are all vectors of length len(t)
```

####Examples
For more examples check out these [IPython notebooks](http://nbviewer.ipython.org/github/jdherman/stockflow/tree/master/examples/).

####License
Copyright (c) 2014 Jon Herman. Released under [the MIT license](https://github.com/jdherman/stockflow/blob/master/LICENSE.md).