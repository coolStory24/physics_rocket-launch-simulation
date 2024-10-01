import pygame
import math

import config
from arguments import configure
from entities import Planet, PhaseControlledRocket, Orbit
from physics import Vector, Point
from groups import create_physics_groups
from simobjects import SimPlanetaryObject, SimRocketObject
from simulation import Simulation
from logger import RocketTracker
from rocket_phases import RocketTakeoffPhase, RocketWaitGreaterHeightPhase, RocketRoundOrbitalManeuverPhase, RocketOrbitCorrectPhase
from widgets import LoggerWidget, TimeScaleWidget, ClockWidget, CaptureWidget

if __name__ == '__main__':
    configure()

    earth = Planet(5.972E24, Point((0, 0)), Vector((0, 0)), 6371E3, math.pi / 12 / 60 / 60)
    moon = Planet(7.346E22, Point((384E6, 0)), Vector((0.0, 1.022E3)), 1737E3, 0)

    target_height = 200_000

    phases = [
        RocketTakeoffPhase(target_height),
        RocketWaitGreaterHeightPhase(target_height),
        RocketRoundOrbitalManeuverPhase(target_height),
    ]

    rocket = PhaseControlledRocket(2E5, 200, earth, 0, phases)
    earth_sprite = SimPlanetaryObject(earth, pygame.Color("deepskyblue"), name="Earth")
    moon_sprite = SimPlanetaryObject(moon, pygame.Color("white"), name="Moon")
    rocket_sprite = SimRocketObject(rocket, name="Rocket")

    # Building graphs
    rocket_tracker = RocketTracker()

    logger_widget = LoggerWidget()
    clock_widget = ClockWidget()
    time_scale_widget = TimeScaleWidget(False, config.TIME_SCALE, config.AMOUNT_OF_ITERATIONS)
    capture_widget = CaptureWidget(None)

    simulation = Simulation(
        time_scale=config.TIME_SCALE,
        amount_of_iterations=config.AMOUNT_OF_ITERATIONS,
        groups=create_physics_groups(earth_sprite, moon_sprite, rocket_sprite),
        widgets=(logger_widget, clock_widget, time_scale_widget, capture_widget),
        clickable=(earth_sprite, moon_sprite, rocket_sprite)
    )
    simulation.run()
