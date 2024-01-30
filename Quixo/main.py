import random
from matplotlib import pyplot as plt
import numpy as np
from game import Game, Move, Player


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MinMax(Player):
    def __init__(self, game: 'Game') -> None:
        super().__init__()
        self.game = game

    def fitness(self, game, maximizingPlayer: bool):
        player = 1 if maximizingPlayer else 0
        opponent = 1 - player
        
        player_score = self.calculate_score(game, player)
        opponent_score = self.calculate_score(game, opponent)

        return player_score - opponent_score

    def calculate_score(self, game, player):
        row_max = max(self.get_point_in_line(row, player) for row in game._board)
        col_max = max(self.get_point_in_line(col, player) for col in game._board.T)
        diag_max = max(self.get_point_in_line(np.diag(game._board), player),
                    self.get_point_in_line(np.diag(np.fliplr(game._board)), player))

        return max(row_max, col_max, diag_max)

    def get_point_in_line(self, line, player):
        current_count = 0

        for element in line:
            if element == player:
                current_count += 1
            
        return current_count
    
    def count_consecutive(self, line, player):  
        count = 0
        max_count = 0
        for cell in line:
            if cell == player:
                count += 1
                max_count = max(max_count, count)
            else:
                count = 0
        return max_count


    def minmax(self, game: 'Game', depth, alpha, beta, maximizingPlayer):
        if depth == 0 or game.check_winner() != -1:
            return self.fitness(game, maximizingPlayer), alpha, beta

        player = 1 if maximizingPlayer else 0
        possible_moves = game.possible_moves(player)

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in possible_moves:
                child = game.create_new_state(move[0], move[1], player)

                eval, alpha, beta = self.minmax(child, depth-1, alpha, beta, False)

                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    break
            return maxEval, alpha, beta
        else:
            minEval = float('inf')
            for move in possible_moves:
                child = game.create_new_state(move[0], move[1], player)
                eval, alpha, beta = self.minmax(child, depth-1, alpha, beta, True)

                minEval = min(minEval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    break
            return minEval, alpha, beta


    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        best_movement = None
        global_eval = float('-inf')

        player = self.game.get_current_player()
        possible_moves = game.possible_moves(player)
        
        random.shuffle(possible_moves)
       
        for move in possible_moves:
            child = self.game.create_new_state(move[0], move[1], player)

            if child.check_winner() == player:
                best_movement = move
                break


            eval, _, _ = self.minmax(child, 4, float('-inf'), float('inf'), player)

            if eval > global_eval:
                global_eval = eval
                best_movement = move
        
        return best_movement
    

if __name__ == '__main__':
    count_0 = 0
    count_1 = 0

    for i in range(100):
        game = Game()

        player1 = RandomPlayer()
        player2 = MinMax(game)
        
        winner = game.play(player1, player2)

        if winner == 0:
            count_0 += 1
        else:
            count_1 += 1

        print(f"{i+1} -> First Player won {count_0} matches")
        print(f"{i+1} -> Second Player won {count_1} matches\n")

