import math

from physics import Entity, Point, Vector, Physics


class Planet(Entity):
    def __init__(self, weight: float, position: Point, speed: Vector, radius: float, angle_speed: float):
        super().__init__(weight, position, speed)
        self.radius = radius
        self.polar_angle = 0
        self.angle_speed = angle_speed

    def surface_speed(self, polar_angle: float):
        return Vector.make_vector_by_polar_angle(polar_angle + math.pi / 2, self.angle_speed * self.radius)


class BaseRocket(Entity):
    def __init__(self, weight: float, payload_weight: float, planet: Planet, polar_angle: float, fuel_speed: float):
        position = planet.position + Vector.make_vector_by_polar_angle(polar_angle, planet.radius + 1)
        speed = planet.surface_speed(polar_angle) + planet.speed
        super().__init__(weight, position, speed)
        self.planet = planet
        self.payload_weight = payload_weight
        self.fuel_speed = fuel_speed

    def fire_engine(self, engine_force_vector: Vector, delta_time: float):
        next_weight = self.weight - engine_force_vector.magnitude * delta_time / self.fuel_speed
        if next_weight >= self.payload_weight:
            self.force += engine_force_vector
            self.weight = next_weight
        else:
            print("FUEL!!!")

    def make_decision(self, delta_time: float):
        pass


class Orbit:
    def __init__(self, planet: Planet, perigee_height: float, eccentricity: float, polar_angle: float):
        self.planet = planet
        self.perigee_height = perigee_height
        self.eccentricity = eccentricity
        self.polar_angle = polar_angle
        self.perigee_distance = planet.radius + perigee_height
        self.semi_major_axis = self.perigee_distance / (1 - eccentricity)
        self.semi_minor_axis = self.semi_major_axis * math.sqrt(1 - eccentricity ** 2)
        self.apogee_distance = self.semi_major_axis * 2 - self.perigee_distance
        self.apogee_height = self.apogee_distance - self.planet.radius

    @staticmethod
    def calculate_orbit(planet: Planet, entity: Entity):
        # Gravitational parameter μ = G * planet_mass
        mu = Physics.G * planet.weight

        # Distance between the planet and the entity
        r = Vector(planet.position, entity.position)

        v = entity.speed.magnitude

        # Specific orbital energy
        epsilon = (v ** 2) / 2 - (mu / r.magnitude)

        # Semi-major axis
        semi_major_axis = -mu / (2 * epsilon)

        # Angular momentum vector h = r x v
        angular_momentum = r.cross_product(entity.speed)
        h = angular_momentum

        # Eccentricity vector
        eccentricity_vector = (entity.speed * (angular_momentum / mu)) - (r / r.magnitude)

        # Eccentricity e
        eccentricity = math.sqrt(1 + (2 * epsilon * h ** 2) / mu ** 2)

        # Perigee distance
        perigee_distance = semi_major_axis * (1 - eccentricity)
        perigee_height = perigee_distance - planet.radius

        polar_angle = math.atan2(eccentricity_vector.y, eccentricity_vector.x)

        return Orbit(planet, perigee_height, eccentricity, polar_angle)
