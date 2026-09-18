from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import snowflake.connector


with open(r"C:\SnowflakeKeys\rsa_key.p8", "rb") as key:
    p_key = serialization.load_pem_private_key(
        key.read(),
        password=b"Lapears1052#",
        backend=default_backend()
    )

pkb = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)


# Create Session
conn = snowflake.connector.connect(
    user="SSAHANI",
    account="xrxqlhd-te93429",
    private_key=pkb,
    warehouse="STOCK_WH",
    database="STOCK_DB",
    schema="RAW"
)

cur = conn.cursor()

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'stock_tricks',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


for message in consumer:

    payload = message.value



    cur.execute(
        """
        INSERT INTO RAW.STOCK_TRADES_RAW
        (
            RAW_DATA
        )
        SELECT PARSE_JSON(%s)
        """,
        (
            json.dumps(payload),
        )
    )

    print(f"Inserted into Snowflake")

