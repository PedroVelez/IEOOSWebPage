import os

import numpy as np  # numerical library
import xarray as xr  # netCDF library
import pandas as pd

import matplotlib.pyplot as plt  # plotting library
from matplotlib.colors import LinearSegmentedColormap
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

cm_data = [[0.2422, 0.1504, 0.6603],[0.2444, 0.1534, 0.6728],[0.2464, 0.1569, 0.6847],[0.2484, 0.1607, 0.6961],[0.2503, 0.1648, 0.7071],[0.2522, 0.1689, 0.7179],[0.254, 0.1732, 0.7286],[0.2558, 0.1773, 0.7393],[0.2576, 0.1814, 0.7501],[0.2594, 0.1854, 0.761],[0.2611, 0.1893, 0.7719],[0.2628, 0.1932, 0.7828],[0.2645, 0.1972, 0.7937],[0.2661, 0.2011, 0.8043],[0.2676, 0.2052, 0.8148],[0.2691, 0.2094, 0.8249],[0.2704, 0.2138, 0.8346],[0.2717, 0.2184, 0.8439],[0.2729, 0.2231, 0.8528],[0.274, 0.228, 0.8612],[0.2749, 0.233, 0.8692],[0.2758, 0.2382, 0.8767],[0.2766, 0.2435, 0.884],[0.2774, 0.2489, 0.8908],[0.2781, 0.2543, 0.8973],[0.2788, 0.2598, 0.9035],[0.2794, 0.2653, 0.9094],[0.2798, 0.2708, 0.915],[0.2802, 0.2764, 0.9204],[0.2806, 0.2819, 0.9255],[0.2809, 0.2875, 0.9305],[0.2811, 0.293, 0.9352],[0.2813, 0.2985, 0.9397],[0.2814, 0.304, 0.9441],[0.2814, 0.3095, 0.9483],[0.2813, 0.315, 0.9524],[0.2811, 0.3204, 0.9563],[0.2809, 0.3259, 0.96],[0.2807, 0.3313, 0.9636],[0.2803, 0.3367, 0.967],[0.2798, 0.3421, 0.9702],[0.2791, 0.3475, 0.9733],[0.2784, 0.3529, 0.9763],[0.2776, 0.3583, 0.9791],[0.2766, 0.3638, 0.9817],[0.2754, 0.3693, 0.984],[0.2741, 0.3748, 0.9862],[0.2726, 0.3804, 0.9881],[0.271, 0.386, 0.9898],[0.2691, 0.3916, 0.9912],[0.267, 0.3973, 0.9924],[0.2647, 0.403, 0.9935],[0.2621, 0.4088, 0.9946],[0.2591, 0.4145, 0.9955],[0.2556, 0.4203, 0.9965],[0.2517, 0.4261, 0.9974],[0.2473, 0.4319, 0.9983],[0.2424, 0.4378, 0.9991],[0.2369, 0.4437, 0.9996],[0.2311, 0.4497, 0.9995],[0.225, 0.4559, 0.9985],[0.2189, 0.462, 0.9968],[0.2128, 0.4682, 0.9948],[0.2066, 0.4743, 0.9926],[0.2006, 0.4803, 0.9906],[0.195, 0.4861, 0.9887],[0.1903, 0.4919, 0.9867],[0.1869, 0.4975, 0.9844],[0.1847, 0.503, 0.9819],[0.1831, 0.5084, 0.9793],[0.1818, 0.5138, 0.9766],[0.1806, 0.5191, 0.9738],[0.1795, 0.5244, 0.9709],[0.1785, 0.5296, 0.9677],[0.1778, 0.5349, 0.9641],[0.1773, 0.5401, 0.9602],[0.1768, 0.5452, 0.956],[0.1764, 0.5504, 0.9516],[0.1755, 0.5554, 0.9473],[0.174, 0.5605, 0.9432],[0.1716, 0.5655, 0.9393],[0.1686, 0.5705, 0.9357],[0.1649, 0.5755, 0.9323],[0.161, 0.5805, 0.9289],[0.1573, 0.5854, 0.9254],[0.154, 0.5902, 0.9218],[0.1513, 0.595, 0.9182],[0.1492, 0.5997, 0.9147],[0.1475, 0.6043, 0.9113],[0.1461, 0.6089, 0.908],[0.1446, 0.6135, 0.905],[0.1429, 0.618, 0.9022],[0.1408, 0.6226, 0.8998],[0.1383, 0.6272, 0.8975],[0.1354, 0.6317, 0.8953],[0.1321, 0.6363, 0.8932],[0.1288, 0.6408, 0.891],[0.1253, 0.6453, 0.8887],[0.1219, 0.6497, 0.8862],[0.1185, 0.6541, 0.8834],[0.1152, 0.6584, 0.8804],[0.1119, 0.6627, 0.877],[0.1085, 0.6669, 0.8734],[0.1048, 0.671, 0.8695],[0.1009, 0.675, 0.8653],[0.0964, 0.6789, 0.8609],[0.0914, 0.6828, 0.8562],[0.0855, 0.6865, 0.8513],[0.0789, 0.6902, 0.8462],[0.0713, 0.6938, 0.8409],[0.0628, 0.6972, 0.8355],[0.0535, 0.7006, 0.8299],[0.0433, 0.7039, 0.8242],[0.0328, 0.7071, 0.8183],[0.0234, 0.7103, 0.8124],[0.0155, 0.7133, 0.8064],[0.0091, 0.7163, 0.8003],[0.0046, 0.7192, 0.7941],[0.0019, 0.722, 0.7878],[0.0009, 0.7248, 0.7815],[0.0018, 0.7275, 0.7752],[0.0046, 0.7301, 0.7688],[0.0094, 0.7327, 0.7623],[0.0162, 0.7352, 0.7558],[0.0253, 0.7376, 0.7492],[0.0369, 0.74, 0.7426],[0.0504, 0.7423, 0.7359],[0.0638, 0.7446, 0.7292],[0.077, 0.7468, 0.7224],[0.0899, 0.7489, 0.7156],[0.1023, 0.751, 0.7088],[0.1141, 0.7531, 0.7019],[0.1252, 0.7552, 0.695],[0.1354, 0.7572, 0.6881],[0.1448, 0.7593, 0.6812],[0.1532, 0.7614, 0.6741],[0.1609, 0.7635, 0.6671],[0.1678, 0.7656, 0.6599],[0.1741, 0.7678, 0.6527],[0.1799, 0.7699, 0.6454],[0.1853, 0.7721, 0.6379],[0.1905, 0.7743, 0.6303],[0.1954, 0.7765, 0.6225],[0.2003, 0.7787, 0.6146],[0.2061, 0.7808, 0.6065],[0.2118, 0.7828, 0.5983],[0.2178, 0.7849, 0.5899],[0.2244, 0.7869, 0.5813],[0.2318, 0.7887, 0.5725],[0.2401, 0.7905, 0.5636],[0.2491, 0.7922, 0.5546],[0.2589, 0.7937, 0.5454],[0.2695, 0.7951, 0.536],[0.2809, 0.7964, 0.5266],[0.2929, 0.7975, 0.517],[0.3052, 0.7985, 0.5074],[0.3176, 0.7994, 0.4975],[0.3301, 0.8002, 0.4876],[0.3424, 0.8009, 0.4774],[0.3548, 0.8016, 0.4669],[0.3671, 0.8021, 0.4563],[0.3795, 0.8026, 0.4454],[0.3921, 0.8029, 0.4344],[0.405, 0.8031, 0.4233],[0.4184, 0.803, 0.4122],[0.4322, 0.8028, 0.4013],[0.4463, 0.8024, 0.3904],[0.4608, 0.8018, 0.3797],[0.4753, 0.8011, 0.3691],[0.4899, 0.8002, 0.3586],[0.5044, 0.7993, 0.348],[0.5187, 0.7982, 0.3374],[0.5329, 0.797, 0.3267],[0.547, 0.7957, 0.3159],[0.5609, 0.7943, 0.305],[0.5748, 0.7929, 0.2941],[0.5886, 0.7913, 0.2833],[0.6024, 0.7896, 0.2726],[0.6161, 0.7878, 0.2622],[0.6297, 0.7859, 0.2521],[0.6433, 0.7839, 0.2423],[0.6567, 0.7818, 0.2329],[0.6701, 0.7796, 0.2239],[0.6833, 0.7773, 0.2155],[0.6963, 0.775, 0.2075],[0.7091, 0.7727, 0.1998],[0.7218, 0.7703, 0.1924],[0.7344, 0.7679, 0.1852],[0.7468, 0.7654, 0.1782],[0.759, 0.7629, 0.1717],[0.771, 0.7604, 0.1658],[0.7829, 0.7579, 0.1608],[0.7945, 0.7554, 0.157],[0.806, 0.7529, 0.1546],[0.8172, 0.7505, 0.1535],[0.8281, 0.7481, 0.1536],[0.8389, 0.7457, 0.1546],[0.8495, 0.7435, 0.1564],[0.86, 0.7413, 0.1587],[0.8703, 0.7392, 0.1615],[0.8804, 0.7372, 0.165],[0.8903, 0.7353, 0.1695],[0.9, 0.7336, 0.1749],[0.9093, 0.7321, 0.1815],[0.9184, 0.7308, 0.189],[0.9272, 0.7298, 0.1973],[0.9357, 0.729, 0.2061],[0.944, 0.7285, 0.2151],[0.9523, 0.7284, 0.2237],[0.9606, 0.7285, 0.2312],[0.9689, 0.7292, 0.2373],[0.977, 0.7304, 0.2418],[0.9842, 0.733, 0.2446],[0.99, 0.7365, 0.2429],[0.9946, 0.7407, 0.2394],[0.9966, 0.7458, 0.2351],[0.9971, 0.7513, 0.2309],[0.9972, 0.7569, 0.2267],[0.9971, 0.7626, 0.2224],[0.9969, 0.7683, 0.2181],[0.9966, 0.774, 0.2138],[0.9962, 0.7798, 0.2095],[0.9957, 0.7856, 0.2053],[0.9949, 0.7915, 0.2012],[0.9938, 0.7974, 0.1974],[0.9923, 0.8034, 0.1939],[0.9906, 0.8095, 0.1906],[0.9885, 0.8156, 0.1875],[0.9861, 0.8218, 0.1846],[0.9835, 0.828, 0.1817],[0.9807, 0.8342, 0.1787],[0.9778, 0.8404, 0.1757],[0.9748, 0.8467, 0.1726],[0.972, 0.8529, 0.1695],[0.9694, 0.8591, 0.1665],[0.9671, 0.8654, 0.1636],[0.9651, 0.8716, 0.1608],[0.9634, 0.8778, 0.1582],[0.9619, 0.884, 0.1557],[0.9608, 0.8902, 0.1532],[0.9601, 0.8963, 0.1507],[0.9596, 0.9023, 0.148],[0.9595, 0.9084, 0.145],[0.9597, 0.9143, 0.1418],[0.9601, 0.9203, 0.1382],[0.9608, 0.9262, 0.1344],[0.9618, 0.932, 0.1304],[0.9629, 0.9379, 0.1261],[0.9642, 0.9437, 0.1216],[0.9657, 0.9494, 0.1168],[0.9674, 0.9552, 0.1116],[0.9692, 0.9609, 0.1061],[0.9711, 0.9667, 0.1001],[0.973, 0.9724, 0.0938],[0.9749, 0.9782, 0.0872],[0.9769, 0.9839, 0.0805]]
parula_map = LinearSegmentedColormap.from_list('parula', cm_data)

