#Scrip para guardar los mapas de Irradiacion Solar MODIS  resultantes
import os
import sys
import psycopg2
import io
import math
import os.path
from osgeo import gdal
def setMaps(namemaps):
    bdtiff=open('FAUX.csv','a')
    map1=""
    for i in range(len(namemaps)-1):
        if 'General' in namemaps[i]:
            map1=namemaps[i]
    #DATOS PARA RECORRER 12 MAPAS 
    infoMapJanury=gdal.Open (namemaps[0],gdal.GA_ReadOnly)
    sizeXCols=infoMapJanury.RasterXSize
    sizeYRows = infoMapJanury.RasterYSize
    geoTransform=infoMapJanury .GetGeoTransform()
    originX = geoTransform[0]
    originY = geoTransform[3]
    m1=gdal.Open (map1).ReadAsArray()
    for x in range(0, sizeYRows, 1): #recorrer el tif horizontalmente
        for y in range(0,sizeXCols,  1):#recorrer el tif verticalmente
            vmap1=-100
            if m1[x][y]<250:
                vmap1=m1[x][y]
                latAux=originX+(450*y)
                latitude=latAux-(latAux%450)
                lonAux=originY-(450*x)#longitud en punto
                longitude=lonAux-(lonAux%450)
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"General"+";"+str(vmap1)+"\n")
    bdtiff.close()
    print "... CONECTANDO"
    try:        
        conn = psycopg2.connect("dbname='geoalternar' user='bayron' password='bayron123' host='localhost' port='5432'")#parametros  para la conexion a la base de datos
        cur = conn.cursor()
        print("Connection OK")
        try:
            filecsv=open('FAUX.csv', 'r')#abrir archivo anteriormente generado con los datos de la imagen landsat
            cur.copy_from(filecsv,'maps_sun_modis', columns = ('latitude', 'longitude', 'tag_time', 'value_radiation'), sep=";" )#copear datos del csv a base de datos
            conn.commit()
            print("COPY OK")
            os.system('rm FAUX.csv') 
        except StandardError, err:
            conn.rollback()
            os.system('rm FAUX.csv')
            print("   Caught error:\n", err)
    except:
        print("No connection")
    
namemaps = os.popen('ls *.tif').read().split("\n")
setMaps(namemaps)
