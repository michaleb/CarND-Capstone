
GAS_DENSITY = 2.858
ONE_MPH = 0.44704


class Controller(object):
    def __init__(self, *args, **kwargs):
    	pass

    	(self, vehicle_mass, brake_deadband, decel_limit, accel_limit, wheel_radius,
    	wheel_base, steer_ratio, max_lat_accel, max_steer_angle):

        # TODO: Implement
        self.yaw_controller = YawController(wheel_base, steer_ratio, 0.1, max_lat_accel, max_steer_angle)

        kp = 0.3
        ki = 0.1
        kd = 0.
        mn = 0.
        mx = 0.2
        self.throttle_controller = PID(kp, ki, kd, mn, mx)

        tau = 0.5
        ts = 0.02
        self.vel_lpf = LowPassFilter(tau, ts)

        self.vehicle_mass = vehicle_mass
        self.brake_deadband = brake_deadband
        self.decel_limit = decel_limit
        self.accel_limit = accel_limit
        self.wheel_radius = wheel_radius
        self.last_time = rospy.get_time()

    def control(self, *args, **kwargs):
    	#(self, current_vel, dbw_enabled, linear_vel, angular_vel):
        # TODO: Change the arg, kwarg list to suit your needs
        # Return throttle, brake, steer

        #if not dbw_enabled:
        #	self.throttle_controller.reset()
        return 1., 0., 0.

        #current_vel = self.vel_lpf.filt(current_vel)
