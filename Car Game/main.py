import pygame
import random

pygame.init()

def rot_center(image, angle):
    loc = image.get_rect().center  # rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite


screen_x = 400
screen_y = 720

window = pygame.display.set_mode((screen_x, screen_y))

car_1 = pygame.image.load('car.png')
car_1_L = pygame.image.load('car_L.png')
car_1_R = pygame.image.load('car_R.png')
car_2 = pygame.image.load('car_2.png')
car_3 = pygame.image.load('car_3.png')

enemy_1 = rot_center(pygame.image.load('enemy_1.png'), 180)
enemy_2 = rot_center(pygame.image.load('enemy_2.png'), 180)
enemy_3 = rot_center(pygame.image.load('enemy_3.png'), 180)
enemy_4 = rot_center(pygame.image.load('enemy_4.png'), 180)

bgOne = pygame.image.load('road.png')
bgTwo = pygame.image.load('road.png')
bgOne_y = 0
bgTwo_y = bgOne.get_height()

loop_1 = True
loop_2 = True
loop_3 = True
loop_4 = True

time = 1000
timer_id1 = pygame.USEREVENT
pipe_timer = pygame.time.set_timer(timer_id1, time)

score = 0
score_font = pygame.font.Font('ImminentLine.ttf', 50)
high_font = pygame.font.Font('ImminentLine.ttf', 20)
bullet_font = pygame.font.Font('ImminentLine.ttf', 20)
resume_font = pygame.font.Font('ImminentLine.ttf', 15)
title_font = pygame.font.Font('ImminentLine.ttf', 80)

enemy_speed = 2
background_speed = 1

explode = [pygame.image.load('explode/ex_1.png'), pygame.image.load('explode/ex_2.png'),
           pygame.image.load('explode/ex_3.png'), pygame.image.load('explode/ex_4.png'),
           pygame.image.load('explode/ex_5.png'), pygame.image.load('explode/ex_6.png'),
           pygame.image.load('explode/ex_7.png'), pygame.image.load('explode/ex_8.png')]

blue_laser = pygame.image.load('lasers/laser_B.png')

high_score = 0

bullet = pygame.image.load('bullet.png')

bullet_id = pygame.USEREVENT + 1
bullet_timer = pygame.time.set_timer(bullet_id, 7000)


class player:
    def __init__(self, x, y, width, height):
        self.explode = False
        self.ex_count = 0
        self.x = x
        self.y = y
        self.middle = True
        self.left = False
        self.width = width
        self.height = height
        self.hit_box = (self.x, self.y, self.width, self.height)
        self.bullet_count = 5

    def draw(self):
        if not self.middle:
            if self.left:
                window.blit(car_1_L, (self.x, self.y))
            elif not self.left:
                window.blit(car_1_R, (self.x, self.y))
        elif self.middle:
            window.blit(car_1, (self.x, self.y))
        # pygame.draw.rect(window, (255, 255, 255), self.hit_box, 1)


class enemies:
    def __init__(self):
        self.ex_count = 0
        self.explode = False
        self.width = 80
        self.height = 140
        self.x = random.randint(1, 3)
        self.y = -200
        if self.x == 1:
            self.x = 70
        elif self.x == 2:
            self.x = 166
        elif self.x == 3:
            self.x = 255
        char = random.randint(1, 3)
        if char == 1:
            self.character = enemy_1
        if char == 2:
            self.character = enemy_2
        if char == 3:
            self.character = enemy_3
        if char == 4:
            self.character = enemy_4
        self.hit_box = (self.x+10, self.y+5, self.width-20, self.height-10)

    def draw(self):
        window.blit(self.character, (self.x, self.y))
        # pygame.draw.rect(window, (255, 255, 255), self.hit_box, 1)

    def check_collision(self, character):
        if self.hit_box[0] <= character.hit_box[0] <= self.hit_box[0]+self.hit_box[2] \
                or self.hit_box[0] + self.hit_box[2] >= character.hit_box[0] + character.hit_box[2] >= self.hit_box[0]:

            if self.hit_box[1] <= character.hit_box[1] <= self.hit_box[1]+self.hit_box[3] \
                    or self.hit_box[1] + self.hit_box[3] >= character.hit_box[1] + character.hit_box[3] >= self.hit_box[1]:
                global loop_1
                global loop_2
                global loop_3
                global loop_4
                loop_1 = False
                loop_3 = True
                loop_4 = True
                self.explode = True
                character.explode = True

class projectile:
    def __init__(self, x, y, character_width):
        self.x = x
        self.y = y
        self.character_width = character_width

    def check_collision(self, character):
        if self.x >= character.hit_box[0] and self.x <= character.hit_box[0] + character.hit_box[2]:
            if self.y >= character.hit_box[1] and self.y <= character.hit_box[1] + character.hit_box[3]:
                character.explode = True

    def draw(self):
        window.blit(blue_laser, (self.x, self.y))


