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
            if isinstance(event, (subscription.event_type)):
                subscription.subscriber.handle_event(event)
        EventRegistrer.events.append(event)

    @staticmethod
    def subscribe(subscriber, event_type):
        EventRegistrer.subscriptions.append(Subscription(subscriber, event_type))

        for event in EventRegistrer.events:
            if isinstance(event, event_type):
                subscriber.handle_event(event)


class EventSubscriber:
    def subscribe(self, event_type):
        EventRegistrer.subscribe(self, event_type)

    def handle_event(self, event):
        raise NotImplementedError()


class Event:
    def __init__(self, time: float):
        self.time = time

    def str_preffix(self):
        seconds = int(self.time % 60)
        minutes = int(self.time / 60 % 60)
        hours = int(self.time / 3600 % 24)
        days = int(self.time / 3600 / 24)
        return f"[{days}d {hours}h {minutes}m {seconds}s]: "

    def __str__(self):
        return "Event with unimplemented to_string()"


class CollisionEvent(Event):
    def __init__(self, time, planet, rocket, collision_angle, finite_speed):
        super().__init__(time)
        self.planet = planet
        self.rocket = rocket
        self.collision_angle = collision_angle
        self.finite_speed = finite_speed

    def __str__(self):
        return self.str_preffix() + f"{self.rocket.name} has fallen on {self.planet.name} at {self.collision_angle:.3f} with speed {self.finite_speed:.3f} m/s"
