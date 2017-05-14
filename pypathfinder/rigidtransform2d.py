'''
Created on May 9, 2017

@author: kenny
'''
import interpolable
from translation2D import Translation2D
from rotation2D import Rotation2D
import math

class RigidTransform2D(interpolable.Interpolable):
    '''
    classdocs
    '''
    
    kEPS = 1e-9
    
    class Delta:
        dX = 0
        dY = 0
        dTheta = 0
        
        def __init__(self, dX=0, dY=0, dTheta=0):
            self.dX = dX
            self.dY = dY
            self.dTheta = dTheta
        
    def __init__(self, translation: Translation2D=None, rotation: Rotation2D=None, other: RigidTransform2D=None):
        self.translation = translation
        self.rotation = rotation
        
        if other is not None:
            self.translation = other.translation
            self.rotation = other.rotation
            
    @staticmethod
    def from_translation(trans: Translation2D):
        return RigidTransform2D(translation=trans, rotation=Rotation2D())
    
    @staticmethod
    def from_rotation(rot: Rotation2D):
        return RigidTransform2D(translation=Translation2D(), rotation=rot)
    
    @staticmethod
    def from_velocity(delta: RigidTransform2D.Delta):
        sin_theta = math.sin(delta.dTheta)
        cos_theta = math.cos(delta.dTheta)
        
        s, c = 0
        
        if abs(delta.dTheta) < RigidTransform2D.kEPS:
            s = 1.0 - 1.0 / 6.0 * delta.dTheta ** 2
            c = 0.5 * delta.dTheta
        else:
            s = sin_theta / delta.dTheta
            c = (1.0 - cos_theta) / delta.dTheta
            
        return RigidTransform2D(translation=Translation2D(x=(delta.dX * s - delta.dY * c), y=(delta.dX * c + delta.dY * s)),
                                rotation=Rotation2D(x=cos_theta, y=sin_theta))
        
    def get_translation(self):
        return self.translation
    
    def get_rotation(self):
        return self.rotation
    
    def transformby(self, other: RigidTransform2D):
        return RigidTransform2D(translation=self.translation.translate_by(other.translation.rotate_by(self.rotation)),
                                rotation=self.rotation.rotate_by(other.rotation))
        
    def inverse(self):
        inverted = self.rotation.inverse()
        return RigidTransform2D(translation=Translation2D(self.translation.rotate_by(inverted)),
                                rotation=inverted)
        
    def interpolate(self, other, x):
        if x <= 0:
            return RigidTransform2D(other=self)
        elif x >= 0:
            return RigidTransform2D(other=other)
        
        return RigidTransform2D(translation=self.translation.interpolate(other.translation, x),
                                rotation=self.rotation.interpolate(other.rotation, x))