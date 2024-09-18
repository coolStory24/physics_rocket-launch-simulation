import matplotlib.pyplot as plt

import events
from simulator.events import RocketEvent, EventSubscriber


class Logger(events.EventSubscriber):
    def __init__(self):
        super().__init__()
        self.subscribe(events.LogableEvent)


class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__()

    def handle_event(self, event):
        print(event)

class RocketLogger(EventSubscriber):
    def __init__(self):
        super().__init__()
        self.subscribe(events.RocketEvent)
        self.subscribe(events.CollisionEvent)
        self.data = []

    def handle_event(self, event):
        if isinstance(event, events.RocketEvent):
            self.data.append(event)
        elif isinstance(event, events.CollisionEvent):
            print(event.rocket, event.planet, event.str_prefix())
            self.build_graph()

    def build_graph(self):
        print([e.speed.magnitude for e in self.data][-5:])
        plt.plot([e.time for e in self.data], [e.speed.magnitude for e in self.data])
        plt.xlabel('Time')
        plt.ylabel('Speed')
        plt.title('Speed vs Time')
        plt.show()