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

        self.colorValue = {
            -1 : pygame.Color(33, 44, 82),
            0 : "gray",
            1 : pygame.image.load('assets\Block Cell1.png'),
            2 : pygame.image.load('assets\Block Cell2.png'),
            3 : pygame.image.load('assets\Block Cell3.png'),
            4 : pygame.image.load('assets\Block Cell4.png'),
            5 : pygame.image.load('assets\Block Cell5.png'),
        }


        self.dragBlock = None
        self.dragBlockIndex = None

        self.playerBlocks = [self.generateBlocks(),self.generateBlocks(),self.generateBlocks()]
        
        for i in range(len(self.playerBlocks)):
            if (self.playerBlocks[i] != -1):
                numberOfBlocks = len(self.playerBlocks)
                xx = self.x + ((((self.width - self.x) / numberOfBlocks) * i) + (((self.width - self.x) / numberOfBlocks) / 2)) - (self.playerBlocks[i].width / 2)
                yy = self.y + (self.height) - (self.playerBlocks[i].height / 2)

                self.playerBlocks[i].setPosition(xx, yy)

    # Update the board state each tick
    def update(self):
        if (self.dragBlock != None):
            self.checkBoardCollision()

        # Allow the player to drag the blocks to the board
        for i in range(len(self.playerBlocks)):
            currentBlock = self.playerBlocks[i]
            
            if (currentBlock != None):
                # Check mouse position if it is hovering a block
                if (pygame.mouse.get_pos()[0] > currentBlock.x and pygame.mouse.get_pos()[0] < (currentBlock.x + currentBlock.width) and 
                    pygame.mouse.get_pos()[1] > currentBlock.y and pygame.mouse.get_pos()[1] < (currentBlock.y + currentBlock.height)):
                    if (pygame.mouse.get_pressed()[0] and self.dragBlock == None): 
                        currentBlock.state = 1 # 1 means it is being dragged
                        self.dragBlock = currentBlock
                        self.dragBlockIndex = i
        
        # Regenerate if there is no more blocks
        self.refillPlayerBlocks()

    # Draw uhh... thingies each tick
    def draw(self, screen):
        # Draw a dark background around the board
        pygame.draw.rect(screen, pygame.Color(23, 29, 77), (self.x - self.margin, self.y - self.margin, (self.width - self.x) + self.margin, (self.height - self.y) + self.margin))

        # Draw each slot of the board
        for i in range(len(self.board)): # Row
            yy = self.y + ((self.slotSize + self.margin) * i)
            for j in range(len(self.board[i])): # Column
                xx = self.x + ((self.slotSize + self.margin) * j)
                # -1 = Empty
                # 0 = Hover
                # > 0 = Naay sulod
                
                if (self.board[i][j] < 1):
                    pygame.draw.rect(screen, (self.colorValue[self.board[i][j]]), (xx, yy, self.slotSize, self.slotSize))
                else:
                    cellImage = self.colorValue[self.board[i][j]]
                    cellImage = pygame.transform.scale(cellImage, (self.slotSize, self.slotSize))
                    self.screen.blit(cellImage, (xx, yy))
        
        # Draw each available blocks at the bottom of the board
        for block in self.playerBlocks:
            if (block != None):
                block.draw(self.screen, self)

    # checks if a position is inside the board
    def checkBoardCollision(self):
        targetX = self.dragBlock.dragX + (self.slotSize/2)
        targetY = self.dragBlock.dragY + (self.slotSize/2)

        if ((targetX > self.x and targetX < self.width) and (targetY > self.y and targetY < self.height)): # Check if the mouse is inside the board
            self.checkSlotCollision(targetX, targetY)
        else:
            self.refreshBoard()
    
    def checkSlotCollision(self, targetX, targetY): # checks if the mouse is hovering a slot
        for i in range(len(self.board)): # Row
            yy = self.y + ((self.slotSize + self.margin) * i)
            for j in range(len(self.board[i])): # Column
                xx = self.x + ((self.slotSize + self.margin) * j)
                currentBoard = self.board[i][j]
                # Check for horizontal and vertical collision
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

    def deployBlock(self, block):
        deployed = False
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (self.board[i][j] == 0):
                    self.board[i][j] = block.value
                    deployed = True
        
        if (deployed):
            self.checkBlast()
            self.playerBlocks[self.dragBlockIndex] = None

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
            0: [[1]],  # Single block
            1: [[1, 1]],  # Horizontal line (2)
            2: [[1], [1]],  # Vertical line (2)
            3: [[1, 1, 1]],  # Horizontal line (3)
            4: [[1], [1], [1]],  # Vertical line (3)
            5: [[1, 1, 1, 1]],  # Horizontal line (4)
            6: [[1], [1], [1], [1]],  # Vertical line (4)
            7: [[1, 1], [1, 1]],  # Square (2x2)
            8: [[1, 1, -1], [-1, 1, 1]],  # Z-shape
            9: [[-1, 1, 1], [1, 1, -1]],  # S-shape
            10: [[1, -1], [1, 1], [-1, 1]],  # T-shape (2x2)
            11: [[1, 1, 1], [-1, 1, -1]],  # T-shape
            12: [[1, 1, -1], [1, 1, 1]],  # L-shape (rotated variant)
            13: [[-1, 1], [-1, 1], [1, 1]],  # L-shape (2x2)
            14: [[1, -1], [1, -1], [1, 1]],  # Reverse L-shape (longer variant)
            15: [[1, 1, 1], [1, -1, -1]],  # L-shape (2x3 matrix variant)
            16: [[-1, -1, 1], [1, 1, 1]],  # Reverse L-shape (2x3 variant)
            17: [[1, 1, 1], [1, 1, 1], [1, 1, 1]], # Square (3x3)
            18: [[1, 1, 1], [-1, -1, 1], [-1, -1, 1]], # L-shape (3x3)
        }
        construct = blockConstruct[random.randint(0, len(blockConstruct)-1)]

        # Have a chance to give a rotated construct of the matrix
        roll = random.randint(0, 360)
        rollCount = roll // 90

        # Rotates as many times randomly yippee o i i a
        while (rollCount > 0):
            construct = list(zip(*construct[::-1]))
            rollCount -= 1

        value = random.randint(1, len(self.colorValue)-2)

        return block.Block(construct, value)
    
    def refillPlayerBlocks(self):
        emptyBlocks = True
        for block in self.playerBlocks:
            if (block != None):
                emptyBlocks = False
        
        if (emptyBlocks):
            for i in range(len(self.playerBlocks)):
                self.playerBlocks[i] = self.generateBlocks()

            for i in range(len(self.playerBlocks)):
                if (self.playerBlocks[i] != -1):
                    numberOfBlocks = len(self.playerBlocks)
                    xx = self.x + ((((self.width - self.x) / numberOfBlocks) * i) + (((self.width - self.x) / numberOfBlocks) / 2)) - (self.playerBlocks[i].width / 2)
                    yy = self.y + (self.height) - (self.playerBlocks[i].height / 2)

                    self.playerBlocks[i].setPosition(xx, yy)

    def setSlotValue(self, row, column, value):
        if (row < len(self.board) and column < len(self.board[row])):
            self.board[row][column] = value

    def print(self):
        for i in self.board:
            print(i)