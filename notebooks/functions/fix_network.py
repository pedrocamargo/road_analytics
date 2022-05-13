from os.path import dirname, join
import pandas as pd

def fix_speeds(project):
    pth = join(dirname(dirname(dirname(__file__))), 'model', 'network')
    
    speeds_and_capacities = pd.read_csv(join(pth, 'speeds_and_capacities.csv'))
    
    # Number of lanes and lane_capacity
    project.conn.execute('Update link_types set lanes=1, lane_capacity=400 where link_type_id not in ("z", "y")')
    project.conn.commit()
    for idx, rec in speeds_and_capacities.iterrows():
        project.conn.execute('Update link_types set lanes=?, lane_capacity=? where link_type=?', [rec.lanes, rec.lane_capacity, rec.link_type])
        project.conn.execute('Update links set lanes_ab=? where lanes_ab is NULL and direction>=0 and link_type=?', [rec.lanes, rec.link_type])
        project.conn.execute('Update links set lanes_ba=? where lanes_ba is NULL and direction>=0 and link_type=?', [rec.lanes, rec.link_type])

    project.conn.execute('Update links set lanes_ab = (select lanes from link_types where link_type=links.link_type) where lanes_ab is NULL')
    project.conn.execute('Update links set lanes_ba =(select lanes from link_types where link_type=links.link_type) where lanes_ba is NULL')
    
    
    # Speeds
    for idx, rec in speeds_and_capacities.iterrows():
        project.conn.execute('Update links set speed_ab=? where direction>=0 and link_type=?', [rec.speed, rec.link_type])
        project.conn.execute('Update links set speed_ba=? where direction<1 and link_type=?', [rec.speed, rec.link_type])

    # Fill the missing ones
    project.conn.execute('Update links set speed_ab=40 where direction>=0 and speed_ab is NULL')
    project.conn.execute('Update links set speed_ba=40 where direction<1 and speed_ba is NULL')
    project.conn.commit()

    
    ### Link capacities
    project.conn.execute('Update links set capacity_ab=lanes_ab* (select lane_capacity from link_types where link_types.link_type=links.link_type)')
    project.conn.execute('Update links set capacity_ba=lanes_ba* (select lane_capacity from link_types where link_types.link_type=links.link_type)')
    project.conn.execute("Update links set capacity_ab=0.1 where modes like '%c%' and capacity_ab=0")
    project.conn.execute("Update links set capacity_ba=0.1 where modes like '%c%' and capacity_ba=0")

    
    ### Applies pavement constraints
    pavement_multiplier = pd.read_csv(join(pth, 'pavement_constraints.csv'))
    
    for idx, rec in pavement_multiplier.iterrows():
        data = [rec.capacity_multiplier, rec.capacity_multiplier, rec.speed_multiplier, rec.speed_multiplier, rec.pavement]
        project.conn.execute('Update links set capacity_ab=capacity_ab*?, capacity_ba=capacity_ba*?, speed_ab=speed_ab*?, speed_ba=speed_ba*? where surface=?', data)
    project.conn.commit()