import pygame
import math

import config
from arguments import configure
from entities import Planet, Orbit
from physics import Vector, Point
from groups import create_physics_groups
from simobjects import SimPlanetaryObject, SimRocketObject
from simulation import Simulation
from logger import RocketTracker
from entities import PhaseControlledRocket
from events import GravityTrackingEvent
from rocket_phases import RocketTestOrbitManeuverPhase, RocketOrbitalBreakPhase, RocketTakeoffPhase, RocketPrintHeightPhase
from rocket_phases import RocketRoundOrbitalManeuverPhase, RocketOrbitCorrectPhase, SetTimeScalePhase
from rocket_phases import RocketWaitGreaterHeightPhase, RocketWaitPolarAnglePhase, RocketOrbitalManeuverPhase, RocketPrelandSlowingPhase, RocketWaitLessHeightPhase, RocketLandPhase
from widgets import LoggerWidget, ClockWidget, TimeScaleWidget, CaptureWidget

if __name__ == '__main__':
    configure()

    earth = Planet(5.972E24, Point((0, 0)), Vector((0, -29780)), 6371E3, -math.pi / 12 / 60 / 60)
    moon = Planet(7.346E22, Point((earth.position.x + 384E6, 0)), Vector((0.0, earth.speed.y -1.022E3)), 1737E3, 0)
    sun = Planet(1.989E30, Point((-1.496E11, 0)), Vector((0, 0)), 696340E3, 0)
    mars = Planet(6.39E23, Point((149293154749.65826 + sun.position.x, -172191648882.55933)), Vector((-18235.423356392195, -15810.429244034829)), 3389E3, 0)

    earth_sprite = SimPlanetaryObject(earth, pygame.Color("deepskyblue"), name="Earth")
    moon_sprite = SimPlanetaryObject(moon, pygame.Color("white"), name="Moon")
    sun_sprite = SimPlanetaryObject(sun, pygame.Color("yellow"), name="Sun")
    mars_sprite = SimPlanetaryObject(mars, pygame.Color("red3"), name="Mars")

    target_height = 50_000_000

    phases = [
        RocketTakeoffPhase(300000),
        RocketWaitGreaterHeightPhase(300000),
        RocketRoundOrbitalManeuverPhase(300000),
        RocketOrbitCorrectPhase(Orbit(earth, 300000, 0, 0)),
        RocketWaitPolarAnglePhase(math.pi, 0.017),
        RocketOrbitalManeuverPhase(Orbit.with_apogee(earth, 300000 + earth.radius, target_height + earth.radius, math.pi)),
        RocketWaitGreaterHeightPhase(target_height),
        RocketRoundOrbitalManeuverPhase(target_height),
        RocketWaitGreaterHeightPhase(target_height),
        SetTimeScalePhase(1000),
        RocketTestOrbitManeuverPhase(earth, sun, mars),
        SetTimeScalePhase(100),
        RocketOrbitalBreakPhase(),
        RocketPrelandSlowingPhase(1 - 1E-4, 1_000_000_000),
        RocketWaitLessHeightPhase(100_000_000),
        SetTimeScalePhase(10),
        RocketPrelandSlowingPhase(1 - 1E-7, 30_000_000),
        RocketWaitLessHeightPhase(20_000_000),
        RocketLandPhase(),
    ]

    rocket = PhaseControlledRocket(9E6, 200, earth, 0, phases, fuel_speed=8000)
    rocket_sprite = SimRocketObject(rocket, name="Rocket")

    # Building graphs
    if config.BUILD_GRAPHICS:
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
        clickable=(earth_sprite, rocket_sprite, mars_sprite, sun_sprite, moon_sprite),
    )
    simulation.run()
