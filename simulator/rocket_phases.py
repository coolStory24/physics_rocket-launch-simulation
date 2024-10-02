import math

from entities import Planet, BaseRocket, Orbit, RocketPhase, PhaseControlledRocket
from physics import Physics, Vector, Point, Entity
from events import EventRegistrer, PrintTotalSimTimeEvent, SetSimulationTimeScaleEvent


class RocketTakeoffPhase(RocketPhase):
    def __init__(self, target_height: float):
        self.target_height = target_height

    def make_decision(self, rocket: PhaseControlledRocket, delta_time: float):
        if Orbit.calculate_orbit(rocket.planet, rocket).apogee_height < self.target_height:
            thrust_direction = rocket.position_vector.normalize()
            thrust_vector = thrust_direction * rocket.weight * rocket.target_acceleration - rocket.gravity_to_planet
            rocket.fire_engine(thrust_vector, delta_time)
        else:
            rocket.end_phase()


class RocketRoundOrbitalManeuverPhase(RocketPhase):
    def __init__(self, target_height: float):
        super().__init__()
        self.target_height = target_height

    def make_decision(self, rocket: PhaseControlledRocket, delta_time):
        target_distance = rocket.planet.radius + self.target_height

        target_speed = math.sqrt(Physics.G * rocket.planet.weight / target_distance)

        delta_v_required = target_speed - rocket.relative_speed.magnitude

        delta_v_actual = min(delta_v_required, rocket.target_acceleration * delta_time)

        maneuver_speed_vector = Vector(rocket.planet.position, rocket.position).rotate(math.pi / 2).normalize()

        thrust_vector = maneuver_speed_vector * (rocket.weight * delta_v_actual / delta_time)

        if rocket.height < self.target_height:
            gravity_vector = Physics.calculate_gravity(rocket.planet, rocket)
            thrust_vector += gravity_vector * (rocket.weight - (thrust_vector + gravity_vector).magnitude * delta_time / rocket.fuel_speed) / rocket.weight

        rocket.fire_engine(thrust_vector, delta_time)

        if delta_v_required <= delta_v_actual:
            rocket.end_phase()


class RocketOrbitalManeuverPhase(RocketPhase):
    def __init__(self, target_orbit: Orbit):
        super().__init__()
        self.target_orbit = target_orbit
        self.maneuver_angle = target_orbit.polar_angle

    def make_decision(self, rocket: PhaseControlledRocket, delta_time):
        target_perigee = self.target_orbit.perigee_distance
        target_apogee = self.target_orbit.semi_major_axis * 2 - target_perigee

        target_speed = math.sqrt(2 * Physics.G * rocket.planet.weight * target_apogee / (target_perigee * (target_perigee + target_apogee)))

        delta_v_required = target_speed - rocket.relative_speed.magnitude

        delta_v_actual = min(delta_v_required, rocket.target_acceleration * delta_time)

        thrust_vector = rocket.relative_speed.normalize() * (rocket.weight * delta_v_actual / delta_time)

        rocket.fire_engine(thrust_vector, delta_time)

        if delta_v_required <= delta_v_actual:
            rocket.end_phase()


class RocketLandPhase(RocketPhase):
    def make_decision(self, rocket: PhaseControlledRocket, delta_time):
        self.deceleration_value = rocket.takeoff_speed.magnitude ** 2 / (2 * rocket.height)

        thrust_value = rocket.weight * self.deceleration_value + rocket.gravity_to_planet.magnitude
        thrust_vector = rocket.position_vector.normalize() * thrust_value

        # calculate presumable speed considering engine thrust after the next simulation speed
        new_force = rocket.gravity_to_planet + thrust_vector
        new_acceleration = new_force / rocket.weight
        new_position = rocket.position + rocket.takeoff_speed * delta_time + new_acceleration * delta_time ** 2 / 2
        new_absolute_height = Physics.calculate_distance(new_position, rocket.planet.position)

        if new_absolute_height > rocket.absolute_height:
            rocket.end_phase()

        rocket.fire_engine(thrust_vector, delta_time)


