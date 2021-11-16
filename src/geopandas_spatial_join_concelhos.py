import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point

#print(gpd.__version__) # '0.6.1'
##gdf = gpd.read_file('ICNF_filtered_data(1980_2000).csv') # not working with csv
##gdf.crs = 'epsg:4326'
##gdf.head()

#print(pd.__version__) # '0.24.2'
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 170)

df = pd.read_csv('ICNF_filtered_data(1980_2000).csv', encoding='utf8')
print(df.columns)
print(df.head())

#geodf= gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LON, df.LAT)) # df.x, df.y
#geodf.crs = {'init': 'epsg:4326'}
##geodf.set_crs(epsg=4326, inplace=True)
##geodf.to_crs("epsg:4326")
#print(geodf.columns)
#print(geodf.head())
#print(geodf.crs)

coords={'init': 'epsg:4326'}
#coords='epsg:4326'
geodf2 = gpd.GeoDataFrame(df, crs=coords, geometry=[Point(xy) for xy in zip(df.x, df.y)]) # x - long, y - lat
print(geodf2.info())
print(geodf2.columns)
print(geodf2.head())
print(geodf2.crs)

#geodf.to_file(driver='ESRI Shapefile', filename='geodf.shp')

concelhos = gpd.read_file('concelhos_mainland_wgs84.shp', encoding='utf8')
print(concelhos.columns)
print(concelhos.head())
print(concelhos.crs)
concelhos2 = concelhos.drop(['ID_0','ISO','NAME_0','ID_1','HASC_2','CCN_2','CCA_2','TYPE_2','ENGTYPE_2','NL_NAME_2','VARNAME_2'], 1)
# 0 for rows and 1 for columns
print(concelhos2.info())
print(concelhos2.head())

##sjoined = gpd.sjoin(gdf_listings, stockholm_areas, op="within")
##The above code joins gdf_listings to stockholm_areas based on their locations.
##https://towardsdatascience.com/how-to-easily-join-data-by-location-in-python-spatial-join-197490ff3544
sjoined = gpd.sjoin(geodf2, concelhos2, op="within", how="left") # op="within" 330425->330300, op="intersects" slow
print(sjoined.info())
print(sjoined.head())

sjoined2 = sjoined.drop('geometry', 1)
sjoined2 = sjoined2.drop('Unnamed: 0', 1)

### tests
sjoined2set = sjoined2.iloc[20000:20100,:] # 100 rows
print(sjoined2set.head())
outfile100 = r"C:\Users\basos\Desktop\convert\ICNF_filtered_data(1980_2000)_concelhos100.csv"
sjoined2set.to_csv(outfile100, index=False, mode='w', encoding='utf8')

wtf=sjoined2[sjoined2['NAME_1'].isnull()]
print(wtf.head())
outfilenan = r"C:\Users\basos\Desktop\convert\ICNF_filtered_data(1980_2000)_concelhosNaN.csv"
wtf.to_csv(outfilenan, index=False, mode='w', encoding='utf8')

#wtf.loc[wtf['year'] == 1993, 'NAME_2' ] = wtf['concelho']
#wtf.loc[wtf['NAME_1'].isnull(), 'NAME_2' ] = wtf['concelho'].str.title()
###

print('not joined', sjoined2.loc[sjoined2['NAME_1'].isnull()].shape[0])
sjoined2.loc[sjoined2['NAME_1'].isnull(), 'NAME_2' ] = sjoined2['concelho'].str.title()
# writing lowercased concelho to non-joined nans
sjoined2['concelho'] = sjoined2['NAME_2']

sjoined2 = sjoined2.drop(['index_right','NAME_1','ID_2','NAME_2'], 1)
print(sjoined2.head())
print(sjoined2.iloc[20017:20022,:])

# invalid coordiantes
print(sjoined2.loc[sjoined2['x'] > -6].shape[0]) # how many rows
sjoined2.loc[sjoined2['x'] > -6, 'x' ] = np.nan
print(sjoined2.loc[sjoined2['x'] < -9.6].shape[0]) # how many rows
sjoined2.loc[sjoined2['x'] < -9.6, 'x' ] = np.nan
print(sjoined2.loc[sjoined2['y'] > 42.2].shape[0]) # how many rows
sjoined2.loc[sjoined2['y'] > 42.2, 'y' ] = np.nan
print(sjoined2.loc[sjoined2['y'] < 36.9].shape[0]) # how many rows
sjoined2.loc[sjoined2['y'] < 36.9, 'y' ] = np.nan

# to save file faster
sjoined2['concelho'] = sjoined2.concelho.astype(str)
sjoined2['Source'] = sjoined2.Source.astype(str)
sjoined2['data_inicio'] = sjoined2['data_inicio'].astype(str)
#sjoined2['month'] = sjoined2['month'].astype(int)
#sjoined2['year'] = sjoined2['year'].astype(int)

grouped = sjoined2.groupby(['concelho','month','year'])['area_total'].agg(['sum'])
burnedarea = grouped.reset_index()
print(burnedarea.head())
outgrouped = r"C:\Users\basos\Desktop\convert\ICNF_filtered_data(1980_2000)_grouped.csv"
burnedarea.to_csv(outgrouped, index=False, mode='w', encoding='utf8')

outfile = r"C:\Users\basos\Desktop\convert\ICNF_filtered_data(1980_2000)_concelhos.csv"
sjoined2.to_csv(outfile, index=False, mode='w', encoding='utf8')
