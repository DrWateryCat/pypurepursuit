from .translation2D import Translation2D

class Circle(object):
    '''
    classdocs
    '''


    def __init__(self, center: Translation2D, radius, turn_right):
        '''
        Constructor
        '''
        
        self.center = center
        self.radius = radius
        self.turn_right = turn_right