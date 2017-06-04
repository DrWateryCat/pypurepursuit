import pypathfinder

robot_frame = pypathfinder.RigidTransform2D(pypathfinder.Translation2D(0, 0), pypathfinder.Rotation2D(1, 0))

waypoints = [
    pypathfinder.Waypoint(pypathfinder.Translation2D(0, 0), 20),
    pypathfinder.Waypoint(pypathfinder.Translation2D(5, 6), 20, "Middle"),
    pypathfinder.Waypoint(pypathfinder.Translation2D(3, 7), 20)
]

path = pypathfinder.Path(waypoints)

controller = pypathfinder.AdaptivePurePursuitController(24, 80.0, 0.01, path, False, 0.25)
print (str(robot_frame))
print (str(path))
print (str(controller))