import numpy as np
import os

global board_state
global next_step

board_state = []
next_step = []


def create_one_round_data(data_list):
    # white is 1, black is -1
    # board = np.zeros((6, 6))       # 6x6
    # board = np.zeros((7, 7))       # 7x7
    # board = np.zeros((8, 8))
    # board = np.zeros((9, 9))   # 9x9
    board = np.zeros((10, 10))       # 10x10

    board[3, 3] = 1
    board[4, 4] = 1
    board[3, 4] = -1
    board[4, 3] = -1
    coloum_dic = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
    current_board = board.copy()
    board_state.append(current_board)

    for indi, action in enumerate(data_list):
        if 'S' in action:
            continue

        row_num = int(action[8]) - 1
        col_num = coloum_dic[action[5]] - 1
        # if (row_num > 5) or (col_num > 5):  # 6x6
        #     return
        # if (row_num > 6) or (col_num > 6):  # 7x7
        #     return
        next_step.append(np.array([row_num, col_num]))
        if action[3] == 'B':
            ## board[row_num,col_num]=-1
            board = board_inspection(board, np.array([row_num, col_num]), -1)
        elif action[3] == 'W':
            ## board[row_num,col_num]=1
            board = board_inspection(board, np.array([row_num, col_num]), 1)
        if indi < (len(data_list) - 1):
            current_board = board.copy()
            board_state.append(current_board)


def is_on_board(y, x):

    # if (0 <= y <= 5) and (0 <= x <= 5):  # 6x6
    # if (0 <= y <= 6) and (0 <= x <= 6):   # 7x7
    # if (0 <= y <= 7) and (0 <= x <= 7):   # 8x8
    # if (0 <= y <= 8) and (0 <= x <= 8):    # 9x9
    if (0 <= y <= 9) and (0 <= x <= 9):  # 10x10
        return True
    else:
        return False


def board_inspection(board, location, value):
    ## board is the current board situation
    ## location is the current chess location
    ## value means is the current black or white
    curre_y, curre_x = location[0], location[1]
    for ydirection, xdirection in ((0, -1), (1, 1), (1, 0), (1, -1), (-1, 0), (-1, -1), (0, 1), (-1, 1)):
        new_y, new_x = curre_y + ydirection, curre_x + xdirection
        while is_on_board(new_y, new_x):
            if board[new_y, new_x] != value:
                new_y, new_x = new_y + ydirection, new_x + xdirection
            else:
                if (curre_y == new_y) and (curre_x != new_x):
                    board[curre_y, curre_x:new_x:np.sign(new_x - curre_x)] = value
                elif (curre_x == new_x) and (curre_y != new_y):
                    board[curre_y:new_y:np.sign(new_y - curre_y), curre_x] = value
                else:
                    board[np.arange(curre_y, new_y, np.sign(new_y - curre_y)), np.arange(curre_x, new_x, np.sign(new_x - curre_x))] = value
                break
    return board

    # print(xdirection,ydirection)


if __name__ == '__main__':
    file_path = 'Training_set/raw'
    file_list = os.listdir(file_path)
    for file in file_list:
        ever_fi_path = os.path.join(file_path, file)
        file_content = open(ever_fi_path).read().split('\n')
        create_one_round_data(file_content)

    # np.savez('train_data_6', state=board_state, action=next_step)  # 6
    # np.savez('train_data_7', state=board_state, action=next_step)  # 7
    # np.savez('train_data', state=board_state, action=next_step)  # 8
    # np.savez('train_data_9',state=board_state,action=next_step)  # 9
    np.savez('train_data_10', state=board_state, action=next_step)
