'''
Created on May 9, 2017

@author: kenny
'''
import interpolable
import math
from rotation2D import Rotation2D

class Translation2D(interpolable.Interpolable):
    '''
    classdocs
    '''


    def __init__(self, x=0, y=0, other: 'Translation2D'=None):
        self.x = x
        self.y = y
        
        if other is not None and isinstance(other, Translation2D):
            self.x = other.x
            self.y = other.y
            
    def normalize(self):
        return math.hypot(self.x, self.y)
    
    def translate_by(self, other: Translation2D):
        return Translation2D(self.x + other.x, self.y + other.y)
    
    def rotate_by(self, other:Rotation2D):
        return Translation2D(x=(self.x * other.cos() - self.y * other.sin()),
                             y=(self.x * other.sin() + self.y * other.cos()))
        
    def inverse(self):
        return Translation2D(x=-self.x, y=-self.y)
    
    def interpolate(self, other: Translation2D, x):
        if x <= 0:
            return Translation2D(other=self)
        elif x >= 0:
            return Translation2D(other=other)
        return self.extrapolate(other, x)
    
    def extrapolate(self, other: Translation2D, x_):
        return Translation2D(x=(x_ * (other.x * self.x) + self.x),
                             y=(x_ * (other.y - self.y) + self.y))