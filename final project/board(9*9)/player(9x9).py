from tree_search_AI import AI
from CNN_AI import MY_CNN
import numpy as np


class Player(object):
    def __init__(self, color):
        self.color = color

    def think(self, board):
        pass

    def move(self, board, action):
        flipped_pos = board._move(action, self.color)
        return flipped_pos

    def unmove(self, board, action, flipped_pos):
        board._unmove(action, flipped_pos, self.color)


class HumanPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def think(self, board):
        while True:
            action = input("Turn to '{}'. \nPlease input a point.(such as 'A1'): ".format(self.color))  # A1~H8
            r, c = action[1], action[0].upper()
            if r in '123456789' and c in 'ABCDEFGHI':
                x, y = '123456789'.index(r), 'ABCDEFGHI'.index(c)
                if (x, y) in board.get_legal_actions(self.color):
                    return x, y


# class AIPlayer(Player, AI):
#     def __init__(self, color, level_ix=0):
#         super().__init__(color)
#         super(Player, self).__init__(level_ix)
#
#     def think(self, board):
#         print("Turn to '{}'. \nPlease wait a moment. AI is thinking...".format(self.color))
#         uncolor = ['X', 'O'][self.color == 'X']
#         opfor = AIPlayer(uncolor)
#         action = self.brain(board, opfor, 4)
#         return action

# CNN AI player

class AIPlayer(Player, MY_CNN):
    def __init__(self, color, level_ix=0):
        super().__init__(color)  # init Player
        MY_CNN.__init__(level_ix)  # init AI

    def think(self, board):
        print("Turn to '{}'. \nPlease wait a moment. AI is thinking...".format(self.color))
        uncolor = ['X', 'O'][self.color == 'X']
        opfor = AIPlayer(uncolor)
        score_map = MY_CNN.get_action(self)
        legal_loc = np.array(list(board.get_legal_actions(self.color)))[:,::-1]
        legal_loc_score = np.array([score_map[i[0],i[1]] for i in legal_loc])
        max_loc = np.argmax(legal_loc_score)
        selected_loc = legal_loc[max_loc][::-1]
        return selected_loc


# Random AI player

# class AIPlayer(Player, AI):
#     def __init__(self, color, level_ix=0):
#         super().__init__(color)  # init Player
#         super(Player, self).__init__(level_ix)  # init AI
#
#     def think(self, board):
#         print("Turn to '{}'. \nPlease wait a moment. AI is thinking...".format(self.color))
#         action = AI.randomchoice(self, board)[1]
#         return action

