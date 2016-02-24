#Scrip para guardar los mapas de radiacion solar MODIS resultantes
import os
import sys
import psycopg2
import io
import math
import os.path
from osgeo import gdal
def setMaps(namemaps):
    bdtiff=open('FAUX.csv','a')
    map5=""
    map6=""
    map7=""
    map8=""
    map9=""
    map10=""
    map11=""
    map12=""
    map13=""
    map14=""
    map15=""
    for i in range(len(namemaps)-1):
        if '2005' in namemaps[i]:
            map5=namemaps[i]
        if '2006' in namemaps[i]:
            map6=namemaps[i]
        if '2007' in namemaps[i]:
            map7=namemaps[i]
        if '2008' in namemaps[i]:
            map8=namemaps[i]
        if '2009' in namemaps[i]:
            map9=namemaps[i]
        if '2010' in namemaps[i]:
            map10=namemaps[i]
        if '2011' in namemaps[i]:
            map11=namemaps[i]
        if '2012' in namemaps[i]:
            map12=namemaps[i]
        if '2013' in namemaps[i]:
            map13=namemaps[i]
        if '2014' in namemaps[i]:
            map14=namemaps[i]
        if '2015' in namemaps[i]:
            map15=namemaps[i]
    #DATOS PARA RECORRER 12 MAPAS 
    infoMapJanury=gdal.Open (namemaps[1],gdal.GA_ReadOnly)
    sizeXCols=infoMapJanury.RasterXSize
    sizeYRows = infoMapJanury.RasterYSize
    geoTransform=infoMapJanury .GetGeoTransform()
    originX = geoTransform[0]
    originY = geoTransform[3]
    m5=gdal.Open (map5).ReadAsArray()
    m6=gdal.Open (map6).ReadAsArray()
    m7=gdal.Open (map7).ReadAsArray()
    m8=gdal.Open (map8).ReadAsArray()
    m9=gdal.Open (map9).ReadAsArray()
    m10=gdal.Open (map10).ReadAsArray()
    m11=gdal.Open (map11).ReadAsArray()
    m12=gdal.Open (map12).ReadAsArray()
    m13=gdal.Open (map13).ReadAsArray()
    m14=gdal.Open (map14).ReadAsArray()
    m15=gdal.Open (map15).ReadAsArray()
    for x in range(0, sizeYRows, 1): #recorrer el tif horizontalmente
        for y in range(0,sizeXCols,  1):#recorrer el tif verticalmente
            vmap5=-500
            vmap6=-600
            vmap7=-700
            vmap8=-800
            vmap9=-900
            vmap10=-1000
            vmap11=-1100
            vmap12=-1200
            vmap13=-1300
            vmap14=-1400
            vmap15=-1400
            if m5[x][y]<250:
                vmap5=m5[x][y]
                vmap6=m6[x][y]
                vmap7=m7[x][y]
                vmap8=m8[x][y]
                vmap9=m9[x][y]
                vmap10=m10[x][y]
                vmap11=m11[x][y]
                vmap12=m12[x][y]
                vmap13=m13[x][y]
                vmap14=m14[x][y]
                vmap15=m15[x][y]
                latAux=originX+(450*y)
                latitude=latAux-(latAux%450)+450
                lonAux=originY-(450*x)#longitud en punto
                longitude=lonAux-(lonAux%450)
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"2005"+";"+str(vmap5)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"2006"+";"+str(vmap6)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"2007"+";"+str(vmap7)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"2008"+";"+str(vmap8)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"2009"+";"+str(vmap9)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"2010"+";"+str(vmap10)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"2011"+";"+str(vmap11)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"2012"+";"+str(vmap12)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"2013"+";"+str(vmap13)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"2014"+";"+str(vmap14)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"2015"+";"+str(vmap15)+"\n")
    bdtiff.close()
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
