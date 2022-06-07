

def overwrite_file(overwirte=False, project):
    
    if overwirte == False:
        print("Ok")
        
    else:

        project.conn.execute('Drop TABLE IF EXISTS country_subdivisions;')
        project.conn.execute(
            'CREATE TABLE IF NOT EXISTS country_subdivisions("country_name" TEXT, "division_name" TEXT, "level" INTEGER);')
        project.conn.execute(
            "SELECT AddGeometryColumn( 'country_subdivisions', 'geometry', 4326, 'MULTIPOLYGON', 'XY' );")

        project.conn.execute("SELECT CreateSpatialIndex( 'country_subdivisions' , 'geometry' );")
        project.conn.commit()

        sql = '''INSERT into country_subdivisions(country_name, division_name, level, geometry)
                                        VALUES(?, ?, ?, CastToMulti(GeomFromWKB(?, 4326)));'''
        for _, rec in gdf.iterrows():
            project.conn.execute(sql, [model_place, rec['name'], rec.level, rec.geometry.wkb])
        project.conn.commit()
