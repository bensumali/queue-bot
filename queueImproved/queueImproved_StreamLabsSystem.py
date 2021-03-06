ScriptName = "Queue Improved"
Website = "https://google.com"
Description = "Reimplementation of queue with better control"
Creator = "pac0ncrack"
Version = "1.0.0"

import sys
sys.path.append('.\Services\Scripts\queueImproved')

import time
from os import listdir
from os.path import isfile, join

from decouple import config
from player import Player
from message import Message
from queue_new import Queue


queue = Queue()
queueFile = "Services/Scripts/queueImproved/source_content/queue.js"

bully = False

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
        'files': {
            'name': config('player1NameFile'),
            'score': config('player1ScoreFile'),
            'streak': config('player1StreakFile'),
            'username': config('player1UsernameFile')
        }
    },
    '2': {
        'username': "",
        'files': {
            'name': config('player2NameFile'),
            'score': config('player2ScoreFile'),
            'streak': config('player2StreakFile'),
            'username': config('player2UsernameFile')
        }
    }
}
videoLastCalled = 0
videoString = ""
videoCommands = []


def Init():
    global videoString
    path = "Services/Scripts/queueImproved/source_formatters/videos"
    video_files = [f for f in listdir(path) if isfile(join(path, f))]
    videoString = "["
    for file in video_files:
        videoString = videoString + "'" + file + "', "
        videoCommands.append(file.split('.')[0])
    videoString = videoString[:-2]
    videoString = videoString + "]"
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
        if data.IsWhisper():
            arg0 = data.GetParam(0)
            arg1 = data.GetParam(1)
            arg2 = data.GetParam(2)
            arg3 = data.GetParam(3)
            if arg0 == "!queue":
                if arg1 == "close":
                    close_queue()
                elif arg1 == "open":
                    open_queue()
                elif arg1 == "clear":
                    clear_queue()
                elif arg1 == "remove":
                    remove_from_queue(arg2)
                elif arg1 == "add":
                    join_queue(arg2, arg3)
            elif arg0 == "!p1" or arg0 == "!p2":
                if arg1 == "won:match":
                    add_match_win_to_current_player(arg0[2])
                elif arg1 == "won:set":
                    get_next_player = False
                    if arg2 == "--next":
                        get_next_player = True
                    add_set_win_to_current_player(arg0[2], get_next_player)
                elif arg1 == "next":
                    pop_next_player(arg0[2])
                elif arg1 == "set:match_wins":
                    set_match_wins_of_current_player(arg0[2], arg2)
                elif arg1 == "set:set_wins":
                    set_set_wins_of_current_player(arg0[2], arg2)
            elif command == "!p1w":
                add_match_win_to_current_player(1)
            elif command == "!p2w":
                add_match_win_to_current_player(2)
            elif command == "!p1l":
                remove_match_win_to_current_player(1)
            elif command == "!p2l":
                remove_match_win_to_current_player(2)
            elif command == "!p1s":
                add_set_win_to_current_player(1)
            elif command == "!p2s":
                add_set_win_to_current_player(2)
            elif command == "!cs":
                clear_scores()
            elif command == "!swap":
                swap_current_players()
            elif command == "!next":
                if param1 == "1":
                    param1 = "2"
                else:
                    param1 = "1"
                add_set_win_to_current_player(param1, True)
            elif command == "!skip":
                if param1 == "1":
                    param1 = "2"
                else:
                    param1 = "1"
                pop_next_player(param1)
        else:
            if command == "!openq":
                open_queue()
            elif command == "!closeq":
                close_queue()
            elif command == "!clearq":
                clear_queue()
            elif command == "!next":
                if param1 == "1":
                    param1 = "2"
                else:
                    param1 = "1"
                add_set_win_to_current_player(param1, True)
            elif command == "!currentplayer":
                send_message(nextUser)
            elif command == "!setplayer":
                set_current_player(param1, param2, data)
            elif command == "!removeplayer":
                remove_from_queue(param1)
            elif command == "!swap":
                swap_current_players()
            elif command == "!p1":
                update_current_player_name(generate_display_name(data), 1)
            elif command == "!p2":
                update_current_player_name(generate_display_name(data), 2)
            elif command == "!p1w":
                add_match_win_to_current_player(1)
            elif command == "!p2w":
                add_match_win_to_current_player(2)
            elif command == "!p1l":
                remove_match_win_to_current_player(1)
            elif command == "!p2l":
                remove_match_win_to_current_player(2)
            elif command == "!p1s":
                add_set_win_to_current_player(1)
            elif command == "!p2s":
                add_set_win_to_current_player(2)
            elif command == "!cs":
                clear_scores()
            elif command == "!clearstreaminfo":
                clear_stream_info()
            elif command == "!skip":
                if param1 == "1":
                    param1 = "2"
                else:
                    param1 = "1"
                pop_next_player(param1)
    if command == "!leave":
        remove_from_queue(data.User)
    elif command == "!setname":
        set_name(data.User, data)
    elif command == "!list":
        display_queue_list_as_chat_message()
    elif command == "!queue":
        display_queue_list_as_chat_message()
    elif command == "!join":
        join_queue(data.User)
    elif command in videoCommands:
        play_video(command)
    return


