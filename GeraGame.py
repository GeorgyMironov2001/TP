import pygame
import math
import random

pygame.init()
win = pygame.display.set_mode((1500, 800))
pygame.display.set_caption("Gera Game")

WalkRight = [pygame.image.load('GeraGame/pygame_right_1.png'), pygame.image.load('GeraGame/pygame_right_2.png'),
             pygame.image.load('GeraGame/pygame_right_3.png'),
             pygame.image.load('GeraGame/pygame_right_4.png'), pygame.image.load('GeraGame/pygame_right_5.png'),
             pygame.image.load('GeraGame/pygame_right_6.png')]

WalkLeft = [pygame.image.load('GeraGame/pygame_left_1.png'), pygame.image.load('GeraGame/pygame_left_2.png'),
            pygame.image.load('GeraGame/pygame_left_3.png'),
            pygame.image.load('GeraGame/pygame_left_4.png'), pygame.image.load('GeraGame/pygame_left_5.png'),
            pygame.image.load('GeraGame/pygame_left_6.png')]

PiratRight = [pygame.image.load('GeraGame/Pirat_right__001.png'), pygame.image.load('GeraGame/Pirat_right__002.png'),
              pygame.image.load('GeraGame/Pirat_right__003.png'), pygame.image.load('GeraGame/Pirat_right__004.png'),
              pygame.image.load('GeraGame/Pirat_right__005.png'), pygame.image.load('GeraGame/Pirat_right__006.png')]

PiratLeft = [pygame.image.load('GeraGame/Pirat_left__001.png'), pygame.image.load('GeraGame/Pirat_left__002.png'),
             pygame.image.load('GeraGame/Pirat_left__003.png'), pygame.image.load('GeraGame/Pirat_left__004.png'),
             pygame.image.load('GeraGame/Pirat_left__005.png'), pygame.image.load('GeraGame/Pirat_left__006.png'), ]
PiratStand = pygame.image.load('GeraGame/PiratStand.png')
BG = pygame.image.load('GeraGame/BG2.jpg')
PlayerStand = pygame.image.load('GeraGame/pygame_idle.png')

clock = pygame.time.Clock()
x = 50
y = 50
width = 60
height = 71
speed = 6

IsJump = False
JumpCount = 10

left = False
right = False

AnimCount = 0

BulletType = "OrdinaryBullet"
BulletTypes = ["OrdinaryBullet", "TeleportBullet"]
bullet_index = 0
health = 100000


class snaryad():
    def __init__(self, x, y, radius, color, BiasX, BiasY, damage):
        self.x = int(x)
        self.y = int(y)
        self.radius = int(radius)
        self.color = color
        self.BiasX = int(BiasX)
        self.BiasY = int(BiasY)
        self.damage = int(damage)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class OrdinaryBullet(snaryad):
    def __init__(self, x, y, radius, color, BiasX, BiasY, damage):
        super().__init__(x, y, radius, color, BiasX, BiasY, damage)


class TeleportBullet(snaryad):
    def __init__(self, x, y, radius, color, BiasX, BiasY, damage):
        super().__init__(x, y, radius, color, BiasX, BiasY, damage)