class RocketOrbitCorrectPhase(RocketPhase):
    def __init__(self, orbit: Orbit):
        self.orbit = orbit

    def calculate_next_orbit(self, engine_force_vector: Vector, rocket, delta_time: float):
        new_force = rocket.gravity_to_planet + engine_force_vector
        new_weight = rocket.weight - engine_force_vector.magnitude * delta_time / rocket.fuel_speed
        new_acceleration = new_force / new_weight
        new_position = rocket.position + rocket.speed * delta_time + new_acceleration * delta_time ** 2 / 2
        new_speed = rocket.speed + new_acceleration * delta_time
        return Orbit.calculate_orbit(rocket.planet, Entity(new_weight, new_position, new_speed))

    def calculate_current_correction_maneuver_coefficient(self, rocket, delta_time: float, current_vector: Vector):
        current_orbit = Orbit.calculate_orbit(rocket.planet, rocket)
        current_distance = current_orbit.apogee_distance - current_orbit.perigee_distance
        left = -1
        right = 1
        coefficient = 0.5
        for i in range(11):
            new_orbit = self.calculate_next_orbit(current_vector * coefficient, rocket, delta_time)
            if new_orbit.apogee_distance - new_orbit.perigee_distance <= current_distance:
                left = coefficient
            else:
                right = coefficient
            coefficient = (left + right) / 2

        return coefficient

    def make_decision(self, rocket: PhaseControlledRocket, delta_time):
        correction_vector = -rocket.position_vector.normalize() * rocket.weight * rocket.target_acceleration
        coefficient = self.calculate_current_correction_maneuver_coefficient(rocket, delta_time, correction_vector)
        rocket.fire_engine(correction_vector * coefficient, delta_time)
        if coefficient < 0.001:
            rocket.end_phase()


class RocketWaitGreaterHeightPhase(RocketPhase):
    def __init__(self, target_height: float):
        self.target_height = target_height

    def make_decision(self, rocket: PhaseControlledRocket, delta_time):
        if rocket.height >= self.target_height:
            rocket.end_phase()


class RocketWaitLessHeightPhase(RocketPhase):
    def __init__(self, target_height: float):
        self.target_height = target_height

    def make_decision(self, rocket: PhaseControlledRocket, delta_time):
        if rocket.height <= self.target_height:
            rocket.end_phase()


class RocketWaitPolarAnglePhase(RocketPhase):
    def __init__(self, target_angle, epsilon):
        self.target_angle = target_angle
        self.epsilon = epsilon

    def make_decision(self, rocket: PhaseControlledRocket, delta_time):
        if abs(rocket.polar_angle - self.target_angle) < self.epsilon:
            rocket.end_phase()


class RocketWaitForPlanetAntiphasePhase(RocketPhase):
    def __init__(self,planet: Planet,  epsilon: float):
        self.epsilon = epsilon
        self.planet = planet

    def make_decision(self, rocket: PhaseControlledRocket, delta_time):
        if abs(Vector(self.planet.position, rocket.planet.position).polar_angle - Vector(rocket.planet.position, rocket.position).polar_angle) < self.epsilon:
            print(rocket.planet.speed.magnitude, rocket.speed.magnitude)
            rocket.planet = self.planet
            rocket.end_phase()
            print("Fly")

class RocketGravityCompensationPhase(RocketPhase):
    def __init__(self, earth: Planet, sun: Planet, mars: Planet):
        self.earth = earth
        self.sun = sun
        self.mars = mars

    def make_decision(self, rocket: PhaseControlledRocket, delta_time):
        print("waiting", Orbit.calculate_orbit(self.sun, rocket).apogee_distance - Physics.calculate_distance(self.sun.position, self.mars.position))
        rocket.fire_engine(Physics.calculate_gravity(self.earth, rocket) * 0.5, delta_time)


