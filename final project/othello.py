from board import Board
import player


# Game
class Game(object):
    def __init__(self):
        self.board = Board()
        self.current_player = None

    # Generate two players
    def make_two_players(self):
        ps = input("Please select two player's type:\n\t0.Human\n\t1.AI\nSuch as:0 0\n:")
        p1, p2 = [int(p) for p in ps.split(' ')]
        if p1 == 1 or p2 == 1:  # Select AI player
            level_ix = int(
                input("Please select the level of AI player.\n\t1: intermediate\n\t2: advanced\n:"))
            if p1 == 0:
                player1 = player.HumanPlayer('X')
                player2 = player.AIPlayer('O', level_ix)
            elif p2 == 0:
                player1 = player.AIPlayer('X', level_ix)
                player2 = player.HumanPlayer('O')
            else:
                player1 = player.AIPlayer('X', level_ix)
                player2 = player.AIPlayer('O', level_ix)
        else:
            player1, player2 = player.HumanPlayer('X'), player.HumanPlayer('O')  # p2p, x goes first

        return player1, player2

    # switch player
    def switch_player(self, player1, player2):
        if self.current_player is None:
            return player1
        else:
            return [player1, player2][self.current_player == player1]

    # print winner
    def print_winner(self, winner):  # winner in [0,1,2]
        print(['Winner is player1', 'Winner is player2', 'Draw'][winner])

    # run game
    def run(self):

        player1, player2 = self.make_two_players()

        print('\nGame start!\n')
        self.board.print_b()  # initial board
        while True:
            self.current_player = self.switch_player(player1, player2)  # switch to current player

            action = self.current_player.think(self.board)  # get current player action

            print("Best Action：", action)
            # print("The coordinate starts with 0, so the row is", action[0] + 1, "the column is ", action[1] + 1)
            if action is not None:
                self.current_player.move(self.board, action)  # current player move

            self.board.print_b()  # current board

            if self.board.teminate():  # if game terminate
                winner = self.board.get_winner()  # get winner 0,1,2
                break
        self.print_winner(winner)
        print('Game over!')

        # self.board.print_history()


if __name__ == '__main__':
    Game().run()