class Person():
    def __init__(self, x, y, width, height, speed, left, right, AnimCount, BulletType, WalkRight, Walkleft,
                 PlayerStand, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.left = left
        self.right = right
        self.AnimCount = AnimCount
        self.BulletType = BulletType
        self.WalkRight = WalkRight
        self.WalkLeft = Walkleft
        self.PlayerStand = PlayerStand
        self.health = health

    def draw(self):
        if self.AnimCount + 1 >= 30:
            self.AnimCount = 0
        if self.left:
            win.blit(self.WalkLeft[self.AnimCount // int(30 / len(self.WalkLeft))],
                     (self.x, self.y))
            self.AnimCount += 1
        elif self.right:
            win.blit(self.WalkRight[self.AnimCount // int(30 / len(self.WalkRight))],
                     (self.x, self.y))
            self.AnimCount += 1
        else:
            win.blit(self.PlayerStand, (self.x, self.y))


class Tramp(Person):
    def __init__(self, x, y, width, height, speed, left, right, AnimCount, BulletType, WalkRight, Walkleft,
                 PlayerStand, IsJump, JumpCount, health, BulletColor):
        super().__init__(x, y, width, height, speed, left, right, AnimCount, BulletType, WalkRight, Walkleft,
                         PlayerStand, health)
        self.IsJump = IsJump
        self.JumpCount = JumpCount
        self.BulletColor = BulletColor


class Pirat(Person):
    def __init__(self, x, y, width, height, speed, left, right, AnimCount, BulletType, WalkRight, Walkleft,
                 PlayerStand, TimeToShoot, health, BulletColor):
        super().__init__(x, y, width, height, speed, left, right, AnimCount, BulletType, WalkRight, Walkleft,
                         PlayerStand, health)
        self.TimeToShoot = TimeToShoot
        self.BulletColor = BulletColor


def DrawWindow():
    win.blit(BG, (0, 0))
    for charaster in Persons:
        charaster.draw()
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


TimeForPirat = 0
bullets = []
Persons = [
    Tramp(x, y, width, height, speed, left, right, AnimCount, BulletType, WalkRight, WalkLeft, PlayerStand, IsJump,
          JumpCount, health, [(0, 0, 0), (50, 50, 255)])]
run = True
while run:

    clock.tick(60)

    for event in pygame.event.get():  # обрабатываем единичные нажатия
        if (event.type == pygame.QUIT):
            run = False
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_TAB):
                bullet_index += 1
                bullet_index = bullet_index % len(BulletTypes)
                Persons[0].BulletType = BulletTypes[bullet_index]
            if (event.key == pygame.K_CAPSLOCK):
                bullet_index += 1
                bullet_index = bullet_index % len(BulletTypes)
                Persons[0].BulletType = BulletTypes[bullet_index]
            if (event.key == pygame.K_p):
                Persons.append(
                    Pirat(x + random.randint(0, 1000), y + random.randint(0, 700), 140, 119, 2, left, right, AnimCount,
                          BulletType, PiratRight,
                          PiratLeft, PiratStand, 1, 10, [(255, 0, 0), (50, 50, 255)]))
        if (event.type == pygame.MOUSEBUTTONDOWN):
            k = (math.sqrt(((event.pos[0] - (round(Persons[0].x + Persons[0].width // 2))) ** 2) + (
                    (event.pos[1] - (round(Persons[0].y + Persons[0].height // 2) + 10)) ** 2))) / 10

            if (Persons[0].BulletType == "TeleportBullet"):
                q = 0
                for x in bullets:
                    if (isinstance(x, TeleportBullet)):
                        q = 1
                        Persons[0].x = x.x
                        Persons[0].y = x.y
                        bullets.pop(bullets.index(x))
                if (q == 0):
                    bullet = TeleportBullet(round(Persons[0].x + Persons[0].width // 2),
                                            round(Persons[0].y + Persons[0].height // 2) + 10, 10, (50, 50, 255),
                                            round((event.pos[0] - round(Persons[0].x + Persons[0].width // 2)) / k),
                                            round((event.pos[1] - round(
                                                Persons[0].y + Persons[0].height // 2) + 10) / k / 2), 1)
                    bullets.append(bullet)
            elif Persons[0].BulletType == "OrdinaryBullet":
                bullet = snaryad(round(Persons[0].x + Persons[0].width // 2),
                                 round(Persons[0].y + Persons[0].height // 2) + 10, 5, (0, 0, 0),
                                 round((event.pos[0] - round(Persons[0].x + Persons[0].width // 2)) / k),
                                 round((event.pos[1] - round(
                                     Persons[0].y + Persons[0].height // 2) + 10) / k), 1)
                bullets.append(bullet)

    for bullet in bullets:
        for charaster in Persons:
            if (not charaster.BulletColor.__contains__(bullet.color)) and ((((charaster.x + round(
                    charaster.width / 2)) - bullet.x) ** 2) + (((charaster.y + round(
                charaster.height / 2)) - bullet.y) ** 2) < ((charaster.height / 2 + bullet.radius / 2) ** 2)):

                charaster.health -= bullet.damage
                bullets.pop(bullets.index(bullet))
                if (charaster.health <= 0):
                    Persons.pop(Persons.index(charaster))
                break
    for bullet in bullets:
        if bullet.x < 1500 and bullet.x > 0 and bullet.y > 0 and bullet.y < 800:
            bullet.x += bullet.BiasX
            bullet.y += bullet.BiasY
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_1]):
        Persons[0].BulletType = "OrdinaryBullet"

    if (keys[pygame.K_2]):
        Persons[0].BulletType = "TeleportBullet"

    if (keys[pygame.K_a]) and Persons[0].x > 5:
        Persons[0].x -= Persons[0].speed
        Persons[0].left = True
        Persons[0].right = False

    elif (keys[pygame.K_d]) and Persons[0].x < 1500 - Persons[0].width - 5:
        Persons[0].x += Persons[0].speed
        Persons[0].right = True
        Persons[0].left = False
    else:
        Persons[0].left = False
        Persons[0].right = False
        Persons[0].AnimCount = 0

    if not (Persons[0].IsJump):
        if (keys[pygame.K_w]) and Persons[0].y > 5:
            if (Persons[0].left):
                Persons[0].y -= round(Persons[0].speed / math.sqrt(2))
                Persons[0].x += round(Persons[0].speed * (1 - (1 / math.sqrt(2))))
            elif Persons[0].right:
                Persons[0].y -= round(Persons[0].speed / math.sqrt(2))
                Persons[0].x -= round(Persons[0].speed * (1 - (1 / math.sqrt(2))))
            else:
                Persons[0].y -= Persons[0].speed

        if (keys[pygame.K_s]) and Persons[0].y < 800 - Persons[0].height - 5:
            if (Persons[0].left):
                Persons[0].y += round(Persons[0].speed / math.sqrt(2))
                Persons[0].x += round(Persons[0].speed * (1 - (1 / math.sqrt(2))))
            elif (Persons[0].right):
                Persons[0].y += round(Persons[0].speed / math.sqrt(2))
                Persons[0].x -= round(Persons[0].speed * (1 - (1 / math.sqrt(2))))
            else:
                Persons[0].y += Persons[0].speed

        if (keys[pygame.K_SPACE]):
            Persons[0].IsJump = True

    else:
        if Persons[0].JumpCount >= -10:
            if (Persons[0].JumpCount >= 0):
                Persons[0].y -= (Persons[0].JumpCount ** 2) / 5
            else:
                Persons[0].y += (Persons[0].JumpCount ** 2) / 5

            Persons[0].JumpCount -= 1
        else:
            Persons[0].IsJump = False
            Persons[0].JumpCount = 10

    if (TimeForPirat == 0):
        Persons.append(
            Pirat(x + random.randint(0, 20), y, 140, 119, 2, left, right, AnimCount, BulletType, PiratRight,
                  PiratLeft, PiratStand, 1, 10, [(255, 0, 0), (50, 50, 255)]))
        TimeForPirat = 1
    for a in range(1, len(Persons)):
        Persons[a].TimeToShoot += 1
        if (((Persons[0].x - Persons[a].x) ** 2) + ((Persons[0].y - Persons[a].y) ** 2) >= 0):
            if (Persons[0].x - Persons[a].x > 0):
                Persons[a].right = True
                Persons[a].left = False
                if Persons[0].x - Persons[a].x <= Persons[a].speed:
                    Persons[a].x += Persons[0].x - Persons[a].x
                else:
                    Persons[a].x += Persons[a].speed

                if (Persons[0].y - Persons[a].y > 0):
                    if (Persons[0].y - Persons[a].y <= Persons[a].speed):
                        Persons[a].y += Persons[0].y - Persons[a].y
                    else:
                        Persons[a].y += Persons[a].speed
                elif (Persons[0].y - Persons[a].y < 0):
                    if (Persons[a].y - Persons[0].y <= Persons[a].speed):
                        Persons[a].y -= Persons[a].y - Persons[0].y
                    else:
                        Persons[a].y -= Persons[a].speed

            elif Persons[0].x - Persons[a].x < 0:
                Persons[a].right = False
                Persons[a].left = True
                if Persons[a].x - Persons[0].x <= Persons[a].speed:
                    Persons[a].x -= Persons[a].x - Persons[0].x
                else:
                    Persons[a].x -= Persons[a].speed

                if (Persons[0].y - Persons[a].y > 0):
                    if (Persons[0].y - Persons[a].y <= Persons[a].speed):
                        Persons[a].y += Persons[0].y - Persons[a].y
                    else:
                        Persons[a].y += Persons[a].speed
                elif (Persons[0].y - Persons[a].y < 0):
                    if (Persons[a].y - Persons[0].y <= Persons[a].speed):
                        Persons[a].y -= Persons[a].y - Persons[0].y
                    else:
                        Persons[a].y -= Persons[a].speed
            else:
                Persons[a].left = False
                Persons[a].right = False

                if (Persons[0].y - Persons[a].y > 0):
                    if (Persons[0].y - Persons[a].y <= Persons[a].speed):
                        Persons[a].y += Persons[0].y - Persons[a].y
                    else:
                        Persons[a].y += Persons[a].speed
                elif (Persons[0].y - Persons[a].y < 0):
                    if (Persons[a].y - Persons[0].y <= Persons[a].speed):
                        Persons[a].y -= Persons[a].y - Persons[0].y
                    else:
                        Persons[a].y -= Persons[a].speed
        else:
            Persons[a].left = False
            Persons[a].right = False

        if (Persons[a].TimeToShoot == 100):
            Persons[a].TimeToShoot = 0
            k = (math.sqrt(((Persons[0].x - (round(Persons[a].x + Persons[a].width // 2))) ** 2) + (
                    (Persons[0].y - (round(Persons[a].y + Persons[a].height // 2) + 10)) ** 2))) / 10
            if (Persons[a].left):
                bullet = snaryad(round(Persons[a].x + Persons[a].width // 2) - 25,
                                 round(Persons[a].y + Persons[a].height // 2) + 7, 5, (255, 0, 0),
                                 round((Persons[0].x - round(Persons[a].x + Persons[a].width // 2)) / k),
                                 round((Persons[0].y + 20 - round(
                                     Persons[a].y + Persons[a].height // 2) + 10) / k), 1)
            else:
                bullet = snaryad(round(Persons[a].x + Persons[a].width // 2) + 25,
                                 round(Persons[a].y + Persons[a].height // 2) + 7, 5, (255, 0, 0),
                                 round((Persons[0].x - round(Persons[a].x + Persons[a].width // 2)) / k),
                                 round((Persons[0].y + 20 - round(
                                     Persons[a].y + Persons[a].height // 2) + 10) / k), 1)
            bullets.append(bullet)

    DrawWindow()
pygame.quit()
