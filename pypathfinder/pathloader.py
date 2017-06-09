from typing import List
from .waypoint import Waypoint

import csv
from .translation2D import Translation2D

class PathLoader(object):
    '''
    classdocs
    '''


    def __init__(self, filename: str):
        '''
        Constructor
        '''
        self.filename = filename
        
    def load_waypoints(self) -> List[Waypoint]:
        ret = List[Waypoint]
        
        with open(self.filename, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ret.append(Waypoint(Translation2D(row['x_position'], row['y_position']), 
                                    row['speed'], 
                                    row['marker'] if row['marker'] is not None else ''))
                
        return ret