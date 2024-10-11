import os

import numpy as np  # numerical library
import xarray as xr  # netCDF library
import pandas as pd

import matplotlib.pyplot as plt  # plotting library
import cartopy  # Map projections libary
import cartopy.crs as ccrs  # Projections list
import cartopy.feature as cfeature

from shapely.geometry import Polygon, Point
from shapely.ops import transform
import pyproj

import cftime

# Funciones
def point_in_polygon(lon, lat, polygon):
    point = Point(lon, lat)
    return polygon.contains(point)

# Transform the polygon to match the DataArray CRS if needed
def transform_polygon(polygon, src_crs='epsg:4326', tgt_crs='epsg:4326'):
    proj = pyproj.Transformer.from_proj(pyproj.Proj(src_crs), pyproj.Proj(tgt_crs), always_xy=True)
    return transform(lambda x, y: proj.transform(x, y), polygon)   

# Carga variables con directorios
HOME=os.environ['HOME']   
f = open(HOME+'/.env', 'r')
for line in f.readlines():
    Name=line.strip().split('=')[0]
    Content=line.strip().split('=')[-1]
    if Name=='dirData' or Name=='dirAnalisis':
        exec(Name + "=" + "'" + Content + "'")
f.close()

base_file1 = dirData + '/Climatologias/Glorys/cmems_mod_glo_phy_my_0.083_P1M-m_202311/'
base_file2 = dirData + '/Climatologias/Glorys/cmems_mod_glo_phy_myint_0.083deg_P1M-m_202311/'
dataDir    = dirAnalisis + '/IEOOSWebPage/data'
imageDir   = dirAnalisis + '/IEOOSWebPage/images'

print('>>>>> dataDir:'+dataDir)

Titulos = ['Demarcación marina canaria','Demarcación marina levantino-balear', 'Demarcación marina noratlántica', 'Demarcación sudatlántica','Demarcación Estrecho y Alborán']
Titulos_short = ['CAN','LEB', 'NOR','SUD','ESA']

files = []
for iy in range(1995,2021):
    for im in range(1,13):
        files.append(base_file1+"mercatorglorys12v1_gl12_mean_%04d%02d.nc"%(iy,im))
for iy in range(2021,2022):
    for im in range(1,7):
        files.append(base_file1+"mercatorglorys12v1_gl12_mean_%04d%02d.nc"%(iy,im))
for iy in range(2021,2022):
    for im in range(7,13):
        files.append(base_file2+"mercatorglorys12v1_gl12_mean_%04d%02d.nc"%(iy,im))
for iy in range(2022,2024):
    for im in range(1,13):
        files.append(base_file2+"mercatorglorys12v1_gl12_mean_%04d%02d.nc"%(iy,im))    

    print('>>>>> Reading files:'str(len(files)))

    DC = xr.open_mfdataset(files)
    DC = DC.drop_vars("mlotst").drop_vars("zos")
    DC = DC.drop_vars("sithick").drop_vars("siconc")
    DC = DC.drop_vars("usi").drop_vars("vsi").drop_vars("uo").drop_vars("vo").drop_vars("bottomT")


for iD in range(0,5):
    titulo = Titulos[iD]
    titulo_short = Titulos_short[iD]

    # Load the data from the .txt file
    demCoord = []
    longDem, latiDem = [], []
    with open('./LimiteDemarcaciones/Demarcacion'+titulo_short+'.txt', 'r') as f:
        for line in f:
            longitude, latitude = map(float, line.split())
            longDem.append(longitude)
            latiDem.append(latitude)
            demCoord.append((longitude,latitude))
    demPolygon = Polygon(demCoord)    
    demPolygon_transformed = transform_polygon(demPolygon)

## select data in the demarcation


    if titulo_short == 'LEB':
        slicelatitude=slice(35.5,42.75)
        slicelongitude=slice(358-360,368-360)
        DC_temp=DC.thetao.sel(latitude=slicelatitude).sel(longitude=slicelongitude).load()
        DC_salt=DC.so.sel(latitude=slicelatitude).sel(longitude=slicelongitude).load()
        print('>>>>> '+titulo)        

    elif  titulo_short == 'NOR':
        slicelatitude=slice(41.5,46.9)
        slicelongitude=slice(346-360,-1.5)
        DC_temp=DC.thetao.sel(latitude=slicelatitude).sel(longitude=slicelongitude).load()
        DC_salt=DC.so.sel(latitude=slicelatitude).sel(longitude=slicelongitude).load()
        print('>>>>> '+titulo)        
        
    elif  titulo_short == 'CAN':
        slicelatitude=slice(24,32.5)
        slicelongitude=slice(335-360,350-360)
        DC_temp=DC.thetao.sel(latitude=slicelatitude).sel(longitude=slicelongitude).load()
        DC_salt=DC.so.sel(latitude=slicelatitude).sel(longitude=slicelongitude).load()
        print('>>>>> '+titulo)

    elif  titulo_short == 'SUD':
        slicelatitude=slice(35.5,37.5)
        slicelongitude=slice(352-360,354.5-360)
        DC_temp=DC.thetao.sel(latitude=slicelatitude).sel(longitude=slicelongitude).load()
        DC_salt=DC.so.sel(latitude=slicelatitude).sel(longitude=slicelongitude).load()
        print('>>>>> '+titulo)

    elif  titulo_short == 'ESA':
        slicelatitude=slice(35.5,37)
        slicelongitude=slice(354-360,358.5-360)
        DC_temp=DC.thetao.sel(latitude=slicelatitude).sel(longitude=slicelongitude).load()
        DC_salt=DC.so.sel(latitude=slicelatitude).sel(longitude=slicelongitude).load()

    ## Mask the data
    mask = np.array([[point_in_polygon(lon,lat,demPolygon_transformed) 
         for lon in DC_temp.longitude.values] 
         for lat in DC_temp.latitude.values])
        
    DC_temp_unmasked = DC_temp
    DC_salt_unmasked = DC_salt

    DC_temp = DC_temp.where(mask)
    DC_salt = DC_salt.where(mask)

    DC_temp.to_netcdf('./Data/Glorys_DC_temp'+titulo_short+'.nc')
    DC_salt.to_netcdf('./Data/Glorys_DC_salt'+titulo_short+'.nc')

    DC_temp_unmasked.to_netcdf('./Data/Glorys_DC_temp_unmasked'+titulo_short+'.nc')
    DC_salt_unmasked.to_netcdf('./Data/Glorys_DC_salt_unmasked'+titulo_short+'.nc')