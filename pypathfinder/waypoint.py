'''
Created on May 10, 2017

@author: kenny
'''
from translation2D import Translation2D

class Waypoint(object):
    '''
    classdocs
    '''


    def __init__(self, position: Translation2D, speed=0, marker=None):
        '''
        Constructor
        '''
        self.position = position
        self.speed = speed
        if marker is None:
            self.marker = ""
        else:
            self.marker = marker