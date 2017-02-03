import pygame
import abc
import colors as c

class SpaceShip:
    __metaclass__ = abc.ABCMeta

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        #this is the amount of pixels this object moves per frame
        self.x_change = 0
        self.y_change = 0
        self.missles = []

    @abc.abstractmethod
    def fireMissle(self, gameDisplay):
        """Implement a fireMissle method for each type of SpaceShip"""
        return

class HumanSpaceShip(SpaceShip):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.type = 'human'
        self.missleColor = c.red

    #now handle removing the missle from the collection when it hits the boundary of the screen
    def fireMissle(self, gameDisplay):
        newMissle = Missle(self.x, self.y, 5, 20, self.missleColor)
        self.missles.append(newMissle)


class AlienSpaceShip1(SpaceShip):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.type = 'alien'

    def fireMissle(self, gameDisplay):
        return 'Fire!'

#should I have the game own missle objects or the firing ship own them?  hmm
#going to have the ships own them for powerups... hmmmmmmm indeed
class Missle():
    #__metaclass__ = abc.ABCMeta

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.x_change = 0
        #defaulting the y movement to 5 so its default behavior is to fly
        self.y_change = -5

    #@abc.abstractmethod
    def move(self):
        self.x += self.x_change
        self.y += self.y_change