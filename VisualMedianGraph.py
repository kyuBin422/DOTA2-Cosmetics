import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style

matplotlib.style.use('ggplot')
with open('TradeDetail.pickle', 'rb') as handle:
    trend = pickle.load(handle)


tmp = trend[0]
fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('time (day)')
ax1.set_ylabel("price $", color=color)
ax1.plot(tmp[:, 0], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('log quantity', color=color)  # we already handled the x-label with ax1
ax2.plot(np.log(tmp[:, 1]), color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.xticks(np.linspace(0, 749, 10), ['Nov 29', 'Dec 3', 'Dec 6', 'Dec 9', 'Dec 13',
                                     'Dec 16', 'Dec 19', 'Dec 23', 'Dec 26', 'Dec 29'])

plt.savefig('image/CosmeticMedianPrices.svg', dpi=1200)