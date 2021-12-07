select to_days(end_ar) as end_date, to_days(s.start_ar) as start_date, s.cost_period, s.bil_id as 'ID', b.cost as 'Цена', b.square as `Площадь`, b.address as `Адрес`
from coursework.string_order as s
inner join coursework.bilboard as b on s.bil_id=b.id
where ord_id='$id'