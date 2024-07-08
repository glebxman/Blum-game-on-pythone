import random
import time
import pygame

from functions import draw_rounded_rect
from main import load_data, add_tickets_if_needed, save_data, SMALL_FONT, SCREEN_WIDTH, SCREEN_HEIGHT, game_loop, \
    screen, STAR_IMAGE, Particle


def main_menu():
    total_blum, tickets, last_ticket_time = load_data()
    tickets, last_ticket_time = add_tickets_if_needed(last_ticket_time, tickets)
    save_data(total_blum, tickets, last_ticket_time)

    if tickets <= 0:
        return

    play_text = SMALL_FONT.render('Play', True, (0, 0, 0))
    start_mining_text = SMALL_FONT.render('Start Mining', True, (0, 0, 0))

    demo_rect = pygame.Rect(50, 400, 360, 200)
    play_button_rect_centered = play_text.get_rect(center=(demo_rect.centerx + 133, demo_rect.top + 170))
    start_mining_button_rect = start_mining_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))

    mining_started = False
    mining_end_time = None
    blum_earned = 0

    particles = pygame.sprite.Group()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_button_rect_centered.collidepoint(pos):
                    if tickets > 0:
                        tickets -= 1
                        total_blum += game_loop()
                        save_data(total_blum, tickets, last_ticket_time)
                elif start_mining_button_rect.collidepoint(pos):
                    if not mining_started:
                        mining_started = True
                        mining_end_time = time.time() + 10
                        blum_earned = 0
                        start_mining_text = SMALL_FONT.render('Mining...', True, (0, 0, 0))
                    elif blum_earned > 0:
                        total_blum += blum_earned
                        blum_earned = 0
                        start_mining_text = SMALL_FONT.render('Start Mining', True, (0, 0, 0))
                        save_data(total_blum, tickets, last_ticket_time)

        if mining_started:
            remaining_time = max(0, mining_end_time - time.time())
            if remaining_time <= 0:
                blum_earned = 58
                mining_started = False
                start_mining_text = SMALL_FONT.render(f'Claim ({blum_earned} Blum)', True, (255, 255, 255))
            else:
                mining_time_text = SMALL_FONT.render(f'{int(remaining_time)}s', True, (255, 255, 255))

        screen.fill((0, 0, 0))

        if len(particles) < 10:
            for _ in range(random.randint(10, 15)):
                particle = Particle()
                particles.add(particle)

        particles.update()
        particles.draw(screen)

        draw_rounded_rect(screen, (15, 15, 15), demo_rect, 20)
        screen.blit(STAR_IMAGE, (190, 460))

        play_button_rect_inflated = play_button_rect_centered.inflate(20, 10)
        draw_rounded_rect(screen, (255, 255, 255), play_button_rect_inflated, 16)
        screen.blit(play_text, play_button_rect_centered.topleft)

        start_mining_button_rect_inflated = start_mining_button_rect.inflate(250, 20)
        button_color = (0, 255, 0) if not mining_started and blum_earned > 0 else (
        150, 150, 150) if mining_started else (255, 255, 255)
        draw_rounded_rect(screen, button_color, start_mining_button_rect_inflated, 10)
        screen.blit(start_mining_text, start_mining_button_rect.topleft)

        total_blum_text = SMALL_FONT.render(f'B {total_blum}', True, (255, 255, 255))
        screen.blit(total_blum_text, (SCREEN_WIDTH // 2 - 18 - total_blum_text.get_height() // 2, 200))

        if mining_started:
            screen.blit(mining_time_text, (
            start_mining_button_rect.right + 10, start_mining_button_rect.centery - mining_time_text.get_height() // 2))

        tickets_text = SMALL_FONT.render(f'Tickets: {tickets}', True, (255, 255, 255))
        screen.blit(tickets_text, (60, SCREEN_HEIGHT - 160))

        pygame.display.flip()


main_menu()
