import pygame
import colors as c
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
    alienStutterStepDistance = -1
    alienStutterStepFrameCounter = 0
    alienStutterStepSpeed = 60 #the lower the number = the faster the aliens step left and right
    alienSpaceShips = []

    lastFire = 0
    missleOffCooldown = True



    #create alien ships
    for i in range(0,10):
        newAlienSpaceShip = AlienSpaceShip1(alienFirstRowX + (i * alienSpaceShipSize * 2), alienFirstRowY, alienSpaceShipSize, alienSpaceShipSize, c.gray)
        alienSpaceShips.append(newAlienSpaceShip)

    while not gameExit:
        #each frame check to see if the human missle is able to fire
        if not missleOffCooldown:
            now = pygame.time.get_ticks()
            if (now - lastFire) > mySpaceShip.missleCooldown:
                missleOffCooldown = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #use keys for testing certain functions
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameExit = True

                elif event.key == pygame.K_LEFT:
                    print('left')
                    mySpaceShip.x_change -= 10

                elif event.key == pygame.K_RIGHT:
                    print('right')
                    mySpaceShip.x_change += 10

                elif event.key == pygame.K_SPACE:
                    print('fire')

                    #each frame we check if the missle is off cooldown.
                    #the default is True so this will fire the first time no matter what
                    if missleOffCooldown:
                        mySpaceShip.fireMissle(gameDisplay)
                        missleOffCooldown = False
                        lastFire = pygame.time.get_ticks()

                elif event.key == pygame.K_w:
                    print('pass')
                    pass

                elif event.key == pygame.K_e:
                    print('pass')
                    pass

                elif event.key == pygame.K_r:
                    print('pass')
                    pass

                elif event.key == pygame.K_t:
                    print('pass')
                    pass

                elif event.key == pygame.K_y:
                    print('pass')
                    pass

                elif event.key == pygame.K_u:
                    print('pass')
                    pass

                elif event.key == pygame.K_i:
                    print('pass')
                    pass

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    mySpaceShip.x_change = 0

                elif event.key == pygame.K_RIGHT:
                    mySpaceShip.x_change = 0

                elif event.key == pygame.K_SPACE:
                    #print('space up')
                    pass

        gameDisplay.fill(c.black)

        #if missles have been fired move them by 1 frame, check if they went off the screen, and check if they collided with something
        if len(mySpaceShip.missles) > 0:
            for missle in mySpaceShip.missles:
                missle.move()
                if not missle.check_bounds(display_width, display_height):
                    print('missle out of bounds')
                    mySpaceShip.missles.remove(missle)
                else:
                    #check collisions with all alien ships
                    if len(alienSpaceShips) > 0:
                        for alienSS in alienSpaceShips:
                            if missle.check_collision(alienSS):
                                mySpaceShip.missles.remove(missle)
                                alienSpaceShips.remove(alienSS)

                pygame.draw.rect(gameDisplay, missle.color, (missle.x, missle.y, missle.width, missle.height))

        mySpaceShip.move()

        pygame.draw.rect(gameDisplay, mySpaceShip.color, (mySpaceShip.x, mySpaceShip.y, mySpaceShip.width, mySpaceShip.height))

        if len(alienSpaceShips) > 0:
            #decide if the aliens are stutter stepping right or left
            stutterStep = 'right'
            alienStutterStepFrameCounter += 1
            if alienStutterStepFrameCounter > alienStutterStepSpeed:
                alienStutterStepFrameCounter = 0
                alienStutterStepDistance *= -1
                if stutterStep == 'right':
                    stutterStep == 'left'
                else:
                    stutterStep == 'right'


            for alienSS in alienSpaceShips:
                alienSS.x_change = alienStutterStepDistance
                alienSS.move()
                pygame.draw.rect(gameDisplay, alienSS.color, (alienSS.x, alienSS.y, alienSS.width, alienSS.height))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()