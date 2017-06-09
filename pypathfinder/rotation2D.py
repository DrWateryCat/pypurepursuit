from .interpolable import Interpolable
import math

class Rotation2D(Interpolable):
    '''
    classdocs
    '''
    
    kEpsilon = 1e-9

    def __init__(self, x=1, y=0, normalize=False, other: 'Rotation2D'=None):
        '''
        Constructor
        '''
        
        self.cos_angle = x
        self.sin_angle = y
        
        if normalize:
            self.normalize()
            
        if other is not None:
            self.cos_angle = other.cos_angle
            self.sin_angle = other.sin_angle
            
    @staticmethod
    def from_radians(rads):
        return Rotation2D(x=math.cos(rads), y=math.sin(rads))
    
    @staticmethod
    def from_degrees(degs):
        return Rotation2D.from_radians(math.radians(degs))
    
    def normalize(self):
        magnitude = math.hypot(self.cos_angle, self.sin_angle)
        
        if magnitude > self.kEpsilon:
            self.sin_angle /= magnitude
            self.cos_angle /= magnitude
        else:
            self.sin_angle = 0
            self.cos_angle = 1
            
    def cos(self):
        return self.cos_angle
    
    def sin(self):
        return self.sin_angle
    
    def get_radians(self):
        return math.atan2(self.sin_angle, self.cos_angle)
    
    def get_degrees(self):
        return math.degrees(self.get_radians())
    
    def rotate_by(self, other: 'Rotation2D'):
        return Rotation2D(x=(self.cos_angle * other.cos_angle - self.sin_angle * other.sin_angle),
                          y=(self.cos_angle * other.sin_angle + self.sin_angle * other.cos_angle),
                          normalize=True)
        
    def inverse(self):
        return Rotation2D(x=self.cos_angle, y=-self.sin_angle)
    
    def interpolate(self, other: Interpolable, x):
        if x <= 0:
            return Rotation2D(other=self)
        elif x >= 1:
            return Rotation2D(other=other)
        
        angle_diff = self.inverse().rotate_by(other).get_radians()
        return self.rotate_by(Rotation2D.from_radians(angle_diff * x))