# Path
HOME=os.environ['HOME']   
f = open(HOME+'/.env', 'r')
for line in f.readlines():
   Name=line.strip().split('=')[0]
   Content=line.strip().split('=')[-1]
   if Name=='dirData' or Name=='dirAnalisis':
      exec(Name + "=" + "'" + Content + "'")
f.close()

dataDir    = dirAnalisis + '/IEOOSWebPage/data'
imageDir   = dirAnalisis + '/IEOOSWebPage/images'

Titulos = ['Demarcación marina canaria','Demarcación marina levantino-balear', 'Demarcación marina noratlántica','Demarcación sudatlántica','Demarcación Estrecho y Alborán']
Titulos_short = ['CAN','LEB', 'NOR','SUD','ESA']

#To compute de climatoloy
yearC1='1995'
yearC2='2000'


# Load the demarcacion data
for iD in range(0,5):
   titulo = Titulos[iD]
   titulo_short = Titulos_short[iD]
   print('>>>>> '+titulo)
   
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

   DC_temp = xr.open_dataset('./Data/Glorys_DC_temp'+titulo_short+'.nc').thetao
   DC_salt = xr.open_dataset('./Data/Glorys_DC_salt'+titulo_short+'.nc').so

   DC_temp_unmasked = xr.open_dataset('./Data/Glorys_DC_temp_unmasked'+titulo_short+'.nc').thetao
   DC_temp_unmasked = xr.open_dataset('./Data/Glorys_DC_salt_unmasked'+titulo_short+'.nc').so

   meanTemp=DC_temp.sel(depth=10, method='nearest').mean('time')
   meanTemp_unmasked=DC_temp_unmasked.sel(depth=10, method='nearest').mean('time')
   print('         > mapa')
