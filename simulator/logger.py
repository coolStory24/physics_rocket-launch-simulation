import matplotlib.pyplot as plt

import events
import config
from events import EventSubscriber
from physics import Physics


class Logger(events.EventSubscriber):
    def __init__(self):
        super().__init__()
        self.subscribe(events.LogableEvent)


class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__()

    def handle_event(self, event):
        print(event)

class RocketTracker(EventSubscriber):
    def __init__(self):
        super().__init__()
        self.subscribe(events.RocketEvent)
        self.subscribe(events.CollisionEvent)
        self.subscribe(events.BuildPlotsEvent)
        self.data = []

    def handle_event(self, event):
        if isinstance(event, events.RocketEvent):
            self.data.append(event)
        elif isinstance(event, events.CollisionEvent) and config.BUILD_GRAPHICS or isinstance(event, events.BuildPlotsEvent):
            self.build_plot()

    def build_plot(self):
        self.build_speed_plot()
        self.build_height_plot()
        self.build_acceleration_plot()
        self.build_position_plot()

    def build_speed_plot(self):
        plt.plot([e.time for e in self.data], [e.speed.magnitude for e in self.data])
        plt.xlabel('Time')
        plt.ylabel('Speed')
        plt.title('Speed vs Time')
        plt.show()

    def build_height_plot(self):
        plt.plot([e.time for e in self.data], [Physics.calculate_distance(e.position, e.planet_position) for e in self.data])
        plt.xlabel('Time')
        plt.ylabel('Height')
        plt.title('Height vs Time')
        plt.show()

    def build_acceleration_plot(self):
        plt.plot([e.time for e in self.data[1:]], [(self.data[i].speed - self.data[i - 1].speed).magnitude / (self.data[i].time - self.data[i - 1].time) for i in range(1, len(self.data))])
        plt.xlabel('Time')
        plt.ylabel('Acceleration')
        plt.title('Acceleration vs Time')
        plt.show()

    def build_position_plot(self):
        plt.plot([e.position.x for e in self.data], [e.position.y for e in self.data])
        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Rocket trajectory')
        plt.show()
