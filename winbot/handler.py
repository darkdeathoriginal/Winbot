commands = {}
welcome = []
messages = []

def Module(object,callback):
    object['callback'] = callback
    commands[f"{object['name']}"] = object

def onJoin(object,callback):
    object['callback'] = callback
    welcome.append(object)
def onMessage(object,callback):
    object['callback'] = callback
    messages.append(object)