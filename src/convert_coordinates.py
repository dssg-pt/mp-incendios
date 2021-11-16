# Python 3.7.3
# Not the best method, running slowly, better to use geopandas

import os
import csv
#from osgeo import gdal
from osgeo import osr
from osgeo import ogr
import time
start=time.time()

# Coordinate Reference System (CRS)
#https://luiscarlosmadeira.blogs.sapo.pt/42487.html
SourceEPSG = 20790 # https://epsg.io/20790 Lisboa Hayford Gauss (IGeoE military national grid)
TargetEPSG = 4326 # https://epsg.io/4326

source = osr.SpatialReference()
#source.ImportFromEPSG(SourceEPSG) # not loading GDAL data sometimes, error argument 2
source.ImportFromProj4('+proj=tmerc +lat_0=39.66666666666666 +lon_0=1 +k=1 +x_0=200000 +y_0=300000 +ellps=intl +towgs84=-304.046,-60.576,103.64,0,0,0,0 +pm=lisbon +units=m +no_defs')

target = osr.SpatialReference()
#target.ImportFromEPSG(TargetEPSG)
target.ImportFromProj4('+proj=longlat +datum=WGS84 +no_defs')

# Input file details
datapath = os.path.abspath("CdD_filtered_data.csv")
outpath = os.path.abspath("CdD_filtered_data_latlong.csv")

def CRSTransform(x, y):
    transform = osr.CoordinateTransformation(source, target)
    point = ogr.Geometry(ogr.wkbPoint)
    point.SetPoint_2D(0, float(x), float(y))
    point.Transform(transform)
    long = point.GetX()
    lat = point.GetY()
    #print(lat,"  ",long)
    return long,lat

fieldnames = ['','concelho','data_inicio','area_total','x','y','month','year','Source']
outfile = open(outpath,'w', encoding='UTF8')
#writer = csv.DictWriter(outfile, fieldnames=fieldnames, lineterminator='\n')
#writer.writeheader()

infile = open(datapath,'r', encoding='UTF8')
reader = csv.DictReader(infile)

with open(outpath, mode='w', encoding='UTF8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    for row in reader:
        #print(row)
        #fieldnames = row.keys()
        x = row['x']
        y = row['y']
        long,lat = CRSTransform(x, y)
        #print(lat, long)
        row['x'] = str(long)
        row['y'] = str(lat)
        #print(row)
        writer.writerow(row)
        if row[''] == "10":
            pass
            #break

outfile.close()
infile.close()

end=time.time()
print('run took', (end-start)/60, 'minutes')
