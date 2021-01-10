import numpy as np
import matplotlib.pyplot as plt
import requests
import matplotlib.style

matplotlib.style.use('ggplot')
data = requests.get(
    "https://steamcommunity.com/market/itemordershistogram?language=english&currency=1&item_nameid=" + str(
        176201364) + "&two_factor=0")
data = data.json()

BuyPrice = []
BuyQuantity = []
SellPrice = []
SellQuantity = []

for key in data['buy_order_graph']:
    BuyPrice.append(float(key[0]))
    BuyQuantity.append(int(key[1]))

for key in data['sell_order_graph']:
    SellPrice.append(float(key[0]))
    SellQuantity.append(int(key[1]))

Buy = np.array([BuyPrice, BuyQuantity]).T
Index = np.argsort(Buy[:, 0])
Buy = Buy[Index, :]

Sell = np.array([SellPrice, SellQuantity]).T
Index = np.argsort(Sell[:, 0])
Sell = Sell[Index, :]

plt.plot(Buy[:, 0], Buy[:, 1], label="Buy Order at Price or Higher")
plt.plot(Sell[:, 0], Sell[:, 1], label="Sell Order at Price or Lower")
plt.legend()

TrickList = []

tmp = np.hstack((BuyPrice, SellPrice))
tmp = np.sort(tmp)
for i in np.arange(0, 50, step=5):
    TrickList.append("$" + str(tmp[i]))
plt.xticks(tmp[np.arange(0, 50, step=5)], TrickList)
plt.xlabel("Price")
plt.ylabel("Quantity")

plt.savefig('image/CurrentPrice.svg', dpi=1200)