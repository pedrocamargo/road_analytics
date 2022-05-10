import folium

def map_all_modes(project):
    links = project.network.links.data
    nodes = project.network.nodes.data

    # We create our Folium layers
    network_links = folium.FeatureGroup("links")
    network_nodes = folium.FeatureGroup("nodes")
    car = folium.FeatureGroup("Car")
    layers = [network_links, network_nodes, car]

    # We do some Python magic to transform this dataset into the format required by Folium
    # We are only getting link_id and link_type into the map, but we could get other pieces of info as well
    for i, row in links.iterrows():
        points = row.geometry.wkt.replace('LINESTRING ', '').replace('(', '').replace(')', '').split(', ')
        points = '[[' + '],['.join([p.replace(' ', ', ') for p in points]) + ']]'
        # we need to take from x/y to lat/long
        points = [[x[1], x[0]] for x in eval(points)]

        _ = folium.vector_layers.PolyLine(points, popup=f'<b>link_id: {row.link_id}</b>', tooltip=f'{row.modes}',
                                          color='gray', weight=1.5).add_to(network_links)

        if 'c' in row.modes:
            _ = folium.vector_layers.PolyLine(points, popup=f'<b>link_id: {row.link_id}</b>', tooltip=f'{row.modes}',
                                             color='red', weight=1.5).add_to(car)
            
    # And now we get the nodes

    for i, row in nodes.iterrows():
        point = (row.geometry.y, row.geometry.x)

        _ = folium.vector_layers.CircleMarker(point, popup=f'<b>node_id: {row.node_id}</b>', tooltip=f'{row.node_id}',
                                              color='black', radius=0.1, fill=True, fillColor='black',
                                              fillOpacity=1.0).add_to(network_nodes)
    
    # We create the map
    long, lat = project.conn.execute('select avg(xmin), avg(ymin) from idx_links_geometry').fetchone()
    map_osm = folium.Map(location=[lat, long], zoom_start=11)

    # add all layers
    for layer in layers:
        layer.add_to(map_osm)

    # And Add layer control before we display it
    folium.LayerControl().add_to(map_osm)
    
    return map_osm