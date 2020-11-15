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
queueClosedPlayer = "QUEUE IS NOW CLOSED"

messageQueueOpen = "The queue is now open!"
messageQueueAlreadyOpen = "Queue's already open you dum fuk"

messageQueueClosed = "The queue is now closed! Thanks for playing!"
messageQueueAlreadyClosed = "It's already closed wtf."

messageJoinQueueClosed = "Sorry, queue's closed"

messageQueueFull = "Sorry, queue's full :/"


lastCheckedQueue = []
players = {}
player1Key = ""
player2Key = ""

class Player:
  def __init__(self, name_twitch, name_display, set_wins, streak, highest_set_wins, highest_streak):
    self.name_twitch = name_twitch
    self.name_display = name_display

    if not streak:
        self.streak = 0
    else:
        self.streak = int(streak)
    if not set_wins:
        self.set_wins = 0
    else:
        self.set_wins = int(set_wins)
    if not highest_streak:
        self.highest_streak = 0
    else:
        self:highest_streak = int(highest_streak)
    if not highest_set_wins:
        self.highest_set_wins = 0
    else
        self.highest_set_wins = int(highest_set_wins)

class Message:
    def __init__(self, command, type, param1, param2):
        self.command = command
        self.type = type
        self.param1 = param1
        self.param2 = param2

    def text(self):
        text = ""
        if self.command == '!setplayer':
            if self.type == 'success':
                text = self.param2 + " has been set as player 1"
            elif self.type == 'error':
                if not self.param1:
                    text = "Error: Specify if you are adding player 1 or 2"
                elif not self.param2:
                    playerSide = "player " + self.param1
                    text = "Error: Can't add " + playerSide + " without a name"
        return text


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
    global player1Key
    global player2Key

    command = data.GetParam(0).lower()
    param1 = data.GetParam(1).lower()
    param2 = data.GetParam(2).lower()
    param3 = data.GetParam(3).lower()
    
    # Commands that are only for mods.
    if Parent.HasPermission(data.User, "Moderator", ""):
        if command == "!openq":
            # Open the queue. Will only work if the queue is not already open
            if not queueOpen:
                queueOpen = True
                queue = []
                write_queue_to_file()
                send_message(messageQueueOpen)
            else:
                send_message(messageQueueAlreadyOpen)
        elif command == "!closeq":
            # Close the queue. Won't work if queue isn't open
            if queueOpen:
                queueOpen = False
                queue.append(queueClosedPlayer)
                write_queue_to_file()
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
        elif command == "!setplayer":
            if param1 == '1':
                if param2:
                    if param2 not in players:
                        if param3:
                            displayName = param3
                        else:
                            displayName = param2
                        newPlayer = Player(param2, displayName, 0)
                        players[param2] = newPlayer
                    player1Key = param2
                    send_message(Message(command, "success", param1, param2).text())






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
        if val != queueClosedPlayer:
            stringToWrite = "<tr>"\
                            "   <td>"\
                            "       <div class='player-queue-player__position'>" + str(index + 1) + ")</div>"\
                            "          <div class='player-queue-player__name'>" + val + "</div>"\
                            "   </td>"\
                            "   <td class='player-queue-player__streak-container'>"\
                            "       <div class='player-queue-player__streak'>" + str(0) + "</div>"\
                            "   </td>"\
                            "</tr>"
        else:
            stringToWrite = "<tr>" \
                            "   <td class='player-queue-player__closed' colspan='2'>" + queueClosedPlayer + "</td>" \
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
    

