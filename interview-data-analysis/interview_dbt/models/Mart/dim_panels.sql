{{config(schema= 'Mart')}}

with panel_master AS (
SELECT
    UPPER(TRIM(EMAIL_ID)) AS EMAIL_ID,
    MAX(PANELIST_NAME) AS PANELIST_NAME
FROM {{ ref('stg_PANEL_AVAILABILITY') }}
GROUP BY 1
)

SELECT *
FROM panel_master