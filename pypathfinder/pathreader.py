from typing import List
from .waypoint import Waypoint
import csv

class PathReader(object):
    '''
    classdocs
    '''
    
    field_names = ['x_position', 'y_position', 'speed', 'marker']

    def __init__(self, filename: str):
        '''
        Constructor
        '''
        self.filename = filename
        
    def write_path(self, waypoints: List[Waypoint]):
        with open(self.filename, 'wb+') as csvfile:
            #Delete contents of file
            csvfile.seek(0, 0)
            csvfile.truncate()
            
            #Open CSV Writer
            writer = csv.DictWriter(csvfile, self.field_names)
            
            #Loop through the waypoints
            for wp in waypoints:
                x = wp.position.x
                y = wp.position.y
                
                writer.writerow({'x_position': x, 'y_position': y, 'speed': wp.speed, 'marker': wp.marker})