def Tick():
    return


def add_match_win_to_current_player(player_side):
    player = players[currentPlayers[str(player_side)]["username"]]
    player.add_match_win()
    write_player_file(player.get_current_match_wins(), 'score', player_side)
    if currentPlayers['1']["username"]:
        player1 = players[currentPlayers['1']["username"]]
        player_1_score = player1.get_current_match_wins()
    else:
        player_1_score = 0
    if currentPlayers['2']["username"]:
        player2 = players[currentPlayers['2']["username"]]
        player_2_score = player2.get_current_match_wins()
    else:
        player_2_score = 0
    send_message("@" + player.username + " won a match! The score is now " + str(player_1_score) + " - " + str(player_2_score) + ".")
    return True


def remove_match_win_to_current_player(player_side): 
    player = players[currentPlayers[str(player_side)]["username"]]
    player.remove_match_win()
    write_player_file(player.get_current_match_wins(), 'score', player_side)
    if currentPlayers['1']["username"]:
        player1 = players[currentPlayers['1']["username"]]
        player_1_score = player1.get_current_match_wins()
    else:
        player_1_score = 0
    if currentPlayers['2']["username"]:
        player2 = players[currentPlayers['2']["username"]]
        player_2_score = player2.get_current_match_wins()
    else:
        player_2_score = 0
    send_message("Removed a match win from @" + player.username + ". The score is now " + str(player_1_score) + " - " + str(player_2_score) + ".")
    return True


def add_set_win_to_current_player(player_side, get_next_player=False):
    global queue
    if player_side == "1":
        losing_player_side = "2"
    else:
        losing_player_side = "1"
    losing_player_username = currentPlayers[losing_player_side]['username']
    if losing_player_username in players:
        players[losing_player_username].reset_streaks()
    winning_player_username = currentPlayers[str(player_side)]['username']
    if winning_player_username in players:
        winning_player = players[winning_player_username]
        winning_player.add_set_win()
        write_player_file(winning_player.get_current_set_streak(), 'streak', player_side)
        send_message("@" + winning_player.username + " won the set!")
    else:
        winning_player = False
    if get_next_player:
        next_player_name = pop_next_player(losing_player_side)
    else:
        next_player_name = False
    find_bully()
    write_bully_file()
    write_win_screen_file(winning_player, player_side, next_player_name)
    return True


def set_match_wins_of_current_player(player_side, wins):
    player_username = currentPlayers[str(player_side)]["username"]
    player = players[player_username]
    player.set_match_wins(wins)
    write_player_file(player.get_current_match_wins(), 'score', player_side)
    send_message("Set @" + player.username + "'s match wins to " + wins)
    return player.set_match_wins(wins)


def set_set_wins_of_current_player(player_side, wins):
    player_username = currentPlayers[str(player_side)]["username"]
    player = players[player_username]
    player.set_set_wins(wins)
    write_player_file(player.get_current_set_streak(), 'streak', player_side)
    send_message("Set @" + player.username + "'s set wins to " + wins)
    find_bully()
    write_bully_file()
    return player.set_set_wins(wins)


