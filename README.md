## stockflow
### System dynamics in Python 

Lightweight data structures for readable, maintainable models. Stocks are nouns and flows connect them. Solves with discrete Euler (forward, explicit) to keep it simple, which is bad if (1) you have closed-form functions for flows, in which case there are better libraries out there, and/or (2) you're concerned about stability. Good for users with flow functions that are discrete, piecewise, or otherwise messy. Also good for education and understanding what a model is actually doing. 

#### How to use

__Create simulation__
```python
from stockflow import simulation

s = simulation(timesteps)
```
Assumes time invariance and starts from `t=0`. Make sure forcing data and constant parameters are defined in the right units, because the simulation knows nothing about this.

__Create stocks__
```python
# define names of states and their initial conditions
s.init_stocks({'A': 0, 'B': 10, 'C': 20})
# or create them one by one:
s.stock('A', 0)
s.stock('B', 10)
# etc.
```

__Define flows as lambda functions__
```python
# The flow called 'Q' moves (stuff) from stock 'A' to stock 'B'. 
# Function f(t) is evaluated at each timestep.
s.flow('Q', start='A', end='B', f=lambda t: k*s.A[t] - l*s.B[t])

# Flow 'P' starts outside the control volume (None) and ends at C. 
# Function f(t) is conditional - no problem.
s.flow('P', start=None, end='C', f=lambda t: m*s.C[t] if s.B[t] > 2 else 0)
# etc.
```
Forcing flows that originate outside the system (control volume) will have `start='None'`. Flows that originate inside the system but leave will have `end='None'`. Flow functions `f` can depend on any stocks or flows that have already been created, accessed with `s.A[t]` for example.

__Define parameters (constants)__
```python
k = 0.2; l = 0.7; m = 1.2
```

__Run simulation and look at time series of stocks/flows__
```python
s.run()
# now access any of s.A, s.B, s.C, s.Q, s.P, which are all vectors of length tstep
```

#### Full example for linear reservoir:
Rainfall `P` (sampled from exponential distribution) enters stock 'S' and flows out with rate `dS/dt = -kS`. One parameter `k` to define. The outflow `Q` is plotted at the end.

```python
from stockflow import simulation
import numpy as np
from matplotlib import pyplot as plt

# using fake precip data
tstep = 100
P = 10*np.random.standard_exponential(tstep,)

# Parameters
k = 0.3

s = simulation(tstep)
s.init_stocks({'S': 0})

s.flow('P', start=None, end='S', f=lambda t: P[t])
s.flow('Q', start='S', end=None, f=lambda t: k*s.S[t])
s.run()

plt.plot(np.arange(tstep), s.Q)
plt.show()
```
