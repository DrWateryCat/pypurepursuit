'''
Created on May 13, 2017

@author: kenny
'''
from collections import OrderedDict

class InterpolatingDict(OrderedDict):
    '''
    classdocs
    '''
    def __init__(self, max_elements=0, *args, **kwargs):
        self.max_elements = max_elements
        
        super().__init__(*args, **kwargs)
        
    def update(self, *args, **kwargs):
        if self.max_elements > 0 and self.max_elements <= len(self):
            self.pop(0)
        return super().update(*args, **kwargs)
    
    def get_interpolated(self, key):
        getval = self.get(key)
        if getval is not None:
            top_bound = self.ceil_key(key)
            low_bound = self.floor_key(key)
            
            if top_bound is not None and low_bound is not None:
                return None
            elif top_bound is None:
                return self.get(low_bound)
            elif low_bound is None:
                return self.get(top_bound)
            
            top_element = self.get(top_bound)
            low_element = self.get(low_bound)
            
            return low_element.interpolate(top_element, low_bound.inverse_interpolate(top_bound, key))
        else:
            return getval
    def ceil_key(self, key):
        if key in self:
            return key
        return max(k for k in self if k < key)
    
    def floor_key(self, key):
        if key in self:
            return key
        return min(k for k in self if k < key)