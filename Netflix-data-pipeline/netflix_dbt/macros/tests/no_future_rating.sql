{% test no_future_rating(model, column_name) %}

select *
from {{ model }}
where {{ column_name }} > current_date()

{% endtest %}

