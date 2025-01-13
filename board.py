import pygame
import block

class Board:
    def __init__(self, x, y, rows, columns, screen, slotSize = 64):
        self.board = [[-1 for i in range(rows)] for j in range(columns)]
        self.slotSize = slotSize
        self.rows = rows
        self.columns = columns
        self.x = x
        self.y = y
        self.screen = screen
        self.margin = 2
        self.width = self.x + ((self.slotSize + self.margin) * self.columns)
        self.height = self.y + ((self.slotSize + self.margin) * self.rows)

        blockSize = 24
        self.playerBlocks = [block.Block([[1, -1, -1, -1], [1, 1, 1, 1]]), 
                             block.Block([[1, 1, 1, 1, 1]]), 
                             block.Block([[1, 1, 1, 1], [-1, -1, -1, 1], [-1, -1, -1, 1]])]

    # Update the board state each tick
    def update(self):
        self.checkBoardCollision()

    # Draw uhh... thingies each tick
    def draw(self, screen):
        colors = {
            -1 : pygame.Color(33, 44, 82),
            0 : "gray",
            1 : "green"
        }

        # Draw each slot of the board
        for i in range(len(self.board)): # Row
            yy = self.y + ((self.slotSize + self.margin) * i)
            for j in range(len(self.board[i])): # Column
                xx = self.x + ((self.slotSize + self.margin) * j)
                # -1 = Empty
                # 0 = Hover
                # > 0 = Naay sulod
                pygame.draw.rect(screen, (colors[self.board[i][j]]), (xx, yy, self.slotSize, self.slotSize))
        
        # Draw each available blocks at the bottom of the board
        for i in range(len(self.playerBlocks)):
            if (self.playerBlocks[i] != -1):
                numberOfBlocks = len(self.playerBlocks)
                xx = self.x + ((((self.width - self.x) / numberOfBlocks) * i) + (((self.width - self.x) / numberOfBlocks) / 2)) - (self.playerBlocks[i].width / 2)
                yy = self.y + (self.height + 92) - (self.playerBlocks[i].height / 2)

                self.playerBlocks[i].setPosition(xx, yy)
                self.playerBlocks[i].draw("red", self.screen)

    # checks if a position is inside the board
    # Currently it checks the mouse position
    def checkBoardCollision(self):
        targetX = pygame.mouse.get_pos()[0]
        targetY = pygame.mouse.get_pos()[1]

        if ((targetX > self.x and targetX < self.width) and (targetY > self.y and targetY < self.height)): # Check if the mouse is inside the board
            self.checkSlotCollision()
    
    def checkSlotCollision(self): # checks if the mouse is hovering a slot
        margin = 2
        for i in range(len(self.board)): # Row
            yy = self.y + ((self.slotSize + margin) * i)
            for j in range(len(self.board[i])): # Column
                xx = self.x + ((self.slotSize + margin) * j)
                currentBoard = self.board[i][j]
                # Check for horizontal and vertical collision
                targetX = pygame.mouse.get_pos()[0]
                targetY = pygame.mouse.get_pos()[1]

                if (targetX > xx and targetX < xx + self.slotSize) and (targetY > yy and targetY < yy + self.slotSize):
                    
                    # Set value to a slot if the mouse is pressed and the slot is empty
                    mouse_pressed = pygame.mouse.get_pressed()[0]
                    if (currentBoard == -1):
                        self.setSlotValue(i, j, 0)
                    if(currentBoard == 0 and mouse_pressed):
                        self.setSlotValue(i, j, 1)

                        self.checkBlast()
                else:
                    if (currentBoard == 0):
                        self.setSlotValue(i, j, -1)

    # Blast is when an entire row or column is filled, then boom shaka laka
    def checkBlast(self):
        # Check Horizontal Blast
        for i in range(len(self.board)):
            flag = False
            for j in range(len(self.board[i])):
                if (self.board[i][j] < 1):
                    flag = True
                    break
            if (flag == False):
                self.blastRow(i)
        
        # Check Vertical Blast
        for i in range(len(self.board)):
            flag = False
            for j in range(len(self.board[i])):
                if (self.board[j][i] < 1):
                    flag = True
                    break
            if (flag == False):
                self.blastColumn(i)

    # Remove an entire Row
    def blastRow(self, row):
        for i in range(len(self.board[row])):
            self.board[row][i] = -1

    # Remove an entire Column
    def blastColumn(self, column):
        for i in range(len(self.board)):
            self.board[i][column] = -1

    def generateBlocks():
        pass

    def setSlotValue(self, row, column, value):
        self.board[row][column] = value

    def print(self):
        for i in self.board:
            print(i)