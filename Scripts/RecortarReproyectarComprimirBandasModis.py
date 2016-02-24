#!/usr/bin/env python3
import os
import os.path
import psycopg2
from osgeo import gdal
import numpy as np
import math
import datetime

def saveTifBD(listBandFolder, dateimg):
    bdtiff=open('FAUX.csv','a')
    bdtiffNubes=open('FAUXNUBES.csv','a')
    nfoband1=gdal.Open (listBandFolder[0],gdal.GA_ReadOnly)
    sizeXCols=nfoband1.RasterXSize
    sizeYRows = nfoband1.RasterYSize
    geoTransform=nfoband1 .GetGeoTransform()
    originX = geoTransform[0]
    originY = geoTransform[3]
    tifband1=gdal.Open (listBandFolder[0]).ReadAsArray()
    tifband2=gdal.Open (listBandFolder[1]).ReadAsArray()
    tifband3=gdal.Open (listBandFolder[2]).ReadAsArray()
    tifband4=gdal.Open (listBandFolder[3]).ReadAsArray()
    tifband5=gdal.Open (listBandFolder[4]).ReadAsArray()
    tifband6=gdal.Open (listBandFolder[5]).ReadAsArray()
    tifband7=gdal.Open (listBandFolder[6]).ReadAsArray()
    for x in range(0, sizeYRows, 1): #recorrer el tif horizontalmente
        for y in range(0,sizeXCols,  1):#recorrer el tif verticalmente
            vb1=tifband1[x][y]
            vb2=tifband2[x][y]
            vb3=tifband3[x][y]
            vb4=tifband4[x][y]
            vb5=tifband5[x][y]
            vb6=tifband6[x][y]
            vb7=tifband7[x][y]
            if vb1>0:
                latAux=originX+(450*y)
                latitude=latAux-(latAux%450)
                lonAux=originY-(450*x)
                longitude=lonAux-(lonAux%450)
                if vb1>0 and vb1<6000:
                    bdtiff.write(str(dateimg)+';'+str(int(latitude))+';'+str(int(longitude))+';'+str(vb1)+';'+str(vb2)+';'+str(vb3)+';'+str(vb4)+';'+str(vb5)+';'+str(vb6)+';'+str(vb7)+"\n")
                if vb1>=6000 and vb1<8000:
                    bdtiffNubes.write(str(dateimg)+';'+str(int(latitude))+';'+str(int(longitude))+';'+str(vb1)+';'+str(vb2)+';'+str(vb3)+";A\n")#ALTOSTRATUS
                if vb1>=8000 and vb1<10000:
                    bdtiffNubes.write(str(dateimg)+';'+str(int(latitude))+';'+str(int(longitude))+';'+str(vb1)+';'+str(vb2)+';'+str(vb3)+";N\n")#Nimbostratus
                    #print(str(latAux)+'||'+str(lonAux)+'||'+str(vb1)+'||'+str(vb2)+'||'+str(vb3)+'||'+str(vb4)+'||'+str(vb5)+'||'+str(vb6)+'||'+str(vb7)+"\n")
    bdtiff.close()
    bdtiffNubes.close()
    try:        
        conn = psycopg2.connect("dbname='modis' user='postgres' password='postgres1' host='localhost' port='5432'")#parametros  para la conexion a la base de datos
        cur = conn.cursor()
        print("Connection OK")
        try:
            filecsv=open('FAUX.csv', 'r')#abrir archivo anteriormente generado con los datos de la imagen modis
            filecsvnubes=open('FAUXNUBES.csv', 'r')#abrir archivo anteriormente generado con los datos de la imagen modis
            cur.copy_from(filecsv,'bands1_7', columns = ('datecapture', 'latitude_3857', 'longitude_3857', 'band1', 'band2',  'band3', 'band4', 'band5', 'band6', 'band7'), sep=";" )#copear datos del csv a base de datos
            cur.copy_from(filecsvnubes,'clouds', columns = ('datecapture', 'latitude_3857', 'longitude_3857', 'band1', 'band2',  'band3', 'type_cloud'), sep=";" )#copear datos del csv a base de datos
            conn.commit()
            print("COPY OK")
            os.system('rm FAUX.csv') 
            os.system('rm FAUXNUBES.csv') 
        except StandardError, err:
            conn.rollback()
            os.system('rm FAUX.csv')
            os.system('rm FAUXNUBES.csv') 
            print("   Caught error:\n", err)
    except:
        print("No connection")
        os.system('rm FAUX.csv')
        os.system('rm FAUXNUBES.csv')  

def reprojectAndClipper(listFileHdf):
    report=open('ReportHDF-Tif.csv','a')
    for i in range(len(listFileHdf)-1):
        if os.path.isfile(listFileHdf[i]):
            folderNametoHDFtotargz=listFileHdf[i].split(".hdf")
            nameHfdFile=listFileHdf[i].split("/")
            os.system('mkdir '+folderNametoHDFtotargz[0])
            os.system('modis_convert.py -s "(0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1)" -o '+folderNametoHDFtotargz[0]+'/'+nameHfdFile[1]+' -e 3857 -g 450 '+listFileHdf[i])
            nameBandTif=os.popen('ls '+folderNametoHDFtotargz[0]+'/*.tif').read().split("\n")
            for j in range(len(nameBandTif)-1):
                os.system('gdalwarp -overwrite -dstnodata 0 -q -cutline '+ 'narino/narino_3857.shp -crop_to_cutline -of GTiff '+ nameBandTif[j]+' '+nameBandTif[j]+'.copy')
                os.system('rm '+nameBandTif[j])
                os.system('mv '+nameBandTif[j]+'.copy '+nameBandTif[j])
                listBandFolder= os.popen('ls '+folderNametoHDFtotargz[0]+'/*.tif').read().split("\n")
            auxdate=nameHfdFile[1].split(".")
            year=auxdate[1][1:5]
            day=auxdate[1][5:8]
            dateimg = datetime.date(int(year), 1, 1) + datetime.timedelta(int(day) - 1)
            saveTifBD(listBandFolder, dateimg)
            os.system('rm -R '+folderNametoHDFtotargz[0])
            report.write(nameHfdFile[1]+";OK\n")
    report.close()        
pathfilesHDF = 'HDF/'
listFileHdf= os.popen('ls '+pathfilesHDF+'*.hdf').read().split("\n")
reprojectAndClipper(listFileHdf)
