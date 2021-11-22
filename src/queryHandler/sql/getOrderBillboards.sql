select (to_days(end_ar) - to_days(s.start_ar)) as days, s.cost_period, s.bil_id as 'ID', b.cost as 'Цена'
from coursework.string_order as s
inner join coursework.bilboard as b on s.bil_id=b.id
where ord_id='$id'