import pygame
import random
import time
import json

from functions import draw_rounded_rect

pygame.init()

SCREEN_WIDTH = 460
SCREEN_HEIGHT = 725
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blum")

STAR_IMAGE = pygame.image.load("Images/star.png")
BOMB_IMAGE = pygame.image.load("Images/bomb.png")
ICE_IMAGE = pygame.image.load("Images/ice.png")
BACKGROUND_IMAGE = pygame.image.load("Images/background.png")

FONT = pygame.font.SysFont(None, 36)
SMALL_FONT = pygame.font.SysFont(None, 36)


def load_data():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            return data.get('total_blum', 0), data.get('tickets', 5), data.get('last_ticket_time', time.time())
    except FileNotFoundError:
        return 0, 5, time.time()


def save_data(total_blum, tickets, last_ticket_time):
    with open('data.json', 'w') as f:
        json.dump({'total_blum': total_blum, 'tickets': tickets, 'last_ticket_time': last_ticket_time}, f)


def add_tickets_if_needed(last_ticket_time, tickets):
    current_time = time.time()
    elapsed_time = current_time - last_ticket_time
    if elapsed_time >= 3600:
        new_tickets = int(elapsed_time // 3600) * 5
        tickets += new_tickets
        last_ticket_time += (elapsed_time // 3600) * 3600
    return tickets, last_ticket_time


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(20, 40)
        self.image = pygame.transform.scale(STAR_IMAGE, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(BOMB_IMAGE, (24, 32))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Ice(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(ICE_IMAGE, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Particle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(random.choice([(255, 255, 255), (200, 200, 200)]))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = random.randint(-20, SCREEN_HEIGHT)
        self.speed_x = random.uniform(-0.2, 0.2)
        self.speed_y = random.uniform(0.2, 0.5)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


def game_loop():
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    score = 0
    time_limit = 30

    freeze_time = 0
    is_frozen = False
    paused_time = 0

    running = True
    start_ticks = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in all_sprites if s.rect.collidepoint(pos)]
                for sprite in clicked_sprites:
                    if isinstance(sprite, Star):
                        score += 1
                        sprite.kill()
                    elif isinstance(sprite, Bomb):
                        score = max(0, score - 100)
                        sprite.kill()
                    elif isinstance(sprite, Ice):
                        is_frozen = True
                        freeze_time = pygame.time.get_ticks()
                        sprite.kill()

        if is_frozen:
            if pygame.time.get_ticks() - freeze_time > 3000:
                is_frozen = False
                paused_time += (pygame.time.get_ticks() - start_ticks) / 1000
                start_ticks = pygame.time.get_ticks()
        else:
            if random.random() < 0.05:
                star = Star()
                all_sprites.add(star)
            if random.random() < 0.005:
                bomb = Bomb()
                all_sprites.add(bomb)
            if random.random() < 0.005:
                ice = Ice()
                all_sprites.add(ice)

            all_sprites.update()

        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 + paused_time
        remaining_time = max(0, time_limit - elapsed_time)
        if remaining_time <= 0:
            running = False

        screen.blit(BACKGROUND_IMAGE, (0, 0))
        all_sprites.draw(screen)
        score_text = FONT.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        time_text = FONT.render(f'Time: {int(remaining_time)}', True, (255, 255, 255))
        screen.blit(time_text, (SCREEN_WIDTH - 110, 10))

        pygame.display.flip()
        clock.tick(60)

    return score