#Mapa a 10 metros   
   fig = plt.figure(figsize=(8,8))
   ax = plt.axes(projection=ccrs.Robinson())
   cmc= ax.contour(meanTemp_unmasked.longitude,
                   meanTemp_unmasked.latitude,
                   meanTemp_unmasked,10,colors='k', transform=ccrs.PlateCarree())
   cm = ax.contourf(meanTemp.longitude,
                    meanTemp.latitude,
                    meanTemp,30,transform=ccrs.PlateCarree(),cmap = plt.cm.RdBu.reversed(),extend='both')
   
   land = cartopy.feature.NaturalEarthFeature('physical', 'land', edgecolor='k', scale = '50m' ,
         facecolor=cfeature.COLORS['land'])
   ax.add_feature(land, facecolor='beige')
   cbar=fig.colorbar(cm,ax=ax, location='bottom', shrink=.8, drawedges=True)
   ax.plot(longDem, latiDem, transform=ccrs.PlateCarree())
   ax.gridlines(draw_labels=True, linewidth=.5,color='gray', alpha=0.5, linestyle='--')
   ax.top_labels = ax.right_labels = False
   #ax.set_title('Temperatura promedio a '+'10 '+'para la '+titulo);
   plt.savefig(imageDir+'/'+titulo_short+'_temp_promedio'+'10'+'.png',bbox_inches='tight', pad_inches=0.1, dpi=300)

   plt.close(fig)

