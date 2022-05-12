from aequilibrae.project import Project
import shapely

def get_main_area(project: Project):
    
    country_wkb = [x[0] for x in project.conn.execute('Select asBinary(geometry) from country_borders')]
    country_geo = shapely.wkb.loads(country_wkb[0])
    
    for main_area in country_geo.geoms:
        if main_area.area > country_geo.area * 0.9:
            break
            
    return main_area