# Market Microstructure Simulator Engine

Lightweight market microstructure simulator: L2 order book, matching engine, tick replay, and a Binance US recorder.

## Quickstart

1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run demo:
```bash
python run.py demo
```

3. Record live data (Binance US):
```bash
python run.py recorder --symbol BTCUSDT --stream trade --duration 60 --out data/binance.jsonl
```

4. Run tests:
```bash
python run.py test
```
or
```bash
pytest -q
```
