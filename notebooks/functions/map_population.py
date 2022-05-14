import folium
from folium.plugins import HeatMap
import pandas as pd
from aequilibrae.project import Project
from shapely import wkb
import geopandas as gpd

def map_pop(project: Project, poi=None, radius=None):
    
    '''
        Function that creates a population heat map.
    '''
    
    if poi == None or radius ==None:
        sql = "select latitude, longitude, population from raw_population"
    else:
        r = radius / 111
        sql = '''SELECT latitude, longitude, population from raw_population 
            WHERE ROWID IN 
            (SELECT ROWID FROM SpatialIndex 
              WHERE f_table_name = 'raw_population' AND search_frame = 
              BuildCircleMbr({}, {},{}))'''.format(poi[1], poi[0], r)
    pop_data = pd.DataFrame(project.conn.execute(sql), columns=['lat', 'long', 'weight'])
    
    
    # We create the map
    long, lat = tuple([pop_data['long'].mean(), pop_data['lat'].mean()])
    
    map_osm = folium.Map(location=[lat, long], zoom_start=11)

    hm = HeatMap(pop_data.values.tolist(), gradient={0.1: 'blue', 0.3: 'lime', 0.5: 'yellow', 0.7: 'orange', 1: 'red'}, 
                    min_opacity=0.05, 
                    max_opacity=0.9, 
                    radius=25,
                    use_local_extrema=True)

    map_osm.add_child(hm)
    
    return map_osm


# def map_pop(project: Project):

    # '''
    #     Function that creates a population map using circle markers.
    # '''

#     # We create our Folium layers
#     network_nodes = folium.FeatureGroup("nodes")

#     sql = "SELECT population, Hex(ST_AsBinary(GEOMETRY)) as geom FROM raw_population;"
#     pop_data = gpd.GeoDataFrame.from_postgis(sql, project.conn, geom_col="geom")
#     pop_data.set_crs('epsg:4326', inplace=True)

#     # We do some Python magic to transform this dataset into the format required by Folium
#     for i, row in pop_data.iterrows():

#         point = (row.geom.y, row.geom.x)
#         # point = (wkb.loads(row.geometry).y, wkb.loads(row.geometry).x)
        
#         if row.population > 5:
#             _ = folium.vector_layers.CircleMarker(point, popup=f'<b>population: {row.population}</b>', tooltip=f'{row.population}',
#                                               color='#2B82C6', weight=0.6, radius=row.population / 4, fill=True, fillColor='red',
#                                               fillOpacity=0.5).add_to(network_nodes)
    
#     # We create the map
#     long, lat = project.conn.execute('select avg(xmin), avg(ymin) from idx_links_geometry').fetchone()
#     map_osm = folium.Map(location=[lat, long], zoom_start=11)
    
#     network_nodes.add_to(map_osm)

#     # And Add layer control before we display it
#     folium.LayerControl().add_to(map_osm)  
    
#     return map_osm