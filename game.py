#game.py

import threading
import pygame.mixer
import random

import pygame
import board
class Game:
    
    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load("assets\Kirby_dream_land_theme_song.mp3")  # or "bg_music.wav"
        pygame.mixer.music.play(-1)  # -1 means loop forever
        pygame.mixer.music.set_volume(0.5)

    def __init__(self, windowWidth, windowHeight, running = True):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.running = running
        
        # Load blast sound effect once
        pygame.mixer.init()
        self.blast_sound = pygame.mixer.Sound("assets\Get out sound effect!!.mp3")
        self.blast_sound.set_volume(2)  # 50% volume


    def run(self):
        while self.running:
            self.end = False
            # pygame setup
            pygame.init()
            
            # Start background music in a separate thread
            music_thread = threading.Thread(target=self.play_music)
            music_thread.daemon = True
            music_thread.start()

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
            # Create a text file to hold the high scores
            scoreFile = open("Score.txt", "a")
            scoreFile.close

            file = open("Score.txt", "r")
            self.highScore = file.readline()
            file.close()

            # Main game loop
            while (True):
                # poll for events
                # pygame.QUIT event means the user clicked X to close your window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                
                self.update()
                self.draw()
                
                if (self.end == True):
                    self.saveScore() # Save the highest score

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

        # End the game
        if (pygame.key.get_pressed()[pygame.K_e]):
            self.end  = True

    def draw(self):
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill(pygame.Color(66, 92, 161))

        # Draw the highest score at the left side of the board
        highScoreX = 32
        highScoreY = self.board.y
        highScoreText = pygame.font.SysFont("Arial", 25).render(f"Highscore:", True, "white")
        self.screen.blit(highScoreText, (32, self.board.y))
        highScoreDisplay = pygame.font.SysFont("Arial", 25).render(f"    {self.highScore}", True, "white")
        self.screen.blit(highScoreDisplay, (32, self.board.y + (highScoreText.get_height() + 2))) # 2 is margin
        
        # Draw the score above the board
        scoreText = pygame.font.SysFont("Arial", 50).render(f"{self.score}", True, "white" if (self.comboCount <= 1) else "yellow")
        self.screen.blit(scoreText,((self.windowWidth//2) - (scoreText.get_width()//2), (60) - (scoreText.get_height())))
        
        self.board.draw(self.screen)

    def addScore(self, blocksPlaced, linesCleared):
        if (linesCleared >= 1): # If the player cleared a line
            self.blast_sound.play()
            self.comboCount += 1 # Add a count to the combo
            self.comboFailCount = 0 # Reset the fail counter of the combo
        else: # If the player fail to clear a line
            self.comboFailCount += 1
            # If we reach the threshold we can place a block without resetting the combo, reset the combo
            if (self.comboFailCount >= self.comboFailMax):
                self.comboFailCount = 0
                self.comboCount = 0

        # Update the score
        self.score += blocksPlaced + ((linesCleared * 10) * (1 + self.comboCount))
    
    def saveScore(self):
        with open("Score.txt", "r+") as file:
            savedScore = file.readline().strip()  # Read the first line and remove whitespace
            savedScore = int(savedScore) if savedScore.isdigit() else 0  # Handle invalid or empty content
            
            if self.score > savedScore:
                file.seek(0)  # Go to the start of the file
                file.write(f"{self.score}")  # Write the new score
                file.truncate()  # Ensure the file is not longer than necessary