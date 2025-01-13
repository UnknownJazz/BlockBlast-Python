import pygame

def initializeBoard(size):
    board = [[-1 for i in range(size)] for j in range(size)]
    return board

def printBoard(board):
    for i in board:
        print(i)

def drawBoard(x, y, board, surface):
    rectSize = 48
    margin = 2
    for i in range(len(board)): # Row
        yy = y + ((rectSize + margin) * i)
        for j in range(len(board[i])): # Column
            xx = x + ((rectSize + margin) * j)
            
            pygame.draw.rect(surface, ("black" if board[i][j] == -1 else "green"), (xx, yy, rectSize, rectSize))
            


def game(windowWidth = 1280, windowHeight = 720):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    clock = pygame.time.Clock()
    running = True

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        board = initializeBoard(9)
        board[3][3] = 1

        # RENDER YOUR GAME HERE
        drawBoard(64, 64, board, screen)
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == '__main__':
    game()

