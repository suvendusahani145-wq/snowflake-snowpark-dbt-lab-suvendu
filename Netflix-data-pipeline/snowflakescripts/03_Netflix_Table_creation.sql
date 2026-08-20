USE DATABASE NETFLIX;
USE WAREHOUSE NETFLIX_WH;
USE SCHEMA NETFLIX.RAW;

CREATE OR REPLACE TABLE NETFLIX.RAW.R_MOVIES
(
movieId NUMBER primary KEY,
title STRING,
genres VARCHAR
);

CREATE TABLE NETFLIX.RAW.R_RATINGS (
    R_KEY NUMBER AUTOINCREMENT START 1 INCREMENT 1,
    movieId NUMBER,
    rating NUMBER(2,1),
    RATING_TIMESTAMP TIMESTAMP,
    CONSTRAINT F_RAT_MOVIES
        FOREIGN KEY (movieId)
        REFERENCES NETFLIX.RAW.R_MOVIES (movieId)
);

CREATE OR REPLACE TABLE  NETFLIX.RAW.r_genome_tags
(tagid NUMBER PRIMARY KEY,
tag VARCHAR);


CREATE or REPLACE TABLE NETFLIX.RAW.R_TAGS
(userID NUMBER,
movieId Number,
tag VARCHAR,
TAG_TIMESTAMP TIMESTAMP,
constraint f_TAG_movies foreign key (movieId)
references r_movies (movieId)
);



CREATE TABLE r_genome_scores
(movieId NUMBER
,tagId NUMBER
,relevance  NUMBER(18,0)
,constraint f_TAG_movies foreign key (movieId)
references r_movies (movieId))




