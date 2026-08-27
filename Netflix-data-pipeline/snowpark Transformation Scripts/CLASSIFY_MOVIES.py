
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from snowflake.snowpark import Session
from snowflake.snowpark import functions as F
from snowflake.snowpark.functions import flatten
import re
 
def create_snowpark_session(
    account: str,
    user: str,
    private_key_path: str,
    private_key_passphrase: str,
    role: str,
    warehouse: str,
    database: str,
    schema: str
) -> Session:
    """Create and return a Snowpark session using RSA key‑pair authentication."""
    # Load private key
    with open(private_key_path, "rb") as key_file:
        p_key = serialization.load_pem_private_key(
            key_file.read(),
            password=private_key_passphrase.encode(),
            backend=default_backend()
        )
 
    # Convert to PKCS#8 DER bytes
    private_key_bytes = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
 
    # Connection parameters
    connection_params = {
        "ACCOUNT": account,
        "USER": user,
        "PRIVATE_KEY": private_key_bytes,
        "ROLE": role,
        "WAREHOUSE": warehouse,
        "DATABASE": database,
        "SCHEMA": schema
    }
 
    # Create and return session
    return Session.builder.configs(connection_params).create()
 


from snowflake.snowpark.functions import udf



def classify_movies(rating: float) -> str:
    if rating >= 4.5:
        return "EXCELLENT"

    elif rating >= 4.0:
        return "GOOD"

    elif rating >= 3.0:
        return "AVERAGE"

    else:
        return "POOR"

# Run
session = create_snowpark_session(
    account="xrxqlhd-te93429",
    user="SSAHANI",
    private_key_path=r"C:\SnowflakeKeys\rsa_key.p8",
    private_key_passphrase="Lapears1052#",
    role="NETFLIX_ROLE",
    warehouse="NETFLIX_WH",
    database="NETFLIX",
    schema="RAW"
)

classify_movies_udf = session.udf.register(
    classify_movies
)

from snowflake.snowpark import functions as F

ratings = session.table("R_RATINGS")

result = ratings.with_column(
    "MOVIE_CATEGORY",
    classify_movies_udf(F.col("RATING")))

result.show()