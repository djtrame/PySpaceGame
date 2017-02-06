import pygame
import colors as c
import random
import re
from PySpaceGame_Classes import *

pygame.init()

display_width = 800
display_height = 600

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('PySpaceGame')

FPS = 30

smallfont = pygame.font.Font("fonts/freesansbold.ttf", 25)
mediumfont = pygame.font.Font("fonts/freesansbold.ttf", 50)
largefont = pygame.font.Font("fonts/freesansbold.ttf", 80)

def main():
    gameOver = False
    gameExit = False

    mySpaceShip = HumanSpaceShip(500, 500, 30, 30, c.blue)
    alienSpaceShipSize = 30
    alienFirstRowX = 120
    alienFirstRowY = 200

    #initialize a game object to keep track of ships, missles and general gameState stuff
    #it doesn't make a lot of sense for all aliens to ahve a fire delay, need to make that individual so the last guy isn't a machine gun
    myGame = Game(60, 30)

    lastFire = 0
    missleOffCooldown = True

    #space invaders is 5 rows of 11
    #only the bottom ship in each row can shoot
    #missles can collide

    #create alien ships
    #missles now are owned by the game, not the ships.
    #i want to find a way for a missle to know its owner so we give that owner powerups in future levels
    testDict = {}
    for i in range(0,10):
        alienSpaceShipColumn = []
        colPrefix = 'c' + str(i)
        for j in range(0, 2):
            newAlienSpaceShip = AlienSpaceShip1(alienFirstRowX + (i * alienSpaceShipSize * 2), alienFirstRowY + (j * alienSpaceShipSize * 2),
                                                alienSpaceShipSize, alienSpaceShipSize, c.gray)
            alienSpaceShipColumn.append(newAlienSpaceShip)
            testDict.update({colPrefix + 'r' + str(j):newAlienSpaceShip})
        myGame.alienSpaceShipColumns.append(alienSpaceShipColumn)

    #decide which alien ships can shoot.  should just be the bottom most ship in each column
    for alienSpaceShipColumn in myGame.alienSpaceShipColumns:
        #the last element in each column is allowed to shoot
        lastIndexOfColumn = len(alienSpaceShipColumn) - 1
        alienSpaceShipColumn[lastIndexOfColumn].canShoot = True


    while not gameExit:
        #each frame check to see if the human missle is able to fire
        if not missleOffCooldown:
            now = pygame.time.get_ticks()
            if (now - lastFire) > mySpaceShip.missleCooldown:
                missleOffCooldown = True

        #each few frames randomly decide for one of the aliens to fire
        myGame.alienRandomFireFrameCounter += 1
        if myGame.alienRandomFireFrameCounter > myGame.alienRandomFireDelay:
            myGame.alienRandomFireFrameCounter = 0

            aliensThatCanShoot = []

            # have the alien ships that can shoot actually fire a missle
            for alienSpaceShipColumn in myGame.alienSpaceShipColumns:
                for alienSS in alienSpaceShipColumn:
                    if alienSS.canShoot == True:
                        aliensThatCanShoot.append(alienSS)
                        #myGame.alienMissles.append(alienSS.fireMissle())

            #randomly pick one of those
            if myGame.count_aliens() > 0:
                randIndex = random.randint(0, len(aliensThatCanShoot) - 1)
                myGame.alienMissles.append(aliensThatCanShoot[randIndex].fireMissle())


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #use keys for testing certain functions
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameExit = True

                elif event.key == pygame.K_LEFT:
                    #print('left')
                    mySpaceShip.x_change -= 10

                elif event.key == pygame.K_RIGHT:
                    #print('right')
                    mySpaceShip.x_change += 10

                elif event.key == pygame.K_SPACE:
                    #print('fire')

                    #each frame we check if the missle is off cooldown.
                    #the default is True so this will fire the first time no matter what
                    if missleOffCooldown:
                        myGame.playerMissles.append(mySpaceShip.fireMissle())
                        missleOffCooldown = False
                        lastFire = pygame.time.get_ticks()

                elif event.key == pygame.K_w:
                    print('Print dictionary:')
                    print(testDict)

                elif event.key == pygame.K_e:
                    #list comprehension on a dictionary
                    listOfAliens = []
                    for key in testDict.keys():
                        if re.search(key, 'c\dr\d'):
                            listOfAliens.append(testDict[key])

                    print(listOfAliens)

                elif event.key == pygame.K_r:
                    print('pass')

                elif event.key == pygame.K_t:
                    print('pass')

                elif event.key == pygame.K_y:
                    print('pass')

                elif event.key == pygame.K_u:
                    print('pass')

                elif event.key == pygame.K_i:
                    print('pass')

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    mySpaceShip.x_change = 0

                elif event.key == pygame.K_RIGHT:
                    mySpaceShip.x_change = 0

                # elif event.key == pygame.K_SPACE:
                #     #print('space up')
                #     pass

        gameDisplay.fill(c.black)

        #if missles have been fired move them by 1 frame, check if they went off the screen, and check if they collided with something
        if len(myGame.playerMissles) > 0:
            for missle in myGame.playerMissles:
                missle.move()
                if not missle.check_bounds(display_width, display_height):
                    #print('missle out of bounds')
                    myGame.playerMissles.remove(missle)
                else:
                    #check collisions with all alien ships
                    if len(myGame.alienSpaceShipColumns) > 0:
                        for alienSSColumn in myGame.alienSpaceShipColumns:
                            for alienSS in alienSSColumn:
                                if missle.check_collision(alienSS):
                                    myGame.playerMissles.remove(missle)
                                    alienSSColumn.remove(alienSS)

                                    #since 1 alien from this column got killed, make sure the bottom most one can shoot
                                    aliensLeftInColumn = len(alienSSColumn)

                                    if aliensLeftInColumn > 0:
                                        alienSSColumn[aliensLeftInColumn - 1].canShoot = True



                pygame.draw.rect(gameDisplay, missle.color, (missle.x, missle.y, missle.width, missle.height))


        if len(myGame.alienMissles) > 0:
            for missle in myGame.alienMissles:
                missle.move()
                if not missle.check_bounds(display_width, display_height):
                    myGame.alienMissles.remove(missle)
                else:
                    if missle.check_collision(mySpaceShip):
                        myGame.alienMissles.remove(missle)
                        print('BOOM! We ded.')

                pygame.draw.rect(gameDisplay, missle.color, (missle.x, missle.y, missle.width, missle.height))

        mySpaceShip.move()

        #draw the player's space ship
        pygame.draw.rect(gameDisplay, mySpaceShip.color, (mySpaceShip.x, mySpaceShip.y, mySpaceShip.width, mySpaceShip.height))

        if len(myGame.alienSpaceShipColumns) > 0:
            #decide if the aliens are stutter stepping right or left
            stutterStep = 'right'
            myGame.alienStutterStepFrameCounter += 1
            if myGame.alienStutterStepFrameCounter > myGame.alienStutterStepDelay:
                myGame.alienStutterStepFrameCounter = 0
                myGame.alienStutterStepDistance *= -1
                if stutterStep == 'right':
                    stutterStep == 'left'
                else:
                    stutterStep == 'right'

            for alienSSColumn in myGame.alienSpaceShipColumns:
                for alienSS in alienSSColumn:
                    alienSS.x_change = myGame.alienStutterStepDistance
                    alienSS.move()
                    pygame.draw.rect(gameDisplay, alienSS.color, (alienSS.x, alienSS.y, alienSS.width, alienSS.height))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()