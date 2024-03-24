from flask import Flask, render_template, request
import random

app = Flask(__name__)

board = [' ' for _ in range(9)]
current_player = 'X'
game_over = False

def check_winner(board):
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != ' ':
            return board[i]
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != ' ':
            return board[i]
    if board[0] == board[4] == board[8] != ' ':
        return board[0]
    if board[2] == board[4] == board[6] != ' ':
        return board[2]
    if ' ' not in board:
        return 'tie'
    return None

def get_available_moves(board):
    return [i for i, val in enumerate(board) if val == ' ']

def minimax(board, depth, maximizing_player):
    winner = check_winner(board)

    if winner == 'X':
        return -10
    elif winner == 'O':
        return 10
    elif winner == 'tie':
        return 0

    if maximizing_player:
        max_eval = -float('inf')
        for move in get_available_moves(board):
            board[move] = 'O'
            eval = minimax(board, depth + 1, False)
            board[move] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_available_moves(board):
            board[move] = 'X'
            eval = minimax(board, depth + 1, True)
            board[move] = ' '
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move(board):
    best_move = -1
    best_eval = -float('inf')
    for move in get_available_moves(board):
        board[move] = 'O'
        eval = minimax(board, 0, False)
        board[move] = ' '
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

def play_ai():
    global board, current_player, game_over

    if not game_over and current_player == 'O':
        move = get_best_move(board)
        board[move] = current_player

        winner = check_winner(board)
        if winner:
            game_over = True

        current_player = 'X'

@app.route('/')
def index():
    play_ai()
    return render_template('index.html', board=board, current_player=current_player, game_over=game_over, winner=check_winner(board))

@app.route('/move', methods=['POST'])
def move():
    global board, current_player, game_over

    position = int(request.form['position'])

    if board[position] == ' ' and not game_over and current_player == 'X':
        board[position] = current_player
        winner = check_winner(board)
        if winner:
            game_over = True
        current_player = 'O'
        play_ai() 
    return index()

@app.route('/reset')
def reset():
    global board, current_player, game_over
    board = [' ' for _ in range(9)]
    current_player = 'X'
    game_over = False
    return index()

if __name__ == '__main__':
    app.run(debug=True)
