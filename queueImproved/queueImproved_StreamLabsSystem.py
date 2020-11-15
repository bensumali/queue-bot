ScriptName = "Queue Improved"
Website = "https://google.com"
Description = "Reimplementation of queue with better control"
Creator = "pac0ncrack"
Version = "1.0.0"

queue = []
queueFile = "Services/Scripts/queueImproved/queueFormatter.html"
player1NameFile = ""
player2NameFile = ""
queueOpen = False
queueMaxCapacity = 10

messageQueueOpen = "The queue is now open!"
messageQueueAlreadyOpen = "Queue's already open you dum fuk"

messageQueueClosed = "The queue is now closed! Thanks for playing!"
messageQueueAlreadyClosed = "It's already closed wtf."

messageJoinQueueClosed = "Sorry, queue's closed"

messageQueueFull = "Sorry, queue's full :/"

lastCheckedQueue = []
playerWins = {}

queueHTMLStart = \
    "<!DOCTYPE html>" \
    "<html lang='en'>" \
    "<head>" \
    "<meta charset='UTF-8'>"\
    "<title>Title</title>"\
    "    <link href='queueFormatter.css' rel='stylesheet'>"\
    "    <script>"\
    "        function reload(){setTimeout(function(){location.reload();},2000)}reload();"\
    "    </script>"\
    "</head>"\
    "<body>"\
    "   <div id='player-queue-container'>"\
    "        <div id='player-queue-container__header'>"\
    "            <h1>Player Queue</h1>"\
    "        </div>"\
    "        <table>"\
    "            <thead>"\
    "                <tr>"\
    "                    <th style='text-align: left;'>Name</th>"\
    "                    <th style='text-align: right;'>Highest Streak</th>"\
    "                </tr>"\
    "            </thead>"\
    "            <tbody>"\

queueHTMLEnd = ""\
    "            </tbody>"\
    "        </table>"\
    "    </div>"\
    "</body>"\
    "</html>"

def Init():
    return

def Execute(data):
    global queueOpen
    global queue
    global nextUser
    
    command = data.GetParam(0).lower()
    
    # Commands that are only for mods.
    if Parent.HasPermission(data.User, "Moderator", ""):
        if command == "!openq":
            # Open the queue. Will only work if the queue is not already open
            if not queueOpen:
                queueOpen = True
                send_message(messageQueueOpen)
            else:
                send_message(messageQueueAlreadyOpen)
        elif command == "!closeq":
            # Close the queue. Won't work if queue isn't open
            if queueOpen:
                queueOpen = False
                send_message(messageQueueClosed)
            else:
                send_message(messageQueueAlreadyClosed)
        elif command == "!next":
            if queueOpen:
                nextUser = queue.pop(0)
                send_message("@" + nextUser + ", you're up next!")
                write_queue_to_file()
        elif command == "!currentplayer":
            send_message(nextUser)


    if command == "!leave":
        userToLeave = data.User
        if userToLeave in queue:
            queue.remove(userToLeave)
            send_message("Adios. " + userToLeave + " has left the queue.")
            write_queue_to_file()
        else:
            send_message(userToLeave + ", you aren't even in line. Pls.")
    if queueOpen:
        # Commands available when the queue is open
        if command == "!join":
            userToAdd = data.User
            if userToAdd not in queue:
                queue.append(userToAdd)
                send_message(userToAdd + ", you have entered the queue. Pos: #" + str(len(queue)) + "!")
                write_queue_to_file()
            else:
                send_message("Dafuq, " + userToAdd + ", you already in line. You #" + str(queue.index(userToAdd)) + ".")
    elif not queueOpen:
        # Spits out error messages if users try to join on a closed queue
        if command == "!join":
            send_message(messageJoinQueueClosed)

    return

def Tick():        
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
    file.write(queueHTMLStart)
    for index, val in enumerate(queue):
        streak = 0
        stringToWrite = "<tr>"\
                        "   <td>"\
                        "       <div class='player-queue-player__position'>" + str(index) + ")</div>"\
                        "          <div class='player-queue-player__name'>" + val + "</div>"\
                        "   </td>"\
                        "   <td class='player-queue-player__streak-container'>"\
                        "       <div class='player-queue-player__streak'>" + str(0) + "</div>"\
                        "   </td>"\
                        "</tr>"
        file.write(stringToWrite)
    file.write(queueHTMLEnd)
    file.close()
    return

def update_player_name_file(fileLocation, name):
    file = open(fileLocation, "w")
    file.write(name)
    file.close()
    return
    

