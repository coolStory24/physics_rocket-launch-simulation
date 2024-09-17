from physics import Entity, Point, Vector


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

    def make_decision(self):
        pass
