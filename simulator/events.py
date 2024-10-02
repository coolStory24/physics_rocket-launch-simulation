from physics import Vector, Point


class Subscription:
    def __init__(self, subscriber, event_type):
        self.subscriber = subscriber
        self.event_type = event_type


class EventRegistrer:
    subscriptions = []
    events = []

    @staticmethod
    def register_event(event):
        for subscription in EventRegistrer.subscriptions:
            if isinstance(event, subscription.event_type):
                subscription.subscriber.handle_event(event)

        if event.store:
            EventRegistrer.events.append(event)

    @staticmethod
    def subscribe(subscriber, *event_types):
        EventRegistrer.subscriptions += [Subscription(subscriber, e) for e in event_types]

        for event_type in event_types:
            for event in EventRegistrer.events:
                if isinstance(event, event_type):
                    subscriber.handle_event(event)


class EventSubscriber:
    def subscribe(self, *event_types):
        EventRegistrer.subscribe(self, *event_types)

    def handle_event(self, event):
        raise NotImplementedError()


class Event:
    def __init__(self, store: bool=True):
        self.store = store


class LogableEvent(Event):
    def __init__(self, store: bool=True):
        super().__init__(store)

    def __str__(self):
        return "Event with unimplemented to_string()"


class CollisionEvent(LogableEvent):
    def __init__(self, planet, rocket, collision_angle, finite_speed):
        super().__init__()
        self.planet = planet
        self.rocket = rocket
        self.collision_angle = collision_angle
        self.finite_speed = finite_speed

    def __str__(self):
        return f"{self.rocket.name} has fallen on {self.planet.name} at {self.collision_angle:.3f} with speed {self.finite_speed:.3f} m/s"

class RocketEvent(Event):
    def __init__(self, time, speed: Vector, position: Point, planet_position: Point):
        super().__init__(store=False)
        self.time = time
        self.speed = speed
        self.position = position
        self.planet_position = planet_position

class SimobjectOutOfFuelEvent(LogableEvent):
    def __init__(self, rocket):
        super().__init__()
        self.rocket = rocket

    def __str__(self):
        return f"{self.rocket.name} is out of fuel!"

class EntityOutOfFuelEvent(Event):
    def __init__(self, rocket):
        super().__init__(store=False)


class BuildPlotsEvent(Event):
    def __init__(self):
        super().__init__(False)

class PauseEvent(Event):
    def __init__(self, is_paused):
        super().__init__(False)
        self.is_paused = is_paused

class TimeScaleUpdateEvent(Event):
    def __init__(self, time_scale, amount_of_iterations):
        super().__init__(False)
        self.time_scale = time_scale
        self.amount_of_iterations = amount_of_iterations

class NoFuelForManeuverEvent(Event):
    def __init__(self, rocket):
        self.rocket = rocket

class FollowEvent(Event):
    def __init__(self):
        super().__init__(False)

class FollowEventCapture(FollowEvent):
    def __init__(self, sprite, screen_pos: Vector):
        super().__init__()
        self.captured_sprite = sprite
        self.screen_pos = screen_pos

class FollowEventUncapture(FollowEvent):
    def __init__(self):
        super().__init__()
