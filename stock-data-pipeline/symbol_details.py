
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import snowflake.connector
import json


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

import finnhub
finnhub_client = finnhub.Client(api_key="dakqam1r01qln1kfqrv0dakqam1r01qln1kfqrvg")

result= finnhub_client.stock_symbols('US')



cur.execute(
        """
        INSERT INTO RAW.DIM_SYMBOLS_RAW
        (
            RAW_DATA
        )
        SELECT PARSE_JSON(%s)
        """,
        (
            json.dumps(result),
        )
    )

print(f"Inserted into Snowflake")



