import folium
import pandas as pd
import geopandas as gpd

def map_capacity(project, location=None, radius=None, cap_threshold=1000):
    links = project.network.links.data
    longc, latc = project.conn.execute('select avg(xmin), avg(ymin) from idx_links_geometry').fetchone()
    
    if None not in [location, radius]:
        r = radius / 111
        sql = '''SELECT link_id from links
            WHERE ROWID IN 
            (SELECT ROWID FROM SpatialIndex 
              WHERE f_table_name = 'links' AND search_frame = 
              BuildCircleMbr({}, {},{}))'''.format(location[1], location[0], r)
        df = pd.read_sql(sql, project.conn)
        links = links[links.link_id.isin(df.link_id)]
        gdf = gpd.GeoDataFrame(links[['link_id', 'geometry']], geometry='geometry')
        centr = gdf.geometry.centroid
        longc = centr.x.mean()
        latc = centr.y.mean()
    
    max_cap = links[['capacity_ab', 'capacity_ba']].max().max()
    multiplier = 8 / max_cap
    
    # We create our Folium layers
    network_links = folium.FeatureGroup("links")
    high_capacity = folium.FeatureGroup("More than 100 Veh/h")
    layers = [network_links, high_capacity]

    # We do some Python magic to transform this dataset into the format required by Folium
    # We are only getting link_id and link_type into the map, but we could get other pieces of info as well
    for i, row in links.iterrows():
        points = row.geometry.wkt.replace('LINESTRING ', '').replace('(', '').replace(')', '').split(', ')
        points = '[[' + '],['.join([p.replace(' ', ', ') for p in points]) + ']]'
        # we need to take from x/y to lat/long
        points = [[x[1], x[0]] for x in eval(points)]
        
        cap = max(row.capacity_ab, row.capacity_ba)
        w = cap * multiplier
        _ = folium.vector_layers.PolyLine(points, tooltip=f'<b>capacity: {cap}</b>',
                                          color='gray', weight=w).add_to(network_links)

        if cap >= cap_threshold:
           _ = folium.vector_layers.PolyLine(points, tooltip=f'<b>capacity: {cap}</b>',
                                          color='red', weight=w).add_to(high_capacity)
    
    # We create the map
    map_osm = folium.Map(location=[latc, longc], zoom_start=11)

    # add all layers
    for layer in layers:
        layer.add_to(map_osm)

    # And Add layer control before we display it
    folium.LayerControl().add_to(map_osm)
    
    return map_osm