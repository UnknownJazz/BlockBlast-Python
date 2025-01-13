import pygame

class Board:
    def __init__(self, rows, columns, slotSize = 64):
        self.board = [[-1 for i in range(rows)] for j in range(columns)]
        self.slotSize = slotSize

    def draw(self, x, y, screen, margin = 2):
        for i in range(len(self.board)): # Row
            yy = y + ((self.slotSize + margin) * i)
        for j in range(len(self.board[i])): # Column
            xx = x + ((self.slotSize + margin) * j)
            
            pygame.draw.rect(screen, ("black" if self.board[i][j] == -1 else "green"), (xx, yy, self.slotSize, self.slotSize))

class Game:
    def __init__(self, windowWidth, windowHeight, running = True):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((windowWidth, windowHeight))
        self.clock = pygame.time.Clock()
        self.running = running

    def run(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("purple")

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()

    def printBoard(board):
        for i in board:
            print(i)


if __name__ == '__main__':
    windowHeight = 720
    windowWidth = 1280

    game = Game(windowWidth, windowHeight)

    game.run()

