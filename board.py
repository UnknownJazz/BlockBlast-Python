import pygame
import block
import random
import copy
import imageGenerator as iG

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
        
        blockPlaced = 0 # Track how many blocks were traced for scoring

        if (self.checkBlockPlacement(row, column, block.dimension, board) == True):
            # Change the values of the board to the dragged block
            blockHeight, blockWidth = len(block.dimension), len(block.dimension[0])
            for i in range(row, row + blockHeight):
                for j in range(column, column + blockWidth):
                    if (block.dimension[i - row][j - column] != -1):
                        board[i][j] = value
                        blockPlaced += 1
            
            # Check whether a line in a board is filled after changing the values of the board based on the dragged block
            linesCleared = self.checkLineClear(board)
        
        if (board == self.board):
            self.playerBlocks[self.dragBlockIndex] = None # Remove the deployed block
            self.game.addScore(blockPlaced, linesCleared) # Update the score on each deployed blocks

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
    def checkLineClear(self, board = None):
        linesCleared = 0 # Track how many lines were cleared for scoring

        filledLines = [[],[]]
        if (board == None):
            board = self.board
        # Check Horizontal lines
        for i in range(len(board)):
            filled = True
            for j in range(len(board[i])):
                if (board[i][j] < 1):
                    filled = False
                    break
            if (filled == True):
                filledLines[0].append(i)
                linesCleared += 1
        
        # Check Vertical lines
        for i in range(len(board)):
            filled = True
            for j in range(len(board[i])):
                if (board[j][i] < 1):
                    filled = False
                    break
            if (filled == True):
                filledLines[1].append(i)
                linesCleared += 1
        
        # Remove all the lines that is filled vertically and horizontally, yeaah!
        for i in filledLines[0]:
            self.clearRow(i, board)
        for i in filledLines[1]:
            self.clearColumn(i, board)
        return linesCleared

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
    def clearRow(self, row, board = None):
        if (board == None):
            board = self.board

        for i in range(len(board[row])):
            self.setSlotValue(row, i, -1, board)

    # Remove an entire Column
    def clearColumn(self, column, board = None):
        if (board == None):
            board = self.board

        for i in range(len(board)):
            self.setSlotValue(i, column, -1, board)

    # Returns a block class with a random construct
    def generateBlocks(self):
        # The structure of the array is like this:
        # [[3x3's], [3x2's], [2x2's], [2x1's and 1x1]]
        blockConstructs = [[ # 3 x 3 and 5 x 1
                            [[1, 1, 1],
                             [1, 1, 1],
                             [1, 1, 1]],
                            
                            [[1, 0, 0],
                             [1, 0, 0],
                             [1, 1, 1]],

                            [[0, 0, 1],
                             [0, 0, 1],
                             [1, 1, 1]],
                             
                            [[1, 1, 1, 1, 1]]],
                            
                            # 3 x 2 and 4 x 1
                           [[[1, 1, 1],
                             [1, 1, 1]],

                            [[1, 1, 1],
                             [0, 0, 1]],
                            
                            [[1, 1, 1],
                             [0, 1, 0]],

                            [[1, 1, 1],
                             [1, 0, 0]],
                             
                            [[1, 1, 1]]],

                            # 2 x 2
                           [[[1, 1],
                             [1, 1]],

                            [[1, 1],
                             [0, 1]],

                            [[1, 0],
                             [0, 1]],
                            ],

                            # 2 x 2 and 1 x 1
                           [[[1, 1]], [[1]]]]

        # Choose random construct based on weights
        constructWeights = [100, 50, 25, 10]
        r = random.randint(0, sum(constructWeights)) # Choose a random point in the weights
        print(f"random value: {r}")

        cursor = 0
        randomSize = 0
        for i in range(len(constructWeights)):
            cursor += constructWeights[i]
            if (cursor >= r):
                randomSize = i
                print(f"size: {i}")
                break

        randomBlock = random.randint(0, len(blockConstructs[randomSize]) - 1)
        construct = blockConstructs[randomSize][randomBlock]

        # Change the matrix's 0's to -1's
        for i in range(len(construct)):
            for j in range(len(construct[i])):
                if (construct[i][j] == 0):
                    construct[i][j] = -1

        value = random.randint(1, len(self.colorValue)-2)
        blockGenerated = block.Block(construct, value)
        #construct = blockConstruct[random.randint(0, len(blockConstruct)-1)]

        # Have a chance to give a rotated construct of the matrix
        roll = random.randint(0, 360)
        rollCount = roll // 90

        # Rotates as many times randomly yippee o i i a
        while (rollCount > 0):
            blockGenerated.rotate()
            rollCount -= 1

        return blockGenerated

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
            random.shuffle(self.playerBlocks)


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