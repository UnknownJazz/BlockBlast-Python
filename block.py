import pygame
# Block States:
# 0 - Free
# 1 - Being dragged by a player
# 2 - It is hovering an emtpy slot on the board

class Block:
    def __init__(self, dimension, value = 1, x = -1, y = -1, margin = 2):
        self.dimension = dimension
        self.value = value
        self.x = x
        self.y = y
        self.dragX = self.x
        self.dragY = self.y
        self.hoverRow = None
        self.hoverColumn = None
        self.margin = margin
        self.size = 18
        self.dragSize = self.size
        self.state = 0 # 0 - static, 1 - dragged by the player
        self.width = ((len(self.dimension[0])) * self.size) + ((len(self.dimension[0])) * self.margin)
        self.height = ((len(self.dimension)) * self.size) + ((len(self.dimension)) * self.margin)

        
    def draw(self, screen, board, highlights = [[], []]):# Highlights = [Rows], [Columns]
        if (self.state == 1):
            self.drag(board)
            self.dragSize = board.slotSize
        else:
            self.dragSize = self.size
        
        if (highlights[0] != [] and self.hoverRow != None):
            for row in range(len(highlights[0])):
                highlights[0][row] -= self.hoverRow

        if (highlights[1] != [] and self.hoverColumn != None):
            for col in range(len(highlights[1])):
                highlights[1][col] -= self.hoverColumn

        cellImage = board.colorValue[self.value]
        cellImage = pygame.transform.scale(cellImage, (self.dragSize, self.dragSize))
        pygame.draw.rect(screen, "white", (self.x - self.margin, self.y - self.margin, self.width + self.margin, self.height + self.margin))

        # Draw each cells of a block
        for i in range(len(self.dimension)):
            yy = self.dragY + ((self.dragSize + self.margin) * i)
            for j in range(len(self.dimension[i])):
                xx = self.dragX + ((self.dragSize + self.margin) * j)
                if ((i in highlights[0] or j in highlights[1]) and self.dimension[i][j] != -1):
                    # pygame.draw.rect(screen, "white", (xx, yy, self.dragSize, self.dragSize))
                    hoverImage = pygame.transform.scale(board.colorValue[-2], (self.dragSize, self.dragSize))
                    screen.blit(hoverImage, (xx, yy))
                    pass
                else:
                    if (self.dimension[i][j] != -1):
                        screen.blit(cellImage, (xx, yy))

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.dragX = x
        self.dragY = y

    def drag(self, board):
        mouse = pygame.mouse
        width = ((len(self.dimension[0])) * self.dragSize) + ((len(self.dimension[0])) * self.margin)
        height = ((len(self.dimension)) * self.dragSize) + ((len(self.dimension)) * self.margin)

        if (mouse.get_pressed()[0]):
            self.dragX = mouse.get_pos()[0] - ((width)/2)
            self.dragY = mouse.get_pos()[1] - (height + 32)

        else:
            if (self.hoverRow != None and self.hoverColumn != None):
                board.deployBlock(self, self.hoverRow, self.hoverColumn)
            board.dragBlock = None
            board.dragBlockIndex = None
            board.refreshBoard()

            self.state = 0
            self.dragX = self.x
            self.dragY = self.y
            self.hoverRow = None
            self.hoverColumn = None

    def rotate(self):
        # Rotates the dimension of the block clockwise
        self.dimension = list(zip(*self.dimension[::-1]))

        # Swap the values of the width and height
        placeholder = self.width
        self.width = self.height
        self.height = placeholder