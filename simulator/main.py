import pygame

from entities import Planet
from groups import GravityGroup, MoveGroup
from physics import Vector, Point
from simulation import Simulation
from simobjects import SimPlanetaryObject
from entities import ProgrammableRocket
from simobjects import SimRocketObject
from groups import SmartGroup

if __name__ == '__main__':
    earth = Planet(5.972E24, Point((0, 0)), Vector((0, 0)), 6371E3)
    moon = Planet(7.346E22, Point((0, 384E6)), Vector((1.022E3, 0)), 1737E3)
    rocket = ProgrammableRocket(
        2.965E6, Point((6371E3, 0)), Vector((0.0, 463.3)),
        [
            ProgrammableRocket.Instruction(Vector((7E7, 0)), 3E2),
            ProgrammableRocket.Instruction(Vector((0, 2E9)), 1)
        ]
    )

    earth_sprite = SimPlanetaryObject(earth, pygame.Color("deepskyblue"))
    moon_sprite = SimPlanetaryObject(moon, pygame.Color("white"))
    rocket_sprite = SimRocketObject(rocket)

    simulation = Simulation(groups=(
        GravityGroup(earth_sprite, moon_sprite, rocket_sprite),
        SmartGroup(rocket_sprite),
        MoveGroup(earth_sprite, moon_sprite, rocket_sprite),
    ), time_scale=600)
    simulation.run()
