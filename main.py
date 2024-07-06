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
ice_image = pygame.image.load("ice.png")
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


class Ice(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(ice_image, (30, 30))
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
    ices = pygame.sprite.Group()

    # Таймер и счетчик очков
    clock = pygame.time.Clock()
    score = 0
    time_limit = 30
    font = pygame.font.SysFont(None, 36)

    # Переменные для заморозки
    freeze_time = 0
    is_frozen = False

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
                        score = max(0, score - 100)
                        sprite.kill()
                    elif isinstance(sprite, Ice):
                        is_frozen = True
                        freeze_time = pygame.time.get_ticks()
                        sprite.kill()

        # Обновление спрайтов только если не заморожено
        if is_frozen:
            if pygame.time.get_ticks() - freeze_time > 3000:  # 3 секунды заморозки
                is_frozen = False
        else:
            # Создание новых звездочек, бомбочек и лединок
            if random.random() < 0.05:
                star = Star()
                all_sprites.add(star)
                stars.add(star)
            if random.random() < 0.005:  # Уменьшено количество бомбочек
                bomb = Bomb()
                all_sprites.add(bomb)
                bombs.add(bomb)
            if random.random() < 0.005:
                ice = Ice()
                all_sprites.add(ice)
                ices.add(ice)

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
                    main_menu()  # Перезапуск игры

        screen.fill((0, 0, 0))
        game_over_text = font.render(f'Game Over! Score: {score}', True, (255, 255, 255))
        restart_text = font.render('Press Enter to Restart', True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2))

        pygame.display.flip()


def main_menu():
    font = pygame.font.SysFont(None, 72)
    play_text = font.render('Play', True, (255, 255, 255))

    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_text.get_rect(center=(screen_width // 2, screen_height // 2)).collidepoint(pos):
                    in_menu = False
                    game_loop()

        screen.fill((0, 0, 0))
        screen.blit(play_text, (screen_width // 2 - play_text.get_width() // 2, screen_height // 2 - play_text.get_height() // 2))

        pygame.display.flip()

main_menu()
