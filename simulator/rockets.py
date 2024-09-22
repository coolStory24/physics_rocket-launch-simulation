from entities import Planet, BaseRocket
from physics import Physics, Vector, Point, Entity


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
        return normalized_target_acceleration_vector * Vector.scalar_mul(normalized_target_acceleration_vector, self.speed - self.planet.speed)

    def get_height(self):
        return Physics.calculate_distance(self.position, self.planet.position) - self.planet.radius

    def should_stop_ascending(self):
        current_kinetic_energy = self.weight * self.takeoff_speed.magnitude ** 2 / 2
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
