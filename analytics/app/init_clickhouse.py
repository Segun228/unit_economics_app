from clickhouse_driver import Client
import clickhouse_connect
from dotenv import load_dotenv
import os
import logging

load_dotenv()

host = os.getenv("CLICKHOUSE_HOST")
port = os.getenv("CLICKHOUSE_PORT")
username = os.getenv("CLICKHOUSE_USER", "default")
password = os.getenv("CLICKHOUSE_PASSWORD", "")


if not host or not port or not username:
    raise RuntimeError("ENV variables are missing")

client = clickhouse_connect.get_client(host=host, port=int(port), username=username, password = password)

def create_logs_table():
    client.command("""
    CREATE DATABASE IF NOT EXISTS logs_database
    """)

    client.command("""
    CREATE TABLE IF NOT EXISTS logs_database.logs (
        timestamp DateTime,
        user_id UInt64,
        is_authenticated UInt8,
        telegram_id String,
        trace_id String,
        action String,
        response_code UInt16,
        request_method String,
        request_body String,
        platform String,
        level String,
        source String,
        env String,
        event_type String,
        message String
    ) ENGINE = MergeTree()
    ORDER BY timestamp
    """)
    
    logging.info("Table 'logs_database.logs' ensured.")

if __name__ == "__main__":
    create_logs_table()