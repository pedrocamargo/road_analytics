from aequilibrae import Project

from gpbp.model_creation.country_subdivisions import get_subdivisions


def add_subdivisions_to_model(project: Project, model_place: str, levels_to_add=2, overwrite=True):
    """"""

    # TODO: Setup the sub-divisions file to contain all levels (up to 5)
    # Setup the addition of subdivisions up to the desired level
    # TODO: Add the overwrite feature so we just skip the function if subdivisions already exist

    gdf = get_subdivisions(model_place)

    if gdf.shape[0] == 0:
        return

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
