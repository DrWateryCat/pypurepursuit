'''
Created on May 13, 2017

@author: kenny
'''
from interpolable import Interpolable
from inverseinterpolable import InverseInterpolable

class InterpolatingValue(Interpolable, InverseInterpolable):
    def __init__(self, val):
        self.val = val
        
    def interpolate(self, other: InterpolatingValue, x):
        delta = other.val - self.val
        search_y = delta * x + self.val
        
        return InterpolatingValue(search_y)
    
    def inverse_interpolate(self, upper: InterpolatingValue, query: InterpolatingValue):
        upper_to_lower = upper.val - self.val
        if upper_to_lower <= 0:
            return 0
        query_to_lower = query.val - self.val
        if query_to_lower <= 0:
            return 0
        return query_to_lower / upper_to_lower