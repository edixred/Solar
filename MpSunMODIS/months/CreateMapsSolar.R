# Ordinary Kriging

library(rgdal)
library(maptools)
library(gstat)
library(sp)
library(geoR)

args <- commandArgs(TRUE)

dataIn <- args[1]
gridIn <- 'grid450.csv'
nameGeotiff <- args[2]

data<-read.table(dataIn, sep=";", header=T)

geoValue <- as.geodata(data,1:2,10)
#plot(geoValue)

coordinates(data)=~latitude+longitude

## poner sistema de coordenadas a los datos
proj4string(data)=CRS("+init=epsg:3857")

# Cargar malla 1000,2500, 5000, 6000
study.grid <-read.table(gridIn, sep=",", header=T)

coordinates(study.grid)=~X+Y

## poner sistema de coordenadas a la malla
proj4string(study.grid)=CRS("+init=epsg:3857")

# Ajustando el variograma
# primer trazo del variograma
#plot(variogram(Value~1,data))

#Crear un modelo del variograma
study.grid<- as(study.grid, "SpatialPixelsDataFrame")
mod<-vgm(psill=var(data$Value),model="Sph",range=sqrt(areaSpatialGrid(study.grid))/4,nugget=0)

# Segundo, se ajusta el variograma
# Vamas a ajustar el variograma a modelo REML
#fit_reml<-fit.variogram.reml(Value~1,data,model=mod)

#plot(variogram(Value~1,data),fit_reml,main="REML Model")

# Ahora vamos a intentar ajustar el variograma con otro algoritmo 
# por ejemplo con el cuadrado minimo ordinario 
fit_ols<-fit.variogram(variogram(Value~1,data),model=mod,fit.method=6)

#plot(variogram(Value~1,data),fit_ols,main="OLS Model")

#Kriging 1-out Cross Validation
#cross1<-krige.cv(Value~1,data,model=fit_reml)

#Goodness of Fit of the Cross Validation
#RSQR<-as.numeric(cor.test(data$Value,cross1$var1.pred)$estimate)^2  #Pearson's R Squared
#RMSD<-sqrt(sum((cross1$residual)^2)/length(data$Value))             #Root Mean Square Deviation


#Let's try a cross validation using the OLS model
#cross1<-krige.cv(Value~1,data,model=fit_ols)

#Goodness of Fit of the Cross Validation
#RSQR<-as.numeric(cor.test(data$Value,cross1$var1.pred)$estimate)^2  #Pearson's R Squared
#RMSD<-sqrt(sum((cross1$residual)^2)/length(data$Value))             #Root Mean Square Deviation

#Plot observed versus residuals
#plot(data$Value,cross1$var1.pred,asp=1,xlab="Observed",ylab="Predicted")
#abline(0,1,col="red",cex=0.5)

#The results are apparently better, just because the number of observation is smaller
#in this case, because the area is a field the best cross-validation is the one embedded into gstat
#but for larger areas, catchment or landscape scale, this validation procedure is less time and RAM consuming


#Interpolation and Map creation
#now that we finished the cross-validation part we can proceed to the creation of the map
map<-krige(Value~1,data,model=fit_ols,newdata=study.grid)
#spplot(map,"var1.pred",col.regions=terrain.colors(50))

writeGDAL(map["var1.pred"], fname=nameGeotiff, drivername = "GTiff", 
          type = "Float32", mvFlag = 255)
