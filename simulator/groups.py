from pygame.sprite import Group, Sprite

from physics import Vector, Physics
from simobjects import SimRocketObject, SimPlanetaryObject


class PhysicsGroup(Group):
    def __init__(self, *sprites: Sprite):
        super().__init__(*sprites)

    def update(self, delta_time: float):
        entities = [sprite.entity for sprite in self.sprites()]
        for entity in entities:
            entity.force = Vector((0, 0))


class GravityGroup(PhysicsGroup):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def update(self, delta_time: float):
        entities = [sprite.entity for sprite in self.sprites()]
        for i, entity in enumerate(entities):
            for other_entity in entities[i + 1:]:
                Physics.apply_gravity(entity, other_entity)


class MoveGroup(PhysicsGroup):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def update(self, delta_time: float):
        entities = [sprite.entity for sprite in self.sprites()]
        for entity in entities:
            Physics.move(entity, delta_time)


class SmartGroup(PhysicsGroup):
    def __init__(self, *sprites: SimRocketObject):
        super().__init__(*sprites)

    def update(self, delta_time: float):
        rockets = [sprite.entity for sprite in self.sprites()]
        for rocket in rockets:
            rocket.make_decision()


class CollisionGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def update(self, delta_time: float):
        rockets = [sprite for sprite in self.sprites() if isinstance(sprite, SimRocketObject)]
        planets = [sprite for sprite in self.sprites() if isinstance(sprite, SimPlanetaryObject)]

        for rocket in rockets:
            for planet in planets:
                diff = Vector(planet.entity.position, rocket.entity.position)
                if diff.magnitude < planet.entity.radius:
                    rocket.kill()


class RenderGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def render(self, screen, scale: float, offset: Vector):
        for entity in self.sprites():
            entity.draw(screen, scale, offset)
