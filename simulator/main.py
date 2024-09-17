import pygame

from entities import Planet, BaseRocket
from physics import Vector, Point
from groups import GravityGroup, MoveGroup, CollisionGroup, SmartGroup
from simobjects import SimPlanetaryObject, SimRocketObject
from simulation import Simulation

if __name__ == '__main__':
    earth = Planet(5.972E24, Point((0, 0)), Vector((0, 0)), 6371E3)
    moon = Planet(7.346E22, Point((384E6, 0)), Vector((0.0, 1.022E3)), 1737E3)
    rocket = BaseRocket(100, Point((7.371E6, 0)), Vector((0.0, 4.35E3)))

    earth_sprite = SimPlanetaryObject(earth, pygame.Color("deepskyblue"))
    moon_sprite = SimPlanetaryObject(moon, pygame.Color("white"))
    rocket_sprite = SimRocketObject(rocket)

    simulation = Simulation(groups=(
        GravityGroup(earth_sprite, moon_sprite, rocket_sprite),
        SmartGroup(rocket_sprite),
        CollisionGroup(earth_sprite, moon_sprite, rocket_sprite),
        MoveGroup(earth_sprite, moon_sprite, rocket_sprite),
    ))
    simulation.run()
