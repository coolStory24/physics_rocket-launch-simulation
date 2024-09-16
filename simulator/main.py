import pygame

from entities import Planet
from groups import GravityGroup, MoveGroup
from physics import Vector, Point
from simulation import Simulation
from simobjects import SimPlanetaryObject
from entities import BaseRocket
from simobjects import SimRocketObject
from groups import SmartGroup

if __name__ == '__main__':
    earth = Planet(5.972E24, Point((0, 0)), Vector((0, 0)), 6371E3)
    moon = Planet(7.346E22, Point((384E6, 0)), Vector((0.0, 1.022E3)), 1737E3)
    rocket = BaseRocket(100, Point((7.371E6, 0)), Vector((0.0, 7.35E3)))

    earth_sprite = SimPlanetaryObject(earth, pygame.Color("deepskyblue"))
    moon_sprite = SimPlanetaryObject(moon, pygame.Color("white"))
    rocket_sprite = SimRocketObject(rocket)

    simulation = Simulation(groups=(
        GravityGroup(earth_sprite, moon_sprite, rocket_sprite),
        SmartGroup(rocket_sprite),
        MoveGroup(earth_sprite, moon_sprite, rocket_sprite),
    ))
    simulation.run()
