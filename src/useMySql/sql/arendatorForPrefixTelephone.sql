select id as ID, name as `Имя`, date as `Дата`, telephone as `Телефон`
from `coursework`.arendator
where telephone LIKE '$prefix%'
