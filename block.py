import pygame
# Mouse States:
# -1 - Free
# 1 - Being dragged by a player
class Block:
    def __init__(self, dimension, x = -1, y = -1, margin = 2):
        self.dimension = dimension
        self.x = x
        self.y = y
        self.dragX = self.x
        self.dragY = self.y
        self.margin = margin
        self.size = 18
        self.state = 0 # 0 - static, 1 - dragged by the player
        self.width = ((len(self.dimension[0])) * self.size) + ((len(self.dimension[0])) * self.margin)
        self.height = ((len(self.dimension)) * self.size) + ((len(self.dimension)) * self.margin)

        
    def draw(self, color, screen):
        pygame.draw.rect(screen, "white", (self.x - self.margin, self.y - self.margin, self.width + self.margin, self.height + self.margin))
        
        for i in range(len(self.dimension)):
            yy = self.dragY + ((self.size + self.margin) * i)
            for j in range(len(self.dimension[i])):
                xx = self.dragX + ((self.size + self.margin) * j)

                if (self.dimension[i][j] != -1):
                    pygame.draw.rect(screen, color, (xx, yy, self.size, self.size))

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.dragX = x
        self.dragY = y

    def drag(self):
        mouse = pygame.mouse
        if (mouse.get_pressed()[0]):
            self.dragX = mouse.get_pos()[0]
            self.dragY = mouse.get_pos()[1]


