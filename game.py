import pygame
import random
import sys
from config import*
from player import Player
from obstacle import Obstacle

pygame.font.init()
font = pygame.font.Font("assets/dogicabold.ttf", 15)

class HealthItem:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/health.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")
        
        self.heart_image = pygame.image.load("assets/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))

        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
        self.background_image = pygame.image.load("assets/background.png").convert()
        self.background_scroll = 0
        self.background_speed = 2
        self.collision_count = 0
        self.max_collisions = 3
        self.score = 0

        self.lives = 3
        self.max_lives = 3
        self.health_items= []


    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()

    def update(self):
        self.player.update()

        
        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0

        if random.randint(0, 100) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        if random.randint(0, 200) < 1:
            health_x = WIDTH
            health_y = HEIGHT - 70
            self.health_items.append(HealthItem(health_x, health_y))

        for health_item in self.health_items[:]:
            health_item.update()
            if self.player.get_rect().colliderect(health_item.rect):
                if self.lives < self.max_lives:
                    self.lives += 1
                    self.health_items.remove(health_item)
            elif health_item.rect.right < 0:
                self.health_items.remove(health_item)

        player_x = self.player.get_rect().x
        for obstacle in self.obstacles:
            if player_x > obstacle.rect.x + obstacle.rect.width and not hasattr(obstacle, 'passed'):
                self.score += 10 
                setattr(obstacle, 'passed', True)  
            obstacle.update()

        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.rect.x + obstacle.rect.width > 0
        ]

        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.collision_count += 1
                self.lives -=1
                self.obstacles.remove(obstacle)
                if self.lives <= 0:
                    self.draw_text(
                        "¡Perdiste!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2
                    )
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()

    def draw(self):
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )

        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for health_item in self.health_items:
            health_item.draw(self.screen)


        self.draw_text(
            f"Puntuación: {self.score}", font, WHITE, self.screen, 350, 30
        )

        for i in range(self.lives):
            self.screen.blit(self.heart_image, (20 + i * 30, 20))
            
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)
