import websocket
import json
from kafka import KafkaProducer

websocket.enableTrace(True)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def on_open(ws):
    print("Connected to Finnhub")

    for symbol in ["AAPL", "MSFT", "TSLA", "NVDA"]:
        ws.send(json.dumps({
            "type": "subscribe",
            "symbol": symbol
        }))
        print(f"Subscribed to {symbol}")

def on_message(ws, message):
    print("MESSAGE:", message)
    data = json.loads(message)

    print("Raw message:", data)

    if data.get("type") == "ping":
        print("Ping received")
        return

    if data.get("type") == "trade":
        producer.send("stock_tricks", value=data)
        producer.flush()

        print("Published to Kafka:", data)

def on_error(ws, error):
    print("ERROR:", error)

def on_close(ws, code, msg):
    print("Closed:", code, msg)

ws = websocket.WebSocketApp(
    "wss://ws.finnhub.io?token=dakqam1r01qln1kfqrv0dakqam1r01qln1kfqrvg",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()