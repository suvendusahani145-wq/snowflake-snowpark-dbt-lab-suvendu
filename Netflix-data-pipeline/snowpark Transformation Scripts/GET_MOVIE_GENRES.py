from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, StringType


def create_snowpark_session(
    account,
    user,
    private_key_path,
    private_key_passphrase,
    role,
    warehouse,
    database,
    schema
):

    with open(private_key_path, "rb") as key_file:
        p_key = serialization.load_pem_private_key(
            key_file.read(),
            password=private_key_passphrase.encode(),
            backend=default_backend()
        )

    private_key_bytes = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    connection_params = {
        "ACCOUNT": account,
        "USER": user,
        "PRIVATE_KEY": private_key_bytes,
        "ROLE": role,
        "WAREHOUSE": warehouse,
        "DATABASE": database,
        "SCHEMA": schema
    }

    return Session.builder.configs(connection_params).create()


# Create Session
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


# UDTF Class
class GetMovieGenres:

    def process(self, genres: str):

        if not genres:
            return

        for genre in genres.split("|"):
            yield (genre,)


# Register UDTF
session.udtf.register(
    GetMovieGenres,
    output_schema=StructType([
        StructField("GENRE", StringType())
    ]),
    name="GETMOVIEGENRES",
    replace=True
)


# Test UDTF
session.sql("""
SELECT
    M.TITLE,
    G.GENRE
FROM R_MOVIES M,
TABLE(GETMOVIEGENRES(M.GENRES)) G
LIMIT 20
""").show()