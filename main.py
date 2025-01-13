import pygame
import time

class Board:
    def __init__(self, x, y, rows, columns, slotSize = 64):
        self.board = [[-1 for i in range(rows)] for j in range(columns)]
        self.slotSize = slotSize
        self.rows = rows
        self.columns = columns
        self.x = x
        self.y = y

    def draw(self, screen, margin = 2):
        for i in range(len(self.board)): # Row
            yy = self.y + ((self.slotSize + margin) * i)
            for j in range(len(self.board[i])): # Column
                xx = self.x + ((self.slotSize + margin) * j)
                # -1 = Empty
                # 0 = Hover
                # > 0 = Naay sulod
                pygame.draw.rect(screen, ("black" if self.board[i][j] == -1 else "green"), (xx, yy, self.slotSize, self.slotSize))

    def update(self):
        self.checkMouseCollision()

    def checkMouseCollision(self):
        # Set the color of the slot as Gray if the mouse is hovering over it
        yy = self.y + ((self.slotSize + 2) * self.rows)
        if (pygame.mouse.get_pos()[0] > self.x and pygame.mouse.get_pos()[1] < yy): # Check if the mouse is inside the board
            print("Mouse is in the box")
        else:
            print("Not in the box")

    def print(self):
        for i in self.board:
            print(i)

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
                    
            self.update()
            self.draw()

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()

    def update(self):
        boardSize = 9
        boardSlotSize = 48

        boardX = (self.windowWidth / 2) - (((boardSlotSize+2) * boardSize) / 2)
        boardY = 8
        self.board = Board(boardX, boardY, boardSize, boardSize, boardSlotSize)

        self.board.update()

    def draw(self):
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("purple")
        
        self.board.draw(self.screen)

if __name__ == '__main__':
    windowHeight = 720
    windowWidth = 1280

    game = Game(windowWidth, windowHeight)

    game.run()

