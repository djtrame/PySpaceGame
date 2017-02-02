import pygame
import abc

class SpaceShip:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        #this is the amount of pixels this object moves per frame
        self.x_change = 0
        self.y_change = 0


