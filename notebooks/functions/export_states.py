from aequilibrae import Parameters, logger, Project

from functions.admin_level_per_country import admin_level
#from functions.states_in_country import states_names
from shapely.geometry import MultiPolygon, Point, LineString
from shapely.ops import polygonize

def export_states_to_project(states_borders, states_names, project):
    
    """
    This function exports the states borders to the project folder.
    """
    for key in states_names.keys():
        project.conn.execute('CREATE TABLE IF NOT EXISTS state_borders("state_name" TEXT);')
        project.conn.execute("SELECT AddGeometryColumn( 'state_borders', 'geometry', 4326, 'MULTIPOLYGON', 'XY' );")
        project.conn.execute("SELECT CreateSpatialIndex( 'state_borders' , 'geometry' );")
        project.conn.commit()
        project.conn.execute('INSERT into state_borders(state_name, geometry) VALUES(?, GeomFromWKB(?, 4326));', \
                             [states_names[key], MultiPolygon(polygonize(states_borders[key])).wkb])
        project.conn.commit()