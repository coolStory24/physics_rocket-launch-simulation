import math


class Vector:
    def __init__(self, *args):
        if len(args) == 1 and (isinstance(args[0], list) or isinstance(args[0], tuple)):
            self._coordinates = args[0][::]
        elif len(args) == 2 and all(isinstance(arg, Point) for arg in args):
            point1, point2 = args
            self._coordinates = [j - i for i, j in zip(point1.coordinates, point2.coordinates)]
        else:
            raise ValueError("Invalid number of arguments")

    def __neg__(self):
        return Vector([-i for i in self._coordinates])

    def __add__(self, other):
        return Vector([i + j for i, j in zip(self._coordinates, other.coordinates)])

    def __iadd__(self, other):
        self._coordinates = [i + j for i, j in zip(self._coordinates, other.coordinates)]
        return self

    def __sub__(self, other):
        return Vector([i - j for i, j in zip(self._coordinates, other.coordinates)])

    def __isub__(self, other):
        self._coordinates = [i - j for i, j in zip(self._coordinates, other.coordinates)]
        return self

    def __mul__(self, number: float):
        return Vector([i * number for i in self._coordinates])

    def __truediv__(self, number: float):
        return Vector([i / number for i in self._coordinates])

    def __getitem__(self, item: int):
        return self._coordinates[item]

    def __len__(self):
        return len(self.coordinates)

    def __repr__(self):
        return f"Vector({self._coordinates})"

    def copy(self):
        return Vector(self._coordinates)

    def cross_product(self, other):
        if len(other.coordinates) == 2 and len(self._coordinates) == 2:
            return self.coordinates[0] * other.coordinates[1] - self.coordinates[1] * other.coordinates[0]

    def rotate(self, angle: float):
        return Vector((self.x * math.cos(angle) - self.y * math.sin(angle), self.x * math.sin(angle) + self.y * math.cos(angle)))

    @property
    def coordinates(self):
        return tuple(self._coordinates)

    @property
    def x(self):
        return self._coordinates[0]

    @property
    def y(self):
        return self._coordinates[1]

    @property
    def magnitude(self):
        return math.sqrt(sum([i ** 2 for i in self._coordinates]))

    def normalize(self):
        magnitude = self.magnitude
        return Vector([i / magnitude for i in self._coordinates])

    @staticmethod
    def dot_product(v1, v2):
        return sum([i * j for i, j in zip(v1, v2)])

    @property
    def polar_angle(self):
        return math.atan2(self.y, self.x) % (math.pi * 2)

    @staticmethod
    def make_vector_by_polar_angle(polar_angle: float, magnitude: float):
        x = magnitude * math.cos(polar_angle)
        y = magnitude * math.sin(polar_angle)
        return Vector((x, y))


class Point:
    def __init__(self, coordinates):
        self._coordinates = coordinates

    def __getitem__(self, item):
        return self._coordinates[item]

    def __add__(self, vector: Vector):
        return Point([i + j for i, j in zip(self._coordinates, vector.coordinates)])

    def __sub__(self, vector: Vector):
        return Point([i - j for i, j in zip(self._coordinates, vector.coordinates)])

    @property
    def x(self):
        return self._coordinates[0]

    @property
    def y(self):
        return self._coordinates[1]

    @property
    def coordinates(self):
        return self._coordinates

    def __repr__(self):
        return f"Point({self.coordinates})"


class Entity:
    def __init__(self, weight: float, position: Point, speed: Vector, force: Vector=Vector((0, 0))):
        self.position = position
        self.speed = speed
        self.weight = weight
        self.force = force


class Physics:
    G = 6.67430e-11

    @staticmethod
    def calculate_distance(point1: Point, point2: Point):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    @staticmethod
    def calculate_gravity(body1: Entity, body2: Entity):
        weight1 = body1.weight
        weight2 = body2.weight
        distance = Physics.calculate_distance(body1.position, body2.position)
        gravity_force = Physics.G * weight1 * weight2 / distance ** 2
        force_vector = Vector(body1.position, body2.position).normalize() * gravity_force
        return force_vector

    @staticmethod
    def apply_gravity(body1: Entity, body2: Entity):
        force_vector = Physics.calculate_gravity(body1, body2)
        body1.force += force_vector
        body2.force -= force_vector

    @staticmethod
    def move(body: Entity, delta_time: float):
        acceleration = body.force / body.weight
        body.position = body.position + body.speed * delta_time + acceleration * delta_time ** 2 / 2
        body.speed += acceleration * delta_time
