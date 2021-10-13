class GlobalEvent:
    MSG_TYPE_SERIES = 1
    def __init__(self):
        self.observers = {}

    def add_observer(self,msg_type,observer):
        if msg_type in self.observers.keys():
            self.observers[msg_type].append(observer)
        else:
            self.observers[msg_type] = [observer]

    def notify(self,msg_type,data):
        if msg_type in self.observers.keys():
            for o in self.observers[msg_type]:
                o.handle_data(data)

g = GlobalEvent()
