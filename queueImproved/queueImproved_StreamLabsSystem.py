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
queueClosedPlayer = "QUEUE IS CLOSED"

messageQueueOpen = "The queue is now open!"
messageQueueAlreadyOpen = "Queue's already open you dum fuk"

messageQueueClosed = "The queue is now closed! Thanks for playing!"
messageQueueAlreadyClosed = "It's already closed wtf."

messageJoinQueueClosed = "Sorry, queue's closed"

messageQueueFull = "Sorry, queue's full :/"


lastCheckedQueue = []
players = {}
currentPlayers = {
    '1': {
        'username': "",
        'file': "Services/Scripts/queueImproved/player1name.html"
    },
    '2': {
        'username': "",
        'file': "Services/Scripts/queueImproved/player2name.html"
    }
}

queueHTMLStart = "" \
                 "<!DOCTYPE html>" \
                 "<html lang='en'>" \
                 "<head>" \
                 "<meta charset='UTF-8'>" \
                 "<title>Title</title>" \
                 "    <link href='queueFormatter.css' rel='stylesheet'>" \
                 "    <script>" \
                 "        function reload(){setTimeout(function(){location.reload();},2000)}reload();" \
                 "    </script>" \
                 "</head>" \
                 "<body>" \
                 "   <div id='player-queue-container'>" \
                 "        <div id='player-queue-container__header'>" \
                 "            <h1>Player Queue</h1>" \
                 "        </div>" \
                 "        <table>" \
                 "            <thead>" \
                 "                <tr>" \
                 "                    <th style='text-align: left;'>Name</th>" \
                 "                    <th style='text-align: right;'>Highest Streak</th>" \
                 "                </tr>" \
                 "            </thead>" \
                 "            <tbody>" \

queueHTMLEnd = \
    "" \
    "            </tbody>" \
    "        </table>" \
    "    </div>" \
    "</body>" \
    "</html>"

playerNameHTMLStart = "" \
    "<!DOCTYPE html>" \
    "<html lang='en'>" \
    "<head>" \
    "<meta charset='UTF-8'>" \
    "<title>Title</title>" \
    "    <link href='playerNameScore.css' rel='stylesheet'>" \
    "    <script>" \
    "        function reload(){setTimeout(function(){location.reload();},2000)}reload();" \
    "    </script>" \
    "</head>" \
    "<body>" \

playerNameHTMLEnd = "" \
    "</body>" \
    "</html>"


class Player:
    def __init__(self, username, display_name="", match_wins=0, match_streak=0, highest_match_streak=0, set_wins=0, set_streak=0, highest_set_streak=0):
        """
        :param username: REQUIRED - Username this object represents
        :param display_name: OPTIONAL - Alias that the user wants to be represented as on stream
        :param match_wins: OPTIONAL - Current amount of matches won by this player. Defaults to 0.
        :param match_streak: OPTIONAL - Current amount of concurrent matches won by this player. Defaults to 0.
        :param highest_match_streak: OPTIONAL - Highest amount of concurrent matches won by this player. Defaults to 0.
        :param set_wins: OPTIONAL - Current amount of sets won by this player. Defaults to 0.
        :param set_streak: OPTIONAL - Current number of concurrent sets this player has won. Defaults to 0.
        :param highest_set_streak:  OPTIONAL - Highest amount of concurrent sets won by this player. Defaults to 0.
        """
        self.username = username
        if not display_name:
            self.display_name = username
        else:
            self.display_name = display_name

        self.match_wins = int(match_wins)
        self.match_streak = int(match_streak)
        self.highest_match_streak = int(highest_match_streak)
        self.set_wins = int(set_wins)
        self.set_streak = int(set_streak)
        self.highest_set_streak = int(highest_set_streak)

        def set_display_name(name):
            self.display_name = name

        def add_match_win():
            ++self.match_wins

        def remove_match_win():
            --self.match_wins

        def set_match_wins(wins):
            self.match_wins = wins

        def add_set_win():
            ++self.set_wins


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
                text = "@" + self.param2 + " has been set as player " + self.param1
            elif self.type == 'error':
                if not self.param1:
                    text = "Error: Specify if you are adding player 1 or 2"
                elif not self.param2:
                    playerSide = "player " + self.param1
                    text = "Error: Can't add " + playerSide + " without a name"
        return text




def Init():

    return

def Execute(data):
    global queueOpen
    global queue
    global nextUser
    global currentPlayers

    command = data.GetParam(0).lower()
    param1 = data.GetParam(1).lower()
    param2 = data.GetParam(2).lower()
    param3 = data.GetParam(3).lower()
    
    # Commands that are only for mods.
    if Parent.HasPermission(data.User, "Moderator", ""):
        if command == "!openq":
            open_queue(param1)
        elif command == "!closeq":
            close_queue()
        elif command == "!clearq":
            clear_queue()
        elif command == "!next":
            pop_next_player(param1)
        elif command == "!currentplayer":
            send_message(nextUser)
        elif command == "!setplayer":
            set_player(param1, param2, data)
        elif command == "!removeplayer":
            remove_from_queue(param1)
        elif command == "!swap":
            swap_current_players()
    if command == "!leave":
        remove_from_queue(data.User)
    elif command == "!setname":
        set_name(data.User, data)
    if queueOpen:
        # Commands available when the queue is open
        if command == "!join":
            join_queue(data.User)
    elif not queueOpen:
        # Spits out error messages if users try to join on a closed queue
        if command == "!join":
            send_message(messageJoinQueueClosed)

    return


def Tick():        
    return


