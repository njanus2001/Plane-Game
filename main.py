import pygame
import os
from plane import Plane
from coin import Coin
from random import randrange

# Set window configuration constants
WIDTH, HEIGHT = 1200, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Game")

# Set image assets as constants
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sky.png")), (WIDTH, HEIGHT))
COIN = pygame.transform.scale(pygame.image.load(os.path.join("assets", "coin.png")), (50, 50))
PLANE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "plane.png")), (150, 150))


def main():
    """Main function"""
    run = True
    fps = 60
    main_font = pygame.font.SysFont("impact", 50)
    points = 0
    player_velocity = 15

    level = 0
    wave_length = 0

    coins = []
    coin_velocity = 3

    plane = Plane((WIDTH / 2) - (PLANE.get_width() / 2), (HEIGHT - PLANE.get_height()), PLANE)

    clock = pygame.time.Clock()

    def redraw_window():
        WINDOW.blit(BG, (0, 0))

        level_label = main_font.render(f'Level: {level}', True, (0, 0, 0))
        points_label = main_font.render(f'Points: {points}', True, (0, 0, 0))

        plane.draw(WINDOW)
        for coin in coins:
            coin.draw(WINDOW)

        WINDOW.blit(level_label, (10, 10))
        WINDOW.blit(points_label, (WIDTH - points_label.get_width() - 10, 10))

        pygame.display.update()

    while run:
        clock.tick(fps)

        if len(coins) == 0:
            level += 1
            wave_length = wave_length + 5
            for i in range(wave_length):
                coin = Coin(randrange(100, WIDTH - 100), randrange(-2000, -100), COIN)
                coins.append(coin)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # Up
        if keys[pygame.K_UP] and plane.y - player_velocity > 0:
            plane.y -= player_velocity
        # Right
        elif keys[pygame.K_RIGHT] and plane.x + player_velocity + plane.get_width() < WIDTH:
            plane.x += player_velocity
        # Down
        elif keys[pygame.K_DOWN] and plane.y + player_velocity + plane.get_height() < HEIGHT:
            plane.y += player_velocity
        # Left
        elif keys[pygame.K_LEFT] and plane.x - player_velocity > 0:
            plane.x -= player_velocity

        for coin in coins:
            coin.move(coin_velocity)
            if collision(coin, plane):
                coins.remove(coin)
                points += 1
            elif coin.is_off_screen(HEIGHT):
                coins.remove(coin)

        redraw_window()


def collision(obj1, obj2):
    """Detects collisions between the player and coins."""
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main_menu():
    menu_font = pygame.font.SysFont("impact", 50)
    run = True
    while run:
        WINDOW.blit(BG, (0, 0))

        menu_label = menu_font.render("CLICK YOUR MOUSE TO PLAY!", True, (0, 0, 0))
        WINDOW.blit(menu_label, ((WIDTH - menu_label.get_width()) / 2, (HEIGHT / 2 - menu_label.get_height() / 2)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    main_menu()
