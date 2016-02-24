insert into  Cb300point 
--create TABLE cb300point as(
select datecapture,latitude,longitude,band1,band2,band3,type_cloud from clouds join best300point using(latitude,longitude) where band1>6500 and band2>6500 and band3>6500 order by 1
