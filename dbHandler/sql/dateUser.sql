select c.id, name, address
from university.clients as c
left join university.connected_services as cs on c.id =cs.id_client and cs.subscribe_date >= '$before' and cs.subscribe_date < '$after'
where  cs.id is NULL