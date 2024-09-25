import math

from entities import Planet, BaseRocket, Orbit
from physics import Physics, Vector, Point


class VerticalTakeOffRocket(BaseRocket):
    # 1. Take off while maintaining certain acceleration
    # 2. Turn off engines, wait to fly to the desired height
    # 3. Once reached the pre-determined height, activate deceleration engines
    def __init__(self, weight, payload_weight, planet: Planet, polar_angle: float,
                 target_height: float=250000, target_acceleration=9.8 * 1, engine_firing_height: float=90000, fuel_speed : float = 3000):
        super().__init__(weight, payload_weight, planet, polar_angle, fuel_speed)
        self.planet = planet
        # maximum height, that the rocket should reach
        self.target_height = target_height
        # acceleration value, that the rocket should maintain while climbing
        self.target_acceleration_value = target_acceleration
        self.phase = self.phase_take_off
        # height, at which the rocket should start deceleration while descending
        self.engine_firing_height = engine_firing_height
        self.deceleration_value = None

    @property
    def takeoff_speed(self):
        normalized_target_acceleration_vector = Vector(self.planet.position, self.position).normalize()
        return normalized_target_acceleration_vector * Vector.dot_product(normalized_target_acceleration_vector, self.speed - self.planet.speed)

    def get_height(self):
        return Physics.calculate_distance(self.position, self.planet.position) - self.planet.radius

    def should_stop_ascending(self):
        return Orbit.calculate_orbit(self.planet, self).apogee_height >= self.target_height

    def phase_take_off(self, delta_time:float=0):
        if not self.should_stop_ascending():
            gravity_force_vector = Physics.calculate_gravity(self, self.planet)
            normalized_target_acceleration_vector = Vector(self.planet.position, self.position).normalize()
            thrust_vector = normalized_target_acceleration_vector * self.weight * self.target_acceleration_value - gravity_force_vector
            self.fire_engine(thrust_vector, delta_time)
        else:
            self.phase = self.phase_wait

    def phase_wait(self, delta_time:float=0):
        if self.get_height() < self.engine_firing_height:
            self.phase = self.phase_land

    def phase_land(self, delta_time: float):
        gravity_force_vector = Physics.calculate_gravity(self, self.planet)
        self.deceleration_value = self.takeoff_speed.magnitude ** 2 / (2 * self.get_height())

        thrust_value = self.weight * self.deceleration_value + gravity_force_vector.magnitude
        thrust_vector = Vector(self.planet.position, self.position).normalize() * thrust_value

        # calculate presumable speed considering engine thrust after the next simulation speed
        new_force = gravity_force_vector + thrust_vector
        new_acceleration = new_force / self.weight
        new_position = self.position + self.takeoff_speed * delta_time + new_acceleration * delta_time ** 2 / 2
        new_absolute_height = Physics.calculate_distance(new_position, self.planet.position)
        current_absolute_height = Physics.calculate_distance(self.position, self.planet.position)
        if new_absolute_height > current_absolute_height:
            self.phase = None
        self.fire_engine(thrust_vector, delta_time)

    def make_decision(self, delta_time: float):
        if self.phase is not None:
            self.phase(delta_time)


class OrbitalManeuverRocket(BaseRocket):
    def __init__(self, weight, payload_weight, planet: Planet, target_orbit: Orbit, initial_position: Point, initial_speed: Vector, maneuver_acceleration: float = 2.0 * 9.8, fuel_speed: float = 3000):
        super().__init__(weight, payload_weight, planet, 0, fuel_speed)
        self.position = initial_position
        self.speed = initial_speed
        self.target_orbit = target_orbit
        self.planet = planet
        self.maneuver_acceleration = maneuver_acceleration
        self.maneuver_angle = target_orbit.polar_angle
        self.phase = self.phase_wait

    def get_true_anomaly(self):
        position_vector = Vector(self.planet.position, self.position)
        angle = math.atan2(position_vector.y, position_vector.x)
        if angle < 0:
            angle += 2 * math.pi
        return angle

    def phase_wait(self, delta_time: float):
        current_true_anomaly = self.get_true_anomaly()

        if abs(current_true_anomaly - self.maneuver_angle) < 0.01:
            self.phase = self.phase_perform_maneuver

    def phase_perform_maneuver(self, delta_time: float):
        target_perigee = self.target_orbit.perigee_distance
        target_apogee = self.target_orbit.semi_major_axis * 2 - target_perigee

        target_speed = math.sqrt(2 * Physics.G * self.planet.weight * target_apogee / (target_perigee * (target_perigee + target_apogee)))

        delta_v_required = target_speed - self.speed.magnitude

        delta_v_actual = min(delta_v_required, self.maneuver_acceleration * delta_time)

        thrust_vector = self.speed.normalize() * (self.weight * delta_v_actual / delta_time)

        self.fire_engine(thrust_vector, delta_time)

        if delta_v_required <= delta_v_actual:
            self.phase = None

    def make_decision(self, delta_time: float):
        if self.phase is not None:
            self.phase(delta_time)


