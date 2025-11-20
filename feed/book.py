from bisect import bisect_left, insort
from collections import defaultdict
from sortedcontainers import SortedList

class Side:
    def __init__(self, reverse=False):
        # keep sorted list of prices
        self.prices = SortedList()
        self.book = {}  # price -> size
        self.reverse = reverse

    def update(self, price: float, size: float):
        # price: float, size: float (0 removes level)
        if size <= 0:
            if price in self.book:
                del self.book[price]
                try:
                    self.prices.remove(price)
                except ValueError:
                    pass
        else:
            if price not in self.book:
                self.prices.add(price)
            self.book[price] = size

    def best(self):
        if not self.prices:
            return None, 0.0
        if self.reverse:
            price = self.prices[-1]
        else:
            price = self.prices[0]
        return price, self.book.get(price, 0.0)

    def top_n(self, n=5):
        if self.reverse:
            prices = list(reversed(self.prices[-n:]))
        else:
            prices = list(self.prices[:n])
        return [(p, self.book.get(p, 0.0)) for p in prices]


class OrderBook:
    def __init__(self):
        # bids highest-first (reverse=True), asks lowest-first
        self.bids = Side(reverse=True)
        self.asks = Side(reverse=False)

    def update_bid(self, price: float, size: float):
        self.bids.update(price, size)

    def update_ask(self, price: float, size: float):
        self.asks.update(price, size)

    def snapshot(self, top_n=5):
        return {
            "bids": self.bids.top_n(top_n),
            "asks": self.asks.top_n(top_n)
        }

    def mid(self):
        bid, _ = self.bids.best()
        ask, _ = self.asks.best()
        if bid is None or ask is None:
            return None
        return (bid + ask) / 2.0
