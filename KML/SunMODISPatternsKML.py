#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  windRoseKML.py
#  
#  Copyright 2015 Omar Ernesto Cabrera Rosero <omarcabrera@udenar.edu.co>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 
  
import Pdbc
import math
from pyproj import Proj, transform
from pykml.factory import KML_ElementMaker as KML
from lxml import etree
  
db = Pdbc.DBConnector('modis', 'bayron', 'bayron123', 'localhost', '5432')
  
inf = float("inf")
  
dictDirection ={'1':(0,195.985), '2':(195.985, 196.496), '3':(196.496,197.047), '4':(197.047,199.124),
             '5':(199.124,205.954), '6':(205.954, 228.426), '7':(228.426, 233.534), '8':(233.534, inf)} 
               
colors = {'1':'ff0000ff', '2':'ffff00ff', '3':'ffff0000', '4':'ffffff00', 
          '5':'ff00ff00', '6':'ff00ffff', '7':'ff00007f', '8':'ff7f007f'}
            
def reproject3857to4326(point):
    inProj = Proj(init='epsg:3857')
    outProj = Proj(init='epsg:4326')
    x,y = transform(inProj,outProj,point[0],point[1])
    pointstr = str(x)+','+str(y) 
    return pointstr
  
def buildKML(patterns, latitude, longitude,days,frequence):
    patterns = [(i.replace("\'",'').replace('\"','')) for i in patterns]
    origin = (latitude, longitude)
    count = 100
    global pm1
    pm1 = KML.Placemark(
            KML.TimeStamp(KML.when(count)),
            KML.name("f: "+str(frequence)),
            KML.Point( KML.coordinates(reproject3857to4326(origin))),
            KML.Style(
                KML.IconStyle(
                    KML.Icon(KML.href(""))
                )
            )
    )
    folder.append(pm1)
    for pattern in patterns:
        coor = reproject3857to4326(origin)
        if(pattern == '1'):
            pm1 = KML.Placemark(
            KML.TimeStamp(KML.when(count)),
            KML.Point( KML.coordinates(coor)),
            KML.Style(
                KML.IconStyle(
                    KML.Icon(KML.href("suns/so1.png"))
                )
            )
            )
            folder.append(pm1)
        elif(pattern == '2'):
            pm1 = KML.Placemark(
            KML.TimeStamp(KML.when(count)),
            KML.Point( KML.coordinates(coor)),
            KML.Style(
                KML.IconStyle(
                    KML.Icon(KML.href("suns/so2.png"))
                )
            )
            )
            folder.append(pm1)
        elif(pattern == '3'):
            pm1 = KML.Placemark(
            KML.TimeStamp(KML.when(count)),
            KML.Point( KML.coordinates(coor)),
            KML.Style(
                KML.IconStyle(
                    KML.Icon(KML.href("suns/so3.png"))
                )
            )
            )
            folder.append(pm1)
        elif(pattern == '4'):
            pm1 = KML.Placemark(
            KML.TimeStamp(KML.when(count)),
            KML.Point( KML.coordinates(coor)),
            KML.Style(
                KML.IconStyle(
                    KML.Icon(KML.href("suns/so4.png"))
                )
            )
            )
            folder.append(pm1)
        elif(pattern == '5'):
            pm1 = KML.Placemark(
            KML.TimeStamp(KML.when(count)),
            KML.Point( KML.coordinates(coor)),
            KML.Style(
                KML.IconStyle(
                    KML.Icon(KML.href("suns/so5.png"))
                )
            )
            )
            folder.append(pm1)
        elif(pattern == '6'):
            pm1 = KML.Placemark(
            KML.TimeStamp(KML.when(count)),
            KML.Point( KML.coordinates(coor)),
            KML.Style(
                KML.IconStyle(
                    KML.Icon(KML.href("suns/so6.png"))
                )
            )
            )
            folder.append(pm1)
        elif(pattern == '7'):
            pm1 = KML.Placemark(
            KML.TimeStamp(KML.when(count)),
            KML.Point( KML.coordinates(coor)),
            KML.Style(
                KML.IconStyle(
                    KML.Icon(KML.href("suns/so7.png"))
                )
            )
            )
            folder.append(pm1)
        elif(pattern == '8'):
            pm1 = KML.Placemark(
            KML.TimeStamp(KML.when(count)),
            KML.Point( KML.coordinates(coor)),
            KML.Style(
                KML.IconStyle(
                    KML.Icon(KML.href("suns/so8.png"))
                )
            )
            )
            folder.append(pm1)
        count+=100
        
  
def drawPatterns(table, param):
    query = 'SELECT * FROM best300point ORDER BY latitude, longitude'
    stations = db.resultQuery(query)
    for station in stations:
        query = 'SELECT max({0}) FROM {1} WHERE latitude={2} and longitude={3}'.format(param, table, station[0], station[1])
        maxParam = db.resultQuery(query)
        if(param == 'len_pattern'):
            query = '''SELECT 
                            *
                       FROM 
                            {0} 
                       WHERE 
                            latitude={1} and longitude={2} and {3}={4}
                       ORDER BY 
                            len_pattern, diff_solar, frequency'''.format(table, station[0], station[1], param, maxParam[0][0])
        elif(param == 'frequency'):
            query = '''SELECT 
                            *
                       FROM 
                            {0} 
                       WHERE 
                            latitude={1} and longitude={2} and {3}={4}
                       ORDER BY 
                            frequency, len_pattern, diff_solar'''.format(table, station[0], station[1], param, maxParam[0][0])
        elif(param == 'diff_solar'):
            query = '''SELECT 
                            *
                       FROM 
                            {0} 
                       WHERE 
                            latitude={1} and longitude={2} and {3}={4}
                       ORDER BY 
                            diff_solar, len_pattern, frequency'''.format(table, station[0], station[1], param, maxParam[0][0])
             
          
        result = db.resultQuery(query)
        latitude = result[0][1]
        longitude = result[0][2]
        patterns = result[0][3]
        days = result[0][4]
        frequence = result[0][5]
        print(stations,param,patterns)
        buildKML(patterns, latitude, longitude,days,frequence)
         
      
def main():
    global folder
    namesKML = ['diff_solar','len_pattern', 'frequency']
      
    for nameKML in namesKML:
        folder = KML.Folder()    
        for i in range(1,9):
            style = KML.Style(
                        KML.PolyStyle(
                            KML.color(colors[str(i)]),
                            KML.colorMode('normal')
                            ),
                        id="color"+str(i)
                    )    
            folder.append(style)
        drawPatterns('patternsbyday', nameKML)       
        outfile = open(nameKML+'.kml','wb')
        outfile.write(etree.tostring(folder, pretty_print=True))
        outfile.close()    
  
if __name__ == '__main__':
    main()
