import numpy as np


class Board(object):
    def __init__(self):
        self.empty = '.'
        self._board = [[self.empty for _ in range(9)] for _ in range(9)] # 规格：8*8
        self._board[4][5], self._board[5][4] = 'X', 'X'
        self._board[4][4], self._board[5][5] = 'O', 'O'

    def __getitem__(self, index):
        return self._board[index]

    def get_matrix(self):
        board1 = self._board
        b_array = []
        for i in range(9):
            for j in range(9):
                if board1[i][j] == 'X':
                    b_array.append(1)
                elif board1[i][j] == 'O':
                    b_array.append(-1)
                else:
                    b_array.append(0)
        b_array_mx = np.reshape(np.array(b_array), [9, 9])
        return b_array_mx

    def print_b(self):
        board = self._board
        print(' ', ' '.join(list('ABCDEFGHI')))
        for i in range(9):
            print(str(i+1),' '.join(board[i]))

    def teminate(self):
        list1 = list(self.get_legal_actions('X'))
        list2 = list(self.get_legal_actions('O'))
        return [False, True][len(list1) == 0 and len(list2) == 0]

    def get_winner(self):
        s1, s2 = 0, 0
        for i in range(9):
            for j in range(9):
                if self._board[i][j] == 'X':
                    s1 += 1
                if self._board[i][j] == 'O':
                    s2 += 1
        if s1 > s2:
            return 0
        elif s1 < s2:
            return 1
        elif s1 == s2:
            return 2

    def _move(self, action, color):
        x, y = action
        self._board[x][y] = color

        return self._flip(action, color)

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

    def _unmove(self, action, flipped_pos, color):
        self._board[action[0]][action[1]] = self.empty

        uncolor = ['X', 'O'][color == 'X']
        for p in flipped_pos:
            self._board[p[0]][p[1]] = uncolor

    def _get_lines(self, action):
        board_coord = [(i, j) for i in range(9) for j in range(9)]

        r, c = action
        ix = r * 9 + c
        r, c = ix // 9, ix % 9
        left = board_coord[r * 9:ix]
        right = board_coord[ix + 1:(r + 1) * 9]
        top = board_coord[c:ix:9]
        bottom = board_coord[ix + 9:9 * 9:9]

        if r <= c:
            lefttop = board_coord[c - r:ix:10]
            rightbottom = board_coord[ix + 10:(8 - (c - r)) * 9 + 8 + 1:10]
        else:
            lefttop = board_coord[(r - c) * 9:ix:10]
            rightbottom = board_coord[ix + 10:8 * 9 + (8 - (c - r)) + 1:10]

        if r + c <= 8:
            leftbottom = board_coord[ix + 8:(r + c) * 9:8]
            righttop = board_coord[r + c:ix:7]
        else:
            leftbottom = board_coord[ix + 8:8 * 9 + (r + c) - 8 + 1:8]
            righttop = board_coord[((r + c) - 8) * 9 + 8:ix:8]

        left.reverse()
        top.reverse()
        lefttop.reverse()
        righttop.reverse()
        lines = [left, top, lefttop, righttop, right, bottom, leftbottom, rightbottom]
        return lines

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

    def get_legal_actions(self, color):
        uncolor = ['X', 'O'][color == 'X']
        uncolor_near_points = []

        board = self._board
        for i in range(9):
            for j in range(9):
                if board[i][j] == uncolor:
                    for dx, dy in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
                        x, y = i + dx, j + dy
                        if 0 <= x <= 8 and 0 <= y <= 8 and board[x][y] == self.empty and (
                        x, y) not in uncolor_near_points:
                            uncolor_near_points.append((x, y))
        for p in uncolor_near_points:
            if self._can_fliped(p, color):
                yield p


if __name__ == '__main__':
    board = Board()
    board.print_b()
    print(list(board.get_legal_actions('X')))