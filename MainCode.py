import sys

import pygame
from SpriteSheet import SpriteSheet
import math
import random
from pygame.locals import *

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

fps = 60
fpsClock = pygame.time.Clock()

clock = pygame.time.Clock()

width, height = 900, 900
pygame.display.set_caption("Devastation Derby")
screen = pygame.display.set_mode((width, height))

class Level():
    def __init__(self):
        self.ScrollX = 0
        self.ScrollY = 0

        self.PowerUps = pygame.sprite.Group()

        self.powerupsound = pygame.mixer.Sound("Sounds/power_up.wav")

        self.background = pygame.image.load("Battlegrounds/RoadRage.jpg")
        self.background = pygame.transform.scale(self.background, (1500, 1500))

    def drawmap(self):
        screen.blit(self.background, ((0 + self.ScrollX), (0 + self.ScrollY)))


    def shiftmaxX(self, left):
        if left == True:
            self.ScrollX = 200
        else:
            self.ScrollX = -750

    def shift_world(self, shift_x, shift_y, poweruplist):
        self.ScrollX = self.ScrollX + shift_x
        self.ScrollY = self.ScrollY + shift_y

        for powerup in poweruplist:
            powerup.rect.x = powerup.rect.x + shift_x
            powerup.rect.y = powerup.rect.y + shift_y

class Collision(pygame.sprite.Sprite):
    def __init__(self, width, height):

        super(Collision, self).__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

class LevelCollisions(pygame.sprite.Sprite):
    def __init__(self):

        self.collision_list = pygame.sprite.Group()

        Level.__init__(self)

        collideparts = []

        for collide in collideparts:
            platform = Collision(collide[0], collide[1])
            platform.rect.x = collide[2]
            platform.rect.y = collide[3]
            self.collision_list.add(platform)


class spawn_powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30, 30])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        self.poweruptypes = ["FireMissile", "HomingMissile", "PowerMissile", "Napalm", "RearMines", "FreezeMissile", "RicochetBombs", "Health", "Satellite", "Shotgun", "Grenade"]

        self.powerupstate = random.choice(self.poweruptypes)

        self.rect.x = x
        self.rect.y = y

        level.PowerUps.add(self)





class PlayerVehicle(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 5
    MAX_REVERSE_SPEED = 2
    ACCELERATION = 2
    TURN_SPEED = 4

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.CarSprites = SpriteSheet("Sprites/SuperCar.png")

        ############# POWER UPS #############

        self.powerups = {
            "None": 999,
            "SpecialWeapon": 3,
            "FireMissile": 0,
            "HomingMissile": 0,
            "PowerMissile": 0,
            "Napalm": 0,
            "RearMines": 0,
            "FreezeMissile": 0,
            "RicochetBombs": 0,
            "Health": 0,
            "Satellite": 0,
            "Shotgun": 0,
            "Grenade": 0
        }

        self.CurrentPowerUp = self.powerups["SpecialWeapon"]

        ############# POWER UPS #############

        self.src_image = self.CarSprites.get_image(15, 201, 35, 60)
        self.rect = self.src_image.get_rect()
        self.position = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0

        self.machinegunsound = pygame.mixer.Sound("Sounds/machine_guns.wav")
        self.specialweaponsound = pygame.mixer.Sound("Sounds/hammerhead_special.wav")
        self.enginesound = pygame.mixer.Sound("Sounds/engine4.wav")
        self.powerupsound = pygame.mixer.Sound("Sounds/power_up.wav")
        self.powerupsound.set_volume(.1)
        self.turning = pygame.mixer.Sound("Sounds/skid.wav")

        self.enginesound.play(-1)

        self.MachineGunOn = False

        self.specialon = False

    def MachineGun(self):
        if self.MachineGunOn == False:
            self.MachineGunOn = True
            self.machinegunsound.play()

    def UsePowerUp(self):
        if self.specialon == False:
            if self.CurrentPowerUp == self.powerups["SpecialWeapon"] and self.powerups["SpecialWeapon"] > 0:
                self.specialon = True
                self.powerups["SpecialWeapon"] -= 1
                self.specialweaponsound.play()


    def positionsetX(self, setpos):
        self.position = setpos, self.position[1]

    def positionsetY(self, setpos):
        self.position = self.position[0], setpos

    def update(self, deltat, level):
        # SIMULATION
        self.speed += (self.k_up + self.k_down)

        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < -self.MAX_REVERSE_SPEED:
            self.speed = -self.MAX_REVERSE_SPEED

        self.direction += (self.k_right + self.k_left)
        x, y = (self.position)
        rad = self.direction * math.pi / 180
        x += -self.speed * math.sin(rad)
        y += -self.speed * math.cos(rad)
        self.position = (x, y)

        self.image = pygame.transform.scale(self.src_image, (50, 80))
        self.image = pygame.transform.rotate(self.image, self.direction)

        self.rect = self.image.get_rect()
        self.rect.center = self.position

        hit_list = pygame.sprite.spritecollide(self, level.PowerUps, False)

        for item in hit_list:
            for listitem in self.powerups:
                if listitem == item.powerupstate:
                    self.powerups[listitem] += 1
                    self.powerupsound.play()
                    print(listitem + ": " + str(self.powerups[listitem]))
            item.kill()




# Game loop.


def Main():
    rect = screen.get_rect()

    level = Level()

    #collisions = LevelCollisions()

    player = PlayerVehicle((500, 500))
    #player.rect.x = 410
    #player.rect.y = 375

    sprites_list = pygame.sprite.Group()

    #collide_list = pygame.sprite.Group()

    powerup_list = pygame.sprite.Group()

    #car_group = pygame.sprite.RenderPlain(player)

    sprites_list.add(player)

    while True:
        deltat = clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if not hasattr(event, 'key'): continue
            down = event.type == KEYDOWN

            if event.key == K_RIGHT:
                player.k_right = down * -5
            elif event.key == K_LEFT:
                player.k_left = down * 5
            elif event.key == K_UP:
                player.k_up = down * 2
            elif event.key == K_DOWN:
                player.k_down = down * -2
            elif event.key == K_SPACE:
                player.MachineGun()
                pow = spawn_powerup(50,50, level)
                powerup_list.add(pow)
            elif event.key == K_LCTRL:
                player.UsePowerUp()

            # Update.
        # Draw.


        if player.rect.right >= 700:
            diff = player.rect.right - 700
            level.shift_world(-diff, 0, powerup_list)
            player.positionsetX(660)
            player.rect.right = 700

        if player.rect.left <= 200:
            diff = 200 - player.rect.left
            level.shift_world(diff, 0, powerup_list)
            player.positionsetX(240)
            player.rect.left = 200

        if player.rect.bottom >= 700:
            diff = player.rect.bottom - 700
            level.shift_world(0, -diff, powerup_list)
            player.positionsetY(660)
            player.rect.bottom = 700

        if player.rect.top <= 200:
            diff = 200 - player.rect.top
            level.shift_world(0, diff, powerup_list)
            player.positionsetY(240)
            player.rect.top = 200

        screen.fill(BLUE)

        level.drawmap()

        powerup_list.draw(screen)

        sprites_list.update(deltat, level)

        sprites_list.update(deltat, level)
        sprites_list.draw(screen)



        pygame.display.flip()
        fpsClock.tick(fps)

Main()