def clear_current_players():
    player1username = currentPlayers["1"]["username"]
    player2username = currentPlayers["2"]["username"]
    if player1username:
        players[player1username].reset_streaks()
    if player2username:
        players[player2username].reset_streaks()
    currentPlayers["1"]["username"] = ""
    currentPlayers["2"]["username"] = ""
    write_player_file('0', 'streak', '1')
    write_player_file('0', 'streak', '2')
    write_player_file('', 'name', '1')
    write_player_file('', 'name', '2')
    write_player_file('', 'username', '1')
    write_player_file('', 'username', '2')
    clear_scores()


def set_current_player(player_side, username, data=""):
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
            display_name = username
            # Check to see if we already have the player in our dictionary
            if username not in players:
                # If we don't have the player in our dictionary, create a new Player instance for them and add to the dictionary
                new_player = Player(username, display_name)
                players[username] = new_player
            player = players[username]
            # Map the currentPlayers dictionary with the user's username. We can grab the appropriate info from the players dictionary
            currentPlayers[str(player_side)]['username'] = username
            player.set_set_wins(0)
            write_player_file(display_name, 'name', player_side)
            write_player_file(player.get_current_match_wins(), 'score', player_side)
            write_player_file(player.get_current_set_streak(), 'streak', player_side)
            write_player_file(username, 'username', player_side)
            send_message(Message("!setplayer", "success", player_side, username).text())
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
    if queue.clear_queue():
        write_queue_to_file()
        send_message("Queue is now empty.")


def remove_from_queue(username):
    global queue
    user_to_leave = username
    if queue.remove_player(username):
        send_message("Adios. " + user_to_leave + " has been removed from the queue.")
        write_queue_to_file()
    else:
        send_message(user_to_leave + ", you aren't even in line. Pls.")


def join_queue(username, position=-1):
    """
    :param username: User that wants to join the queue
    :return: bool
    """
    global players
    global queue
    if not queue.is_open:
        send_message(messageJoinQueueClosed)
        return False
    else:
        if is_currently_playing(username):
            send_message("You can't join the queue while playing.")
            return False
        if queue.add_player(username, position):
            add_player_record(username)
            send_message("@" + username + ", you have entered the queue. Pos: #" + str(queue.players.index(username) + 1) + "!")
            write_queue_to_file()
            return True
        else:
            send_message("Dafuq, @" + username + ", you already in line. You #" + str(queue.players.index(username) + 1) + ".")
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


def write_player_file(value, file_type, side):
    file = open(currentPlayers[str(side)]['files'][file_type], "w")
    file.write("export default { '" + str(file_type) + "': '" + str(value) + "'}")
    file.close()
    return True


def write_bully_file():
    if bully:
        file = open(config('bullyFile'), "w")
        file.write("export default { 'username': '" + str(bully.username) + "', 'wins': '" + str(bully.highest_set_streak) + "'}")
        file.close()
    return True

def clear_bully_info():
    file = open(config('bullyFile'), "w")
    file.write("export default { 'username': '', 'wins': ''}")
    file.close()
    bully = False
    return True

def write_queue_to_file():
    global queue
    file = open(queueFile, "w")
    file.write("export default { 'players': [")
    for index, val in enumerate(queue.players):
        player = players.get(val)
        string_to_write = "{'name': '" + str(player.display_name) + "', 'streak': '" + str(player.highest_set_streak) + "'}, "
        file.write(string_to_write)
    file.write("], 'is_open': " + str(queue.is_queue_open()).lower() + " }")
    file.close()
    return


def close_queue():
    # Close the queue. Won't work if queue isn't open
    global queue
    if queue.is_queue_open():
        queue.close_queue()
        write_queue_to_file()
        send_message(messageQueueClosed)
        return True
    else:
        send_message(messageQueueAlreadyClosed)
        return False


def pop_next_player(player_side):
    global queue
    if len(queue.players) > 0:
        next_player = queue.players.pop(0)
        send_message("@" + next_player + ", you're up next!")
        clear_scores()
        set_current_player(player_side, next_player)
        clear_scores()
        write_queue_to_file()
    else:
        send_message("No one's got next. Sure is lonely in here...")
        next_player = False
    return next_player


