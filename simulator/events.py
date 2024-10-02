from physics import Vector, Point, Physics
from entities import BaseRocket


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
    def __init__(self, time: float, store: bool=True):
        self.time = time
        self.store = store


class LogableEvent(Event):
    def __init__(self, time: float, store: bool=True):
        super().__init__(time, store)

    def __str__(self):
        return "Event with unimplemented to_string()"

    def str_prefix(self):
        seconds = int(self.time % 60)
        minutes = int(self.time / 60 % 60)
        hours = int(self.time / 3600 % 24)
        days = int(self.time / 3600 / 24)
        return f"[{days}d {hours}h {minutes}m {seconds}s]: "


class CollisionEvent(LogableEvent):
    def __init__(self, time, planet, rocket, collision_angle, finite_speed):
        super().__init__(time)
        self.planet = planet
        self.rocket = rocket
        self.collision_angle = collision_angle
        self.finite_speed = finite_speed

    def __str__(self):
        return self.str_prefix() + f"{self.rocket.name} has fallen on {self.planet.name} at {self.collision_angle:.3f} with speed {self.finite_speed:.3f} m/s"

class RocketEvent(Event):
    def __init__(self, time, speed: Vector, position: Point, planet_position: Point):
        super().__init__(time, store=False)
        self.speed = speed
        self.position = position
        self.planet_position = planet_position


class GravityTrackingEvent(Event):
    sun = None
    earth = None
    def __init__(self, time, rocket: BaseRocket):
        super().__init__(time)
        self.rocket = rocket
        self.sun_position = GravityTrackingEvent.sun.position
        self.earth_position = GravityTrackingEvent.earth.position
        self.sun_gravity = Physics.calculate_gravity(GravityTrackingEvent.sun, rocket).magnitude
        self.earth_gravity = Physics.calculate_gravity(GravityTrackingEvent.earth, rocket).magnitude


class BuildPlotsEvent(Event):
    def __init__(self):
        super().__init__(0, False)

class PauseEvent(Event):
    def __init__(self, is_paused):
        super().__init__(0, False)
        self.is_paused = is_paused

class TimeScaleUpdateEvent(Event):
    def __init__(self, time_scale, amount_of_iterations):
        super().__init__(0, False)
        self.time_scale = time_scale
        self.amount_of_iterations = amount_of_iterations

class FollowEvent(Event):
    def __init__(self):
        super().__init__(0, False)

class FollowEventCapture(FollowEvent):
    def __init__(self, sprite, screen_pos: Vector):
        super().__init__()
        self.captured_sprite = sprite
        self.screen_pos = screen_pos

class FollowEventUncapture(FollowEvent):
    def __init__(self):
        super().__init__()


class PrintTotalSimTimeEvent(Event):
    def __init__(self):
        super().__init__(0, False)


class SetSimulationTimeScaleEvent(Event):
    def __init__(self, time_scale: float):
        super().__init__(0, False)
        self.time_scale = time_scale
