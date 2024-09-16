from physics import Entity, Point, Vector


class Planet(Entity):
    def __init__(self, weight: float, position: Point, speed: Vector, radius: float):
        super().__init__(weight, position, speed)
        self.radius = radius


class BaseRocket(Entity):
    def __init__(self, weight, position: Point, speed: Vector):
        super().__init__(weight, position, speed)

    def fire_engine(self, engine_force_vector: Vector):
        self.force += engine_force_vector

    def make_decision(self, delta_time: float):
        raise NotImplementedError()


class ProgrammableRocket(BaseRocket):
    class Instruction:
        def __init__(self, engine_force_vector: Vector, time_to_use: float):
            self.engine_force_vector = engine_force_vector
            self.time_to_use = time_to_use

    def __init__(self, weight, position: Point, speed: Vector, instructions: list):
        super().__init__(weight, position, speed)
        self.fly_time = 0
        self.active_instruction_use_time = 0
        self.active_instruction_index = 0
        self.instructions = instructions
        self.active_instruction = instructions[0]

    def make_decision(self, delta_time):
        self.fly_time += delta_time
        self.active_instruction_use_time += delta_time

        if self.active_instruction != None and self.active_instruction_use_time > self.active_instruction.time_to_use:
            self.active_instruction_use_time = 0
            self.active_instruction_index += 1
            if self.active_instruction_index < len(self.instructions):
                self.active_instruction = self.instructions[self.active_instruction_index]
            else:
                self.active_instruction = None

        if self.active_instruction != None:
            self.fire_engine(self.active_instruction.engine_force_vector)
