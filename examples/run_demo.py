import sys
from pathlib import Path

# Add project root to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from replay.replay import replay
from feed.book import OrderBook

def main():
    print("Running demo replay (100 ticks)...")
    ob, me = replay(n_ticks=100, speed=0.0)
    snap = ob.snapshot(5)
    print("Top book snapshot:")
    print("Bids:", snap["bids"])
    print("Asks:", snap["asks"])
    print("Trades (sample):", me.get_trades(5))

if __name__ == "__main__":
    main()
