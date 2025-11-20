import random
import time
from feed.book import OrderBook
from matching.engine import MatchingEngine

def gen_sample_ticks(n=1000, seed=0):
    """Generate synthetic L1 ticks (mid, spread) for n events."""
    rng = random.Random(seed)
    mid = 100.0
    for i in range(n):
        mid += rng.normalvariate(0, 0.05)
        spread = max(0.01, abs(rng.normalvariate(0.02, 0.02)))
        bid = round(mid - spread/2, 2)
        ask = round(mid + spread/2, 2)
        bidsz = rng.randint(50, 200)
        asksz = rng.randint(50, 200)
        yield {"ts": i, "bid": bid, "bidsz": bidsz, "ask": ask, "asksz": asksz}

def replay(n_ticks=1000, speed=0.0):
    """Replay synthetic ticks into a local order book and matching engine."""
    ob = OrderBook()
    me = MatchingEngine()
    for tick in gen_sample_ticks(n_ticks):
        # Update book L1
        ob.bids.update(tick["bid"], tick["bidsz"])
        ob.asks.update(tick["ask"], tick["asksz"])

        # Occasionally place a market taker
        if tick["ts"] % 20 == 0:
            # place a small market buy consuming best asks
            me.place_limit("sell", tick["ask"], 10)
            trades = me.match_market("buy", size_limit=5)
            # trades appended inside engine

        if speed > 0:
            time.sleep(speed)
    return ob, me
