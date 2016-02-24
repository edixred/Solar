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
    map2=""
    map3=""
    map4=""
    map5=""
    map6=""
    map7=""
    map8=""
    map9=""
    map10=""
    map11=""
    map12=""
    for i in range(len(namemaps)-1):
        if 'anuary' in namemaps[i]:
            map1=namemaps[i]
        if 'ebruary' in namemaps[i]:
            map2=namemaps[i]
        if 'arch' in namemaps[i]:
            map3=namemaps[i]
        if 'pril' in namemaps[i]:
            map4=namemaps[i]
        if 'ay' in namemaps[i]:
            map5=namemaps[i]
        if 'un' in namemaps[i]:
            map6=namemaps[i]
        if 'ul' in namemaps[i]:
            map7=namemaps[i]
        if 'ugust' in namemaps[i]:
            map8=namemaps[i]
        if 'eptember' in namemaps[i]:
            map9=namemaps[i]
        if 'ctober' in namemaps[i]:
            map10=namemaps[i]
        if 'ovember' in namemaps[i]:
            map11=namemaps[i]
        if 'ecember' in namemaps[i]:
            map12=namemaps[i]
    #DATOS PARA RECORRER 12 MAPAS 
    infoMapJanury=gdal.Open (namemaps[1],gdal.GA_ReadOnly)
    sizeXCols=infoMapJanury.RasterXSize
    sizeYRows = infoMapJanury.RasterYSize
    geoTransform=infoMapJanury .GetGeoTransform()
    originX = geoTransform[0]
    originY = geoTransform[3]
    m1=gdal.Open (map1).ReadAsArray()
    m2=gdal.Open (map2).ReadAsArray()
    m3=gdal.Open (map3).ReadAsArray()
    m4=gdal.Open (map4).ReadAsArray()
    m5=gdal.Open (map5).ReadAsArray()
    m6=gdal.Open (map6).ReadAsArray()
    m7=gdal.Open (map7).ReadAsArray()
    m8=gdal.Open (map8).ReadAsArray()
    m9=gdal.Open (map9).ReadAsArray()
    m10=gdal.Open (map10).ReadAsArray()
    m11=gdal.Open (map11).ReadAsArray()
    m12=gdal.Open (map12).ReadAsArray()
    for x in range(0, sizeYRows, 1): #recorrer el tif horizontalmente
        for y in range(0,sizeXCols,  1):#recorrer el tif verticalmente
            vmap1=-100
            vmap2=-200
            vmap3=-300
            vmap4=-400
            vmap5=-500
            vmap6=-600
            vmap7=-700
            vmap8=-800
            vmap9=-900
            vmap10=-1000
            vmap11=-1100
            vmap12=-1200
            if m1[x][y]<250:
                vmap1=m1[x][y]
                vmap2=m2[x][y]
                vmap3=m3[x][y]
                vmap4=m4[x][y]
                vmap5=m5[x][y]
                vmap6=m6[x][y]
                vmap7=m7[x][y]
                vmap8=m8[x][y]
                vmap9=m9[x][y]
                vmap10=m10[x][y]
                vmap11=m11[x][y]
                vmap12=m12[x][y]
                latAux=originX+(450*y)
                latitude=latAux-(latAux%450)+450
                lonAux=originY-(450*x)#longitud en punto
                longitude=lonAux-(lonAux%450)
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"January"+";"+str(vmap1)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"February"+";"+str(vmap2)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"March"+";"+str(vmap3)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"April"+";"+str(vmap4)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"May"+";"+str(vmap5)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"June"+";"+str(vmap6)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"July"+";"+str(vmap7)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"August"+";"+str(vmap8)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"September"+";"+str(vmap9)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"October"+";"+str(vmap10)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"November"+";"+str(vmap11)+"\n")
                bdtiff.write(str(math.trunc(latitude))+";"+str(math.trunc(longitude))+";"+"December"+";"+str(vmap12)+"\n")
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
