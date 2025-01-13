import pygame
import board

class Game:
    def __init__(self, windowWidth, windowHeight, running = True):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((windowWidth, windowHeight))
        self.clock = pygame.time.Clock()
        self.running = running

        boardSize = 9
        boardSlotSize = 48

        boardX = (self.windowWidth / 2) - (((boardSlotSize+2) * boardSize) / 2)
        boardY = 8
        self.board = board.Board(boardX, boardY, boardSize, boardSize, boardSlotSize)

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

