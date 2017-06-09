from builtins import set
from .pathsegment import PathSegment
from typing import List
from .translation2D import Translation2D
from .waypoint import Waypoint

import math

class Path:
    '''
    classdocs
    '''
    
    kCompletedPercentage = 0.99


    def __init__(self, waypoints: List[Waypoint]):
        '''
        Constructor
        '''
        self.markers_crossed = set()
        self.waypoints = waypoints
        self.segments = list()
        
        for i in range(0, len(waypoints) - 1, 1):
            seg = PathSegment(start=waypoints[i].position, end=waypoints[i+1].position, speed=waypoints[i].speed)
            self.segments.append(seg)
            
        if len(waypoints) > 0:
            first_waypoint = self.waypoints.pop(0)
            if first_waypoint.marker != "":
                self.markers_crossed.add(first_waypoint.marker)
            
    def update(self, position:Translation2D):
        rv = 0.0
        it = iter(self.segments)
        for segment in it:
            closest_point_report = segment.get_closest_point(position)
            
            if closest_point_report.index >= self.kCompletedPercentage:
                self.segments.remove(segment)
                
                if len(self.waypoints) > 0:
                    waypoint = self.waypoints.pop(0)
                    
                    if waypoint.marker != "":
                        self.markers_crossed.add(waypoint.marker)
            else:
                if closest_point_report.index > 0.0:
                    segment.update_start(closest_point_report.closest_point)
                    
                rv = closest_point_report.distance
                
                try:
                    _next = next(it)
                    next_closest_point_report = _next.get_closest_point()
                    
                    if next_closest_point_report.index > 0 and next_closest_point_report.index < self.kCompletedPercentage and next_closest_point_report.distance < rv:
                        next.update_start(next_closest_point_report.closest_point)
                        rv = next_closest_point_report.distance
                        
                        self.segments.pop(0)
                        if len(self.waypoints) > 0:
                            waypoint = self.waypoints.pop(0)
                            if waypoint.marker != "":
                                self.markers_crossed.add(waypoint.marker)
                        
                    
                except StopIteration:
                    break
        return rv
    
    def get_markers_crossed(self):
        return self.markers_crossed
    
    def get_remaining_length(self):
        length = 0.0
        for i in self.segments:
            length += i.length
        return length
            
    def get_lookahead_point(self, position: Translation2D, lookahead_distance) -> PathSegment.Sample:
        if len(self.segments) == 0:
            return PathSegment.Sample(Translation2D(), speed=0)
        
        
        pos_inverse = position.inverse()
        if pos_inverse.translate_by(self.segments[0].start).normalize() >= lookahead_distance:
            #Just return the first point
            #print ("Returning first point")
            return PathSegment.Sample(self.segments[0].start, self.segments[0].speed)
        
        for segment in self.segments:
            distance = pos_inverse.translate_by(segment.end).normalize()
            if distance >= lookahead_distance:
                #Segment contains lookahead point
                intersection_point = self.get_first_circle_segment_intersection(segment, position, lookahead_distance)
                
                if intersection_point is not None:
                    #print ("Return intersection point")
                    return PathSegment.Sample(intersection_point, segment.speed)
                else:
                    print("ERROR: No Intersection point?")
                    
        #After last point, extrapolate forward
        last_segment = self.segments[-1]
        new_last_segment = PathSegment(last_segment.start, last_segment.interpolate(10000), last_segment.speed)
        
        intersection_point = self.get_first_circle_segment_intersection(new_last_segment, position, lookahead_distance)
        
        if intersection_point is not None:
            #print ("Returning circle intersection")
            return PathSegment.Sample(intersection_point, last_segment.speed)
        else:
            print("ERROR: No intersection point anywhere on the line?")
            return PathSegment.Sample(last_segment.end, last_segment.speed)
        
    def get_first_circle_segment_intersection(self, segment: PathSegment, center: Translation2D, radius):
        x1 = segment.start.x - center.x
        y1 = segment.start.y - center.y
        x2 = segment.end.x - center.x
        y2 = segment.end.y - center.y
        
        dX = x2 - x1
        dY = y2 - y1
        
        dr_squared = (dX ** 2) + (dY ** 2)
        
        det = x1 * y2 - x2 - y1
        
        discriminant = dr_squared * (radius ** 2) - (det ** 2)
        
        if discriminant < 0:
            #No intersection
            return None
        
        sqrt_discriminant = math.sqrt(discriminant)
        
        pos_solution = Translation2D(x=((det * dY + (-1 if dY < 0 else 1) * dX * sqrt_discriminant) / dr_squared + center.x),
                                     y=((-det * dX + abs(dY) * sqrt_discriminant) / dr_squared + center.y))
        neg_solution = Translation2D(x=((det * dY - (-1 if dY < 0 else 1) * dX * sqrt_discriminant) / dr_squared + center.x),
                                     y=((-det * dX - abs(dY) * sqrt_discriminant) / dr_squared + center.y))
        
        pos_dot_product = segment.dot_product(pos_solution)
        neg_dot_product = segment.dot_product(neg_solution)
        
        if pos_dot_product < 0 and neg_dot_product >= 0:
            return neg_solution
        elif pos_dot_product >= 0 and neg_dot_product < 0:
            return pos_solution
        else:
            if abs(pos_dot_product) <= abs(neg_dot_product):
                return pos_solution
            else:
                return neg_solution