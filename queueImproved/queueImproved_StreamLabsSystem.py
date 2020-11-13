ScriptName = "Queue Improved"
Website = "https://google.com"
Description = "Reimplementation of queue with better control"
Creator = "pac0ncrack"
Version = "1.0.0"

queue = []
queueFile = "queueFile.csv"
queueOpen = False
queueMaxCapacity = 10

messageQueueOpen = "The queue is now open!"
messageQueueAlreadyOpen = "Queue's already open you dum fuk"

messageQueueClosed = "The queue is now closed! Thanks for playing!"
messageQueueAlreadyClosed = "It's closed already wtf."

messageJoinQueueClosed = "Sorry, queue's not open"
messageLeaveQueueClosed = "Queue's not even open how do you even leave it"

messageQueueFull = "Sorry, queue's full :/"

lastCheckedQueue = []
playerWins = {}

def Init():
    return

def Execute(data):
    global queueOpen
    global queue
    command = data.GetParam(0)

    # Commands that are only for mods. These commands are only available by whispering to the bot

    if data.IsWhisper():
        if Parent.HasPermission(data.User, "Moderator", ""):
            if command == "!openQueue":
                # Open the queue. Will only work if the queue is not already open
                if not queueOpen:
                    queueOpen = True
                    send_message(messageQueueOpen)
                else:
                    send_whisper(data.User, messageQueueAlreadyOpen)
            elif command == "!closeQueue":
                # Close the queue. Won't work if queue isn't open
                if queueOpen:
                    queueOpen = False
                    queue = []
                    write_queue_to_file()
                    send_message(messageQueueClosed)
                else:
                    send_whisper(data.User, messageQueueAlreadyClosed)
            elif command == "!next":
                if queueOpen:
                    nextUser = queue.pop(0)
                    send_message("@" + nextUser + ", you're up next!")
                    write_queue_to_file()
                else:
                    send_whisper(data.User, messageJoinQueueClosed)



    else:
        if queueOpen:
            # Commands available when the queue is open
            if command == "!join":
                userToAdd = data.User
                if userToAdd not in queue:
                    queue.append(userToAdd)
                    send_message(userToAdd + ", you have entered the queue. Pos: #" + str(len(queue) - 1) + "!")
                    write_queue_to_file()
                else:
                    send_message("Dafuq, " + userToAdd + ", you already in line. You #" + str(queue.index(userToAdd)) + ".")
            elif command == "!leave":
                userToLeave = data.User
                if userToLeave in queue:
                    queue.remove(userToLeave)
                    send_message("Adios. " + userToLeave + " has left the queue.")
                    write_queue_to_file()
                else:
                    send_message(userToLeave + ", you aren't even in line. Pls.")
        elif not queueOpen:
            # Spits out error messages if users try to join on a closed queue
            if command == "!join":
                send_message(messageJoinQueueClosed)
            elif command == "!leave":
                send_message(messageLeaveQueueClosed)

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

def write_queue_to_file():
    file = open(queueFile, "w")
    for val in queue:
        file.write(val + "\n")
    file.close()
    return
