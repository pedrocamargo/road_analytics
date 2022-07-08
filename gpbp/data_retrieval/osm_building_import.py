import sqlite3
from aequilibrae import Project
from gpbp.data_retrieval.osm_tags.import_osm_data import import_osm_data

def osm_building_import(project:Project, osm_data:dict, model_place:str):
        
    df = import_osm_data(model_place, osm_data, project, tag='building')
    """
    print('Saving OSM buildings.')

    project.conn.execute('CREATE TABLE IF NOT EXISTS osm_buildings("type" TEXT, "id" INTEGER, "building" TEXT, \
                            "zone_id" INTEGER, "area" FLOAT);')
    project.conn.execute("SELECT AddGeometryColumn('osm_buildings', 'geometry', 4326, 'POINT', 'XY' );")
    project.conn.execute("SELECT CreateSpatialIndex( 'osm_buildings' , 'geometry' );")
    project.conn.commit()

    list_of_tuples = [(x, y, z, a, b, c) for x, y, z, a, b, c in zip(df.type, df.id, df.building, df.zone_id, df.area, df.geom.wkb)]

    qry = f"INSERT into osm_buildings(type, id, building, zone_id, area, geometry) VALUES(?, ?, ?, ?, ?, CastToPoint(GeomFromWKB(?, 4326)));"
    project.conn.execute(qry, list_of_tuples)
    project.conn.commit()
    """

    ###Saving OSM buildings by category

    zoning = project.zoning
    fields = zoning.fields

    groups = df.groupby(['building', 'zone_id']).count()[['id']]

    groups['area'] = df.groupby(['building', 'zone_id']).sum().round(decimals=2)['area'].tolist()

    unique_building_values = ['residential', 'temporary_accomodation', 'commercial', 'Religious', 
                              'civic_amenity', 'agriculture_plant_production', 'sports', 'cars', 'storage', 
                              'power_techincal', 'others', 'undetermined']

    for value in unique_building_values:
        fields.add('osm_' + value + '_building', 'Number of ' + value + ' buildings provided by OSM', 'INTEGER')
        fields.add('osm_' + value + '_building_area', value + ' building area provided by OSM', 'INTEGER')

    
    single_tuple_1 = (int(row.id), idx[1])
    single_tuple_2 = (row.area, idx[1])
    
    #Essa query tem que mudar
    qry = f'UPDATE zones SET {field_name_1}=? WHERE zone_id=?;'
    project.conn.execute(qry, single_tuple_1)
    project.conn.commit()

    qry = f'UPDATE zones SET {field_name_1}=0 WHERE {field_name_1} IS NULL;'
    project.conn.execute(qry)
    project.conn.commit()

    qry = f'UPDATE zones SET {field_name_2}=? WHERE zone_id=?;'
    project.conn.execute(qry, single_tuple_2)
    project.conn.commit()

    qry = f'UPDATE zones SET {field_name_2}=0 WHERE {field_name_2} IS NULL;'
    project.conn.execute(qry)
    project.conn.commit()

    qry = 'UPDATE zones SET osm_residential_building=0, osm_temporary_accomodation_building=0, \
           osm_commercial_building=0, osm_Religious_building=0, osm_civic_amenity_building=0, \
           osm_agriculture_plant_production_building=0, osm_sports_building=0, osm_cars_building=0,\
           osm_power_techincal_building=0, osm_other_building=0, osm_undetermined_building=0 WHERE' #query incompleta
