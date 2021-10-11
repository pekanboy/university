select id, name, price_per_day
from university.services as s
where  s.price_per_day > $price
