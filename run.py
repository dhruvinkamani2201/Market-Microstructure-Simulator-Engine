import sys
import subprocess
import argparse
from pathlib import Path

ROOT = Path(__file__).parent

def run_demo():
    subprocess.check_call([sys.executable, str(ROOT / "examples" / "run_demo.py")])

def run_recorder(symbol="BTCUSDT", stream="trade", duration=30, out="data/binance.jsonl"):
    recorder = ROOT / "recorder" / "binance_recorder.py"
    subprocess.check_call([sys.executable, str(recorder), "--symbol", symbol, "--stream", stream, "--duration", str(duration), "--out", out])

def run_tests():
    subprocess.check_call([sys.executable, "-m", "pytest", "-q"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["demo","recorder","test"])
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--stream", default="trade")
    parser.add_argument("--duration", type=int, default=30)
    parser.add_argument("--out", default="data/binance.jsonl")
    args = parser.parse_args()

    if args.cmd == "demo":
        run_demo()
    elif args.cmd == "recorder":
        run_recorder(symbol=args.symbol, stream=args.stream, duration=args.duration, out=args.out)
    elif args.cmd == "test":
        run_tests()

if __name__ == "__main__":
    main()
