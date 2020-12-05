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