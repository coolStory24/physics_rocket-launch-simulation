import pygame
import math

import config
from arguments import configure
from entities import Planet, PhaseControlledRocket, Orbit
from physics import Vector, Point, Physics
from groups import create_physics_groups
from simobjects import SimPlanetaryObject, SimRocketObject
from simulation import Simulation
from logger import RocketTracker
from rocket_phases import RocketTakeoffPhase, RocketWaitGreaterHeightPhase, RocketRoundOrbitalManeuverPhase, \
    RocketOrbitCorrectPhase
from entities import OrbitInitRocket
from rocket_phases import RocketWaitForPlanetAntiphasePhase, RocketOrbitalManeuverPhase, RocketGravityCompensationPhase
from events import GravityTrackingEvent
from rocket_phases import RocketSolarManeuverPhase, RocketTestOrbitManeuverPhase, RocketOrbitalBreakPhase
from widgets import LoggerWidget, ClockWidget, TimeScaleWidget, CaptureWidget

if __name__ == '__main__':
    configure()

    earth = Planet(5.972E24, Point((0, 0)), Vector((0, -29780)), 6371E3, math.pi / 12 / 60 / 60)
    moon = Planet(7.346E22, Point((earth.position.x + 384E6, 0)), Vector((0.0, earth.speed.y -1.022E3)), 1737E3, 0)
    sun = Planet(1.989E30, Point((-1.496E11, 0)), Vector((0, 0)), 696340E3, 0)
    # mars = Planet(6.39E23, Point((0.783E11, 0)), Vector((0, -24135.043771816236)), 3389E3, math.pi / 24.62 / 2 / 60 / 60)
    mars = Planet(6.39E23, Point((-203238809218.32413 + sun.position.x, -103113512342.06726 + sun.position.y)), Vector((-21523.3767293377, 10919.917217382656)), 3389E3, math.pi / 24.62 / 2 / 60 / 60)

    earth_sprite = SimPlanetaryObject(earth, pygame.Color("deepskyblue"), name="Earth")
    moon_sprite = SimPlanetaryObject(moon, pygame.Color("white"), name="Moon")
    sun_sprite = SimPlanetaryObject(sun, pygame.Color("yellow"), name="Sun")
    mars_sprite = SimPlanetaryObject(mars, pygame.Color("red3"), name="Mars")

    target_height = 50_000_000

    phases = [
        # RocketTakeoffPhase(target_height),
        # RocketWaitGreaterHeightPhase(target_height),
        # RocketRoundOrbitalManeuverPhase(target_height),
        RocketWaitForPlanetAntiphasePhase(sun, 0.017),
        # RocketRoundOrbitalManeuverPhase(Physics.calculate_distance(sun.position, earth.position) + earth.radius + target_height - sun.radius),
        # RocketOrbitalManeuverPhase(Orbit(sun, Physics.calculate_distance(sun.position, earth.position), 0.209, 0))
        # RocketBreakFromPlanetPhase(sun),
        # RocketTransferToMarsPhase(Physics.calculate_distance(sun.position, mars.position), sun)
        # RocketRoundOrbitalManeuverPhase(Physics.calculate_distance(sun.position, earth.position)),
        # RocketSolarManeuverPhase(earth, sun, Orbit(sun, Physics.calculate_distance(sun.position, earth.position), 0.209, 0)),
        RocketTestOrbitManeuverPhase(earth, sun, mars),
        # RocketGravityCompensationPhase(earth, sun, mars)
        RocketOrbitalBreakPhase()
    ]

    # rocket = PhaseControlledRocket(2E5, 200, earth, 0, phases)
    rocket = OrbitInitRocket(9E6, 200, earth, Point((0, earth.radius + target_height)), earth.speed + Vector((2659.10, 0)), phases, fuel_speed=8000)
    rocket_sprite = SimRocketObject(rocket, name="Rocket")

    # Building graphs
    rocket_tracker = RocketTracker()

    GravityTrackingEvent.sun = sun
    GravityTrackingEvent.earth = earth

    logger_widget = LoggerWidget()
    clock_widget = ClockWidget()
    time_scale_widget = TimeScaleWidget(False, config.TIME_SCALE, config.AMOUNT_OF_ITERATIONS)
    capture_widget = CaptureWidget(None)

    simulation = Simulation(
        time_scale=config.TIME_SCALE,
        amount_of_iterations=config.AMOUNT_OF_ITERATIONS,
        groups=create_physics_groups(earth_sprite, moon_sprite, sun_sprite, mars_sprite, rocket_sprite),
        widgets=(logger_widget, clock_widget, time_scale_widget, capture_widget),
        clickable=(earth_sprite, rocket_sprite)
    )
    simulation.run()
