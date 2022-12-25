import arcgis
import pandas as pd
from collections import Counter

data = pd.DataFrame.spatial.from_featureclass("F:/ArcGIS_detection/packages/Natural_Earth_quick_start/110m_physical/ne_110m_lakes.shp")
duplicate = data[data.duplicated(['name'])]
print(duplicate)

single_columns = data['name'].tolist()
print(single_columns)

entry_search = Counter(single_columns)
print(entry_search)

duplicate_individuals_search = list([item for item in entry_search if entry_search[item]>1])
print(duplicate_individuals_search)
