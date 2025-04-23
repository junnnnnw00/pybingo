import random
import time

# global variables
checked = []
LOG_PATH = 'result.txt'

# create boards from file
def create_board_from_file(file_path):
    with open(file_path, encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    size = int(lines[0])
    player_board = [l.split() for l in lines[1:size + 1]]
    computer_board = [l.split() for l in lines[size + 1:2 * size + 1]]
    return player_board, computer_board, size

# create random boards
def create_random_board(size):
    board_alphabet = [chr(i) for i in range(ord('A'), ord('A') + size**2)]
    random.shuffle(board_alphabet)
    player_board = [board_alphabet[i:i + size] for i in range(0, len(board_alphabet), size)]
    random.shuffle(board_alphabet)
    computer_board = [board_alphabet[i:i + size] for i in range(0, len(board_alphabet), size)]
    return player_board, computer_board, size

# print the boards
def boards_to_string(player_board, computer_board, size, hide_comp=True):
    s = ''
    s+='[Player]\t\t\t\t\t[Computer]\n'
    for i in range(size):
        for j in range(size):
            s += '+---'
        s+='+\t\t\t\t\t'
        for j in range(size):
            s += '+---'
        s += '+\n'

        for j in range(size):
            s += '| '+player_board[i][j] + ' '
        s += '|\t\t\t\t\t'
        for j in range(size):
            if computer_board[i][j] == '#':
                s += '| # '
            elif hide_comp:
                s += '|   '
            else:
                s += '| ' + computer_board[i][j] + ' '
        s += '|\n'

    for j in range(size):
        s += '+---'
    s += '+\t\t\t\t\t'
    for j in range(size):
        s += '+---'
    s += '+\n'
    return s

# wirte log file
def write_log(text):
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

# mark the board     
def mark_board(board, choice, size):
    global checked
    checked.append(choice)
    for i in range(size):
        for j in range(size):
            if board[i][j] == choice:
                board[i][j] = '#'
                return True
    return False

# check if there is a bingo
def check_bingo(board, size):
    # check rows and columns
    for i in range(size):
        if all(board[i][j]=='#' for j in range(size)): return True
        if all(board[j][i]=='#' for j in range(size)): return True
    # check diagonals
    if all(board[i][i]=='#' for i in range(size)): return True
    if all(board[i][size-1-i]=='#' for i in range(size)): return True
    return False

# check if the character is valid
def valid_character(c, size):
    c=c.upper() # convert to uppercase
    return (
        len(c) == 1 and
        ord('A')<=ord(c)<ord('A')+size**2 and
        c not in checked
    )
    
# get valid player choice
def get_player_choice(board, size):
    while True:
        choice = input('Enter your choice: ')
        if valid_character(choice, size):
            return choice
        print('Invalid choice. Try again.')

# get random computer choice
def get_computer_choice(board, size):
    # get all valid choices computer can make
    remainding = [
        board[i][j] for i in range(size) for j in range(size) if board[i][j] not in checked
    ]
    return random.choice(remainding)


def main():
    # initialize game
    global checked
    checked = []
    open(LOG_PATH, 'w').close()  # clear log file
    
    # create boards
    mode = input('Select mode (1: Random, 2: File): ')
    while mode not in ['1', '2']:
        print("Invalid input. Enter 1 or 2.")
        mode = input('Select mode (1: Random, 2: File): ')
    if mode == '1':
        size = int(input('Enter board size: '))
        while size not in [3, 4, 5]:
            print("Invalid input. Enter 3 to 5.")
            size = int(input("Enter board size (3~5): "))
        player_board, computer_board, size = create_random_board(size)
    else:
        file_path = input('Enter file path: ')
        player_board, computer_board, size = create_board_from_file(file_path)
    
    # first print the boards
    print('\n'+boards_to_string(player_board, computer_board, size)+'\n')
    write_log(boards_to_string(player_board, computer_board, size, False))
    
    # game loop
    while True:
        # player turn
        player_choice = get_player_choice(player_board, size)
        mark_board(player_board, player_choice, size)
        mark_board(computer_board, player_choice, size)

        # print the boards
        print('\n'+boards_to_string(player_board, computer_board, size)+'\n')
        write_log(f"Player's choice: {player_choice}\n")
        write_log(boards_to_string(player_board, computer_board, size, False))

        # check for win
        player_bingo = check_bingo(player_board, size)
        computer_bingo = check_bingo(computer_board, size)
        if player_bingo or computer_bingo:
            break

        # computer turn
        time.sleep(0.5)
        computer_choice = get_computer_choice(computer_board, size)
        print(f"Computer's choice: {computer_choice}")
        mark_board(computer_board, computer_choice, size)
        mark_board(player_board, computer_choice, size)
        
        # print the boards
        print('\n'+boards_to_string(player_board, computer_board, size)+'\n')
        write_log(f"Computer's choice: {computer_choice}\n")
        write_log(boards_to_string(player_board, computer_board, size, False))

        # check for win
        player_bingo = check_bingo(player_board, size)
        computer_bingo = check_bingo(computer_board, size)
        if player_bingo or computer_bingo:
            break
        
    # print result
    if player_bingo and computer_bingo: result = "Draw!"
    elif player_bingo: result = "You win!"
    elif computer_bingo: result = "Computer wins!"
    
    print('\n'+result+'\n')
    write_log('\n'+result+'\n')
        
if __name__ == '__main__':
    main()