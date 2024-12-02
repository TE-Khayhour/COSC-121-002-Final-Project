import json
import sys
import time
from copy import deepcopy

import pygame
from pygame.locals import *

from logic import *

# set up pygame for main gameplay
pygame.init()
c = json.load(open("constants.json", "r"))
screen = pygame.display.set_mode(
    (c["size"], c["size"]))
my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)
WHITE = (255, 255, 255)


def winCheck(board, status, theme, text_col, moves):
    """
    Check game status and display win/lose result.

    Parameters:
        board (list): game board
        status (str): game status
        theme (str): game interface theme
        text_col (tuple): text colour
        moves (int): number of moves made by the player
    Returns:
        board (list): updated game board
        status (str): game status
    """
    if status != "PLAY":
        size = c["size"]
        # Calculate final score
        score = sum(sum(row) for row in board)

        # Fill the window with a transparent background
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        s.fill(c["colour"][theme]["over"])
        screen.blit(s, (0, 0))

        # Display win/lose status
        if status == "WIN":
            msg = "YOU WIN!"
        else:
            msg = "GAME OVER!"

        screen.blit(my_font.render(msg, 1, text_col), (140, 150))

        # Display moves and score
        screen.blit(my_font.render(f"Moves: {moves}", 1, text_col), (140, 220))
        screen.blit(my_font.render(f"Score: {score}", 1, text_col), (140, 260))

        # Ask user to play again
        screen.blit(my_font.render("Play again? (y/ n)", 1, text_col), (80, 310))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == K_n):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == K_y:
                    # 'y' is pressed to start a new game
                    board = newGame(theme, text_col)
                    return (board, "PLAY")
    return (board, status)


def newGame(theme, text_col):
    """
    Start a new game by resetting the board.

    Parameters:
        theme (str): game interface theme
        text_col (tuple): text colour
    Returns:
        board (list): new game board
    """
    # clear the board to start a new game
    board = [[0] * 4 for _ in range(4)]
    display(board, theme)

    screen.blit(my_font.render("NEW GAME!", 1, text_col), (130, 225))
    pygame.display.update()
    # wait for 1 second before starting over
    time.sleep(1)

    board = fillTwoOrFour(board, iter=2)
    display(board, theme)
    return board


def restart(board, theme, text_col):
    """
    Ask user to restart the game if 'n' key is pressed.

    Parameters:
        board (list): game board
        theme (str): game interface theme
        text_col (tuple): text colour
    Returns:
        board (list): new game board
    """
    # Fill the window with a transparent background
    s = pygame.Surface((c["size"], c["size"]), pygame.SRCALPHA)
    s.fill(c["colour"][theme]["over"])
    screen.blit(s, (0, 0))

    screen.blit(my_font.render("RESTART? (y / n)", 1, text_col), (85, 225))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_n):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == K_y:
                board = newGame(theme, text_col)
                return board


def display(board, theme, paused=False):
    """
    Display the board 'matrix' on the game window.

    Parameters:
        board (list): game board
        theme (str): game interface theme
        paused (bool): whether the game is paused
    """
    screen.fill(tuple(c["colour"][theme]["background"]))
    box = c["size"] // 4
    padding = c["padding"]
    for i in range(4):
        for j in range(4):
            colour = tuple(c["colour"][theme][str(board[i][j])])
            pygame.draw.rect(screen, colour, (j * box + padding,
                                              i * box + padding,
                                              box - 2 * padding,
                                              box - 2 * padding), 0)
            if board[i][j] != 0:
                if board[i][j] in (2, 4):
                    text_colour = tuple(c["colour"][theme]["dark"])
                else:
                    text_colour = tuple(c["colour"][theme]["light"])
                # display the number at the centre of the tile
                screen.blit(my_font.render("{:>4}".format(
                    board[i][j]), 1, text_colour),
                    # 2.5 and 7 were obtained by trial and error
                    (j * box + 2.5 * padding, i * box + 7 * padding))

    # Display paused message if game is paused
    if paused:
        pause_font = pygame.font.SysFont(c["font"], c["font_size"] * 2, bold=True)
        pause_text = pause_font.render("PAUSED", 1, (255, 0, 0))
        screen.blit(pause_text,
                    (c["size"] // 2 - pause_text.get_width() // 2, c["size"] // 2 - pause_text.get_height() // 2))

    pygame.display.update()


def playGame(theme, difficulty):
    """
    Main game loop function.

    Parameters:
        theme (str): game interface theme
        difficulty (int): game difficulty, i.e., max. tile to get
    """
    # initialise game status
    status = "PLAY"
    moves = 0  # Count the number of moves
    undo_stack = []  # Stack to keep track of board states for undo
    paused = False  # Pause status

    # set text colour according to theme
    if theme == "light":
        text_col = tuple(c["colour"][theme]["dark"])
    else:
        text_col = WHITE

    board = newGame(theme, text_col)

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_q):
                # exit if q is pressed
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Space key to pause/unpause
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    display(board, theme, paused)
                    continue  # Skip other key checks when pausing/unpausing

                # Skip other key checks if game is paused
                if paused:
                    continue

                # 'n' is pressed to restart the game
                if event.key == pygame.K_n:
                    board = restart(board, theme, text_col)

                # 'b' is pressed to return to the main menu
                if event.key == pygame.K_b:
                    return  # Exit the playGame function and go back to the main menu

                # 'u' is pressed for undo
                if event.key == pygame.K_u:
                    if undo_stack:
                        board = undo_stack.pop()
                        display(board, theme)
                    continue

                # Handle movement keys
                if event.key in (pygame.K_w, pygame.K_UP):
                    key = 'w'
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    key = 's'
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    key = 'a'
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    key = 'd'
                else:
                    # If no valid key is pressed, skip this iteration
                    continue

                # obtain new board by performing move on old board's copy
                new_board = move(key, deepcopy(board))

                # proceed if change occurs in the board after making move
                if new_board != board:
                    # Save the current board to undo stack
                    undo_stack.append(deepcopy(board))

                    # Increment the moves counter
                    moves += 1

                    # fill 2/4 after every move
                    board = fillTwoOrFour(new_board)
                    display(board, theme)

                    # update game status
                    status = checkGameStatus(board, difficulty)

                    # check if the game is over
                    (board, status) = winCheck(board, status, theme, text_col, moves)