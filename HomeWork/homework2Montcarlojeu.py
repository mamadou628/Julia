import numpy as np
from copy import deepcopy

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3))  # 0=vide, 1=Joueur1, 2=Joueur2
        self.current_player = 1  # Joueur1 commence

    def get_legal_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def make_move(self, move):
        i, j = move
        self.board[i, j] = self.current_player
        self.current_player = 3 - self.current_player  # Change de joueur

    def check_winner(self):
        for player in [1, 2]:
            if (np.any(np.all(self.board == player, axis=0)) or
                np.any(np.all(self.board == player, axis=1)) or
                np.all(np.diag(self.board) == player) or
                np.all(np.diag(np.fliplr(self.board)) == player)):
                return player
        return 0  # Pas de gagnant

    def is_terminal(self):
        return self.check_winner() != 0 or len(self.get_legal_moves()) == 0

    def simulate_random_playout(self):
        while not self.is_terminal():
            legal_moves = self.get_legal_moves()
            move = legal_moves[np.random.choice(len(legal_moves))]
            self.make_move(move)
        return self.check_winner()

    def display_board(self):
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        for row in self.board:
            print(' | '.join(symbols[int(cell)] for cell in row))
            print('-' * 9)


class MCTSNode:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.children = []
        self.N = 0
        self.Q = 0
        self.untried_moves = game_state.get_legal_moves()

    def uct_select_child(self, exploration_weight=1.41):
        scores = [
            (child.Q / child.N) + exploration_weight * np.sqrt(np.log(self.N) / child.N)
            for child in self.children
        ]
        return self.children[np.argmax(scores)]

    def add_child(self, move):
        new_game_state = deepcopy(self.game_state)
        new_game_state.make_move(move)
        child = MCTSNode(new_game_state, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, reward):
        self.N += 1
        self.Q += reward


def mcts(root_state, iterations=1000):
    root = MCTSNode(root_state)
    player = root_state.current_player

    for _ in range(iterations):
        node = root

        # 1. Sélection
        while node.untried_moves == [] and node.children != []:
            node = node.uct_select_child()

        # 2. Expansion
        if node.untried_moves != []:
            move = node.untried_moves[np.random.choice(len(node.untried_moves))]
            node = node.add_child(move)

        # 3. Simulation
        game_state = deepcopy(node.game_state)
        winner = game_state.simulate_random_playout()

        # 4. Rétropropagation
        if winner == player:
            reward = 1
        elif winner == 0:
            reward = 0.5
        else:
            reward = 0

        while node is not None:
            node.update(reward)
            node = node.parent

    return max(root.children, key=lambda x: x.N).move


def play_game():
    game = TicTacToe()
    print("Bienvenue au Morpion ! Vous êtes 'X' (Joueur 1).")

    choice = input("tappe q pour sortir").strip().lower()

    if choice == 'q':
        print("Vous avez choisi de quitter le jeu.")
        return  # Quitter la fonction immédiatement (fin du jeu)
    
    while not game.is_terminal():
        game.display_board()
        if game.current_player == 1:
            while True:
                try:
                    move = tuple(map(int, input("Entrez votre coup ligne et colone: ").split(',')))
                    if move in game.get_legal_moves():
                        break
                    else:
                        print("Coup invalide. Réessayez.")
                except:
                    print("Entrée incorrecte. Format attendu : ligne,colonne (ex : 0,2)")
        else:
            print("L'IA réfléchit...")
            move = mcts(game, iterations=1000)

        game.make_move(move)

    game.display_board()
    winner = game.check_winner()
    if winner == 0:
        print("Match nul !")
    else:
        if winner == 1:
            print("Vous avez gagnez")
        else:
            print("vous avez perdu")


def ai_vs_ai():
    game = TicTacToe()
    print("Début d'une partie IA vs IA")

    while not game.is_terminal():
        game.display_board()
        print(f"Joueur {game.current_player} (IA) réfléchit...")
        move = mcts(game, iterations=1000)
        game.make_move(move)

    game.display_board()
    winner = game.check_winner()
    print("Résultat final : ", "Match nul" if winner == 0 else f"Joueur {winner} gagne")


# Lance le jeu
#play_game()
#Pour tester IA vs IA : décommente la ligne ci-dessous
#ai_vs_ai()