# Calculo de perfiles promedios
   print('         > calculando perfiles')

   prof_mean_temp = DC_temp.stack(flat_dim=('longitude', 'latitude','time')).mean('flat_dim')
   prof_std_temp  = DC_temp.stack(flat_dim=('longitude', 'latitude','time')).std('flat_dim')
   prof_mean_salt = DC_salt.stack(flat_dim=('longitude', 'latitude','time')).mean('flat_dim')
   prof_std_salt  = DC_salt.stack(flat_dim=('longitude', 'latitude','time')).std('flat_dim')

# Perfiles
   print('         > figura perfiles')
   fig,ax= plt.subplots(1,2,figsize=(14,8))
   ax[0].plot(prof_mean_temp,prof_mean_temp.depth,color='blue')  
   ax[0].plot(prof_mean_temp+1.5*prof_std_temp,prof_mean_temp.depth,color='red')  
   ax[0].plot(prof_mean_temp-1.5*prof_std_temp,prof_mean_temp.depth,color='red')  
   ax[0].invert_yaxis()
   ax[0].set_ylim([2000,0]);
   ax[0].grid()
   ax[0].set_title('Temperatura');
   ax[0].set_ylabel('Presión') 

   ax[1].plot(prof_mean_salt,prof_mean_temp.depth,color='blue')  
   ax[1].plot(prof_mean_salt+1.5*prof_std_salt,prof_mean_salt.depth,color='red')  
   ax[1].plot(prof_mean_salt-1.5*prof_std_salt,prof_mean_salt.depth,color='red')  
   ax[1].invert_yaxis()
   ax[1].set_ylim([2000,0]);
   ax[1].grid()
   ax[1].set_title('Salinidad');
   ax[1].set_ylabel('Presión') 
   plt.savefig(imageDir+'/'+titulo_short+'_perfiles_T_S_promedio.png')
   plt.close(fig)
   
## Seasonal cycle
   print('         > calculando seasonal')
	#Create monthly climatology
   DC_temp_clim = DC_temp.sel(time=slice(yearC1,yearC2)).groupby('time.month').mean(dim='time').load();
   DC_salt_clim = DC_salt.sel(time=slice(yearC1,yearC2)).groupby('time.month').mean(dim='time').load();

#Create anomaly
   DC_temp_anom = DC_temp.groupby('time.month') - DC_temp_clim
   DC_temp_anom.load();
   DC_salt_anom = DC_salt.groupby('time.month') - DC_salt_clim
   DC_salt_anom.load();

