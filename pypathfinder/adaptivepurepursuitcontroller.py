'''
Created on May 10, 2017

@author: kenny
'''

from path import Path
from rigidtransform2d import RigidTransform2D
from translation2D import Translation2D
from rotation2D import Rotation2D
from circle import Circle
import math

class AdaptivePurePursuitController:
    '''
    classdocs
    '''
    
    kEpsilon = 1e-9
    kMinSpeed = 4.0
    
    def __init__(self, fixed_lookahead, max_accel, nominal_dt, path: Path, reverse, path_completion_tolerance):
        self.fixed_lookahead = fixed_lookahead
        self.max_accel = max_accel
        self.path = path
        self.dT = nominal_dt
        self.last_command = None
        self.reversed = reverse
        self.path_completion_tolerance = path_completion_tolerance
        self.last_time = 0
        
    def is_done(self):
        remaining_length = self.path.get_remaining_length()
        return remaining_length <= self.path_completion_tolerance
    
    def update(self, robot_pose: RigidTransform2D, now) -> RigidTransform2D.Delta:
        pose = robot_pose
        if self.reversed:
            pose = RigidTransform2D(translation=robot_pose.get_translation(),
                                    rotation=robot_pose.get_rotation().rotate_by(Rotation2D.from_radians(math.pi)))
        
        distance_from_path = self.path.update(robot_pose.get_translation())
        if self.is_done():
            return RigidTransform2D.Delta()
        
        lookahead_point = self.path.get_lookahead_point(robot_pose.get_translation(), distance_from_path + self.fixed_lookahead)
        circle = AdaptivePurePursuitController.join_path(pose, lookahead_point.translation)
        
        speed = lookahead_point.speed
        if self.reversed:
            speed *= -1
            
        dT = now - self.last_time
        if self.last_command is None:
            self.last_command = RigidTransform2D.Delta()
            dT = self.dT
            
        accel = (speed - self.last_command.dX) / dT
        if accel < -self.max_accel:
            speed = self.last_command.dX - self.max_accel * dT
        elif accel > self.max_accel:
            speed = self.last_command + self.max_accel * dT
            
        remaining_distance = self.path.get_remaining_length()
        max_allowed_speed = math.sqrt(2 * self.max_accel * remaining_distance)
        
        if abs(speed) > max_allowed_speed:
            speed = max_allowed_speed * math.copysign(1, speed)
            
        if abs(speed) < self.kMinSpeed:
            speed = self.kMinSpeed * math.copysign(1, speed)
            
        rv = None
        if circle is not None:
            rv = RigidTransform2D.Delta(speed, 0, 
                                        (-1 if circle.turn_right else 1) * abs(speed) / circle.radius)
        else:
            rv = RigidTransform2D.Delta(speed)
            
        self.last_time = now
        self.last_command = rv
        
        return rv
    
    def get_markers_crossed(self):
        return self.path.get_markers_crossed()
    
    @staticmethod
    def join_path(robot_pose: RigidTransform2D, lookahead_point: Translation2D) -> Circle:
        x1 = robot_pose.get_translation().x
        y1 = robot_pose.get_translation().y
        x2 = lookahead_point.x
        y2 = lookahead_point.y
        
        pose_to_lookahead = robot_pose.get_translation().inverse().translate_by(lookahead_point)
        cross_product = pose_to_lookahead.x * robot_pose.get_rotation().sin() - pose_to_lookahead.y * robot_pose.get_rotation().cos()
        
        if abs(cross_product) < AdaptivePurePursuitController.kEpsilon:
            return None
        
        dX = x1 - x2
        dY = y1 - y2
        
        mY = (-1 if cross_product > 0 else 1) * robot_pose.get_rotation().cos()
        mX = (1 if cross_product > 0 else -1) * robot_pose.get_rotation().sin()
        
        cross_term = mX * dX + mY * dY
        
        if abs(cross_term) < AdaptivePurePursuitController.kEpsilon:
            return None
        
        return Circle(Translation2D((mX * (x1 * x1 - x2 * x2 - dY * dY) + 2 * mY * x1 * dY) / (2 * cross_term),
                      (-mY * (-y1 * y1 + y2 * y2 + dX * dX) + 2 * mX * y1 * dX) / (2 * cross_term)),
                      0.5 * abs((dX * dX + dY * dY) / cross_term), cross_product > 0)