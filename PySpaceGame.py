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

    mySpaceShip = HumanSpaceShip(500, 500, 20, 20, c.blue)

    while not gameExit:

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
                    mySpaceShip.fireMissle(gameDisplay)

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

        mySpaceShip.x += mySpaceShip.x_change

        pygame.draw.rect(gameDisplay, mySpaceShip.color, (mySpaceShip.x, mySpaceShip.y, mySpaceShip.width, mySpaceShip.height))

        if len(mySpaceShip.missles) > 0:
            missle = mySpaceShip.missles[0]
            missle.move()
            pygame.draw.rect(gameDisplay, missle.color, (missle.x, missle.y, missle.width, missle.height))

        pygame.draw.rect(gameDisplay, c.green, (400, 300, 10, 10))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()