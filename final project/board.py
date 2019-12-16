import numpy as np


# build board
class Board(object):
    def __init__(self):
        self.empty = '.'
        self._board = [[self.empty for _ in range(8)] for _ in range(8)]  # size：8*8
        self._board[3][4], self._board[4][3] = 'X', 'X'
        self._board[3][3], self._board[4][4] = 'O', 'O'
        # print(self._board)

    # Board[][]
    def __getitem__(self, index):
        return self._board[index]

    def get_matrix(self):
        board1 = self._board
        b_array = []
        for i in range(8):
            for j in range(8):
                if board1[i][j] == 'X':
                    b_array.append(1)
                elif board1[i][j] == 'O':
                    b_array.append(-1)
                else:
                    b_array.append(0)
        b_array_mx = np.reshape(np.array(b_array), [8, 8])
        return b_array_mx
        # print(b_array_mx)

    # print board
    def print_b(self):
        board = self._board
        print(' ', ' '.join(list('ABCDEFGH')))
        for i in range(8):
            print(str(i + 1), ' '.join(board[i]))

    # board terminate
    def teminate(self):
        list1 = list(self.get_legal_actions('X'))
        list2 = list(self.get_legal_actions('O'))
        return [False, True][len(list1) == 0 and len(list2) == 0]

    # get winner
    def get_winner(self):
        s1, s2 = 0, 0
        for i in range(8):
            for j in range(8):
                if self._board[i][j] == 'X':
                    s1 += 1
                if self._board[i][j] == 'O':
                    s2 += 1
        if s1 > s2:
            return 0  # X wins
        elif s1 < s2:
            return 1  # O wins
        elif s1 == s2:
            return 2  # draw

    # move
    def _move(self, action, color):
        x, y = action
        self._board[x][y] = color

        return self._flip(action, color)

    # filp
    def _flip(self, action, color):
        flipped_pos = []

        for line in self._get_lines(action):
            for i, p in enumerate(line):
                if self._board[p[0]][p[1]] == self.empty:
                    break
                elif self._board[p[0]][p[1]] == color:
                    flipped_pos.extend(line[:i])
                    break

        for p in flipped_pos:
            self._board[p[0]][p[1]] = color

        return flipped_pos

    # undo
    def _unmove(self, action, flipped_pos, color):
        self._board[action[0]][action[1]] = self.empty

        uncolor = ['X', 'O'][color == 'X']
        for p in flipped_pos:
            self._board[p[0]][p[1]] = uncolor

    # turn rules
    def _get_lines(self, action):

        board_coord = [(i, j) for i in range(8) for j in range(8)]

        r, c = action
        ix = r * 8 + c
        r, c = ix // 8, ix % 8
        left = board_coord[r * 8:ix]  # turn
        right = board_coord[ix + 1:(r + 1) * 8]
        top = board_coord[c:ix:8]  # reverse
        bottom = board_coord[ix + 8:8 * 8:8]

        if r <= c:
            lefttop = board_coord[c - r:ix:9]  # reverse
            rightbottom = board_coord[ix + 9:(7 - (c - r)) * 8 + 7 + 1:9]
        else:
            lefttop = board_coord[(r - c) * 8:ix:9]  # reverse
            rightbottom = board_coord[ix + 9:7 * 8 + (7 - (c - r)) + 1:9]

        if r + c <= 7:
            leftbottom = board_coord[ix + 7:(r + c) * 8:7]
            righttop = board_coord[r + c:ix:7]  # reverse
        else:
            leftbottom = board_coord[ix + 7:7 * 8 + (r + c) - 7 + 1:7]
            righttop = board_coord[((r + c) - 7) * 8 + 7:ix:7]  # reverse

        left.reverse()
        top.reverse()
        lefttop.reverse()
        righttop.reverse()
        lines = [left, top, lefttop, righttop, right, bottom, leftbottom, rightbottom]
        return lines

    # check turn of chess pieces
    def _can_fliped(self, action, color):
        flipped_pos = []

        for line in self._get_lines(action):
            for i, p in enumerate(line):
                if self._board[p[0]][p[1]] == self.empty:
                    break
                elif self._board[p[0]][p[1]] == color:
                    flipped_pos.extend(line[:i])
                    break
        return [False, True][len(flipped_pos) > 0]

    # legal action
    def get_legal_actions(self, color):
        uncolor = ['X', 'O'][color == 'X']  # opposite color
        uncolor_near_points = []  #

        board = self._board
        for i in range(8):
            for j in range(8):
                if board[i][j] == uncolor:
                    for dx, dy in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
                        x, y = i + dx, j + dy
                        if 0 <= x <= 7 and 0 <= y <= 7 and board[x][y] == self.empty and (
                                x, y) not in uncolor_near_points:
                            uncolor_near_points.append((x, y))
        for p in uncolor_near_points:
            if self._can_fliped(p, color):
                yield p


if __name__ == '__main__':
    board = Board()
    board.print_b()
    board.get_matrix()
    print(list(board.get_legal_actions('X')))
