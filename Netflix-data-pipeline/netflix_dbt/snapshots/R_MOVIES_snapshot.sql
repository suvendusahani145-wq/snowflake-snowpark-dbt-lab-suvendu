{% snapshot R_MOVIES %}



{{
  config(unique_key='MOVIEID',
         strategy='check',
         check_cols=['TITLE','GENRES']
        )
}}


select *
from {{ source('Bronze', 'R_MOVIES') }}


{% endsnapshot %}