#Figuras ciclo estacional
   rangoT= np.arange(4,25,0.25)
   rangoTt=np.arange(4,25,2)
   rangoTcb=np.arange(13,24,2)

   rangoS= np.arange(35.,38,0.05)
   rangoSt=np.arange(35.,38,0.25)

   rangop=[0,450]
   colorMap=parula_map
   presionTickss=[0,50,100,150]
   presionTicksi=[400,800,1200,1600,2000]

   mesTticks=[1,3,6,9,12]
   mesTticksT=['Enero','Marzo', 'Junio','Septiembre','']

   fig, ax = plt.subplots(2, 2 , figsize=(20,9))
   ax0 = fig.add_axes((0.04, 0.64, 0.44, 0.32))
   ax1 = fig.add_axes((0.04, 0.07, 0.44, 0.54))
   ax2 = fig.add_axes((0.50, 0.64, 0.44, 0.32))
   ax3 = fig.add_axes((0.50, 0.07, 0.44, 0.54))
   cbarTem = fig.add_axes([0.08, 0.02, 0.36, 0.015])
   cbarSal = fig.add_axes([0.54, 0.02, 0.36, 0.015])

   ax0.contourf(DC_temp_clim.mean(dim='longitude').mean(dim='latitude').month,
            DC_temp_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(0,400)).depth,
            DC_temp_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(0,400)).transpose(),rangoT,extend='both',
            cmap = colorMap)
   cm = ax0.contour(DC_temp_clim.mean(dim='longitude').mean(dim='latitude').month,
              DC_temp_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(0,400)).depth,
              DC_temp_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(0,400)).transpose(),levels=rangoTt,colors='k')
   ax0.invert_yaxis()
   ax0.clabel(cm, fmt='%2.0f', colors='w', fontsize=10)
   ax0.set_ylim([200,0]);
   ax0.set_ylabel('Presión') 
   ax0.set_xticks(mesTticks,['','', '','','']) 
   ax0.set_yticks(presionTickss)
   ax0.set_title('Temperatura')

   cmTem = ax1.contourf(DC_temp_clim.mean(dim='longitude').mean(dim='latitude').month,
            DC_temp_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(200,2600)).depth,
            DC_temp_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(200,2600)).transpose(),rangoT,extend='both',
            cmap = colorMap)

   cm = ax1.contour(DC_temp_clim.mean(dim='longitude').mean(dim='latitude').month,
              DC_temp_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(200,2600)).depth,
              DC_temp_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(200,2600)).transpose(),levels=rangoTt,colors='k')

   ax1.clabel(cm, fmt='%2.2f', colors='w', fontsize=10)
   ax1.invert_yaxis()
   ax1.set_ylim([2000,400]);
   ax1.set_xticks([1,3,6,9,12], ['Enero','Marzo', 'Junio','Septiembre','']) 
   ax1.set_yticks(presionTicksi)
   fig.colorbar(cmTem, cax=cbarTem,ticks=rangoTt,orientation='horizontal')

  ## Salinidad
   ax2.contourf(DC_salt_clim.mean(dim='longitude').mean(dim='latitude').month,
            DC_salt_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(0,400)).depth,
            DC_salt_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(0,400)).transpose(),rangoS,extend='both',
            cmap = colorMap)
   cm=ax2.contour(DC_salt_clim.mean(dim='longitude').mean(dim='latitude').month,
              DC_salt_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(0,400)).depth,
              DC_salt_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(0,400)).transpose(),levels=rangoSt,colors='k')
   ax2.invert_yaxis()
   ax2.clabel(cm, fmt='%2.0f', colors='w', fontsize=10)
   ax2.set_ylim([200,0]);
   ax2.set_title('Salinidad')
   ax2.set_xticks(mesTticks,['','', '','','']) 
   ax2.set_yticks(presionTickss)

   cmSal = ax3.contourf(DC_salt_clim.mean(dim='longitude').mean(dim='latitude').month,
            DC_salt_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(200,2600)).depth,
            DC_salt_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(200,2600)).transpose(),rangoS,extend='both',
            cmap = colorMap)

   cm = ax3.contour(DC_salt_clim.mean(dim='longitude').mean(dim='latitude').month,
              DC_salt_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(200,2600)).depth,
              DC_salt_clim.mean(dim='longitude').mean(dim='latitude').sel(depth=slice(200,2600)).transpose(),levels=rangoSt,colors='k')

   ax3.clabel(cm, fmt='%2.2f', colors='w', fontsize=10)
   ax3.invert_yaxis()
   ax3.set_ylim([2000,400]);
   ax3.set_xticks([1,3,6,9,12], ['Enero','Marzo', 'Junio','Septiembr','']) 
   ax3.set_yticks(presionTicksi)

   fig.colorbar(cmSal, cax=cbarSal,ticks=rangoSt,orientation='horizontal')
   plt.savefig(imageDir+'/'+titulo_short+'_climatologia.png',bbox_inches='tight', pad_inches=0.1, dpi=300)

# Weighted horizontal mean
   print('         > promedios por area ')

   weights = np.cos(np.deg2rad(DC_temp.latitude))
   weights = weights/weights.max()
   weights.name = "weights"
   DC_temp_weighted = DC_temp.weighted(weights)
   DC_salt_weighted = DC_salt.weighted(weights)
   DC_temp_anom_weighted = DC_temp_anom.weighted(weights)
   DC_salt_anom_weighted = DC_salt_anom.weighted(weights)
   DC_temp_wmean = DC_temp_weighted.mean(("longitude", "latitude"),skipna=True).load()
   DC_salt_wmean = DC_salt_weighted.mean(("longitude", "latitude"),skipna=True).load()
   DC_temp_anom_wmean = DC_temp_anom_weighted.mean(("longitude", "latitude"),skipna=True).load()
   DC_salt_anom_wmean = DC_salt_anom_weighted.mean(("longitude", "latitude"),skipna=True).load()


   fig, ax = plt.subplots(2, 1 , sharex=True, figsize=(14,8))
   ax[0].contourf(DC_temp_wmean.time, DC_temp_wmean.depth, 
  DC_temp_wmean.transpose(), 32,cmap = plt.cm.RdBu.reversed())
   #ax[0].set_title('Variacion temporal Temperatura promedio')
   ax[0].set_ylabel('Presión') 
   ax[0].invert_yaxis()
   ax[0].set_ylim([200,0]);

   ax[1].contourf(DC_temp_wmean.time, DC_temp_wmean.depth, 
  DC_temp_wmean.transpose(), 32,cmap = plt.cm.RdBu.reversed())
   ax[1].set_ylabel('Presión') 
   ax[1].invert_yaxis()
   ax[1].set_ylim([2000,200]);
   fig.tight_layout()
   plt.savefig(imageDir+'/'+titulo_short+'_SeccionTemporal_T.png')
   plt.close(fig)

