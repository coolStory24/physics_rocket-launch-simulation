import pygame

from entities import Planet, SimPlanetaryObject
from groups import GravityGroup, MoveGroup
from physics import Vector, Point
from simulation import Simulation

if __name__ == '__main__':
    earth = Planet(5.972E24, Point((0, 0)), Vector((0, 0)), 6371e3)
    earth_sprite = SimPlanetaryObject(earth, (640, 360), pygame.Color("deepskyblue"))
    simulation = Simulation(groups=(
        GravityGroup(earth_sprite),
        MoveGroup(earth_sprite),
    ))
    simulation.run()
