import pygame
import random
import math

pygame.init()
win = pygame.display.set_mode((1500, 800))
pygame.display.set_caption("Gera Game")


def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


WalkRight = [pygame.image.load('GeraGame/pygame_right_1.png'), pygame.image.load('GeraGame/pygame_right_2.png'),
             pygame.image.load('GeraGame/pygame_right_3.png'),
             pygame.image.load('GeraGame/pygame_right_4.png'), pygame.image.load('GeraGame/pygame_right_5.png'),
             pygame.image.load('GeraGame/pygame_right_6.png'), ]

WalkLeft = [pygame.image.load('GeraGame/pygame_left_1.png'), pygame.image.load('GeraGame/pygame_left_2.png'),
            pygame.image.load('GeraGame/pygame_left_3.png'),
            pygame.image.load('GeraGame/pygame_left_4.png'), pygame.image.load('GeraGame/pygame_left_5.png'),
            pygame.image.load('GeraGame/pygame_left_6.png'), ]
PiratRight = [pygame.image.load('GeraGame/2_entity_000_WALK_000.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_001.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_002.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_003.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_004.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_005.png'),
              pygame.image.load('GeraGame/2_entity_000_WALK_006.png')]
PiratLeft = [pygame.image.load('GeraGame/2_entity_000_WALKLeft_000.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_001.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_002.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_003.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_004.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_005.png'),
             pygame.image.load('GeraGame/2_entity_000_WALKLeft_006.png')]
BackGrounds = [[pygame.image.load('GeraGame/весна1.jpg'), pygame.image.load('GeraGame/весна2.jpg'),
                pygame.image.load('GeraGame/весна3.jpg'), pygame.image.load('GeraGame/весна4.jpg')],
               [pygame.image.load('GeraGame/лето1.jpg'), pygame.image.load('GeraGame/лето2.jpg'),
                pygame.image.load('GeraGame/лето3.jpg'), pygame.image.load('GeraGame/лето4.jpg'),
                pygame.image.load('GeraGame/лето8.jpg')],
               [pygame.image.load('GeraGame/осень1.jpg'), pygame.image.load('GeraGame/осень2.jpg'),
                pygame.image.load('GeraGame/осень3.jpg'), pygame.image.load('GeraGame/осень4.jpg')],
               [pygame.image.load('GeraGame/зима1.jpg'), pygame.image.load('GeraGame/зима2.jpg'),
                pygame.image.load('GeraGame/зима3.jpg'), pygame.image.load('GeraGame/зима4.jpg'),
                pygame.image.load('GeraGame/зима5.jpg')]]

sezon = 0
BGIndex = 0
PiratStand = pygame.image.load('GeraGame/2_entity_000_ATTACK_003.png')
PlayerStand = pygame.image.load('GeraGame/pygame_idle.png')

bomb = pygame.image.load('GeraGame/бомба.png')
Explosion = [pygame.image.load('GeraGame/Explosion1.png'), pygame.image.load('GeraGame/Explosion2.png'),
             pygame.image.load('GeraGame/Explosion3.png'), pygame.image.load('GeraGame/Explosion4.png'),
             pygame.image.load('GeraGame/Explosion5.png')]
clock = pygame.time.Clock()
x = 50
y = 50
width = 60
height = 71
speed = 5

IsJump = False
JumpCount = 10

left = False
right = False

AnimCount = 0

BulletType = "OrdinaryBullet"
KindsOfBullet = ["OrdinaryBullet", "TeleportBullet"]
BuletIndex = 0


class Weapon():
    x = None
    y = None


