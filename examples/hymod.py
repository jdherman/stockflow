from stockflow import simulation
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

t = np.arange(0, 200, 1)
P = 5*np.random.standard_exponential(len(t),)

s = simulation(t)
s.stocks({'S': 100})

# Parameters
Sm_max = 8; B = 0.7; alpha = 0.6; Kf = 0.5; Ks = 0.05

s = simulation(t)
s.stocks({'Sm': 5, 'Sf1': 0, 'Sf2': 0, 'Sf3': 0, 'Ss1': 0})
s.flow('P', start=None, end='Sm', f=lambda t: P[t])
s.flow('Pe', start='Sm', end='Sf1', f=lambda t: s.P*(1-max(1-s.Sm/Sm_max,0)**B))
s.flow('Ea', start='Sm', end=None, f=lambda t: min(2*(s.Sm/Sm_max), s.Sm))

s.flow('fast_to_slow', start='Sf1', end='Ss1', f=lambda t: (1-alpha)*s.Pe)
s.flow('Qf1', start='Sf1', end='Sf2', f=lambda t: Kf*s.Sf1)
s.flow('Qf2', start='Sf2', end='Sf3', f=lambda t: Kf*s.Sf2)
s.flow('Qf3', start='Sf3', end=None, f=lambda t: Kf*s.Sf3)
s.flow('Qs1', start='Ss1', end=None, f=lambda t: Ks*s.Ss1)

s.run(discrete=True)

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.stackplot(t, s.Qs1, s.Qf3)
ax1.set_xlabel("Time (Days)")
ax1.set_ylabel("Streamflow (mm)")
ax1.set_ylim([0, np.max(s.Qf3+s.Qs1)*2])

ax11 = ax1.twinx()
ax11.bar(t, P)
ax11.set_ylim([0, np.max(P)*2])
ax11.invert_yaxis()
ax11.grid(False)

Sall = [s.Sm, s.Sf1+s.Sf2+s.Sf3, s.Ss1]
Sfrac = [S/sum(Sall) for S in Sall]
ax2.stackplot(t, *Sfrac)

plt.show()
