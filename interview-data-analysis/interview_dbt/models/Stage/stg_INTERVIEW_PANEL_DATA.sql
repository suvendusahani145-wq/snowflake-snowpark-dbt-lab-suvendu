{{config(materialized= 'incremental', 
          schema= 'staging',
          unique_key= 'INTERVIEW_KEY',
          incremental_strategy= 'merge')}}

SELECT 
       INTERVIEW_KEY,
       CANDIDATE_NAME,
       GROUP_NAME,
       DEMAND,
       EXPERIENCE_YEARS,
       CASE WHEN EXPERIENCE_YEARS_NUM < 3 THEN 'JUNIOR'
            WHEN EXPERIENCE_YEARS_NUM <7 THEN 'MID'
            ELSE 'SENIOR'
            END AS EXPERIENCE_BAND,
       PROFILE_SHARED_BY,
       CONTACT_DETAILS,
       CANDIDATE_EMAIL_ID,
       CANNDIATE_MOBILE,
       ASSIGNED_DATE,
       EVALUATION_DATE_TIME,
       PANEL_NAME,
       L1_STATUS,
       L2_STATUS,
       CUSTOMER_ROUND_STATUS,
       L1_FEEDBACK,
       L2_FEEDBACK,
       COMMENTS,
       ACTION_ITEM
FROM {{ ref('Bronze_INTERVIEW_PANEL_DATA') }}