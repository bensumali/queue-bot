ScriptName = "Queue Improved"
Website = "https://google.com"
Description = "Reimplementation of queue with better control"
Creator = "pac0ncrack"
Version = "1.0.0"

queue = []
queueFile = "queueFile"
queueOpen = False
queueMaxCapacity = 10

messageQueueOpen = "The queue is now open!"
messageQueueAlreadyOpen = "Queue's already open you dum fuk"

messageQueueClosed = "The queue is now closed! Thanks for playing!"
messageQueueAlreadyClosed = "It's closed already wtf."

messageQueueFull = "Sorry, queue's full :/"

lastCheckedQueue = []
playerWins = {}

def Init():
    return

def Execute(data):
    global queueOpen
    global queue
    command = data.GetParam(0)
    if data.IsWhisper():
        if Parent.HasPermission(data.User, "Moderator", ""):
            if command == "!openQueue":
                if not queueOpen:
                    queueOpen = True
                    send_message(messageQueueOpen)
                else:
                    send_whisper(data.User, messageQueueAlreadyOpen)
            elif command == "!closeQueue":
                if queueOpen:
                    queueOpen = False
                    send_message(messageQueueClosed)
                else:
                    send_whisper(data.User, messageQueueAlreadyClosed)

    else:
        if queueOpen:
            if command == "!join":
                userToAdd = data.User
                if userToAdd not in queue:
                    queue.append(userToAdd)
                    send_message(userToAdd + ", you have entered the queue. Pos: #" + str(len(queue) - 1) + "!")
                else:
                    send_message("Dafuq, " + userToAdd + ", you already in line. You #" + str(queue.index(userToAdd)) + ".")
            elif command == "!leave":
                userToLeave = data.User
                if userToLeave in queue:
                    queue.remove(userToLeave)
                    send_message("Adios. " + userToLeave + " has left the queue.")
                else:
                    send_message(userToLeave + ", you aren't even in line. Pls.")

    return

def Tick():
    # global lastCheckedQueue
    # queue = Parent.GetQueue(10)
    #
    # if queue != lastCheckedQueue:
    #     lastCheckedQueue = queue
        # Probably write at this point
        
    return


def send_message(message):
    Parent.SendStreamMessage(message)
    return

def is_queue_open():
    return queueOpen

def send_whisper(user, message):
    Parent.SendStreamWhisper(user, message)
