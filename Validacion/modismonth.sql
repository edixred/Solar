SELECT m.* FROM( 
(SELECT grid450_id,value_point AS january FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='January') a1 
NATURAL JOIN 
(SELECT grid450_id,value_point AS february FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='February') a2 
NATURAL JOIN 
(SELECT grid450_id,value_point AS march FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='March') a3 
NATURAL JOIN 
(SELECT grid450_id,value_point AS april FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='April') a4 
NATURAL JOIN 
(SELECT grid450_id,value_point AS May FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='May') a5 
NATURAL JOIN 
(SELECT grid450_id,value_point AS June FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='June') a6 
NATURAL JOIN 
(SELECT grid450_id,value_point AS July FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='July') a7 
NATURAL JOIN 
(SELECT grid450_id,value_point AS August FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='August') a8 
NATURAL JOIN 
(SELECT grid450_id,value_point AS September FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='September') a9 
NATURAL JOIN 
(SELECT grid450_id,value_point AS october FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='October') a10 
NATURAL JOIN 
(SELECT grid450_id,value_point AS november FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='November') a11 
NATURAL JOIN 
(SELECT grid450_id,value_point AS december FROM grid_450 natural join  maps_sun_modis where latitude_3857=? and longitude_3857=? and tag_time='December') a12 
) as m