class Bomb(Weapon):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    bomb = bomb
    damage = 5
    AnimCount = 0
    Explosion = Explosion
    IsBoom = False
    cost = 6

    def draw(self, win, i):
        if self.AnimCount + 1 >= 30:
            weapons.pop(i)
        if self.IsBoom:
            win.blit(self.Explosion[self.AnimCount // round(1 + (30 / len(self.Explosion)))], (self.x, self.y))
            self.AnimCount += 1
        else:
            win.blit(self.bomb, (self.x, self.y))


class snaryad():
    x = None
    y = None
    radius = None
    color = None
    BiasX = None
    BiasY = None
    damage = None
    TimeToLife = None

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def Work(self):
        if self.TimeToLife > 0:
            self.x += self.BiasX
            self.y += self.BiasY
            self.TimeToLife -= 1
        else:
            bullets.pop(bullets.index(bullet))


class OrdinaryBullet(
    snaryad):  # bullets.append(OrdinaryBullet(x1, y1, 5, (0, 0, 0), BiasX, BiasY, 1, "OrdinaryBullet"))

    def __init__(self, x, y, BiasX, BiasY):
        self.x = x
        self.y = y
        self.BiasX = BiasX
        self.BiasY = BiasY

    color = (0, 0, 0)
    radius = 5
    damage = 1
    type = "OrdinaryBullet"
    TimeToLife = 200

    cost = 0


class TeleportBullet(
    snaryad):  # bullets.append(TeleportBullet(x1, y1, 10, (0, 0, 255), BiasX, BiasY, 1, "TeleportBullet"))
    def __init__(self, x, y, BiasX, BiasY):
        self.x = x
        self.y = y
        self.BiasX = BiasX
        self.BiasY = BiasY

    radius = 10
    color = (0, 0, 255)
    type = "TeleportBullet"
    TimeToLife = 300
    cost = 1


class Person():
    x = None
    y = None
    width = None
    height = None
    speed = None
    left = None
    right = None
    AnimCount = None
    WalkRight = None
    WalkLeft = None
    PlayerStand = None
    health = None
    Colors = None

    def draw(self, win):
        if self.AnimCount + 1 >= 30:
            self.AnimCount = 0
        if self.left:
            win.blit(self.WalkLeft[self.AnimCount // round(1 + (30 / len(self.WalkLeft)))], (self.x, self.y))
            self.AnimCount += 1
        elif self.right:
            win.blit(self.WalkRight[self.AnimCount // round(1 + (30 / len(self.WalkRight)))], (self.x, self.y))
            self.AnimCount += 1
        else:
            win.blit(self.PlayerStand, (self.x, self.y))
        x = self.x
        y = self.y
        for i in range(self.health):
            pygame.draw.circle(win, (255, 0, 0), (x + i * 4, y), 2)


class Tramp(Person):
    x = 50
    y = 50
    width = width
    height = height
    speed = 5
    left = False
    right = False
    AnimCount = 0
    WalkRight = WalkRight
    WalkLeft = WalkLeft
    PlayerStand = PlayerStand
    health = 10
    Colors = [(0, 0, 0), (0, 0, 255)]
    IsJump = False
    JumpCount = 10
    BulletType = "OrdinaryBullet"
    up = False
    down = False
    money = 10
    TimeForPirat = 0

    def AddPirat(self):
        x = random.randint(5, 1450)
        y = random.randint(5, 750)
        Wherex = random.randint(-200, 200)
        Wherey = random.randint(-200, 200)
        Persons.append(Pirat(x, y, Wherex, Wherey))

    def Work(self):
        pass


class Pirat(Person):
    def __init__(self, x, y, WhereGoX, WhereGoY):
        self.x = x
        self.y = y
        self.WhereGoX = WhereGoX
        self.WhereGoY = WhereGoY

    # x = random.randint(5, 1450)
    # y = random.randint(5, 750)
    width = 140
    height = 119
    speed = 4
    left = False
    right = False
    AnimCount = 0
    WalkRight = PiratRight
    WalkLeft = PiratLeft
    PlayerStand = PiratStand
    health = 10
    Colors = [(255, 0, 0), (0, 0, 255)]
    TimeToShoot = 0

    # WhereGoX = random.randint(-200, 200)
    # WhereGoY = random.randint(-200, 200)

    def Work(self):
        global Persons
        self.TimeToShoot += 1  # Обрабатываем выстрел пирата
        if (self.TimeToShoot >= 130):
            self.TimeToShoot = 0
            x1 = round(self.x + self.width // 2)
            y1 = round(self.y + self.height // 2 + 10)
            tox = Persons[0].x + (Persons[0].width) // 2
            toy = Persons[0].y + (Persons[0].height) // 2
            if (Persons[0].left):
                tox -= random.randint(120, 160)
            elif (Persons[0].right):
                tox += random.randint(120, 160)

            if (Persons[0].up):
                toy -= random.randint(120, 160)
            elif (Persons[0].down):
                toy += random.randint(120, 160)
            k = (math.sqrt((toy - y1) ** 2 + (tox - x1) ** 2) / 4) / 2.5
            if (not k == 0):
                BiasX = round((tox - x1) / k)
                BiasY = round((toy - y1) / k)
            else:
                BiasX = (tox - x1)
                BiasY = (toy - y1)
            bullets.append(OrdinaryBullet(x1, y1, BiasX, BiasY))
            bullets[len(bullets) - 1].color = (255, 0, 0)
        # Движение врагов
        x1 = self.x
        y1 = self.y
        tox = Persons[0].x + self.WhereGoX
        toy = Persons[0].y + self.WhereGoY
        self.right = bool((tox - x1) > 0)
        self.left = bool((tox - x1) < 0)
        if (math.fabs(tox - x1) < self.speed):
            self.x = tox
        else:
            if (tox - x1 > 0):
                self.x += self.speed
            else:
                self.x -= self.speed

        if (math.fabs(toy - y1) < self.speed):
            self.y = toy
        else:
            if (toy - y1 > 0):
                self.y += self.speed
            else:
                self.y -= self.speed


def DrawWindow():
    win.fill((0, 0, 0))
    win.blit(BackGrounds[sezon][BGIndex], (0, 0))
    for charaster in Persons:
        charaster.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for weapon in weapons:
        weapon.draw(win, weapons.index(weapon))
    # Рисуем интерфейс
    x = 4
    y = 4
    for i in range(Persons[0].health):
        pygame.draw.circle(win, (255, 0, 0), (x + i * 6, y), 5)
    f1 = pygame.font.Font(None, 36)
    text1 = f1.render(Persons[0].BulletType, 1, (180, 0, 0))
    mon = f1.render(str(Persons[0].money), 1, (255, 215, 0))
    win.blit(text1, (4, 4))
    win.blit(mon, (4, 25))
    pygame.display.update()


def DrawMenu():
    win.fill((255, 255, 255))
    f1 = pygame.font.Font(None, 42)
    text1 = f1.render("Start", 1, (0, 0, 255))
    win.blit(text1, (740, 360))
    pygame.display.update()


menu = True
while menu:
    clock.tick(120)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            menu = False
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (event.pos[0] > 700 and event.pos[0] < 800 and event.pos[1] > 300 and event.pos[1] < 500):
                menu = False
    DrawMenu()

Persons = [Tramp()]

bullets = []
weapons = []
run = True
while run:

    clock.tick(120)
    if (len(Persons) < 4):
        for i in range(4):
            Persons[0].AddPirat()
    for event in pygame.event.get():  # обрабатываем единичные нажатия
        if (event.type == pygame.QUIT):
            run = False
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (Persons[0].BulletType == "OrdinaryBullet"):
                x1 = round(Persons[0].x + Persons[0].width // 2)
                y1 = round(Persons[0].y + Persons[0].height // 2 + 10)
                tox = event.pos[0]
                toy = event.pos[1]
                k = (math.sqrt((toy - Persons[0].y) ** 2 + (tox - Persons[0].x) ** 2) / 4) / 2.5
                BiasX = (tox - x1)
                BiasY = (toy - y1)
                if (not k == 0):
                    BiasX = round((tox - x1) / k)
                    BiasY = round((toy - y1) / k)
                else:
                    BiasX = (tox - x1)
                    BiasY = (toy - y1)
                bullets.append(OrdinaryBullet(x1, y1, BiasX, BiasY))

            if (Persons[0].BulletType == "TeleportBullet" and Persons[0].money >= TeleportBullet.cost):
                Persons[0].money -= TeleportBullet.cost
                q = 0
                for bullet in bullets:
                    if (bullet.type == "TeleportBullet"):
                        q = 1
                        Persons[0].x = bullet.x
                        Persons[0].y = bullet.y
                        if (Persons[0].x > 1499):
                            sezon += 1
                            sezon %= 4
                            BGIndex %= len(BackGrounds[sezon])
                            for i in range(1, len(Persons)):
                                Persons[i].x -= 1500
                            for bul in bullets:
                                bul.x -= 1500
                            for weap in weapons:
                                weap.x -= 1500
                        if (Persons[0].x < 0):
                            sezon -= 1
                            sezon %= 4
                            BGIndex %= len(BackGrounds[sezon])
                            for i in range(1, len(Persons)):
                                Persons[i].x += 1500
                            for bul in bullets:
                                bul.x += 1500
                            for weap in weapons:
                                weap.x += 1500
                        if (Persons[0].y < 0):
                            BGIndex += 1
                            BGIndex %= len(BackGrounds[sezon])
                            for i in range(1, len(Persons)):
                                Persons[i].y += 800
                            for bul in bullets:
                                bul.y += 800
                            for weap in weapons:
                                weap.y += 800
                        if (Persons[0].y > 799):
                            BGIndex -= 1
                            BGIndex %= len(BackGrounds[sezon])
                            for i in range(1, len(Persons)):
                                Persons[i].y -= 800
                            for bul in bullets:
                                bul.y -= 800
                            for weap in weapons:
                                weap.y -= 800
                        Persons[0].y %= 800
                        Persons[0].x %= 1500
                        bullets.pop(bullets.index(bullet))
                if (q == 0):
                    x1 = round(Persons[0].x + Persons[0].width // 2)
                    y1 = round(Persons[0].y + Persons[0].height // 2) + 10
                    tox = event.pos[0]
                    toy = event.pos[1]
                    k = (math.sqrt((toy - Persons[0].y) ** 2 + (tox - Persons[0].x) ** 2) / 4) / 3.3
                    if (not k == 0):
                        BiasX = round((tox - x1) / k)
                        BiasY = round((toy - y1) / k)
                    else:
                        BiasX = (tox - x1)
                        BiasY = (toy - y1)
                    bullets.append(TeleportBullet(x1, y1, BiasX, BiasY))
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_1):
                Persons[0].BulletType = "OrdinaryBullet"
            if (event.key == pygame.K_2):
                Persons[0].BulletType = "TeleportBullet"
            if (event.key == pygame.K_b and Persons[0].money >= Bomb.cost):
                Persons[0].money -= Bomb.cost
                x = Persons[0].x + Persons[0].width // 2
                y = Persons[0].y + Persons[0].height // 2
                weapons.append(Bomb(x, y))
            if (event.key == pygame.K_h and Persons[0].money > 0 and Persons[0].health < 10):
                Persons[0].health += 1
                Persons[0].money -= 1
            if (event.key == pygame.K_p):
                Persons[0].AddPirat()
            if (event.key == pygame.K_TAB):
                BuletIndex += 1
                BuletIndex = BuletIndex % len(KindsOfBullet)
                Persons[0].BulletType = KindsOfBullet[BuletIndex]
    if (Persons[0].TimeForPirat >= 500):
        Persons[0].AddPirat()
        Persons[0].TimeForPirat = 0
    else:
        Persons[0].TimeForPirat += 1

    for bullet in bullets:
        for charaster in Persons:
            if (not charaster.Colors.__contains__(bullet.color)
                    and (dist(round(charaster.x + charaster.width // 2),
                              round(charaster.y + charaster.height // 2) + 10, bullet.x,
                              bullet.y) < charaster.height / 2)):
                charaster.health -= bullet.damage
                bullets.pop(bullets.index(bullet))
                if (charaster.health <= 0):
                    if (type(charaster) == Tramp):
                        run = False
                    Persons[0].money += 9
                    Persons.pop(Persons.index(charaster))

                break
    for weapon in weapons:
        flag = False
        for i in range(1, len(Persons)):
            if (not weapon.IsBoom):
                if ((dist(round(Persons[i].x + Persons[i].width // 2),
                          round(Persons[i].y + Persons[i].height // 2) + 10, weapon.x,
                          weapon.y) < 150)):
                    Persons[i].health -= weapon.damage
                    flag = True
        if (flag):
            weapon.IsBoom = True
    for charaster in Persons:
        if (charaster.health <= 0):
            Persons.pop(Persons.index(charaster))
            Persons[0].money += 9

    if (not run):
        break
    for bullet in bullets:
        bullet.Work()
    keys = pygame.key.get_pressed()

    if (keys[pygame.K_a]):
        Persons[0].x -= Persons[0].speed
        if (Persons[0].x < 0):
            sezon -= 1
            sezon %= 4
            BGIndex %= len(BackGrounds[sezon])
            for i in range(1, len(Persons)):
                Persons[i].x += 1500
            for bullet in bullets:
                bullet.x += 1500
            for weap in weapons:
                weap.x += 1500

        Persons[0].x %= 1500
        Persons[0].left = True
        Persons[0].right = False

    elif (keys[pygame.K_d]):
        Persons[0].x += Persons[0].speed
        if (Persons[0].x > 1499):
            sezon += 1
            sezon %= 4
            BGIndex %= len(BackGrounds[sezon])
            for i in range(1, len(Persons)):
                Persons[i].x -= 1500
            for bullet in bullets:
                bullet.x -= 1500
            for weap in weapons:
                weap.x -= 1500
        Persons[0].x %= 1500
        Persons[0].right = True
        Persons[0].left = False
    else:
        Persons[0].left = False
        Persons[0].right = False
        Persons[0].AnimCount = 0

    if not (Persons[0].IsJump):
        if (keys[pygame.K_w]):
            Persons[0].y -= Persons[0].speed
            Persons[0].up = True
            Persons[0].down = False
            if (Persons[0].y < 0):
                BGIndex += 1
                BGIndex %= len(BackGrounds[sezon])
                for i in range(1, len(Persons)):
                    Persons[i].y += 800
                for bullet in bullets:
                    bullet.y += 800
                for weap in weapons:
                    weap.y += 800
            Persons[0].y %= 800
        elif (keys[pygame.K_s]):
            Persons[0].y += Persons[0].speed
            Persons[0].up = False
            Persons[0].down = True
            if (Persons[0].y > 799):
                BGIndex -= 1
                BGIndex %= len(BackGrounds[sezon])
                for i in range(1, len(Persons)):
                    Persons[i].y -= 800
                for bullet in bullets:
                    bullet.y -= 800
                for weap in weapons:
                    weap.y -= 800
            Persons[0].y %= 800
        else:
            Persons[0].up = False
            Persons[0].down = False
        if (keys[pygame.K_SPACE]):
            Persons[0].IsJump = True
    else:
        if Persons[0].JumpCount >= -10:
            if (Persons[0].JumpCount >= 0):
                Persons[0].y -= int((Persons[0].JumpCount ** 2) / 5)
            else:
                Persons[0].y += int((Persons[0].JumpCount ** 2) / 5)

            Persons[0].JumpCount -= 1
        else:
            Persons[0].IsJump = False
            Persons[0].JumpCount = 10
    for i in range(1, len(Persons)):
        Persons[i].Work()
    DrawWindow()
pygame.quit()
