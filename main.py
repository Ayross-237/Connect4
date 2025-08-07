from typing import Optional
from support import *


def generate_initial_board() -> list[str]:
    """Creates and returns an empty board to play on.

    Returns:
        list[str]: The empty board.
    """
    return BOARD_SIZE * [BOARD_SIZE*BLANK_PIECE]


def is_column_full(column: str) -> bool:
    """Checks whether the selected column is full.

    Parameters:
        column(str): The column being checked.

    Returns:
        bool: True if column is full, False otherwise.

    Preconditions:
        column is a valid column state.
    """
    return column[0] != BLANK_PIECE


def is_column_empty(column: str) -> bool:
    """Checks whether the selected column is empty.

    Parameters:
        column(str): The column being checked.

    Returns:
        bool: True if column is empty, False otherwise.
    
    Preconditions:
        column is a valid column state.
    """
    return column[-1] == BLANK_PIECE


def display_board(board: list[str]) -> None:
    """Displays the current state of the board.

    Parameters:
        board(list[str]): The board being displayed.

    Preconditions:
        board and the strings inside board are all of length BOARD_SIZE.
    """
    column_label = COLUMN_NUMBER_SEPARATOR
    
    for i in range(BOARD_SIZE):
        column_label += str(i+1) + COLUMN_NUMBER_SEPARATOR
        row = COLUMN_SEPARATOR
        
        for j in range(BOARD_SIZE):
            row += board[j][i] + COLUMN_SEPARATOR
        print(row)
        
    print(column_label)


def check_input(command: str) -> bool:
    """Checks whether the entered input is a valid command.

    Parameters:
        command(str): The command the user is trying to execute.

    Returns:
        bool: True if a valid command has been entered, False otherwise.
        
    Preconditions:
        The column number entered by the user when using the a or r commands
        will be a positive, single-digit integer.

    """
    valid_input_type = ((command in VALID_COMMANDS[4:] and len(command) == 1)
                        or (len(command) == 2
                            and command[0] in VALID_COMMANDS[:4]
                            and command[1].isnumeric()
                            )
                        )

    valid_column_number = (len(command) == 2
                           and valid_input_type
                           and int(command[1]) in range (1, BOARD_SIZE + 1)
                           )

    if valid_column_number or valid_input_type and len(command) == 1:
        return True
    elif valid_input_type:
        print(INVALID_COLUMN_MESSAGE)
    else:
        print(INVALID_FORMAT_MESSAGE)
    return False


def get_action() -> str:
    """Repeatedly prompts for input until the user enters a valid command.

    Returns:
        str: The first valid command that the user enters.
    """
    while True:
        command = input(ENTER_COMMAND_MESSAGE)
        if check_input(command):
            return command


def add_piece(board: list[str], piece: str, column_index: int) -> bool:
    """Adds the chosen piece to the chosen board and column, so long as the
       column is not full.

    Parameters:
        board(list[str]): The board to add the piece to.
        piece(str): The piece to be added.
        column_index(int): The column to add the piece to.

    Returns:
        bool: True if a piece has been added, False otherwise.

    Preconditions:
        board represents a valid game state.
        board and the strings inside board are all of length BOARD_SIZE.
        column_index is a valid index for board (0-indexed).
        piece is of length 1.
    """
    if is_column_full(board[column_index]):
        print(FULL_COLUMN_MESSAGE)
        return False
    
    i = 1
    while i < BOARD_SIZE:
        if board[column_index][i] != BLANK_PIECE:
            break
        i += 1
        
    board[column_index] = (i-1)*BLANK_PIECE + piece + board[column_index][i:]   
    return True


def remove_piece(board: list[str], column_index: int) -> bool:
    """Removes the bottom piece from the chosen board and column, so long as
    the column is not empty.

    Parameters:
        board(list[str]): The board to remove the piece from.
        column_index(int): The column to remove the piece from.

    Returns:
        bool: True if a piece has been removed, False otherwise.

    Preconditions:
        board represents a valid game state.
        board and the strings inside board are all of length BOARD_SIZE.
        column_index is a valid index for board (0-indexed).
    """
    if is_column_empty(board[column_index]):
        print(EMPTY_COLUMN_MESSAGE)
        return False

    board[column_index] = BLANK_PIECE + board[column_index][:-1]
    return True

    
