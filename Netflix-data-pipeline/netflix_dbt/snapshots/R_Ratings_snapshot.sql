{% snapshot R_ratings_snapshot %}

{{
  config(unique_key='R_KEY',
         strategy= 'check',
         check_cols=['Movieid','Rating']
         )
}}

select * 
from {{ source('RAW','R_RATINGS') }}

{% endsnapshot %}