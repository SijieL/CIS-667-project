import torch
import model
from board import Board

cnn = model.CNN()
# call model, should load different model at each board size

# cnn.load_state_dict(torch.load('net_params_6.pkl'))  # 6x6
# cnn.load_state_dict(torch.load('net_params_7.pkl'))   # 7x7
cnn.load_state_dict(torch.load('net_params.pkl'))  # 8x8
# cnn.load_state_dict(torch.load('net_params_9.pkl'))  # 9x9
# cnn.load_state_dict(torch.load('net_params_10.pkl'))  # 10x10
board = Board()


class MY_CNN():
    def __int__(self, level_ix=0):
        self.level = ['beginner', 'intermediate', 'advanced'][level_ix]

    def get_action(self):
        self.state = board.get_matrix()

        # state2d = torch.zeros([1, 2, 6, 6])
        # state2d = torch.zeros([1, 2, 7, 7])
        state2d = torch.zeros([1, 2, 8, 8])
        # state2d = torch.zeros([1, 2, 9, 9])
        # state2d = torch.zeros([1, 2, 10, 10])


        # for i in range(6):
        # for i in range(7):
        for i in range(8):
        # for i in range(9):
        # for i in range(10):

            # for j in range(6):
            # for j in range(7):
            for j in range(8):
            # for j in range(9):
            # for j in range(10):
                if self.state[i][j] == 1:
                    state2d[0, 0, i, j] = 1
                elif self.state[i][j] == -1:
                    state2d[0, 1, i, j] = -1
        score = cnn(state2d)
        score = score.detach().numpy()
        # score_map = score.reshape(6, 6)
        # score_map = score.reshape(7, 7)
        score_map = score.reshape(8, 8)
        # score_map = score.reshape(9, 9)
        # score_map = score.reshape(10, 10)

        return score_map
