from stockflow import simulation
import numpy as np
from matplotlib import pyplot as plt

# hymod as defined by Gharari et al. HESS 2013 (an approach to identify..)
# using fake P/Ep data here
tstep = 1000
P = 0.1*np.ones((tstep,))
Ep = np.zeros((tstep,))

# Parameters
Sm_max = 10; B = 1; alpha = 0.9; Kf = 0.5; Ks = 0.05

s = simulation(tstep)
s.init_stocks({'Sm': 0, 'Sf1': 0, 'Sf2': 0, 'Sf3': 0, 'Ss1': 0})
# soil moisture, 3 quickflow "f" reservoirs, and 1 slow flow "s" reservoir

s.flow('P', start=None, end='Sm', f=lambda t: P[t])
s.flow('Pe', start='Sm', end='Sf1', f=lambda t: max(P[t]*(1-(1-s.Sm[t]/Sm_max)**B), P[t]+s.Sm[t]-Sm_max))
s.flow('Ea', start='Sm', end=None, f=lambda t: min(Ep[t]*(s.Sm[t]/Sm_max), Ep[t]))
# effective precip Pe follows PDM model from Moore. Actual evap Ea.

s.flow('fast_to_slow', start='Sf1', end='Ss1', f=lambda t: (1-alpha)*s.Pe[t])
s.flow('Qf1', start='Sf1', end='Sf2', f=lambda t: Kf*s.Sf1[t])
s.flow('Qf2', start='Sf2', end='Sf3', f=lambda t: Kf*s.Sf2[t])
s.flow('Qf3', start='Sf3', end=None, f=lambda t: Kf*s.Sf3[t])
s.flow('Qs1', start='Ss1', end=None, f=lambda t: Ks*s.Ss1[t])

# each timestep, flows will be evaluated in the order they're defined
# so if they depend on other flows, be sure to put the independent ones first

s.run()

# total streamflow is s.Qs1 + s.Qf3, but can also plot other fluxes
# plt.plot(np.arange(tstep), s.Qs1, np.arange(tstep), s.Qf3)
plt.plot(np.arange(tstep), s.Sm)
plt.show()

# check water balance
print np.sum(s.Qs1+s.Qf3-P+s.Ea) + s.Sm[tstep-1] + s.Sf1[tstep-1] + s.Sf2[tstep-1] + s.Sf3[tstep-1] + s.Ss1[tstep-1]
