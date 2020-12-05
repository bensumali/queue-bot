class Queue:
    def __init__(self, players=[], is_open=False, max_capacity=10):
        """
        :param players: OPTIONAL - List of players' usernames in the current queue
        :param is_open: OPTIONAL - Boolean that indicates if the queue is open
        :param max_capacity: OPTIONAL - Max # of players allowed in the queue at any given time
        """
        self.players = players
        self.is_open = is_open
        self.max_capacity = max_capacity

    def is_queue_open(self):
        return self.is_open

    def clear_queue(self):
        self.players = []
        return True

    def close_queue(self):
        self.is_open = False
        return True

    def open_queue(self):
        self.is_open = True
        return True

    def set_max_capacity(self, max_capacity):
        self.max_capacity = max_capacity
        return True

    def add_player(self, username, position=-1, ignore_close=False):
        if username not in self.players:
            if self.is_open or ignore_close is True:
                if len(self.players) < self.max_capacity:
                    if position > -1:
                        self.players.insert(position, username)
                    else:
                        self.players.append(username)
                    return True
        return False

    def remove_player(self, username):
        if username in self.players:
            self.players.remove(username)
            return True
        return False
