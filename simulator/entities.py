from inspect import signature

from physics import Entity, Physics, Point, Vector


class Planet(Entity):
    def __init__(self, weight: float, position: Point, speed: Vector, radius: float, angle_speed: float):
        super().__init__(weight, position, speed)
        self.radius = radius
        self.polar_angle = 0
        self.angle_speed = angle_speed


class BaseRocket(Entity):
    def __init__(self, weight, position: Point, speed: Vector):
        super().__init__(weight, position, speed)

    def fire_engine(self, engine_force_vector: Vector):
        self.force += engine_force_vector

    def make_decision(self, delta_time: float):
        pass


class VerticalTakeOffRocket(BaseRocket):
    def __init__(self, weight, position: Point, speed: Vector, planet: Planet, target_height: float=250000, target_acceleration=9.8 * 1, engine_firing_height: float=90000):
        super().__init__(weight, position, speed)
        self.planet = planet
        # maximum height, that the rocket should reach
        self.target_height = target_height
        # acceleration value, that the rocket should maintain while climbing
        self.target_acceleration_value = target_acceleration
        self.phase = self.phase_take_off
        # height, at which the rocket should start deceleration while descending
        self.engine_firing_height = engine_firing_height
        self.deceleration_value = None

    def get_height(self):
        return Physics.calculate_distance(self.position, self.planet.position) - self.planet.radius

    def should_stop_ascending(self):
        current_kinetic_energy = self.weight * self.speed.magnitude ** 2 / 2
        k = Physics.G * self.planet.weight * self.weight
        current_height = self.get_height()
        potential_energy = -1 * k / (self.planet.radius + self.target_height) - -1 * k / (self.planet.radius + current_height)
        if potential_energy < current_kinetic_energy:
            return True
        return False
    
    def phase_take_off(self, delta_time:float=0):
        if not self.should_stop_ascending():
            gravity_force_vector = Physics.calculate_gravity(self, self.planet)
            normalized_target_acceleration_vector = Vector(self.planet.position, self.position).normalize()
            thrust_vector = normalized_target_acceleration_vector * self.weight * self.target_acceleration_value - gravity_force_vector
            self.fire_engine(thrust_vector)
        else:
            self.phase = self.phase_wait

    def phase_wait(self, delta_time:float=0):
        if self.get_height() < self.engine_firing_height:
            self.phase = self.phase_land

    def phase_land(self, delta_time: float):
        gravity_force_vector = Physics.calculate_gravity(self, self.planet)
        if self.deceleration_value is None:
            self.deceleration_value = self.speed.magnitude ** 2 / (2 * self.get_height())

        thrust_value = self.weight * self.deceleration_value + gravity_force_vector.magnitude
        thrust_vector = Vector(self.planet.position, self.position).normalize() * thrust_value

        # calculate presumable speed considering engine thrust after the next simulation speed
        new_force = gravity_force_vector + thrust_vector
        new_acceleration = new_force / self.weight
        new_position = self.position + self.speed * delta_time + new_acceleration * delta_time ** 2 / 2
        new_absolute_height = Physics.calculate_distance(new_position, self.planet.position)
        current_absolute_height = Physics.calculate_distance(self.position, self.planet.position)
        if new_absolute_height > current_absolute_height:
            self.phase = None
        self.fire_engine(thrust_vector)

    def make_decision(self, delta_time: float):
        # 1. Take off while maintaining certain acceleration
        # 2. Turn off engines, wait to fly to the desired height
        # 3. Once reached the pre-determined height, activate deceleration engines
        self.phase(delta_time)
