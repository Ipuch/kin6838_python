import numpy as np
import matplotlib.pyplot as plt

fs = [1, 2, 4]
all_time = np.linspace(start=0, stop=2, num=200)
# all_time = np.linspace(0, 2, 2)
t = all_time[0:100]

for f in fs:
    y = np.sin(2*np.pi*f*t)
    plt.plot(t, y, label='{} Hz'.format(f))

plt.legend()
plt.savefig('basics_python.png')