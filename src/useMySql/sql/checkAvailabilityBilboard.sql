SELECT bil_id as id
from coursework.string_order
where bil_id = '$id' and
(start_ar < '$end_date' and end_ar >= '$end_date' or start_ar < '$start_date' and end_ar >= '$start_date')
