from pygame.sprite import Group, Sprite

from physics import Vector, Physics


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


class RenderGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def render(self, screen, scale: float, offset: Vector):
        for entity in self.sprites():
            entity.draw(screen, scale, offset)
