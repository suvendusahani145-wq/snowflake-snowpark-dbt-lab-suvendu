select *
from {{ ref('stg_R_RATINGS') }}
where rating < 2