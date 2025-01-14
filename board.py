import pygame
import block
import random
import copy

class Board:
    def __init__(self, x, y, rows, columns, screen, game, slotSize = 64):
        self.game = game
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
            self.checkBoardCollision(self.dragBlock.dragX + (self.slotSize/2), self.dragBlock.dragY + (self.slotSize/2))

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

    def refreshBoard(self):
        if (self.dragBlock != None):
            self.dragBlock.hoverRow = None
            self.dragBlock.hoverColumn = None
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (self.board[i][j] == 0):
                    self.setSlotValue(i, j, -1)

    def deployBlock(self, block, row, column, board = None, value = None):
        if (board == None):
            board = self.board
        if (value == None):
            value = block.value
        
        if (self.checkBlockPlacement(row, column, block.dimension, board) == True):
            # Change the values of the board to the dragged block
            blockHeight, blockWidth = len(block.dimension), len(block.dimension[0])
            for i in range(row, row + blockHeight):
                for j in range(column, column + blockWidth):
                    if (block.dimension[i - row][j - column] != -1):
                        #if (board[i][j] == -1):
                        board[i][j] = value
            # Check whether a line in a board is filled after changing the values of the board based on the dragged block
            self.checkBlast(board)
        if (board == self.board):
            self.playerBlocks[self.dragBlockIndex] = None
        self.checkBoardLose()

    def checkBoardLose(self):
        board = self.board
        # Check the board if it loses
        emptyBlocks = True
        for block in self.playerBlocks:
            if (block != None):
                emptyBlocks = False

        # If there is a block remaining, check whether it can be place on the board
        if (emptyBlocks == False):
            gameEnd = True
            for block in self.playerBlocks:
                if (block != None):
                    blockHeight, blockWidth = len(block.dimension), len(block.dimension[0])
                    # Check if the remaining block can fit anywhere on the board
                    for i in range(len(self.board) - blockHeight + 1):
                        for j in range(len(self.board[i]) - blockWidth + 1):
                            if (self.checkBlockPlacement(i, j, block.dimension, board)):
                                gameEnd = False
                            if (gameEnd == False):
                                break
                        if (gameEnd == False):
                            break
            self.game.end = gameEnd

    # checks if a position is inside the board
    def checkBoardCollision(self, targetX, targetY):
        if ((targetX > self.x and targetX < self.width) and (targetY > self.y and targetY < self.height)): # Check if the mouse is inside the board
            self.checkSlotCollision(targetX, targetY)
        else:
            self.refreshBoard()
    
    def checkSlotCollision(self, targetX, targetY): # checks if the mouse is hovering a slot
        for i in range(len(self.board)): # Row
            yy = self.y + ((self.slotSize + self.margin) * i)
            for j in range(len(self.board[i])): # Column
                xx = self.x + ((self.slotSize + self.margin) * j)

                # Check for horizontal and vertical collision
                # If the first slot of the block we are dragging is hovering an empty slot in the board
                if (targetX > xx and targetX < xx + self.slotSize) and (targetY > yy and targetY < yy + self.slotSize):
                    heldBlock = self.dragBlock.dimension
                    block_height, block_width = len(heldBlock), len(heldBlock[0])

                    # Proceed with updating the board only if no collision with values > 0
                    if (self.checkBlockPlacement(i, j, self.dragBlock.dimension)):
                        # First, update the board with the heldBlock values
                        if (i + block_height <= len(self.board) and j + block_width <= len(self.board[i])):
                            for k in range(len(self.board)):
                                for l in range(len(self.board[k])):
                                    # Check if the position is within the heldBlock's area
                                    if (i <= k < i + block_height) and (j <= l < j + block_width):
                                        self.dragBlock.hoverRow = i
                                        self.dragBlock.hoverColumn = j

                                        # Update only if the corresponding heldBlock value is not -1
                                        if heldBlock[k - i][l - j] != -1:
                                            if self.board[k][l] == -1:
                                                self.setSlotValue(k, l, 0)
                                        elif (self.board[k][l] == 0):
                                            self.setSlotValue(k, l, -1)
                                    else:
                                        # Set all other positions to -1
                                        if (self.board[k][l] == 0):
                                            self.setSlotValue(k, l, -1)
                        else:
                            self.refreshBoard()
                    else:
                        self.refreshBoard()

    # Blast is when an entire row or column is filled, then boom shaka laka
    def checkBlast(self, board = None):
        if (board == None):
            board = self.board
        # Check Horizontal lines
        for i in range(len(board)):
            flag = False
            for j in range(len(board[i])):
                if (board[i][j] < 1):
                    flag = True
                    break
            if (flag == False):
                self.blastRow(i, board)
        
        # Check Vertical lines
        for i in range(len(board)):
            flag = False
            for j in range(len(board[i])):
                if (board[j][i] < 1):
                    flag = True
                    break
            if (flag == False):
                self.blastColumn(i, board)

    def checkBlockPlacement(self, row, column, blockDimension, board = None):
        if (board == None):
            board = self.board
        blockHeight, blockWidth = len(blockDimension), len(blockDimension[0])

        # Check if the entire block collides with a value > 0 in the board before proceeding
        canPlaceBlock = True
        for k in range(row, row + blockHeight):
            for l in range(column, column + blockWidth):
                # Ensure we don't go out of bounds
                if k < len(board) and l < len(board[k]):
                    # Check only where the block has a value greater than 0
                    if blockDimension[k - row][l - column] > 0 and board[k][l] > 0:
                        canPlaceBlock = False
                        break
            if (canPlaceBlock == False):
                break
        return canPlaceBlock

    def removeBlock(self, array, index):
        # Remove the deployed block
        array[index] = None

    # Remove an entire Row
    def blastRow(self, row, board = None):
        if (board == None):
            board = self.board

        for i in range(len(board[row])):
            self.setSlotValue(row, i, -1, board)

    # Remove an entire Column
    def blastColumn(self, column, board = None):
        if (board == None):
            board = self.board

        for i in range(len(board)):
            self.setSlotValue(i, column, -1, board)

    # Returns a block class with a random construct
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
            19: [[-1, 1], [1, -1]],
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
    
    # Refills the player blocks with a set of new block
    def refillPlayerBlocks(self):
        # Player must use all three blocks first before generating new ones
        emptyBlocks = True
        for block in self.playerBlocks:
            if (block != None):
                emptyBlocks = False
        
        if (emptyBlocks):
            # Add blocks
            transposedBoard = copy.deepcopy(self.board)
            for i in range(len(self.playerBlocks)):
                # Generate Blocks for the player
                while self.playerBlocks[i] is None:
                    generatedBlock = self.generateBlocks()
                    blockHeight, blockWidth = len(generatedBlock.dimension), len(generatedBlock.dimension[0])
                    generateNew = True

                    # Check if the block can fit anywhere on the board
                    for j in range(len(self.board) - blockHeight + 1):
                        for k in range(len(self.board[j]) - blockWidth + 1):
                            if self.checkBlockPlacement(j, k, generatedBlock.dimension, transposedBoard):
                                generateNew = False  # Found a valid placement
                                self.deployBlock(generatedBlock, j, k, transposedBoard)
                                break
                        if not generateNew:
                            break

                    if not generateNew:
                        # Assign the generated block since it fits
                        self.playerBlocks[i] = generatedBlock
                    else:
                        # If no valid placement exists, generate a new block
                        continue


            # Set the position of the blocks below the board
            for i in range(len(self.playerBlocks)):
                if (self.playerBlocks[i] != -1):
                    numberOfBlocks = len(self.playerBlocks)
                    xx = self.x + ((((self.width - self.x) / numberOfBlocks) * i) + (((self.width - self.x) / numberOfBlocks) / 2)) - (self.playerBlocks[i].width / 2)
                    yy = self.y + (self.height) - (self.playerBlocks[i].height / 2)

                    self.playerBlocks[i].setPosition(xx, yy)

    # Sets the value of a slot in the board
    def setSlotValue(self, row, column, value, board = None):
        if (board == None):
            board = self.board

        if (row < len(board) and column < len(board[row])):
            board[row][column] = value

    def print(self):
        for i in self.board:
            print(i)