class RocketSolarManeuverPhase(RocketPhase):
    def __init__(self, earth: Planet, sun: Planet, target_orbit: Orbit):
        self.earth = earth
        self.sun = sun
        self.target_orbit = target_orbit

    def make_decision(self, rocket: PhaseControlledRocket, delta_time):
        target_perigee = self.target_orbit.perigee_distance
        target_apogee = self.target_orbit.semi_major_axis * 2 - target_perigee

        target_speed = math.sqrt(2 * Physics.G * rocket.planet.weight * target_apogee / (target_perigee * (target_perigee + target_apogee)))
        # target_speed = math.sqrt(2 * Physics.G * self.target_orbit.planet.weight * target_apogee / (target_perigee * (target_perigee + target_apogee)))

        delta_v_required = target_speed - rocket.relative_speed.magnitude

        delta_v_actual = min(delta_v_required, rocket.target_acceleration * delta_time)

        thrust_vector = rocket.relative_speed.normalize() * (rocket.weight * delta_v_actual / delta_time)
        thrust_vector += Physics.calculate_gravity(self.earth, rocket)

        rocket.fire_engine(thrust_vector, delta_time)

        if delta_v_required <= delta_v_actual:
            rocket.end_phase()


class RocketTestOrbitManeuverPhase(RocketPhase):
    def __init__(self, earth: Planet, sun: Planet, mars: Planet):
        self.earth = earth
        self.sun = sun
        self.mars = mars
        self.total_time = 0

    def make_decision(self, rocket: PhaseControlledRocket, delta_time):
        orbit = Orbit.calculate_orbit(self.sun, rocket)
        # print(orbit.apogee_distance - Physics.calculate_distance(self.sun.position, self.mars.position), Physics.calculate_distance(self.sun.position, rocket.position) - Physics.calculate_distance(self.mars.position, self.sun.position))
        distance = Physics.calculate_distance(self.sun.position, rocket.position) - Physics.calculate_distance(self.mars.position, self.sun.position)
        # print(Orbit.calculate_orbit(self.sun, self.mars).apogee_distance - Orbit.calculate_orbit(self.sun, self.mars).perigee_distance)
        if abs(distance) < 60_000_000:
            print("distance:", distance)
            EventRegistrer.register_event(PrintTotalSimTimeEvent())
            print("angle:", Vector(self.sun.position, rocket.position).polar_angle)
            print("\n")
            EventRegistrer.register_event(SetSimulationTimeScaleEvent(10))
            rocket.planet = self.mars
            rocket.end_phase()

        sun_rocket_vector = Vector(self.sun.position, rocket.position).normalize()
        thrust_direction = Vector((sun_rocket_vector.y, -sun_rocket_vector.x)).normalize()
        # thrust_direction = rocket.speed.normalize()
        self.total_time += delta_time
        if self.total_time >= 0.3 * 10 ** 7:
            return
        thrust_vector = Physics.calculate_gravity(self.earth, rocket) * 0.093
        if orbit.apogee_distance <= Physics.calculate_distance(self.sun.position, self.mars.position):
            thrust_vector += thrust_direction * (rocket.weight * rocket.target_acceleration) * 0.5

        rocket.fire_engine(thrust_vector, delta_time)


class RocketOrbitalBreakPhase(RocketPhase):
    def __init__(self):
        pass

    def make_decision(self, rocket: PhaseControlledRocket, delta_time: float):
        try:
            orbit = Orbit.calculate_orbit(rocket.planet, rocket)
            print("Done! eccentricity: ", orbit.eccentricity)
        except ValueError:
            print("Stop!")
            thrust_direction = -rocket.relative_speed.normalize()
            thrust_vector = thrust_direction * rocket.weight * rocket.target_acceleration
            rocket.fire_engine(thrust_vector, delta_time)
