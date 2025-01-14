import pygame
import board
class Game:
    def __init__(self, windowWidth, windowHeight, running = True):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.running = running


    def run(self):
        while self.running:
            self.end = False
            # pygame setup
            pygame.init()
            self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
            self.clock = pygame.time.Clock()
            
            # instanciate the board
            boardSize = 8
            boardSlotSize = 48

            boardX = (self.windowWidth / 2) - (((boardSlotSize+2) * boardSize) / 2)
            boardY = 64
            self.board = board.Board(boardX, boardY, boardSize, boardSize, self.screen, self, boardSlotSize)

            # Main game loop
            while (True):
                # poll for events
                # pygame.QUIT event means the user clicked X to close your window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()

                self.draw()
                self.update()
                
                if (self.end == True):
                    # If the state of the game is end, display Game End or something
                    noBlocksText = pygame.font.SysFont("Arial", 100).render("Game End", True, "white")
                    self.screen.blit(noBlocksText,((self.windowWidth//2) - (noBlocksText.get_width()//2), (self.windowHeight//2) - (noBlocksText.get_height())))
                    restartText = pygame.font.SysFont("Arial", 50).render("Press [R] to restart :)", True, "white")
                    self.screen.blit(restartText,((self.windowWidth//2) - (restartText.get_width()//2), (self.windowHeight//2) - (restartText.get_height()) + noBlocksText.get_height()))
                    
                    # Restart the game
                    if (pygame.key.get_pressed()[pygame.K_r]):
                        break

                # flip() the display to put your work on screen
                pygame.display.flip()

                self.clock.tick(60)  # limits FPS to 60

    def update(self):
        self.board.update()

    def draw(self):
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill(pygame.Color(66, 92, 161))
        
        self.board.draw(self.screen)