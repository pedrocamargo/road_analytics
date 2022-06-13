import imp
from aequilibrae import Project, Parameters
import sqlite3

def trigger_population(project:Project, source:str):

    #conn = project.conn
    #population = 'raw_population' in [x[0] for x in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

    if 'raw_population' in [x[0] for x in project.conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
        print(f'raw_population file will be overwritten.')
        project.conn.execute('Drop table if exists raw_population')
        project.conn.commit()  

    else:
        pass

