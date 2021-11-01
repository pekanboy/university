select id as ID, name as 'Имя', price_per_day as 'Цена за день'
from university.services as s
where  s.price_per_day > $price
