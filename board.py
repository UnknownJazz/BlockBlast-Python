import pygame
import block
import random

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

        self.dragBlock = -1

        self.playerBlocks = [self.generateBlocks(),self.generateBlocks(),self.generateBlocks()]
        
        for i in range(len(self.playerBlocks)):
            if (self.playerBlocks[i] != -1):
                numberOfBlocks = len(self.playerBlocks)
                xx = self.x + ((((self.width - self.x) / numberOfBlocks) * i) + (((self.width - self.x) / numberOfBlocks) / 2)) - (self.playerBlocks[i].width / 2)
                yy = self.y + (self.height + 92) - (self.playerBlocks[i].height / 2)

                self.playerBlocks[i].setPosition(xx, yy)

    # Update the board state each tick
    def update(self):
        if (self.dragBlock != -1):
            self.checkBoardCollision()

        for i in range(len(self.playerBlocks)):
            currentBlock = self.playerBlocks[i]

            # Check mouse position if it is hovering a block
            if (pygame.mouse.get_pos()[0] > currentBlock.x and pygame.mouse.get_pos()[0] < (currentBlock.x + currentBlock.width) and 
                pygame.mouse.get_pos()[1] > currentBlock.y and pygame.mouse.get_pos()[1] < (currentBlock.y + currentBlock.height)):
                if (pygame.mouse.get_pressed()[0] and self.dragBlock == -1): 
                    currentBlock.state = 1 # 1 means it is being dragged
                    self.dragBlock = currentBlock

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
        for block in self.playerBlocks:
            if (block != -1):
                block.draw("red", self.screen, self)

    # checks if a position is inside the board
    def checkBoardCollision(self):
        targetX = self.dragBlock.dragX + (self.slotSize/2)
        targetY = self.dragBlock.dragY + (self.slotSize/2)

        if ((targetX > self.x and targetX < self.width) and (targetY > self.y and targetY < self.height)): # Check if the mouse is inside the board
            self.checkSlotCollision(targetX, targetY)
        else:
            self.refreshBoard()
    
    def checkSlotCollision(self, targetX, targetY): # checks if the mouse is hovering a slot
        margin = 2
        for i in range(len(self.board)): # Row
            yy = self.y + ((self.slotSize + margin) * i)
            for j in range(len(self.board[i])): # Column
                xx = self.x + ((self.slotSize + margin) * j)
                currentBoard = self.board[i][j]
                # Check for horizontal and vertical collision
                print(f"{self.dragBlock.dragX}, {self.dragBlock.dragY}")

                # If the first slot of the block we are dragging is hovering an empty slot in the board
                if (targetX > xx and targetX < xx + self.slotSize) and (targetY > yy and targetY < yy + self.slotSize):
                    heldBlock = self.dragBlock.dimension
                    block_height, block_width = len(heldBlock), len(heldBlock[0])

                    # Check if the entire heldBlock collides with a value > 0 in the board before proceeding
                    canPlaceBlock = True
                    for k in range(i, i + block_height):
                        for l in range(j, j + block_width):
                            # Ensure we don't go out of bounds
                            if k < len(self.board) and l < len(self.board[k]):
                                # Check only where the heldBlock has a value greater than 0
                                if heldBlock[k - i][l - j] > 0 and self.board[k][l] > 0:
                                    canPlaceBlock = False
                                    break
                        if not canPlaceBlock:
                            break

                    # Proceed with updating the board only if no collision with values > 0
                    if canPlaceBlock:
                        # First, update the board with the heldBlock values
                        if (i + block_height <= len(self.board) and j + block_width <= len(self.board[i])):
                            for k in range(len(self.board)):
                                for l in range(len(self.board[k])):
                                    # Check if the position is within the heldBlock's area
                                    if (i <= k < i + block_height) and (j <= l < j + block_width):
                                        # Update only if the corresponding heldBlock value is not -1
                                        if heldBlock[k - i][l - j] != -1:
                                            if self.board[k][l] == -1:
                                                self.board[k][l] = 0
                                        elif (self.board[k][l] == 0):
                                            self.board[k][l] = -1
                                    else:
                                        # Set all other positions to -1
                                        if (self.board[k][l] == 0):
                                            self.board[k][l] = -1
                        else:
                            self.refreshBoard()

    def refreshBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (self.board[i][j] == 0):
                    self.board[i][j] = -1

    def deployBlock(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (self.board[i][j] == 0):
                    self.board[i][j] = 1
        self.checkBlast()

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

    def generateBlocks(self):
        blockConstruct = {
            0 : [[1, 1, 1, 1, 1 ]],
            1 : [[1, -1, -1, -1], [1, 1, 1, 1]],
            2 : [[1, 1, 1, 1], [-1, -1, -1, 1], [-1, -1, -1, 1]],
            3 : [[1]],
            4 : [[1, 1]],
            5 : [[1, 1],[-1, 1]]
        }

        return block.Block(blockConstruct[random.randint(0, len(blockConstruct)-1)])

    def setSlotValue(self, row, column, value):
        if (row < len(self.board) and column < len(self.board[row])):
            self.board[row][column] = value

    def print(self):
        for i in self.board:
            print(i)