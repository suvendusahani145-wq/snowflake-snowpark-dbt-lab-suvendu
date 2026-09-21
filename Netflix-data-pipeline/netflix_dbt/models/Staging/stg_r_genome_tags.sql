select
    tag_id,
    tag,
    length(tag) as tag_length,
    case
        when tag ilike '%action%'
        then 'ACTION'
        when tag ilike '%romance%'
        then 'ROMANCE'
        else 'OTHER'
    end as tag_category

from {{ ref('Bronze_R_GENOME_TAGS') }}