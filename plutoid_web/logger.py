from fluent.sender import FluentSender

fluent_sender = None


def log(label, data):
    if fluent_sender: fluent_sender.emit(label, data)
    else: print(label, data)


def init_logger(prefix):
    global fluent_sender
    fluent_sender = FluentSender(prefix)
