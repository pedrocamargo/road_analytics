import folium

def map_capacity(project):
    links = project.network.links.data
    
    max_cap = links[['capacity_ab', 'capacity_ba']].max().max()
    multiplier = 7 / max_cap
    
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
        _ = folium.vector_layers.PolyLine(points, popup=f'<b>capacity: {cap}</b>', tooltip=f'{row.modes}',
                                          color='gray', weight=w).add_to(network_links)

        if cap >= 1000:
           _ = folium.vector_layers.PolyLine(points, popup=f'<b>capacity: {cap}</b>', tooltip=f'{row.modes}',
                                          color='red', weight=w).add_to(high_capacity)
    
    # We create the map
    long, lat = project.conn.execute('select avg(xmin), avg(ymin) from idx_links_geometry').fetchone()
    map_osm = folium.Map(location=[lat, long], zoom_start=11)

    # add all layers
    for layer in layers:
        layer.add_to(map_osm)

    # And Add layer control before we display it
    folium.LayerControl().add_to(map_osm)
    
    return map_osm