class ComplexRocket(BaseRocket):
    def __init__(self, weight: float, payload_weight: float, planet: Planet, polar_angle: float, target_orbit: Orbit, target_acceleration: float = 3.0 * 9.8, fuel_speed: float = 3000):
        super().__init__(weight, payload_weight, planet, polar_angle, fuel_speed)
        self.target_orbit = target_orbit
        self.target_acceleration = target_acceleration
        self.phase = self.phase_take_off
        self.target_height = target_orbit.perigee_height

    @property
    def takeoff_speed(self):
        normalized_target_acceleration_vector = Vector(self.planet.position, self.position).normalize()
        return normalized_target_acceleration_vector * Vector.dot_product(normalized_target_acceleration_vector,
                                                                          self.speed - self.planet.speed)
    def get_height(self):
        return Physics.calculate_distance(self.position, self.planet.position) - self.planet.radius

    def should_stop_ascending(self):
        return Orbit.calculate_orbit(self.planet, self).apogee_height >= self.target_height

    def phase_take_off(self, delta_time: float = 0):
        if not self.should_stop_ascending():
            gravity_force_vector = Physics.calculate_gravity(self, self.planet)
            normalized_target_acceleration_vector = Vector(self.planet.position, self.position).normalize()
            thrust_vector = normalized_target_acceleration_vector * self.weight * self.target_acceleration - gravity_force_vector
            self.fire_engine(thrust_vector, delta_time)
        else:
            self.phase = self.phase_wait_for_maneuver

    def phase_wait_for_maneuver(self, delta_time: float):
        if self.get_height() >= (self.target_height - 1):
            self.phase = self.phase_perform_maneuver

    def phase_perform_maneuver(self, delta_time: float):
        target_perigee = self.target_orbit.perigee_distance
        target_apogee = self.target_orbit.semi_major_axis * 2 - target_perigee

        target_speed = math.sqrt(2 * Physics.G * self.planet.weight * target_apogee / (target_perigee * (target_perigee + target_apogee)))

        delta_v_required = target_speed - self.speed.magnitude

        delta_v_actual = min(delta_v_required, self.target_acceleration * delta_time)

        maneuver_speed_vector = Vector(self.planet.position, self.position).rotate(math.pi / 2).normalize()

        thrust_vector = maneuver_speed_vector * (self.weight * delta_v_actual / delta_time)

        if self.get_height() < self.target_height:
            gravity_vector = Physics.calculate_gravity(self.planet, self)
            thrust_vector += gravity_vector * (self.weight - (thrust_vector + gravity_vector).magnitude * delta_time / self.fuel_speed) / self.weight

        self.fire_engine(thrust_vector, delta_time)

        if delta_v_required <= delta_v_actual:
            self.phase = self.phase_wait_for_correction_maneuver

    def phase_wait_for_correction_maneuver(self, delta_time: float):
        if self.get_height() <= self.target_height:
            self.phase = self.phase_correct_orbit

    def phase_correct_orbit(self, delta_time: float):
        normalized_correction_vector = Vector(self.planet.position, self.position).normalize()
        self.fire_engine(normalized_correction_vector * (self.weight * (self.target_acceleration * delta_time) / delta_time), delta_time)

    def make_decision(self, delta_time: float):
        orbit = Orbit.calculate_orbit(self.planet, self)
        print(self.phase, self.get_height(), orbit.eccentricity, orbit.perigee_height, orbit.apogee_height)
        if self.phase is not None:
            self.phase(delta_time)