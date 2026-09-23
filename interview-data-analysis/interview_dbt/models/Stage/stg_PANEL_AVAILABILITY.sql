{{config(materialized= 'incremental', 
          schema= 'Stage',
          unique_key= ['EMAIL_ID','INTERVIEW_DATE'],
          incremental_strategy= 'merge')}}

SELECT
    PANELIST_NAME,
    EMAIL_ID,
    AVAILABILITY_STATUS,
    CASE
        WHEN UPPER(AVAILABILITY_STATUS) LIKE '%PTO%'
        OR UPPER(AVAILABILITY_STATUS) LIKE '%NOT AVAILABLE%'
        OR UPPER(AVAILABILITY_STATUS) LIKE 'NA%'
        OR AVAILABILITY_STATUS = 'x'
        THEN 'UNAVAILABLE'
        WHEN UPPER(AVAILABILITY_STATUS) LIKE 'TENTATIVE%'
        THEN 'TENTATIVE'
        ELSE 'AVAILABLE'
    END AS AVAILABILITY_CATEGORY,
    INTERVIEW_DATE
    FROM {{ ref('Bronze_PANEL_AVAILABILITY')}}


{% if is_incremental()%}
WHERE INTERVIEW_DATE >= (SELECT COALESCE(DATEADD(DAY,-7,MAX(INTERVIEW_DATE)),'1900-01-01'::DATE) FROM {{this}})
{%endif%}