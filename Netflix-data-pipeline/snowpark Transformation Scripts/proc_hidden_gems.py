from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from snowflake.snowpark import Session
from snowflake.snowpark import functions as F
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


proc_sql = """CREATE OR REPLACE PROCEDURE proc_hidden_gems()
       RETURNS STRING

       LANGUAGE PYTHON
       RUNTIME_VERSION = '3.11'
       PACKAGES = ('snowflake-snowpark-python')
       HANDLER = 'run'
       AS
       $$
from snowflake.snowpark import functions as F
def run(session):
            ratings = session.table("R_RATINGS")

            stats = ratings.group_by("MOVIEID").\
            agg(F.count("RATING").alias("RATING_COUNT"), F.avg("RATING").alias("AVG_RATING"))

            result = stats.filter((F.col("AVG_RATING")>4) & ((F.col("RATING_COUNT") > 200) & (F.col("RATING_COUNT") <= 500)))

            movies = session.table("R_MOVIES")

            final_result = result.join(movies,result["MOVIEID"] == movies["MOVIEID"]).select(movies["TITLE"])

            movies_list = final_result.collect()

            return ", ".join([row["TITLE"] for row in movies_list])
       $$ """

session.sql(proc_sql).collect()


result = session.sql(
    "CALL proc_hidden_gems()"
 ).collect()

print(result[0][0])