{{config(schema= 'Mart')}}

with panel_perf as(
SELECT
    PANEL_NAME,
    TO_CHAR(EVALUATION_DATE_TIME, 'MON-YYYY') AS INTERVIEW_MONTH,
    COUNT(DISTINCT INTERVIEW_KEY) AS NUMBER_OF_INTERVIEWS,

    SUM(
        CASE
            WHEN upper(L1_STATUS) = 'REJECTED'
              OR upper(L2_STATUS) = 'REJECTED'
              OR upper(CUSTOMER_ROUND_STATUS) = 'REJECTED'
            THEN 1
            ELSE 0
        END
    ) AS NUMBER_OF_CANDIDATE_REJECTED,

    SUM(
        CASE
            WHEN upper(CUSTOMER_ROUND_STATUS) = 'SELECTED'
            THEN 1
            ELSE 0
        END
    ) AS NUMBER_OF_CANDIDATE_SELECTED,
        SUM(
        CASE
            WHEN upper(L1_STATUS) = 'SELECTED' AND L2_STATUS IS NULL AND CUSTOMER_ROUND_STATUS IS NULL
            THEN 1
            WHEN upper(L2_STATUS) = 'SELECTED' AND CUSTOMER_ROUND_STATUS IS NULL
            THEN 1
            ELSE 0
        END
    ) AS NUMBER_OF_CANDIDATE_PENDING,
            SUM(
        CASE
            WHEN L1_STATUS LIKE '%Candidate Didnt joined%' OR L2_STATUS LIKE '%Candidate Didnt joined%' OR CUSTOMER_ROUND_STATUS LIKE '%Candidate Didnt joined%'
            THEN 1
            WHEN L1_STATUS LIKE '%No Show%' OR L2_STATUS LIKE '%No Show%' OR CUSTOMER_ROUND_STATUS LIKE '%No Show%'
            THEN 1
            WHEN UPPER(L1_STATUS) ='CANCELLED' OR UPPER(L2_STATUS) = 'CANCELLED' OR UPPER(CUSTOMER_ROUND_STATUS) = 'CANCELLED'
            THEN 1
            ELSE 0
        END
    ) AS NUMBER_OF_CANDIDATE_NO_SHOW

FROM {{ ref('stg_INTERVIEW_PANEL_DATA') }}

GROUP BY
    PANEL_NAME,
    TO_CHAR(EVALUATION_DATE_TIME, 'MON-YYYY'))

    SELECT
        INTERVIEW_MONTH,
        TRIM(f.VALUE::STRING) AS PANEL_NAME,
        NUMBER_OF_INTERVIEWS,
        NUMBER_OF_CANDIDATE_REJECTED,
        NUMBER_OF_CANDIDATE_SELECTED,
        NUMBER_OF_CANDIDATE_PENDING,
        NUMBER_OF_CANDIDATE_NO_SHOW
    FROM panel_perf  fp,
         LATERAL FLATTEN(
             INPUT => SPLIT(fp.PANEL_NAME,'&')
         ) f