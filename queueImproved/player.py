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

    def get_current_match_wins(self):
        return self.match_wins

    def get_current_set_streak(self):
        return self.set_streak

    def set_display_name(self, name):
        self.display_name = name

    def add_match_win(self):
        self.match_wins = int(self.match_wins) + 1

    def remove_match_win(self):
        self.match_wins = int(self.match_wins) - 1

    def clear_set_match_wins(self):
        self.set_wins = 0

    def set_match_wins(self, wins):
        self.match_wins = wins
        return True

    def set_set_wins(self, wins):
        self.set_wins = wins
        self.set_streak = wins
        if self.set_wins > self.highest_set_streak:
            self.highest_set_streak = self.set_wins
        return True

    def add_set_win(self):
        self.set_wins = int(self.set_wins) + 1
        self.set_streak = int(self.set_streak) + 1
        if self.set_wins > self.highest_set_streak:
            self.highest_set_streak = int(self.set_wins)

    def reset_streaks(self):
        self.set_wins = 0
        self.match_wins = 0
        self.set_streak = 0
        self.match_streak = 0
        return True

    def reset_match_streak(self):
        self.match_streak = 0
        return True
