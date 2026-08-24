
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

def genre_analysis(session: Session):

    movies = session.table("R_MOVIES")

    movies_split = movies.with_column("NEW SPLIT GENRE",F.split(F.col("GENRES"),F.lit("|")))

    result = (
              movies_split.join_table_function(
                                              flatten(F.col("NEW SPLIT GENRE"))
              )
              .select(
                      F.col("MOVIEID"),
                      F.col("TITLE"),
                      F.col("VALUE").alias("GENRE")
              )
    )

    return result
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

result = genre_analysis(session)

result.show()

result.write.mode("overwrite").save_as_table("NETFLIX.MART.GENRE_ANALYSIS")   