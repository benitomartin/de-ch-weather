 {#
    This macro returns warnings of the air quality
#}


{% macro get_warnings(category) -%}
    case
        when {{ category }} = 'Excellent air quality' then 'None. Enjoy the day!'
        when {{ category }} = 'Good air quality' then 'None. Enjoy the day!'
        when {{ category }} = 'Moderate air quality' then 'People unusually sensitive to air pollution: Plan strenuous outdoor activities when air quality is better'
        when {{ category }} = 'Low air quality' then 'Cut back or reschedule strenuous outdoor activities'
        when {{ category }} = 'Poor air quality' then 'Avoid all outdoor physical activities'
    end
{% endmacro %}