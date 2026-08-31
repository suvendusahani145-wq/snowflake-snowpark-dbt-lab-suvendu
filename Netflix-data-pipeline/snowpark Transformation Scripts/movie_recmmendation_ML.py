
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


ratings = session.table("R_RATINGS")
movies = session.table("R_MOVIES")
tags = session.table("R_TAGS")

rating_stats = ratings.group_by("MOVIEID").agg(F.avg("RATING").alias("AVG_RATING"),F.count("RATING").alias("RATING_COUNT"))

# result = movies.join(rating_stats,movies["MOVIEID"] == rating_stats["MOVIEID"]).select(movies["MOVIEID"],movies["TITLE"],
#                                                                                      movies["GENRES"],
#                                                                                      rating_calc["AVG_RATING"],
#                                                                                      rating_calc["RATING_COUNT"])

tag_stats = (
    tags
    .group_by("MOVIEID")
    .agg(
        F.array_agg("TAG").alias("TAGS")
    )
)


movie_features = (movies
    .join(rating_stats, "MOVIEID")
    .join(tag_stats, "MOVIEID")
)

# movie_features.show()

target_movie = "Toy Story (1995)"

target_genres = movie_features.filter(F.col("TITLE") == 'Toy Story (1995)').select("GENRES").collect()[0]["GENRES"]

target_genres_set = set(target_genres.split("|"))
# print(target_genres_set)


source_movie = "Grumpier Old Men (1995)"

source_genres = movie_features.filter(F.col("TITLE") == source_movie).select("GENRES").collect()[0]["GENRES"]

source_genres_set = set(source_genres.split("|"))
# print(source_genres_set)

common_genre = source_genres_set.intersection(target_genres_set)
recommendations = []

for row in movie_features.collect():
    # print(row)
    source_movie = row["TITLE"]

    source_genres = row["GENRES"]

    source_genres_set = set(source_genres.split("|"))
    # print(source_genres_set)

    genre_score = len(source_genres_set.intersection(target_genres_set))

    final_score = genre_score + row["AVG_RATING"]

    # common_genre = source_genres_set.intersection(target_genres_set)
    if final_score > 8 and target_movie != source_movie:
        recommendations.append((row["TITLE"],genre_score,row["AVG_RATING"],final_score))


recommendations.sort(
    key=lambda x: x[3],
    reverse=True
)
for rec in recommendations[:10]:
    print(rec[0], "-", rec[3])

  

