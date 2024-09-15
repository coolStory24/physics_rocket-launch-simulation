import pygame

from simulator.entities import Planet, SimPlanetaryObject
from simulator.physics import Vector, Point
from simulator.simulation import Simulation

if __name__ == '__main__':
    Earth = Planet(5.972E24, Point((0, 0)), Vector((0, 0)), 6371e3)
    EarthSprite = SimPlanetaryObject(Earth, (640, 360), pygame.Color("deepskyblue"))
    simulation = Simulation(planets=(EarthSprite, ))
    simulation.run()