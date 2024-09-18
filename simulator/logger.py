import events


class Logger(events.EventSubscriber):
    def __init__(self):
        super().__init__()
        self.subscribe(events.Event)


class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__()

    def handle_event(self, event):
        print(event)
