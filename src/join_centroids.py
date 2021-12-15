import pandas as pd

#print(pd.__version__) # '0.24.2'
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 170)

grouped = pd.read_csv('All_data_1980_2021_grouped.csv', encoding='utf8')
print(grouped.columns)
print(grouped.info())
print(grouped.head())

centroids = pd.read_csv('concelhos_centroids_mainland_table.csv', encoding='utf8')
print(centroids.columns)
print(centroids.info())
print(centroids.head())

duplicates = centroids[centroids.duplicated(['NAME_2'], keep=False)]
print('duplicates')
print(duplicates) # second are weird places

centroids = centroids[['NAME_2','x','y']] # keep only these columns
print(centroids.head())

print(centroids.shape)
centroids = centroids.drop_duplicates(subset = ['NAME_2']) # keeps first by default
print(centroids.shape)

print(grouped.shape)
grouped2 = grouped.merge(centroids, left_on='concelho',  right_on='NAME_2',  how='left')
#left2.merge(right2, left_on='keyLeft', right_on='keyRight', how='left') # preserving left df (first one)
print(grouped2.head())
print(grouped2.shape)

print('not joined', grouped2.loc[grouped2['NAME_2'].isnull()].shape[0])
not_joined = grouped2.loc[grouped2['NAME_2'].isnull()]
print(not_joined)

#print('why joined', grouped2.loc[grouped2['concelho'].isnull()].shape[0])
#why_joined = grouped2.loc[grouped2['concelho'].isnull()]
#print(why_joined)

grouped2 = grouped2.drop('NAME_2', 1)
outfile = 'All_data_1980_2021_grouped_centroids.csv'
grouped2.to_csv(outfile, index=False, mode='w', encoding='utf8')
