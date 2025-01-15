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

            # Game data
            self.score = 0
            self.comboFailCount = 0
            self.comboFailMax = 3
            self.comboCount = 0

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

        # Draw the score above the board
        scoreText = pygame.font.SysFont("Arial", 50).render(f"{self.score}", True, "white" if (self.comboCount <= 1) else "yellow")
        self.screen.blit(scoreText,((self.windowWidth//2) - (scoreText.get_width()//2), (60) - (scoreText.get_height())))
        
        self.board.draw(self.screen)

    def addScore(self, blocksPlaced, linesCleared):
        if (linesCleared >= 1): # If the player cleared a line
            self.comboCount += 1 # Add a count to the combo
            self.comboFailCount = 0 # Reset the fail counter of the combo
        else: # If the player fail to clear a line
            self.comboFailCount += 1
            # If we reach the threshold we can place a block without resetting the combo, reset the combo
            if (self.comboFailCount >= self.comboFailMax):
                self.comboFailCount = 0
                self.comboCount = 0

        print(f"combo Count: {self.comboCount} combo Fail: {self.comboFailCount}")
        # Update the score
        self.score += blocksPlaced + ((linesCleared * 10) * (1 + self.comboCount))