def set_player(player_side, username, data):
    """
    Set a player to either player slot. Can take in a player's desired alias too.
    :param player_side: REQUIRED - Integer that represents which player is being added
    :param username: REQUIRED - Username of the player being added
    :param data: OPTIONAL - Check to see if there was any desired display name passed in
    :return: bool
    """
    # Check to see if the player side was passed as a param
    if not player_side:
        # If it wasn't then we tell the user they dum as fuk
        send_message(Message("!setplayer", "error", player_side, username).text())
        return False
    else:
        # If we get the player side passed in as a param, we continue with the rest of the checks
        # Check if there was a username passed in
        if username:
            # If there was a username passed in, continue with the rest of the checks
            # Check to see if a displayname was passed in
            display_name = generate_display_name(data)
            # Check to see if we already have the player in our dictionary
            if username not in players:
                # If we don't have the player in our dictionary, create a new Player instance for them and add to the dictionary
                new_player = Player(username, displayname)
                players[username] = new_player
            # Map the currentPlayers dictionary with the user's username. We can grab the appropriate info from the players dictionary
            currentPlayers[player_side]['username'] = username
            send_message(Message("!setplayer", "success", player_side, username).text())
            write_player_name_file(displayname, player_side)

            return True
        else:
            # If there's no username, then the user fuked up
            send_message(Message("!setplayer", "error", player_side, username).text())
            return False


def open_queue(fresh=False):
    global queueOpen
    global queue
    global queueClosedPlayer
    # Open the queue. Will only work if the queue is not already open
    if not queueOpen:
        queueOpen = True
        if fresh:
            queue = []
        elif queueClosedPlayer in queue:
            queue.remove(queueClosedPlayer)
        write_queue_to_file()
        write_player_name_file('', '1')
        write_player_name_file('', '2')
        send_message(messageQueueOpen)
    else:
        send_message(messageQueueAlreadyOpen)


def generate_display_name(data):
    i = 1
    word = data.GetParam(i)
    display_name = ""
    while word != '':
        if i > 1:
            display_name += " "
        display_name += word
        i += 1
        word = data.GetParam(i)
    display_name += ""
    return display_name


def clear_queue():
    global queue
    queue = []
    return True


def remove_from_queue(username):
    user_to_leave = username
    if user_to_leave in queue:
        queue.remove(user_to_leave)
        send_message("Adios. " + user_to_leave + " has been removed from the queue.")
        write_queue_to_file()
    else:
        send_message(user_to_leave + ", you aren't even in line. Pls.")


def join_queue(username):
    """
    :param username: User that wants to join the queue
    :return: bool
    """
    global players
    userToAdd = username
    if userToAdd not in queue:
        queue.append(userToAdd)
        if userToAdd not in players:
            new_player = Player(username)
            players[userToAdd] = new_player
        send_message("@" + userToAdd + ", you have entered the queue. Pos: #" + str(len(queue)) + "!")
        write_queue_to_file()
        return True
    else:
        send_message("Dafuq, @" + userToAdd + ", you already in line. You #" + str(queue.index(userToAdd) + 1) + ".")
        return False


def send_message(message):
    Parent.SendStreamMessage(message)
    return


def is_queue_open():
    return queueOpen


def send_whisper(user, message):
    Parent.SendStreamWhisper(user, message)


def set_name(username, data):
    global players
    if not data.GetParam(0):
        send_message("If you want a different name, you have to tell me what it is you asshat")
        return False
    else:
        display_name = generate_display_name(data)
        if username not in players:
            new_player = Player(username, display_name)
            players[username] = new_player
        else:
            player = players.get(username)
            player.set_name(display_name)
        send_message("Changed @" + username + "'s display name to '" + display_name + "'")
        return True


def write_player_name_file(displayname, side):
    file = open(currentPlayers[side]['file'], "w")
    file.write(playerNameHTMLStart)
    stringtowrite = "<div class='player-name player-side-"+side+"'>"+displayname+"</div>"
    file.write(stringtowrite)
    file.write(playerNameHTMLEnd)
    file.close()
    return True


def write_queue_to_file():
    file = open(queueFile, "w")
    file.write(queueHTMLStart)
    for index, val in enumerate(queue):
        if val != queueClosedPlayer:
            player = players.get(val)
            stringToWrite = "<tr>"\
                            "   <td>"\
                            "       <div class='player-queue-player__position'>" + str(index + 1) + ")</div>"\
                            "          <div class='player-queue-player__name'>" + str(player.display_name) + "</div>"\
                            "   </td>"\
                            "   <td class='player-queue-player__streak-container'>"\
                            "       <div class='player-queue-player__streak'>" + str(player.highest_set_streak) + "</div>"\
                            "   </td>"\
                            "</tr>"
        else:
            stringToWrite = "<tr>" \
                            "   <td class='player-queue-player__closed' colspan='2'>" + str(queueClosedPlayer) + "</td>" \
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


def close_queue():
    # Close the queue. Won't work if queue isn't open
    global queueOpen
    if queueOpen:
        queueOpen = False
        queue.append(queueClosedPlayer)
        write_queue_to_file()
        send_message(messageQueueClosed)
    else:
        send_message(messageQueueAlreadyClosed)


def pop_next_player(player_side):
    next_user = queue.pop(0)
    currentPlayers[player_side]['username'] = next_user
    send_message("@" + next_user + ", you're up next!")
    write_queue_to_file()
    return True


def swap_current_players():
    player_1 = currentPlayers['1']
    player_2 = currentPlayers['2']

    currentPlayers['1'] = player_2
    currentPlayers['2'] = player_1
    return True

def reset_current_scores():
    return True