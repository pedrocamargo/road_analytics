import pandas as pd
import sqlite3
from aequilibrae import Project

def trigger_import_amenities(project:Project, export_csv=True):

    #Importar amenities na área em questão
    #Exportar como .csv  bool
    

    #Salvar no layer de zonas

    zoning = project.zoning
    fields = zoning.fields

    list_of_tuples = list(zip(dict_pop.values(), dict_pop.keys()))

    for _, row in df.iterrows():

        fields.add(row.field_name, row.desc_field, 'INTEGER')

        zones_qry = f'UPDATE zones SET {row.field_name}=? WHERE zone_id=?;'
        project.conn.executemany(qry, list_of_tuples)
        project.conn.commit()
    pass