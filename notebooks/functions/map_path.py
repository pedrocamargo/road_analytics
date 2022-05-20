import folium

def map_single_path(project, path_results):
    links = project.network.links.data
    
    links = links[links.link_id.isin(path_results.path)]
    path_layer = folium.FeatureGroup("Path")
    layers = [path_layer]

    # We do some Python magic to transform this dataset into the format required by Folium
    # We are only getting link_id and link_type into the map, but we could get other pieces of info as well
    for i, row in links.iterrows():
        points = row.geometry.wkt.replace('LINESTRING ', '').replace('(', '').replace(')', '').split(', ')
        points = '[[' + '],['.join([p.replace(' ', ', ') for p in points]) + ']]'
        # we need to take from x/y to lat/long
        points = [[x[1], x[0]] for x in eval(points)]

        _ = folium.vector_layers.PolyLine(points, popup=f'<b>link_id: {row.link_id}</b>', tooltip=f'{row.modes}',
                                             color='yellow', weight=3).add_to(path_layer)
    
    # We create the map
    long, lat = project.conn.execute('select avg(xmin), avg(ymin) from idx_links_geometry').fetchone()
    map_osm = folium.Map(location=[lat, long], zoom_start=11)

    # add all layers
    path_layer.add_to(map_osm)
        

    # And Add layer control before we display it
    folium.LayerControl().add_to(map_osm)
    
    return map_osm