import math

from physics import Entity, Point, Vector, Physics


class Planet(Entity):
    def __init__(self, weight: float, position: Point, speed: Vector, radius: float, angle_speed: float):
        super().__init__(weight, position, speed)
        self.radius = radius
        self.polar_angle = 0
        self.angle_speed = angle_speed

    def surface_speed(self, polar_angle: float):
        return Vector.make_vector_by_polar_angle(polar_angle + math.pi / 2, 2 * math.pi * self.angle_speed * self.radius)


class BaseRocket(Entity):
    def __init__(self, weight, payload_weight, planet: Planet, polar_angle: float, fuel_speed: float):
        position = planet.position + Vector.make_vector_by_polar_angle(polar_angle, planet.radius + 1)
        speed = planet.surface_speed(polar_angle) + planet.speed
        super().__init__(weight, position, speed)
        self.payload_weight = payload_weight
        self.fuel_speed = fuel_speed

    def fire_engine(self, engine_force_vector: Vector, delta_time: float):
        next_weight = self.weight - engine_force_vector.magnitude * delta_time / self.fuel_speed
        if next_weight >= self.payload_weight:
            self.force += engine_force_vector
            self.weight = next_weight

    def make_decision(self, delta_time: float):
        pass
