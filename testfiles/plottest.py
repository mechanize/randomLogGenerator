import matplotlib.pyplot as plt
from time import sleep

fig = plt.figure(1, figsize=(10, 5))
ax0 = fig.add_subplot(121)
ax1 = fig.add_subplot(122)
ax0.plot([1, 2, 3], [2, 4, 6])
ax0.plot([1, 2, 3], [4, 5, 6])
ax1.plot([1, 2, 3], [3, 6, 9])
ax0.set_ylim(0)
fig.show()
sleep(5)
