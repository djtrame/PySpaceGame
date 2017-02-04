import pygame
import abc
import colors as c

class SpaceShip:
    __metaclass__ = abc.ABCMeta

    def __init__(self, x, y, width, height, color, missleCooldown):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.missleCooldown = missleCooldown

        #this is the amount of pixels this object moves per frame
        self.x_change = 0
        self.y_change = 0
        self.missles = []

    def leftSide(self):
        return self.x

    def rightSide(self):
        return self.x + self.width

    def topSide(self):
        return self.y

    def bottomSide(self):
        return self.y + self.height

    def move(self):
        self.x += self.x_change

    @abc.abstractmethod
    def fireMissle(self, gameDisplay):
        """Implement a fireMissle method for each type of SpaceShip"""
        return


class HumanSpaceShip(SpaceShip):
    def __init__(self, x, y, width, height, color, missleCooldown=500):
        super().__init__(x, y, width, height, color, missleCooldown)
        self.type = 'human'
        self.missleColor = c.red

    #now handle removing the missle from the collection when it hits the boundary of the screen
    def fireMissle(self, gameDisplay):
        newMissle = Missle(self.x + (self.width / 2), self.y, 5, 20, self.missleColor)
        self.missles.append(newMissle)


class AlienSpaceShip1(SpaceShip):
    def __init__(self, x, y, width, height, color, missleCooldown=500):
        super().__init__(x, y, width, height, color, missleCooldown)
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

    def leftSide(self):
        return self.x

    def rightSide(self):
        return self.x + self.width

    def topSide(self):
        return self.y

    def bottomSide(self):
        return self.y + self.height

    #@abc.abstractmethod
    def move(self):
        self.x += self.x_change
        self.y += self.y_change

    #returns True if the missle goes off the screen
    def check_bounds(self, display_width, display_height):
        if 0 < self.x < display_width and 0 < self.y < display_height:
            return True
        else:
            return False

    #returns True if the missle has collided with the spaceShip
    def check_collision(self, spaceShip):
        #if the missle crosses any boundary of the space ship, return true and we'll blow up the missle and the space ship
        if (spaceShip.leftSide() < self.leftSide() < spaceShip.rightSide()) or \
                (spaceShip.leftSide() < self.rightSide() < spaceShip.rightSide()):
            #print('missle within X bounds of spaceship')
            if (spaceShip.topSide() < self.topSide() < spaceShip.bottomSide()) or \
                    (spaceShip.topSide() < self.bottomSide() < spaceShip.bottomSide()):
                #print ('missle within x and y bounds of spaceship')
                return True
        else:
            return False


