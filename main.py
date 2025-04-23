import random

player_board = [[]]
computer_board = [[]]
checked = []

def create_board_from_file(file_path):
    global computer_board, player_board
    with open(file_path, encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
        board_size = int(lines[0])
        player_board = [l.split() for l in lines[1:board_size + 1]]
        computer_board = [l.split() for l in lines[board_size + 1:2 * board_size + 1]]

def create_random_board(board_size):
    global computer_board, player_board
    board_alphabet = [chr(i) for i in range(ord('A'), ord('A') + board_size**2)]
    random.shuffle(board_alphabet)
    player_board = [board_alphabet[i:i + board_size] for i in range(0, len(board_alphabet), board_size)]
    random.shuffle(board_alphabet)
    computer_board = [board_alphabet[i:i + board_size] for i in range(0, len(board_alphabet), board_size)]

def boards_to_string(hide_comp=True):
    s = ''
    s+='[Player]\t\t\t\t\t[Computer]\n'
    for i in range(len(player_board)):
        for j in range(len(player_board)):
            s += '+---'
        s+='+\t\t\t\t\t'
        for j in range(len(computer_board)):
            s += '+---'
        s += '+\n'

        for j in range(len(player_board)):
            s += '| '+player_board[i][j] + ' '
        s += '|\t\t\t\t\t'
        for j in range(len(computer_board)):
            if computer_board[i][j] in checked:
                s += '| # '
            elif hide_comp:
                s += f'|   '
            else:
                s += '| ' + computer_board[i][j] + ' '
        s += '|\n'

    for j in range(len(player_board)):
        s += '+---'
    s += '+\t\t\t\t\t'
    for j in range(len(computer_board)):
        s += '+---'
    s += '+\n'
    return s

def check_bingo(board):
    for row in board:
        if all(x in checked for x in row):
            return True
    for col in range(len(board)):
        if all(board[row][col] in checked for row in range(len(board))):
            return True
    if all(board[i][i] in checked for i in range(len(board))):
        return True
    if all(board[i][len(board)-1-i] in checked for i in range(len(board))):
        return True
    return False

def get_player_choice():
    while True:
        c = input('Your Choice: ')
        if len(c)==1 and c not in checked and ord('A')<=ord(c)<ord('A')+len(player_board)**2:
            mark_board(player_board, c)
            return c
        print('Invalid input. Try again.')

def get_computer_choice():
    c = random.choice([chr(i) for i in range(ord('A'), ord('A') + len(computer_board)**2)])
    while c in checked:
        c = random.choice([chr(i) for i in range(ord('A'), ord('A') + len(computer_board)**2)])
    mark_board(computer_board, c)
    return c

def mark_board(board, choice):
    global checked, computer_board, player_board
    checked.append(choice)
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == choice:
                board[i][j] = '#'
                return True
    return False

if __name__ == '__main__':
    mode = input('Select mode (1: Random, 2: File): ')
    if mode == '1':
        board_size = int(input('Enter board size (3~5): '))
        while board_size<3 or board_size>5:
            print('Invailid input. Enter 3 to 5.')
            board_size = int(input('Enter board size (3~5): '))
        create_random_board(board_size)
    elif mode == '2':
        file_path = input('Enter file path: ')
        create_board_from_file(file_path)
    else:
        print('Invalid mode selected.')