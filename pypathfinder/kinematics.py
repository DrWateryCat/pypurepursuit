from .rigidtransform2d import RigidTransform2D
from .rotation2D import Rotation2D

class Kinematics:
    EPSILON = 1e-9

    class DriveData:
        def __init__(self, left, right):
            self.left = left
            self.right = right

    @staticmethod
    def forward_kinematics_with_gyro(delta_left, delta_right, delta_rotation_rads):
        return RigidTransform2D.Delta(delta_left, delta_right, delta_rotation_rads)

    @staticmethod
    def forward_kinematics(delta_left, delta_right, wheel_slip_factor=0.5, wheel_diameter=6):
        linear_velocity = (delta_left + delta_right) / 2
        delta_v = (delta_right - delta_left) / 2
        delta_rotation = delta_v * 2 * wheel_slip_factor / wheel_diameter
        return RigidTransform2D.Delta(linear_velocity, 0, delta_rotation)

    @staticmethod
    def integrate_forward_kinematics(current_pose: RigidTransform2D, delta_left, delta_right, current_heading: Rotation2D):
        with_gyro = Kinematics.forward_kinematics_with_gyro(delta_left, delta_right, current_pose.get_rotation().inverse().rotate_by(current_heading).get_radians())
        return current_pose.transformby(RigidTransform2D.from_velocity(with_gyro))

    @staticmethod
    def inverse_kinematics(velocity: RigidTransform2D.Delta, wheel_slip_factor=0.5, wheel_diameter=6):
        if abs(velocity.dTheta) < Kinematics.EPSILON:
            return Kinematics.DriveData(velocity.dX, velocity,dY)
        delta_v = wheel_diameter * velocity.dTheta / (2 * wheel_slip_factor)
        return Kinematics.DriveData(velocity.dX - delta_v, velocity.dX + delta_v)