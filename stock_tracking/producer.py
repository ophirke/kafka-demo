import json
import argparse
import time
from kafka import KafkaProducer
import yfinance as yf
from tqdm import tqdm


def produce_stock_data(symbol):
    print("Getting by the second data for", symbol)
    
    data = yf.download(tickers=symbol, period="5d", interval="1m")
    
    # convert the data to a list of dictionaries
    data_dicts = []
    for row in data.iterrows():
        ticker = row[0]
        price = row[1]["Close"].item()
        volume = row[1]["Volume"].item()
        timestamp = ticker.timestamp()
        data_dicts.append({
            "symbol": symbol,
            "timestamp": timestamp,
            "price": price,
            "volume": volume
        })
        
    print("Sending data to Kafka")

    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    for data_dict in tqdm(data_dicts):
        producer.send("stocks", value=data_dict)
        producer.flush()
        time.sleep(0.05)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka producer for stock prices.")
    parser.add_argument("symbol", type=str, help="Stock symbol (e.g., AAPL)")
    args = parser.parse_args()

    produce_stock_data(args.symbol)
