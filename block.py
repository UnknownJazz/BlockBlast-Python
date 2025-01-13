import pygame

class Block:
    def __init__(self, dimension):
        self.dimension = dimension
        
    def draw(self, x, y, color, screen, size = 48, margin = 2):
        for i in range(len(self.dimension)):
            yy = y + ((size + margin) * i)
            for j in range(len(self.dimension[i])):
                xx = x + ((size + margin) * j)

                if (self.dimension[i][j] != -1):
                    pygame.draw.rect(screen, color, (xx, yy, size, size))
