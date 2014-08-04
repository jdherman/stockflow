## stockflow

Simple system dynamics using stocks and flows. Solves with discrete Euler (forward, explicit). Of course there are better ODE solution options if analytical forcing functions are available and you're concerned about stability. This library will be useful for model development with discrete forcing data or complicated conditional functions to define flows. Also good for education and understanding what a model is actually doing.

__Create simulation__
```python
from stockflow import simulation

s = simulation(timesteps)
```
Assumes time-invariance and starts from `t=0`. User should make sure forcing data indexing lines up, and convert back to (time units) when the simulation is over.

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
s.flow('Q', start='A', end='B', f=lambda t: k*s.A[t] - l*s.B[t])
s.flow('P', start=None, end='C', f=lambda t: m*s.C[t] if s.B[t] > 2 else 0)
# etc.
```

__Define parameters (constants)__
```python
k = 0.2; l = 0.7; m = 1.2
```

__Run simulation and look at time series of stocks/flows__
```python
s.run()
# now access any of s.A, s.B, s.C, s.Q, s.P, which are all vectors of length tstep
```

__Full example for linear reservoir (`dS/dt = -kS`):__
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