def is_currently_playing(username):
    if currentPlayers['1']['username'] == username or currentPlayers['2']['username'] == username:
        return True
    else:
        return False


def update_current_player_name(username, player_side):
    
    add_player_record(username)
    player = players[username]
    if player:
        currentPlayers[str(player_side)]['username'] = username
        write_player_file(username, 'name', str(player_side))
        write_player_file(username, 'username', str(player_side))


def add_player_record(username): 
    if username not in players:
        new_player = Player(username)
        players[username] = new_player
        return True
    return False


def swap_current_players():
    player_1_username = currentPlayers['1']['username']
    player_2_username = currentPlayers['2']['username']

    player_1 = players[player_1_username]
    player_2 = players[player_2_username]

    currentPlayers['1']['username'] = player_2_username
    currentPlayers['2']['username'] = player_1_username

    if player_1:
        write_player_file(player_1.match_wins, 'score', 2)
        write_player_file(player_1.set_wins, 'streak', 2)
        write_player_file(player_1.display_name, 'name', 2)
        write_player_file(player_1_username, 'username', 2)

    if player_2:
        write_player_file(player_2.match_wins, 'score', 1)
        write_player_file(player_2.set_wins, 'streak', 1)
        write_player_file(player_2.display_name, 'name', 1)
        write_player_file(player_2_username, 'username', 1)
    return True


def clear_scores():
    player1username = currentPlayers["1"]["username"]
    player2username = currentPlayers["2"]["username"]
    if player1username:
        player1 = players[player1username]
        player1.set_match_wins(0)
    if player2username:
        player2 = players[player2username]
        player2.set_match_wins(0)
    write_player_file('0', 'score', 1)
    write_player_file('0', 'score', 2)


def display_queue_list_as_chat_message():
    count = 0
    chatString = "The queue is " + str(len(queue.players)) + " people deep. "
    for index, val in enumerate(queue.players):
        player = players.get(val)
        count = count + 1
        if count == len(queue.players):
            chatString = chatString + "#" + str(index + 1) + " - " + str(player.display_name)
        else:
            chatString = chatString + "#" + str(index + 1) + " - " + str(player.display_name) + ', '
    send_message(chatString)


def find_bully():
    """
    Finds the player with the highest set streak.
    :return: Player or False if there are no bullies
    """
    global bully
    for index, val in players.items():
        if not bully or int(bully.highest_set_streak) < int(val.highest_set_streak):
            bully = val
            write_bully_file()
            if val.username != bully.username:
                send_message("@" + bully.username + " is now the bully!")
    return bully


def clear_stream_info():
    clear_current_players()
    clear_queue()
    clear_bully_info()
    clear_win_info()

def play_video(command):
    """
    Only writes to file if more than 10 seconds since last call.
    :return: Player or False if there are no bullies
    """
    global videoLastCalled
    now = int(time.time())
    if now > (videoLastCalled + 10):
        videoLastCalled = now

        file = open(config('videoFile'), "w")
        file.write("export default { 'command': '" + command + "', 'timestamp': " + str(now) + ", 'files': " + videoString + "}")
        file.close()
        return True
    else:
        return False


def write_win_screen_file(winning_player, winning_side, next_player):
    """
    Writes file to display the winner and next player.
    :return: Bool
    """
    if winning_player:
        now = int(time.time())
        if not next_player:
            next_player_name = ''
        else:
            next_player_name = next_player
        file = open(config('winScreenFile'), "w")
        file.write("export default { 'winning_side': " + str(winning_side) + ", 'next_player': {'username': '" + next_player_name + "'},'winning_player': {'username': '" + winning_player.username + "', 'set_streak': '" + str(winning_player.set_streak) + "'}, 'bully': {'username': '" + str(bully.username) + "', 'set_streak': '" + str(bully.set_streak) + "'}, 'timestamp': " + str(now) + "}")
        file.close()
    return True


def clear_win_info():
    now = int(time.time())
    file = open(config('winScreenFile'), "w")
    file.write("export default { 'timestamp': " + str(now) + "}")
    file.close()