def check_win(board: list[str]) -> Optional[str]:
    """Checks the current board to see if there are an adequate number of
       connnected pieces. If so, returns a string stating whether player one
       won, player two won or the game was drawn.

    Parameters:
        board(list[str]): The board to be checked.

    Returns:
        str: If a player has won the game, their piece is returned, if it is
             a draw, the blank piece is returned.
        None: If the game has not been won or drawn yet.

    Preconditions:
        board represents a valid game state.
        board and the strings inside board are all of length BOARD_SIZE.
    """
    player_one_win = False
    player_two_win = False
    
    # loops through every piece in the board
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            test_piece = board[i][j]
            [a, b, c, d] = [1, 1, 1, 1] # setting counting variables
            
            if test_piece != BLANK_PIECE:
                # vertical test (upwards)
                if j in range(REQUIRED_WIN_LENGTH - 1, BOARD_SIZE):
                    while j-a >= 0 and board[i][j-a] == test_piece:
                        a += 1

                if i in range(REQUIRED_WIN_LENGTH - 1, BOARD_SIZE):
                    # horizontal test (left)
                    while i-b >= 0 and board[i-b][j] == test_piece:
                        b += 1
                    # diagonal upwards test (left and up)
                    if j in range(REQUIRED_WIN_LENGTH - 1, BOARD_SIZE):
                        while j-c >= 0 and board[i-c][j-c] == test_piece:
                            c += 1
                    # diagonal downwards test (left and down)
                    if j in range(0, BOARD_SIZE - (REQUIRED_WIN_LENGTH - 1)):
                        while j+d <= 7 and board[i-d][j+d] == test_piece:
                            d += 1

            # checks whether any of the tests found a connection greater than
            # or equal to REQUIRED_WIN_LENGTH
            for k in [a, b, c, d]:
                if k >= REQUIRED_WIN_LENGTH and test_piece == PLAYER_1_PIECE:
                    player_one_win = True
                elif k >= REQUIRED_WIN_LENGTH:
                    player_two_win = True

    if player_one_win and player_two_win:
        return BLANK_PIECE
    elif player_one_win:
        return PLAYER_1_PIECE
    elif player_two_win:
        return PLAYER_2_PIECE


def play_game() -> None:
    """Plays a single game of connect 4 from start to finish.
    """
    pieces = [PLAYER_2_PIECE, PLAYER_1_PIECE]
    result_messages = {
        PLAYER_1_PIECE: PLAYER_1_VICTORY_MESSAGE,
        PLAYER_2_PIECE: PLAYER_2_VICTORY_MESSAGE,
        BLANK_PIECE: DRAW_MESSAGE
    }
    board = generate_initial_board()
    player_one_turn = True
    game_finished = False
    winner = None
    
    display_board(board)
    
    while not game_finished:
        board_modified = False
        if player_one_turn:
            print(PLAYER_1_MOVE_MESSAGE)
        else:
            print(PLAYER_2_MOVE_MESSAGE)

        # gets and executes a command from the user
        while not board_modified:
            command = get_action()
            if command in VALID_COMMANDS[4:6]:
                print(HELP_MESSAGE)
                break
            elif command in VALID_COMMANDS[6:]:
                game_finished = True
                break
            elif command[0] in VALID_COMMANDS[:2]:
                board_modified = add_piece(board, pieces[player_one_turn],
                                             int(command[1])-1)
            else:
                board_modified = remove_piece(board, int(command[1])-1)

        # ensures the board is not displayed again if the user uses a quit
        # command
        if game_finished:
            break

        winner = check_win(board)
        if winner:
            game_finished = True

        # ensures it does not become the other player's turn if a help command
        # is used
        if board_modified:
            player_one_turn = not player_one_turn

        display_board(board)

    if winner:
        print(result_messages[winner])

        
def main() -> None:
    """The main function; continually plays games of connect 4 until the user
       decides to stop.
    """
    play = CONTINUE_COMMANDS[0]
    while play in CONTINUE_COMMANDS and len(play) == 1:
        play_game()
        play = input(CONTINUE_MESSAGE)
        
    
if __name__ == "__main__":
    main()
