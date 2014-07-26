from stockflow import simulation

s = simulation(10)
s.init_stocks({'mice': 100})
s.flow('births', start=None, end='mice', f=lambda t: b*s.mice[t])
s.flow('deaths', start='mice', end=None, f=lambda t: d*s.mice[t])
b = 0.5
d = 0.7
s.run()

print s.births