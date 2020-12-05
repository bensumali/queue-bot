ScriptName = "Queue Improved"
Website = "https://google.com"
Description = "Reimplementation of queue with better control"
Creator = "pac0ncrack"
Version = "1.0.0"

import sys
sys.path.append('.\Services\Scripts\queueImproved')

from decouple import config
from player import Player
from message import Message
from queue import Queue


queue = Queue()
queueFile = "Services/Scripts/queueImproved/source_content/queue.js"

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
            open_queue()
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
        elif command == "!p1":
            update_current_player_name(generate_display_name(data), 1)
        elif command == "!p2":
            update_current_player_name(generate_display_name(data), 2)
        elif command == "!p1w":
            increment_score(player1ScoreFile)
        elif command == "!p2w":
            increment_score(player2ScoreFile)
        elif command == "!p1s": 
            write_to_file(player1ScoreFile, param1)
        elif command == "!p2s":
            write_to_file(player2ScoreFile, param1)
        elif command == "!cs": 
            clear_scores()
        
            
        

    if command == "!leave":
        remove_from_queue(data.User)
    elif command == "!setname":
        set_name(data.User, data)
    elif command == "!list": 
        display_queue_list_as_chat_message()
    elif command == "!queue":
        display_queue_list_as_chat_message()

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


def clear_current_players():
    write_player_name_file('', '1')
    write_player_name_file('', '2')
    update_current_player_name('', 1)
    update_current_player_name('', 2)
    clear_scores()


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
                new_player = Player(username, display_name)
                players[username] = new_player
            # Map the currentPlayers dictionary with the user's username. We can grab the appropriate info from the players dictionary
            currentPlayers[player_side]['username'] = username
            send_message(Message("!setplayer", "success", player_side, username).text())
            write_player_name_file(display_name, player_side)

            return True
        else:
            # If there's no username, then the user fuked up
            send_message(Message("!setplayer", "error", player_side, username).text())
            return False


def open_queue():
    global queue
    if not queue.is_queue_open():
        queue.open_queue()
        write_queue_to_file()
        # clear_current_players()
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
    return queue.clear_queue()


def remove_from_queue(username):
    global queue
    user_to_leave = username
    if queue.remove_player(username):
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
    
    if is_currently_playing(username) == True:
        send_message("You can't join the queue while playing.")
        return False

    if userToAdd not in queue:
        queue.append(userToAdd)
        add_player_record(userToAdd)
        send_message("@" + userToAdd + ", you have entered the queue. Pos: #" + str(len(queue)) + "!")
        write_queue_to_file()
        return True
    else:
        send_message("Dafuq, @" + userToAdd + ", you already in line. You #" + str(queue.index(userToAdd) + 1) + ".")
        return False


def send_message(message):
    Parent.SendStreamMessage(message)
    return


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
    global queue
    file = open(queueFile, "w")
    file.write("export default { 'players': [")
    for index, val in enumerate(queue.players):
        # if val != queueClosedPlayer:
        player = players.get(val)
        string_to_write = str(player.display_name) + ", "

            # stringToWrite = "<tr>"\
            #                 "   <td>"\
            #                 "       <div class='player-queue-player__position'>" + str(index + 1) + ")</div>"\
            #                 "          <div class='player-queue-player__name'>" + str(player.display_name) + "</div>"\
            #                 "   </td>"\
            #                 "   <td class='player-queue-player__streak-container'>"\
            #                 "       <div class='player-queue-player__streak'>" + str(player.highest_set_streak) + "</div>"\
            #                 "   </td>"\
            #                 "</tr>"
        # else:
        #     stringToWrite = "<tr>" \
        #                     "   <td class='player-queue-player__closed' colspan='2'>" + str(queueClosedPlayer) + "</td>" \
        #                     "</tr>"
        file.write(string_to_write)
    file.write("], 'is_open': " + str(queue.is_queue_open()).lower() + " }")
    file.close()
    return


def close_queue():
    # Close the queue. Won't work if queue isn't open
    global queue
    if queue.is_queue_open():
        queue.close_queue()
        # write_queue_to_file()
        send_message(messageQueueClosed)
    else:
        send_message(messageQueueAlreadyClosed)


def pop_next_player(player_side):
    next_user = queue.pop(0)
    loser_user = currentPlayers[player_side]['username']
    currentPlayers[player_side]['username'] = next_user
    send_message("@" + next_user + ", you're up next!")

    if player_side == "1":
        write_to_file(player1NameFile, next_user)

        # Because the player is being set in P1, 
        # that means P2 is the winner of the last set.
        # Increment the player 2 winstreak
        # Get p2's username
        player2username = currentPlayers['2']['username']
        # Get the player'2s record
        if not player2username:
            if player2username in players:
                players[player2username].add_set_win
    else:
        write_to_file(player2NameFile, next_user)

        # Because the player is being set in P2, 
        # that means P1 is the winner of the last set.
        # Increment the player 1 winstreak
        player1username = currentPlayers['1']['username']
        if not player1username:
            if player1username in players:
                players[player1username].add_set_win
    write_queue_to_file()
    return True

def is_currently_playing(username):
    if currentPlayers['1']['username'] == username or currentPlayers['2']['username'] == username:
        return True
    else:
        return False

def update_current_player_name(username, player_side):
    
    add_player_record(username)

    if player_side == 1:
        currentPlayers['1']['username'] = username
        write_to_file(config('player1NameFile'), username)
    else:
        currentPlayers['2']['username'] = username
        write_to_file(config('player2NameFile'), username)

def add_player_record(username): 
    if username not in players:
        new_player = Player(username)
        players[username] = new_player

def swap_current_players():
    player_1 = currentPlayers['1']
    player_2 = currentPlayers['2']

    currentPlayers['1'] = player_2
    currentPlayers['2'] = player_1

    write_to_file(player1NameFile, player_2['username'])
    write_to_file(player2NameFile, player_1['username'])
    return True

def increment_score(fileLocation):
    fileReader = open(fileLocation, "r")
    currentScore = int(fileReader.read())
    currentScore = currentScore + 1
    fileReader.close

    write_to_file(fileLocation, str(currentScore))

def clear_scores(): 
    write_to_file(config('player1ScoreFile'), "0")
    write_to_file(config('player2ScoreFile'), "0")

def display_queue_list_as_chat_message():
    count = 0
    chatString = "The queue is " + str(len(queue)) + " people deep. "

    for index, val in enumerate(queue):
        player = players.get(val)
        count = count + 1
        
        if count == len(queue):
            chatString = chatString + "#" + str(index + 1) + " - " + str(player.display_name)
        else:
            chatString = chatString + "#" + str(index + 1) + " - " + str(player.display_name) + ', '
        
    
    send_message(chatString)

def write_to_file(fileLocation, text):
    file = open(fileLocation, "w")
    file.write(text)
    file.close()


