update  cloud2014 Q set type_cloud = (Select 0 from cloud2014 P where band1<6500 and Q.latitude=P.latitude and Q.longitude=P.longitude and Q.datecapture=P.datecapture)

--REPORTE PROMEDIOS MENSUALES DE CADA ESTACION INSTALADA
SELECT 
	farm.id,name,latitude,longitude,extract(month from date), avg(val)
from 
	farm
	join 
	radiation
	on farm.id=idfarm
where 
	val>0 and latitude not like'0' and longitude not like'0'
group by 
	farm.id,extract(month from date)

