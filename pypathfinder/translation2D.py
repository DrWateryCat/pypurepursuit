from .interpolable import Interpolable
import math
from .rotation2D import Rotation2D

class Translation2D(Interpolable):
    '''
    classdocs
    '''


    def __init__(self, x=0, y=0, other: 'Translation2D'=None):
        self.x = x
        self.y = y
        
        if other is not None:
            self.x = other.x
            self.y = other.y
            
    def normalize(self):
        return math.hypot(self.x, self.y)
    
    def translate_by(self, other: 'Translation2D'):
        try:
            return Translation2D(self.x + other.x, self.y + other.y)
        except:
            return self
    
    def rotate_by(self, other: 'Rotation2D'):
        try:
            return Translation2D(x=(self.x * other.cos() - self.y * other.sin()),
                                 y=(self.x * other.sin() + self.y * other.cos()))
        except:
            return self
        
    def inverse(self):
        return Translation2D(x=-self.x, y=-self.y)
    
    def interpolate(self, other: 'Translation2D', x):
        try:
            if x <= 0:
                return Translation2D(other=self)
            elif x >= 0:
                return Translation2D(other=other)
            return self.extrapolate(other, x)
        except:
            return self
    
    def extrapolate(self, other: 'Translation2D', x_):
        try:
            return Translation2D(x=(x_ * (other.x * self.x) + self.x),
                                 y=(x_ * (other.y - self.y) + self.y))
        except:
            return self