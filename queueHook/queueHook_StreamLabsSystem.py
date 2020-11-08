ScriptName = "Queue Hook"
Website = "https://google.com"
Description = "Adds on some additional functionality when users enter/leave the queue"
Creator = "pac0ncrack"
Version = "1.0.0"

lastCheckedQueue = []
queueFile = ""
playerWins = {}

def Init():

    return

def Execute(data):
    return

def Tick():
    global lastCheckedQueue
    queue = Parent.GetQueue(10)

    if queue != lastCheckedQueue:
        lastCheckedQueue = queue
        # Probably write at this point
        
    return


def send_message(message):
    Parent.SendStreamMessage(message)
    return
