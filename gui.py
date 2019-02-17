import pygame


def gui(board):
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 30
    HEIGHT = 30

    # This sets the margin between each cell
    MARGIN = 1

    # Set row 1, cell 5 to one.
    # (Remember rows and column numbers start at zero.)
    #grid[1][5] = 1

    # Initialize pygame
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [311, 311]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("Final Board : " + str(board.capacity) + "% full")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # User clicks the mouse. Get the position
    #            pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
    #            column = pos[0] // (WIDTH + MARGIN)
    #            row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
    #            grid[row][column] = 1
    #            print("Click ", pos, "Grid coordinates: ", row, column)


        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        for row in range(10):
            for column in range(10):
                color = WHITE
                if board.board[row][column] != "":
                    brickType = ord(board.board[row][column][:-1]) - ord('a')
                    if brickType == 0:      # a
                        color = (255, 0, 0)
                    elif brickType == 1:    # b
                        color = (0, 255, 0)
                    elif brickType == 2:    # c
                        color = (0, 0, 255)
                    elif brickType == 3:    # d
                        color = (150, 0, 0)
                    elif brickType == 4:    # e
                        color = (0, 150, 0)
                    elif brickType == 5:    # f
                        color = (0, 0, 150)

                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()