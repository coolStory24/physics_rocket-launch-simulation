import sys

import pygame

from simulator.groups import RenderGroup, PhysicsGroup


class Simulation:
    def __init__(self, dimensions=(1280, 720), pixels_per_meter: float=1e-5, time_scale: float=1, groups=()):
        self.width, self.height = dimensions
        self.main_window = None
        self.pixels_per_meter = pixels_per_meter
        self.time_scale = time_scale

        self.objects = {sprite for group in groups for sprite in group}

        self.groups = [PhysicsGroup(*self.objects)] + list(groups[::])
        self.render_group = RenderGroup(*self.objects)

    def handle_event(self, event):
        pass

    def run(self):
        pygame.init()
        self.main_window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Rocket Simulator')
        delta_time = 0.016
        clock = pygame.time.Clock()
        paused = False

        while not paused:
            self.main_window.fill(pygame.Color("black"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.handle_event(event)

            for group in self.groups:
                group.update(delta_time * self.time_scale)
            self.render_group.render(self.main_window, self.pixels_per_meter)

            pygame.display.flip()
            delta_time = clock.tick(60) / 1000
