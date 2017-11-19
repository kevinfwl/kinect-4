from AI import Connect4 as c4

import os
import requests, numpy as np
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__, static_folder='../art')
api = Api(app)

# CONSTANTS
RUN = 201
TRN = 202
INV = 203
WIN = 204

PORT = 5000

# STORAGE
INFO = {
    'state': {'yellow':21, 'red':21, 'turn': 'yellow', 'ai-chance':0, 'game-over': False, 'cursor': 3},
    'game': c4.startGame('alpha beta pruning'), 
    'possible-moves': [],
    'human-moves': [],
    'ai-moves': []
}

# FUN(CTIONS)
# -> Paint grid
def convert_grid(state):
    mapping = {0: 0, -1: 1, 1: 2}
    state = np.array([[mapping[char] for char in line] for line in state])
    print(len(state))
    for i in range (len(state)):
        for j in range (len(state[i])):
            print(j)
            if j == INFO['state']['cursor']:
                print(state[i,j])
                if INFO['state']['turn'] == 'red':
                    state[i,j] += 3
                else:
                    state[i,j] += 6
    return state
# -> Do a player move if it is valid
def tryMove(human_move):
    # retrieve possible moves
    INFO['possible-moves'] = c4.generate_moves(INFO['game'].state)

    # make sure move is valid
    if not (0 <= human_move <= 6): return 'invalid'
    elif INFO['possible-moves'] == []: return 'tie'
    elif human_move not in INFO['possible-moves']: return 'invalid'

    # move is valid, so apply it to state, and indicate that move was successful
    INFO['game'].state = c4.modify_state(INFO['game'].state, human_move, INFO['game'].human)
    return True
# -> Finds the optimal move using Alpha Beta Pruning algo
def findMove():
    # Decide
    INFO['game'] = c4.Connect4(board=INFO['game'].state)
    algorithm = c4.Alpha_Beta_Pruning.Minimax([INFO['game'].nodes, INFO['game'].edges], False)
    ai_move = int(algorithm.path[1][-1])
    # Apply
    INFO['game'].state = c4.modify_state(INFO['game'].state, ai_move, INFO['game'].ai)
# -> update state to reflect 
def endTurn():
    INFO['state'][INFO['state']['turn']] -= 1
    INFO['state']['turn'] = 'red' if INFO['state']['turn'] == 'yellow' else 'yellow'

# CLASSES
# ->
class Cursor(Resource):
    def get(self, direction):
        if INFO['state']['turn'] == 'yellow':
            if(tryMove(INFO['state']['cursor'])):
                endTurn()
                if INFO['game'].evaluate(INFO['game'].state, INFO['game'].human, c4.generate_moves(INFO['game'].state) == 0) == -c4.constant:
                    return convert_grid(INFO['game'].state).tolist(), WIN # human won
                return convert_grid(INFO['game'].state).tolist(), RUN
            else:
                return 'invalid', INV
        return 'AI turn', TRN

    def post(self, direction):
        if direction == 'left':
            if INFO['state']['cursor'] > 0:
                INFO['state']['cursor'] -= 1

        elif direction == 'right':
            if INFO['state']['cursor'] < 6:
                INFO['state']['cursor'] += 1
# -> 
class Board(Resource):
    def get(self, move): # move number doesn't matter
        return convert_grid(INFO['game'].state).tolist(), RUN # game board

    def post(self, move): # make move
        if not INFO['state']['game-over']:
            # AI
            if move == 9:
                if INFO['state']['turn'] == 'red':
                    # Do turn
                    findMove()
                    endTurn()
                    # Check if won
                    if INFO['game'].evaluate(INFO['game'].state, INFO['game'].ai, c4.generate_moves(INFO['game'].state) == 0) == c4.constant:
                        return convert_grid(INFO['game'].state).tolist(), WIN
                    # Update info
                    INFO['human-moves'] = INFO['game'].evaluate(INFO['game'].state, INFO['game'].human, INFO['possible-moves'] == [])
                    INFO['ai-moves'] = INFO['game'].evaluate(INFO['game'].state, INFO['game'].ai, c4.generate_moves(INFO['game'].state) == 0)
                    INFO['state']['ai-chance'] = INFO['ai-moves'] / (INFO['ai-moves'] + INFO['human-moves'])
                    # Send board, AI made move but did not win
                    return convert_grid(INFO['game'].state).tolist(), RUN
                return 'PC turn', TRN
            # Player
            else:
                if INFO['state']['turn'] == 'yellow':
                    if(tryMove(move)):
                        endTurn()
                        if INFO['game'].evaluate(INFO['game'].state, INFO['game'].human, c4.generate_moves(INFO['game'].state) == 0) == -c4.constant:
                            return convert_grid(INFO['game'].state).tolist(), WIN # human won
                        return convert_grid(INFO['game'].state).tolist(), RUN
                    else:
                        return 'invalid', INV
                return 'AI turn', TRN
        return 'Game already over', WIN
# -> 
class Game(Resource):
    def get(self): # grab game info
        return INFO['state']
    
    def put(self): # initialize game
        INFO['state'] = {'yellow':21, 'red':21, 'turn': 'yellow', 'ai-chance':0, 'game-over': False, 'cursor': 3}
        INFO['game'] = c4.startGame('alpha beta pruning')
        INFO['possible-moves'] = []
        INFO['human-moves'] = []
        INFO['ai-moves'] = []
        return '', RUN

# ADDS -> api.add_resource(Resource, urls, endpoint=Resource.__name__.lower())
api.add_resource(Cursor, '/cursor/<string:direction>')
api.add_resource(Board, '/board/<int:move>')
api.add_resource(Game, '/game')

# RUN
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)