
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
 


def compute_bayesian_weighted_ratings(
        session: Session,
        min_votes_threshold: int = 100
):

    ratings = session.table("NETFLIX.RAW.R_RATINGS")

    # Global average rating (C)
    global_mean = (
        ratings
        .select(F.avg("RATING"))
        .collect()[0][0]
    )

    # Movie statistics
    stats = (
        ratings
        .group_by("MOVIEID")
        .agg(
            F.count("R_KEY").alias("VOTE_COUNT"),
            F.avg("RATING").alias("AVG_RATING")
        )
    )

    v = F.col("VOTE_COUNT")
    m = F.lit(min_votes_threshold)
    r = F.col("AVG_RATING")
    c = F.lit(global_mean)

    result = (
        stats
        .with_column(
            "WEIGHTED_RATING",
            ((v / (v + m)) * r)
            +
            ((m / (v + m)) * c)
        )
        .order_by(F.col("WEIGHTED_RATING").desc())
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

result = compute_bayesian_weighted_ratings(session)

result.show()

result.write.mode("overwrite").save_as_table(
    "NETFLIX.MART.MOVIE_WEIGHTED_RATINGS"
)