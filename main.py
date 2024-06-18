import pygame
import os
import random

pygame.init()

# Constants
LVL_LENGHT = 2000

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
#            pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
# JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
# DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
#            pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1nw.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2nw.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJumpnw.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1nw.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2nw.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

PTERODACTYLUS = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
                 pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

TUMBLEWEED = [pygame.image.load(os.path.join("Assets/Tumbleweed", "Tumbleweed1.png")),
              pygame.image.load(os.path.join("Assets/Tumbleweed", "Tumbleweed2.png")),
              pygame.image.load(os.path.join("Assets/Tumbleweed", "Tumbleweed3.png")),
              pygame.image.load(os.path.join("Assets/Tumbleweed", "Tumbleweed4.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

DESERT_SAND = pygame.image.load(os.path.join("Assets/Other", "Desert.png"))

FONT = pygame.font.Font(None, 36)


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dinoDuck = False
        self.dinoRun = True
        self.dinoJump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput,keyInput):
        global obstacles
        if self.dinoDuck:
            self.duck()
        if self.dinoRun:
            self.run()
        if self.dinoJump:
            self.jump(userInput)

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_w]) and not self.dinoJump:
            self.dinoDuck = False
            self.dinoRun = False
            self.dinoJump = True
        elif (userInput[pygame.K_DOWN] or userInput[pygame.K_s]) and not self.dinoJump:
            self.dinoDuck = True
            self.dinoRun = False
            self.dinoJump = False
        elif not (self.dinoJump or userInput[pygame.K_DOWN]):
            self.dinoDuck = False
            self.dinoRun = True
            self.dinoJump = False
        if keyInput[0]:
            pos = pygame.mouse.get_pos()
            for obstacle in obstacles:
                if isinstance(obstacle, Tumbleweed) and obstacle.is_clicked(pos):
                    obstacles.remove(obstacle)
                    break

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self, userInput):
        self.image = self.jump_img  # Set image to jump_img when jumping
        if self.dinoJump:
            if not userInput[pygame.K_UP] and not userInput[pygame.K_w]:
                if self.jump_vel > 0:
                    self.jump_vel = 0  # Stop upward movement
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.dino_rect.y >= self.Y_POS:
            self.dino_rect.y = self.Y_POS
            self.dinoJump = False  # Reset dinoJump when jump is complete
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(500, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= bg_game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle: # parent class for obstacles
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
    
    def update(self):
        self.rect.x -= fg_game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self,image):
        self.type = random.randint(0,len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = 325

        
class LargeCactus(Obstacle):
    def __init__(self,image):
        self.type = random.randint(0,len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = 300


class Pterodactylus(Obstacle):
    def __init__(self,image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 270
        self.index = 0
    def draw(self,SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class Tumbleweed(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, len(image) - 1)
        super().__init__(image, self.type)
        self.rect.y = random.randint(0,325)
        self.index = 0
        self.y_velocity = -8  # Initial vertical velocity
        self.gravity = 0.5  # Gravity effect

    def draw(self, SCREEN):
        if self.index >= 20:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

    def update(self):
        self.rect.x -= fg_game_speed

        # Bounce effect
        self.rect.y += self.y_velocity
        self.y_velocity += self.gravity

        # Check if the tumbleweed hits the ground and make it bounce
        if self.rect.y >= 320:
            self.rect.y = 320
            self.y_velocity = -abs(self.y_velocity) * 0.8  # Reduce velocity for bouncing effect

        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def main():
    global bg_game_speed, fg_game_speed, x_pos_bg, y_pos_bg, obstacles, points
    run = True  # game start
    clock = pygame.time.Clock()
    player = Dinosaur()
    clouds = [Cloud() for _ in range(3)]
    fg_game_speed = 14
    bg_game_speed = 3
    x_pos_bg = 0
    y_pos_bg = 380
    obstacles = []
    points = 0
    font = pygame.font.Font('freesansbold.ttf',20)
    death_count = 0
    
    def score():
        global points, fg_game_speed
        points += 1
        if points%LVL_LENGHT == 0:
            fg_game_speed += 1
        text = font.render("Points: " + str(points), True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (1000,40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = DESERT_SAND.get_width()
        SCREEN.blit(DESERT_SAND, (x_pos_bg, y_pos_bg))
        SCREEN.blit(DESERT_SAND, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(DESERT_SAND, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= fg_game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))

        # Update player/dinosaur passing keyboard and mouse input
        userInput = pygame.key.get_pressed()
        keyInput = pygame.mouse.get_pressed()
        player.draw(SCREEN)
        player.update(userInput,keyInput)

        if len(obstacles) == 0:
            obstacle_type = random.randint(0, 3)
            if obstacle_type == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif obstacle_type == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif obstacle_type == 2:
                obstacles.append(Pterodactylus(PTERODACTYLUS))
            elif obstacle_type == 3:
                obstacles.append(Tumbleweed(TUMBLEWEED))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                # pygame.draw.rect(SCREEN, (255, 0, 0), player.dino_rect, 2)
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        for cloud in clouds:  # Update and draw each cloud
            cloud.draw(SCREEN)
            cloud.update()

        score()
        
        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))

        text = FONT.render("Press any key to start", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        SCREEN.blit(text,textRect)

        if death_count == 0:
            play_text = FONT.render("To play the game:", True, (0, 0, 0))
            play_textRect = play_text.get_rect()
            play_textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
            SCREEN.blit(play_text, play_textRect)

            instructions1 = FONT.render("Use arrow up button or 'w' key to jump", True, (0, 0, 0))
            instructions1Rect = instructions1.get_rect()
            instructions1Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(instructions1, instructions1Rect)

            instructions2 = FONT.render("Use arrow down button or 's' key to duck", True, (0, 0, 0))
            instructions2Rect = instructions2.get_rect()
            instructions2Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)
            SCREEN.blit(instructions2, instructions2Rect)

            good_luck = FONT.render("Good luck", True, (0, 0, 0))
            good_luckRect = good_luck.get_rect()
            good_luckRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130)
            SCREEN.blit(good_luck, good_luckRect)

        if death_count > 0:
            score = FONT.render("Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
            SCREEN.blit(score,scoreRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()

if __name__ == "__main__":
    menu(death_count=0)