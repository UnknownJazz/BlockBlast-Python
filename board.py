import pygame

class Board:
    def __init__(self, x, y, rows, columns, slotSize = 64):
        self.board = [[-1 for i in range(rows)] for j in range(columns)]
        self.slotSize = slotSize
        self.rows = rows
        self.columns = columns
        self.x = x
        self.y = y

    def draw(self, screen, margin = 2):
        colors = {
            -1 : "black",
            0 : "gray",
            1 : "green"
        }

        self.margin = margin
        for i in range(len(self.board)): # Row
            yy = self.y + ((self.slotSize + margin) * i)
            for j in range(len(self.board[i])): # Column
                xx = self.x + ((self.slotSize + margin) * j)
                # -1 = Empty
                # 0 = Hover
                # > 0 = Naay sulod
                pygame.draw.rect(screen, (colors[self.board[i][j]]), (xx, yy, self.slotSize, self.slotSize))

    def update(self):
        self.checkMouseCollision()

    def checkMouseCollision(self): # checks if the mouse is inside the board
        yy = self.y + ((self.slotSize + 2) * self.rows)
        if (pygame.mouse.get_pos()[0] > self.x and pygame.mouse.get_pos()[1] < yy): # Check if the mouse is inside the board
            self.checkMouseCollisionSlot()
    
    def checkMouseCollisionSlot(self): # checks if the mouse is hovering a slot
        margin = 2
        for i in range(len(self.board)): # Row
            yy = self.y + ((self.slotSize + margin) * i)
            for j in range(len(self.board[i])): # Column
                xx = self.x + ((self.slotSize + margin) * j)
                currentBoard = self.board[i][j]
                # Check for horizontal and vertical collision
                if (pygame.mouse.get_pos()[0] > xx and pygame.mouse.get_pos()[0] < xx + self.slotSize) and (pygame.mouse.get_pos()[1] > yy and pygame.mouse.get_pos()[1] < yy + self.slotSize):
                    
                    # Set value to a slot if the mouse is pressed and the slot is empty
                    mouse_pressed = pygame.mouse.get_pressed()[0]
                    if (currentBoard == -1):
                        self.setSlotValue(i, j, 0)
                    if(currentBoard == 0 and mouse_pressed):
                        self.setSlotValue(i, j, 1)
                else:
                    if (currentBoard == 0):
                        self.setSlotValue(i, j, -1)

    def setSlotValue(self, row, column, value):
        self.board[row][column] = value

    def print(self):
        for i in self.board:
            print(i)