# Smoothed versions
   print('         > interpolo cada m')
   depthi = np.arange(10,4000.5,10)
   DCi_temp_wmean = DC_temp_wmean.interp(depth=depthi)
   DCi_salt_wmean = DC_temp_wmean.interp(depth=depthi)
   DCi_temp_anom_wmean = DC_temp_anom_wmean.interp(depth=depthi)
   DCi_salt_anom_wmean = DC_temp_anom_wmean.interp(depth=depthi)
   DCi_temp_wmean_rolling = DCi_temp_wmean.rolling(time=12,center=True).mean()
   DCi_salt_wmean_rolling = DCi_salt_wmean.rolling(time=12,center=True).mean()
   DCi_temp_anom_wmean_rolling = DCi_temp_anom_wmean.rolling(time=12,center=True).mean()
   DCi_salt_anom_wmean_rolling = DCi_salt_anom_wmean.rolling(time=12,center=True).mean()

## Figura serie temporal promedio
   Posiciones=[(0.10, 0.65, 0.8, 0.22), (0.10, 0.48, 0.8, 0.16),(0.10, 0.10, 0.8, 0.37)]
   
   fig, ax = plt.subplots(3,1,figsize = (14,15),sharex=True)

   # Mean values
   ax[0].plot(DCi_temp_anom_wmean.time[-2],
              DCi_temp_anom_wmean.sel(depth=slice(10,2600)).mean("depth")[-2],
              'ko')
   ax[0].plot(DCi_temp_anom_wmean.time,
              DCi_temp_anom_wmean.sel(depth=slice(10,2600)).mean("depth"),
              color='k',alpha=0.3)
   ax[0].plot(DCi_temp_anom_wmean_rolling.time,
              DCi_temp_anom_wmean_rolling.sel(depth=slice(10,2600)).mean("depth"),
              linewidth=2,color='k',label= '   10 - 2600 dbar')

   ax[0].plot(DCi_temp_anom_wmean.time,
              DCi_temp_anom_wmean.sel(depth=slice(200,800)).mean("depth"),
              color='r',alpha=0.3)
   ax[0].plot(DCi_temp_anom_wmean_rolling.time,
              DCi_temp_anom_wmean_rolling.sel(depth=slice(200,800)).mean("depth"),
              linewidth=2,color='r' ,label= '  200 -  800 dbar')

   ax[0].plot(DCi_temp_anom_wmean.time,
              DCi_temp_anom_wmean.sel(depth=slice(800,1400)).mean("depth"),
              color='b',alpha=0.3)
   
   ax[0].plot(DCi_temp_anom_wmean_rolling.time,
              DCi_temp_anom_wmean_rolling.sel(depth=slice(800,1400)).mean("depth"),
              linewidth=2,color='blue',label= '  800 - 1400 dbar')

   ax[0].plot(DCi_temp_anom_wmean.time, DCi_temp_anom_wmean.sel(depth=slice(1400,2600)).mean("depth"),
              color='g',alpha=0.3)
   
   ax[0].plot(DCi_temp_anom_wmean_rolling.time, DCi_temp_anom_wmean_rolling.sel(depth=slice(1400,2600)).mean("depth"),
              linewidth=2,color='g',label= ' 1400 - 2600 dbar')

   ax[0].grid(linestyle='-', linewidth=.9)
   ax[0].set_position(Posiciones[0])
   ax[0].legend()
   ax[0].set_ylabel('[ºC]')
   ax[0].set_frame_on(False)
   ax[0].set_title('Anomalia (respecto '+yearC1+'-'+yearC2+') de temperatura promedio [ºC] en la '+titulo);

   # UpperOcean
   ax[1].contour(DCi_temp_anom_wmean.time,
                 DCi_temp_anom_wmean.sel(depth=slice(10,800)).depth, 
                 DCi_temp_anom_wmean.sel(depth=slice(10,800)).transpose()
                 ,colors='w',levels=[-0.15, -0.05, 0.05, 0.15] )
   ax[1].contour(DCi_temp_anom_wmean.time, 
                 DCi_temp_anom_wmean.sel(depth=slice(10,800)).depth, 
                 DCi_temp_anom_wmean.sel(depth=slice(10,800)).transpose(),
                 colors='w', linewidths=2,levels=[0] )

   ax[1].contourf(DCi_temp_anom_wmean.time, 
                 DCi_temp_anom_wmean.sel(depth=slice(10,800)).depth, 
                 DCi_temp_anom_wmean.sel(depth=slice(10,800)).transpose(),
                  40, cmap='RdBu_r')
    
   ax[1].set_ylim(0,800)
   ax[1].invert_yaxis()
   ax[1].set_yticks([200,400,600,800])
   ax[1].grid(linestyle='-', linewidth=.9)
   ax[1].set_position(Posiciones[1])

   ax[2].contour(DCi_temp_anom_wmean.time, 
                 DCi_temp_anom_wmean.sel(depth=slice(800,2600)).depth, 
                 DCi_temp_anom_wmean.sel(depth=slice(800,2600)).transpose(),
                 colors='w',levels=[-0.05,0.05] )
   
   ax[2].contour(DCi_temp_anom_wmean.time, 
                 DCi_temp_anom_wmean.sel(depth=slice(800,2600)).depth, 
                 DCi_temp_anom_wmean.sel(depth=slice(800,2600)).transpose(),
                 colors='w', linewidths=3,levels=[0] )
   
   cntr2 = ax[2].contourf(DCi_temp_anom_wmean.time,
                          DCi_temp_anom_wmean.sel(depth=slice(800,2600)).depth, 
                          DCi_temp_anom_wmean.sel(depth=slice(800,2600)).transpose(),
                          40,cmap='RdBu_r')
  
   ax[2].set_ylim(800,2400)
   ax[2].invert_yaxis()
   ax[2].set_yticks([1000,1200,1400,1600,1800,2000,2200,2400])
   ax[2].grid(linestyle='-', linewidth=.9)
   ax[2].set_position(Posiciones[2])
   ax[2].set_ylabel('Presión')

   # Adding the colorbar
   cbaxes = fig.add_axes([0.92, 0.10, 0.02, 0.44])  
   cb = fig.colorbar(cntr2, cax=cbaxes);
   cbaxes.set_ylabel('Temperatura')

   # xtick Labels
   ax[0].set_xticks(pd.date_range(start="1995-01-01", end="2025-01-01",freq='2YS-JAN'));
   ax[1].set_xticks(pd.date_range(start="1995-01-01", end="2025-01-01",freq='2YS-JAN'));
   ax[2].set_xticks(pd.date_range(start="1995-01-01", end="2025-01-01",freq='2YS-JAN'));
   ax[2].set_xticklabels(pd.date_range(start="1995-01-01", end="2025-01-01",freq='2YS-JAN').strftime('%Y'));
   
   #tTActual = sst.time[-1].dt.strftime("%d %B %Y").values + " %2.2f ºC "%(sst[-1].values)
   #tTMaxima =  'Temperatura máxima: ' + "%2.2f ºC"%(tmax) + ' el ' + d_tmax.dt.strftime("%d %B %Y").values
   #tTMinima =  'Temperatura mínima: ' + "%2.2f ºC"%(tmin) + ' el ' + d_tmin.dt.strftime("%d %B %Y").values
   #tPeriodo =  " [" + sstd.time[0].dt.strftime("%d %B %Y").values + " - "+ sstd.time[-1].dt.strftime("%d %B %Y").values + "]"
   #TituloFigura  = 'Temperatura superficial en el '+ titulo
   #ax.set_title(TituloFigura + tPeriodo + '\n' + tTMaxima + ' - ' + tTMinima + tTendencia);

   plt.savefig(imageDir+'/'+titulo_short+'_temp_promedio_capas_contorno.png',bbox_inches='tight', pad_inches=0.1, dpi=300)
   plt.close(fig)

   # Create a Dataset from the DataArrays
   Glorys_means = xr.Dataset({
   'DCi_temp_wmean': DC_temp_wmean,
   'DCi_salt_wmean': DC_salt_wmean,
   'DCi_temp_anom_wmean': DC_temp_wmean,
   'DCi_salt_anom_wmean': DC_salt_wmean,
   'DCi_temp_wmean_rolling': DC_temp_wmean,
   'DCi_salt_wmean_rolling': DC_salt_wmean,
   'DCi_temp_anom_wmean_rolling': DC_temp_wmean,
   'DCi_salt_anom_wmean_rolling': DC_salt_wmean
   })
   Glorys_means.to_netcdf('./Data/Glorys_means'+titulo_short+'.nc')