while loop_2:
    p1 = player(screen_x / 2 - car_1.get_width() / 2 + 6, screen_y - 150, 80, 140)
    enemy_list = []
    laser_list = []
    while loop_3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_1 = False
                loop_2 = False
                loop_3 = False
                loop_4 = False
        keys = pygame.key.get_pressed()
        key_quit = keys[pygame.K_q]
        key_play = keys[pygame.K_w]
        if key_quit:
            loop_1 = False
            loop_2 = False
            loop_3 = False
            loop_4 = False
        if key_play:
            loop_3 = False
        window.blit(bgOne, (0, 0))
        title = title_font.render("CARS", True, (255, 255, 255))
        window.blit(title, (int(screen_x/2) - int(title.get_width()/2) + 10, 100))
        press_play = resume_font.render("Press W to play", True, (255, 255, 255))
        press_quit = resume_font.render("Press Q to Quit", True, (255, 255, 255))
        window.blit(press_play, (int(screen_x/2) - 80, 210))
        window.blit(press_quit, (int(screen_x / 2) - 75, 240))
        window.blit(car_1, (int(screen_x / 2) - int(car_1.get_width() / 2) + 6, screen_y - 400))
        window.blit(car_2, (int(screen_x / 2) - int(car_1.get_width() / 2) + 96, screen_y - 250))
        window.blit(car_3, (int(screen_x / 2) - int(car_1.get_width() / 2) - 86, screen_y - 100))
        pygame.display.update()
    while loop_1:
        if score > 30:
            time = 800
        if score > 60:
            time = 700
            background_speed = 1.5
        if score > 90:
            enemy_speed = 3
            background_speed = 2

        p1.hit_box = (p1.x+20, p1.y+25, p1.width-40, p1.height-40)
        keys = pygame.key.get_pressed()
        key_space = keys[pygame.K_SPACE]
        key_right = keys[pygame.K_d]
        key_left = keys[pygame.K_a]
        key_up = keys[pygame.K_w]
        key_down = keys[pygame.K_s]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_1 = False
                loop_2 = False
                loop_3 = False
                loop_4 = False
            if event.type == timer_id1:
                enemy_list.append(enemies())
                pipe_timer = pygame.time.set_timer(timer_id1, time)
            if event.type == pygame.KEYUP:
                if key_space and p1.bullet_count > 0:
                    laser_list.append(projectile(p1.x + 40, p1.y + 60, 80))
                    p1.bullet_count -= 1
            if event.type == bullet_id:
                p1.bullet_count += 1
        if key_left and p1.x > 70 and p1.y > 0:
            p1.x -= 1.5
            p1.middle = False
            p1.left = True
        else:
            p1.middle = True
        if key_right and (p1.x + car_1.get_width()) < 360 and p1.y > 0:
            p1.x += 1.5
            p1.middle = False
            p1.left = False
        # else:
        #     p1.middle = True
        if key_up and p1.y > 0:
            p1.y -= 1
            p1.middle = True
        if key_down and (p1.y + car_1.get_height()) < screen_y:
            p1.y += 2
            p1.middle = True

        window.blit(bgOne, (0, bgOne_y))
        window.blit(bgTwo, (0, bgTwo_y))
        window.blit(bullet, (5, 650))
        bullet_text = bullet_font.render(str(p1.bullet_count), True, (255, 255, 255))
        window.blit(bullet_text, (30, 660))
        score_text = score_font.render(str(score), True, (255, 255, 255))
        window.blit(score_text, (screen_x / 2 - score_text.get_width() / 2, 0))
        bgOne_y += background_speed
        bgTwo_y += background_speed
        if bgOne_y + 4 > (bgOne.get_height()):
            bgOne_y = bgTwo_y - bgTwo.get_height()
        if bgTwo_y + 4 > (bgTwo.get_height()):
            bgTwo_y = bgOne_y - bgOne.get_height()

        for enemy in enemy_list:
            if round(enemy.ex_count) < 2:
                enemy.hit_box = (enemy.x + 10 + 1, enemy.y + 20, enemy.width - 20, enemy.height - 40)
                enemy.draw()
                enemy.y += enemy_speed
                enemy.check_collision(p1)
            if enemy.explode:
                if enemy.ex_count < 7:
                    window.blit(explode[round(enemy.ex_count)], (enemy.x, enemy.y))
                    enemy.ex_count += 0.05
                    # print(enemy.ex_count)
        for enemy in enemy_list:
            if enemy.y > 800:
                enemy_list.remove(enemy)
                score += 1
            if enemy.ex_count > 6.9:
                enemy_list.remove(enemy)
                score += 1
        for laser in laser_list:
            laser.draw()
            laser.y -= 4
            for enemy in enemy_list:
                laser.check_collision(enemy)
        for laser in laser_list:
            if laser.y < -100:
                laser_list.remove(laser)

        p1.draw()
        pygame.display.update()


    while loop_4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_1 = False
                loop_2 = False
                loop_3 = False
                loop_4 = False
            if event.type == pygame.KEYDOWN:
                loop_1 = True
                loop_2 = True
                loop_3 = True
                loop_4 = False

        window.blit(bgOne, (0, bgOne_y))
        window.blit(bgTwo, (0, bgTwo_y))

        for enemy in enemy_list:
            if round(enemy.ex_count) < 2:
                enemy.draw()
            if enemy.explode:
                if enemy.ex_count < 7:
                    window.blit(explode[round(enemy.ex_count)], (enemy.x, enemy.y))
                    enemy.ex_count += 0.05
                    # print(enemy.ex_count)

        if round(p1.ex_count) < 2:
            p1.draw()
        if p1.explode:
            if p1.ex_count < 7:
                window.blit(explode[round(p1.ex_count)], (p1.x, p1.y))
                p1.ex_count += 0.05
                # print(p1.ex_count)
        score_text = score_font.render("YOU DIED", True, (255, 255, 255))
        window.blit(score_text, (screen_x / 2 - score_text.get_width() / 2, screen_y / 2 - score_text.get_height()))
        if high_score < score:
            high_score = score
        high = high_font.render(f'High Score: {high_score}', True, (255, 255, 255))
        window.blit(high, (screen_x / 2 - high.get_width() / 2, screen_y / 2 - high.get_height() - 90))

        resume = resume_font.render("Press Any Key to Continue", True, (255, 255, 255))
        window.blit(resume, (screen_x / 2 - resume.get_width() / 2, screen_y / 2 - resume.get_height() + 50))
        pygame.display.update()

pygame.quit()
