--SELECT avg(val) from radiation where idfarm=205 and date BETWEEN '2015-01-01 00:00:0.000' AND '2016-01-30 00:00:0.000' group by extract(day from date)
SELECT 
	avg(val),extract(month from date) m,extract(day from date) d from radiation 
where 
	idfarm=222 and date BETWEEN '2015-10-03 00:00:0.000' AND '2015-12-31 00:00:0.000' 
group by 
	extract(day from date),extract(month from date)
order by 2,3

--SELECT * from radiation limit 10