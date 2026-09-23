from snowflake.snowpark import functions as F

def model(dbt, session):

    ratings = dbt.ref("stg_R_RATINGS")
    movies = dbt.ref("stg_R_MOVIES")

    # Rating Statistics
    rating_stats = (
        ratings
        .group_by("MOVIEID")
        .agg(
            F.avg("RATING").alias("AVG_RATING"),
            F.count("RATING").alias("RATING_COUNT")
        )
    )

    # Movie Features
    movie_features = (
        movies
        .join(rating_stats, "MOVIEID")
    )

    # Target Movie
    target_movie = "Toy Story (1995)"

    target_genres = (
        movie_features
        .filter(F.col("TITLE") == target_movie)
        .select("GENRES")
        .collect()[0]["GENRES"]
    )

    genre_list = target_genres.split("|")

    # Build similarity score
    score_expr = F.lit(0)

    for genre in genre_list:
        score_expr = score_expr + F.iff(
            F.col("GENRES").contains(genre),
            1,
            0
        )

    recommendations = (
        movie_features
        .filter(F.col("TITLE") != target_movie)
        .with_column("GENRE_SCORE", score_expr)
        .with_column(
            "FINAL_SCORE",
            F.col("GENRE_SCORE") + F.col("AVG_RATING")
        )
        .filter(F.col("FINAL_SCORE") > 8)
        .sort(F.col("FINAL_SCORE").desc())
        .select(
            "MOVIEID",
            "TITLE",
            "AVG_RATING",
            "RATING_COUNT",
            "GENRE_SCORE",
            "FINAL_SCORE"
        )
    )

    return recommendations
