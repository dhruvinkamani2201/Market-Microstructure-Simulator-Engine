import asyncio
import websockets
import json
import argparse
from pathlib import Path
import time

BASE = "wss://stream.binance.us:9443/ws/"

async def record(symbol: str, stream: str, out: str, duration: int):
    uri = BASE + f"{symbol.lower()}@{stream}"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    start = time.time()
    with open(out, "a") as fh:
        async with websockets.connect(uri, max_size=2**25) as ws:
            while time.time() - start < duration:
                msg = await ws.recv()
                fh.write(json.dumps({"recv_ts": int(time.time()*1000), "msg": json.loads(msg)}) + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--stream", default="trade", help="trade | depth")
    parser.add_argument("--out", default="data/binance.jsonl")
    parser.add_argument("--duration", type=int, default=30)
    args = parser.parse_args()
    asyncio.run(record(args.symbol, args.stream, args.out, args.duration))

if __name__ == "__main__":
    main()
