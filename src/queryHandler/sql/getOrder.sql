select o.id as ID, o.start_date, o.fullcost, o.arend_id
from coursework.`order` as o
where start_date='$start_date' and arend_id='$arend_id'
