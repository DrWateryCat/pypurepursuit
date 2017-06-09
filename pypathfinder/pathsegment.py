from .translation2D import Translation2D
import math

class PathSegment(object):
    '''
    classdocs
    '''
    
    kEpsilon = 1e-9
    
    class Sample:
        def __init__(self, translation: Translation2D, speed: float=0):
            self.translation = translation
            self.speed = speed
            
    class ClosestPointReport:
        index = 0
        clamped_index = 0
        closest_point = None #Translation2D
        distance = 0

    def __init__(self, start: Translation2D, end: Translation2D, speed=0):
        '''
        Constructor
        '''
        self.end = end
        self.speed = speed
        
        self.update_start(start)
        
    def update_start(self, start: Translation2D):
        self.start = start
        self.start_to_end = self.start.inverse().translate_by(self.end)
        
        self.length = self.start_to_end.normalize()
        
    def interpolate(self, index):
        return self.start.interpolate(self.end, index)
    
    def dot_product(self, other: Translation2D):
        start_to_other = self.start.inverse().translate_by(other)
        return self.start_to_end.x * start_to_other.x + self.start_to_end.y * start_to_other.y
    
    def get_closest_point(self, query_point: Translation2D):
        rv = self.ClosestPointReport()
        
        if self.length > self.kEpsilon:
            dot_product = self.dot_product(query_point)
            rv.index = dot_product / (self.length ** 2)
            rv.clamped_index = min(1.0, max(0.0, rv.index))
            rv.closest_point = self.interpolate(rv.index)
        else:
            rv.index = rv.clamped_index = 0.0
            rv.closest_point = Translation2D(other=self.start)
            
        rv.distance = rv.closest_point.inverse().translate_by(query_point).normalize()
        
        return rv