# 
   fig, ax = plt.subplots(2,1, figsize=(14,12))
   # Mean values
   media=DCi_temp_wmean.sel(depth=slice(200,2600)).mean("depth").mean('time')
   ax[0].plot(DCi_temp_wmean.time[-2],
 DCi_temp_wmean.sel(depth=slice(200,2600)).mean("depth")[-2]-media,'ko')
   ax[0].plot(DCi_temp_wmean.time,
 DCi_temp_wmean.sel(depth=slice(200,2600)).mean("depth")-media,color='k',alpha=0.3)
   ax[0].plot(DCi_temp_wmean_rolling.time,
 DCi_temp_wmean_rolling.sel(depth=slice(200,2600)).mean("depth")-media,linewidth=2,color='k',
 label= '  200 - 2600 dbar')

   media=DCi_temp_wmean.sel(depth=slice(200,800)).mean("depth").mean('time')
   ax[0].plot(DCi_temp_wmean.time,
 DCi_temp_wmean.sel(depth=slice(200,800)).mean("depth")-media,color='r',alpha=0.3)
   ax[0].plot(DCi_temp_wmean_rolling.time,
 DCi_temp_wmean_rolling.sel(depth=slice(200,800)).mean("depth")-media,linewidth=2,color='r' ,
 label= '  200 -  800 dbar')

   media=DCi_temp_wmean.sel(depth=slice(800,1400)).mean("depth").mean('time')
   ax[0].plot(DCi_temp_wmean.time,
 DCi_temp_wmean.sel(depth=slice(800,1400)).mean("depth")-media,color='b',alpha=0.3)
   ax[0].plot(DCi_temp_wmean_rolling.time,
 DCi_temp_wmean_rolling.sel(depth=slice(800,1400)).mean("depth")-media,linewidth=2,color='blue',
 label= '  800 - 1400 dbar')

   media=DCi_temp_wmean.sel(depth=slice(1400,2600)).mean("depth").mean('time')
   ax[0].plot(DCi_temp_wmean.time,
 DCi_temp_wmean.sel(depth=slice(1400,2600)).mean("depth")-media,color='g',alpha=0.3)
   ax[0].plot(DCi_temp_wmean_rolling.time,
 DCi_temp_wmean_rolling.sel(depth=slice(1400,2600)).mean("depth")-media,linewidth=2,color='g',
 label= ' 1400 - 2600 dbar')

   ax[0].grid(linestyle='-', linewidth=.9)
   ax[0].legend()
   ax[0].set_ylabel('[ºC]')
   ax[0].set_title('Temperatura promedio-media capa [ºC] en la '+titulo);

   # Anomalias
   ax[1].plot(DCi_temp_anom_wmean.time[-2],
 DCi_temp_anom_wmean.sel(depth=slice(20,2600)).mean("depth")[-2],'ko')

   ax[1].plot(DCi_temp_anom_wmean.time,
 DCi_temp_anom_wmean.sel(depth=slice(20,2600)).mean("depth"),color='k',alpha=0.3)
   ax[1].plot(DCi_temp_anom_wmean_rolling.time,
 DCi_temp_anom_wmean_rolling.sel(depth=slice(20,2600)).mean("depth"),linewidth=2,color='k',
 label= '   20 - 2600 dbar')

   ax[1].plot(DCi_temp_anom_wmean.time,
 DCi_temp_anom_wmean.sel(depth=slice(200,800)).mean("depth"),color='r',alpha=0.3)
   ax[1].plot(DCi_temp_anom_wmean_rolling.time,
 DCi_temp_anom_wmean_rolling.sel(depth=slice(200,800)).mean("depth"),linewidth=2,color='r' ,
 label= '  200 -  800 dbar')

   ax[1].plot(DCi_temp_anom_wmean.time,
 DCi_temp_anom_wmean.sel(depth=slice(800,1400)).mean("depth"),color='b',alpha=0.3)
   ax[1].plot(DCi_temp_anom_wmean_rolling.time,
 DCi_temp_anom_wmean_rolling.sel(depth=slice(800,1400)).mean("depth"),linewidth=2,color='blue',
 label= '  800 - 1400 dbar')

   ax[1].plot(DCi_temp_anom_wmean.time,
 DCi_temp_anom_wmean.sel(depth=slice(1400,2600)).mean("depth"),color='g',alpha=0.3)
   ax[1].plot(DCi_temp_anom_wmean_rolling.time,
 DCi_temp_anom_wmean_rolling.sel(depth=slice(1400,2600)).mean("depth"),linewidth=2,color='g',
 label= ' 1400 - 2600 dbar')

   ax[1].grid(linestyle='-', linewidth=.9)
   ax[1].legend()
   ax[1].set_ylabel('[ºC]')
   ax[1].set_title('Anomalia (respecto '+yearC1+'-'+yearC2+') de temperatura promedio [ºC] en la '+titulo);
   plt.savefig(imageDir+'/'+titulo_short+'_temp_promedio_capas.png')
