# Moses Muwanga
# https://web.archive.org/web/20191205024932/http://people.scs.carleton.ca/~arunka/courses/comp1405/assignments/a5/


def readLevel(n):
    '''This function takes an integer as argument representing the level number, 
    reads the appropriate game board from file and returns the gameboard as a 2D list of symbols (strings).'''

    try:
        # Open the file, read the lines, and close the file
        level = open('./ascii_levels/ascii_level' + str(n) + '.txt', 'r')
        # Create an empty list to store the gameboard
        gameboard = []
        # Read each line of the files as a list of strings
        level_lines = level.readlines()

        # Add the characters from each line to a list, then those lists to the gameboard
        for i in level_lines:

            # Remove trailing '\n' from each line
            separate = i.strip('\n')

            # Create a list with each symbol as an element
            new_list = []
            for character in separate:
                new_list.append(character)

            # Append the list to the gameboard
            gameboard.append(new_list)

        # Close the file
        level.close()

        # Return the gameboard
        return gameboard

    except:
        print(f"Failed to read level {n}. Game Over")
        exit()


def displayBoard(lis):
    '''This function takes a gameboard as argument and 
    displays the board to the console including row and column labels.'''

    # Create the column based on the amount of symbols in the level
    columns = ''
    length = len(lis[0])

    # Make the values from 0 - 9
    for j in range(length):
        if j >= 30:
            columns += str(j - 30)
        elif j >= 20:
            columns += str(j - 20)
        elif j >= 10:
            columns += str(j - 10)
        else:
            columns += str(j)

    # Print the gameboard for the given level
    print('    ', columns)
    print('    ', '-' * len(columns))

    sym = ''
    for i in range(len(lis)):
        for k in lis[i]:
            sym += k
        if i <= 9:
            print(f"0{i} | {sym}")
        else:
            print(f"{i} | {sym}")
        sym = ''


def getUserAction(height, width):
    '''This function takes two integers as argument representing the height and width of the game board.
    Then prompts the user for their action, ensures it is valid, and returns the action as a list containing 
    the user's symbol, row, and column inputs.'''

    # Ask the user to enter a symbol and ensure that it is valid
    symbol = input('Enter a symbol: ')
    if symbol == '@' or symbol == '#' or symbol == '%' or symbol == '&':
        valid = True
    else:
        valid = False

    # If the user enters an invalid symbol, ask them again
    while valid == False:
        print('Sorry, please select one of: # & % @')
        symbol = input('Enter a symbol: ')
        if symbol == '@' or symbol == '#' or symbol == '%' or symbol == '&':
            valid = True
        else:
            valid = False

    # Ask the user to enter a row and ensure that it is valid
    while True:
        try:
            row = int(input(f'Select a row [0,{height - 1}]: '))
        except:
            print(f'Error bad row. Enter a number from 0 to {height - 1}.')
            continue
        if row in range(0, height):
            break
        else:
            print(f'Error bad row. Enter a number from 0 to {height - 1}.')

    # Ask the user to enter a column and ensure that it is valid
    while True:
        try:
            column = int(input(f'Select a col [0,{width - 1}]: '))
        except:
            print(f'Error bad column. Enter a number from 0 to {width - 1}.')
            continue
        if column in range(0, width):
            break
        else:
            print(f'Error bad column. Enter a number from 0 to {width - 1}.')

    return [symbol, row, column]


def fill(gameboard, target_symbol, user_symbol, row, column):
    '''This function mutates the input gameboard so that all contiguous symbols matching
    the inputted target symbol should be replaced with the inputted user's symbol.'''

    # if the target is the same as the user, do nothing
    if target_symbol == user_symbol:
        return

    # if the its out of bounds, do nothing
    if len(gameboard) - 1 < row or len(gameboard[0]) - 1 < column or row < 0 or column < 0:
        return

    # if the target is not equal to what is in the gameboard, do nothing
    if target_symbol != gameboard[row][column]:
        return

    # If the users symbol is the same as the one on the gameboard, do nothing
    if user_symbol == gameboard[row][column]:
        return

    # Change the symbol in the gameboard with the users symbol
    gameboard[row][column] = user_symbol

    # Fill all adjacent board cells with the symbol by recursively applying this fill to them.
    fill(gameboard, target_symbol, user_symbol, row, column + 1)
    fill(gameboard, target_symbol, user_symbol, row, column - 1)
    fill(gameboard, target_symbol, user_symbol, row + 1, column)
    fill(gameboard, target_symbol, user_symbol, row - 1, column)


def check(lis):
    '''This function checks to see if all possible moves have been made'''

    first_row = lis[0][0]
    for i in lis:
        for j in i:
            if j != first_row:
                return False

    return True


def main():
    '''This function orchestrates the core behaviour of the game.'''

    # Initialize the level and amount of moves the player has made
    level = 1
    total_moves = 0

    # Flag to play the game
    play = True

    # Playing the game
    while play:

        # Play 5 levels
        while level <= 5:

            # Get the symbols to fill the board, depending on the level
            game_symbols = readLevel(level)
            # Get the height of the gameboard
            height = len(game_symbols)
            # Get the width of the gameboard
            width = len(game_symbols[0])

            # Initialize the amount of moves done in the level
            level_moves = 0
            # Check to see if the all the switches have been made
            checker = check(game_symbols)

            # Make the switches
            while checker == False:

                # Show the gameboard
                displayBoard(game_symbols)
                # Get the users input
                actions = getUserAction(height, width)
                user_symbol = actions[0]
                target_symbol = game_symbols[actions[1]][actions[2]]
                row = actions[1]
                column = actions[2]
                switch = fill(game_symbols, target_symbol,
                              user_symbol, row, column)

                # Check to see if more switches can be made
                checker = check(game_symbols)

                # Add a move
                level_moves += 1

            # Report the users resaults for each level
            print(f'Level {level} Completed in {level_moves} moves!')
            print()
            print()

            # Sum up the total amount of moves it took the user
            total_moves += level_moves

            # Go to the next level
            level += 1

        # Report the resaults of the game
        print('You Win! Thanks for playing!')
        print(f'Total moves: {total_moves}')

        # Ask the user if they would like to play again, restart if 'y', stop if 'n'
        while True:
            play_again = input('Would you like to play again? (y/n): ')
            if play_again == 'y':
                break
            elif play_again == 'n':
                exit()
            else:
                print("")
                print('Please enter "y" or "n".')
                print("")

        main()


main()
