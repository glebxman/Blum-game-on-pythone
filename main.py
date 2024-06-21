import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
screen_width = 460
screen_height = 725
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blum")

# Загрузка изображений
star_image = pygame.image.load("star.png")
bomb_image = pygame.image.load("bomb.png")
background_image = pygame.image.load("background.png")

# Классы объектов
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(20, 40)  # Разные размеры звездочек
        self.image = pygame.transform.scale(star_image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(bomb_image, (24, 32))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

def game_loop():
    # Группы спрайтов
    all_sprites = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    # Таймер и счетчик очков
    clock = pygame.time.Clock()
    score = 0
    time_limit = 30
    font = pygame.font.SysFont(None, 36)

    # Основной цикл игры
    running = True
    game_over = False
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
                        score = max(0, score - 100)  # Минимум 0 очков
                        sprite.kill()

        # Создание новых звездочек и бомбочек
        if random.random() < 0.05:
            star = Star()
            all_sprites.add(star)
            stars.add(star)
        if random.random() < 0.01:  # Уменьшено количество бомбочек
            bomb = Bomb()
            all_sprites.add(bomb)
            bombs.add(bomb)

        # Обновление спрайтов
        all_sprites.update()

        # Проверка времени
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > time_limit:
            game_over = True
            running = False

        # Рендеринг
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        time_text = font.render(f'Time: {int(time_limit - seconds)}', True, (255, 255, 255))
        screen.blit(time_text, (screen_width - 150, 10))

        pygame.display.flip()
        clock.tick(60)

    # Экран конца игры
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over = False
                    game_loop()  # Перезапуск игры

        screen.fill((0, 0, 0))
        game_over_text = font.render(f'Game Over! Score: {score}', True, (255, 255, 255))
        restart_text = font.render('Press Enter to Restart', True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2))

        pygame.display.flip()

game_loop()
