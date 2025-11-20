from collections import deque, defaultdict
import time

class MatchingEngine:
    def __init__(self):
        # book: side -> price -> deque of (order_id, size)
        self.book = {"buy": defaultdict(deque), "sell": defaultdict(deque)}
        self.next_id = 1
        self.trades = []

    def place_limit(self, side, price, size, metadata=None):
        """Place a limit order as resting order."""
        oid = self.next_id
        self.next_id += 1
        self.book[side][price].append({"id": oid, "size": float(size), "meta": metadata or {}})
        return oid

    def cancel(self, side, price, order_id):
        """Cancel a resting order if present."""
        dq = self.book[side].get(price)
        if not dq:
            return False
        for i, order in enumerate(dq):
            if order["id"] == order_id:
                dq.remove(order)
                return True
        return False

    def match_market(self, taker_side, size_limit=None, price_limit=None):
        """Taker side is 'buy' or 'sell'. Match against opposite book until size consumed or no match."""
        opposite = "sell" if taker_side == "buy" else "buy"
        # Get sorted price levels
        price_levels = sorted(self.book[opposite].keys())
        if opposite == "sell":
            # sells ascending (best low first)
            sorted_prices = price_levels
        else:
            # buys descending (best high first)
            sorted_prices = list(reversed(price_levels))

        remaining = size_limit if size_limit is not None else float("inf")
        trades = []

        for p in sorted_prices:
            if remaining <= 0:
                break
            if price_limit is not None:
                if taker_side == "buy" and p > price_limit:
                    break
                if taker_side == "sell" and p < price_limit:
                    break

            dq = self.book[opposite].get(p)
            while dq and remaining > 0:
                resting = dq[0]
                trade_size = min(resting["size"], remaining)
                trade = {"price": p, "size": trade_size, "time": time.time(), "against": resting["id"]}
                trades.append(trade)
                self.trades.append(trade)

                resting["size"] -= trade_size
                remaining -= trade_size
                if resting["size"] <= 1e-12:
                    dq.popleft()
            if not dq:
                self.book[opposite].pop(p, None)

        return trades

    def get_trades(self, limit=100):
        return list(self.trades[-limit:])
