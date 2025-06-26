import pygame
import sys
import math
import random
import json
import os
from pygame.locals import *
from assets import load_assets

WIDTH, HEIGHT = 800, 600
FPS = 60
LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, 'r') as f:
        return json.load(f)

def save_to_leaderboard(name, score):
    leaderboard = load_leaderboard()
    updated = False
    for entry in leaderboard:
        if entry["name"] == name:
            if score > entry["score"]:
                entry["score"] = score
            updated = True
            break
    if not updated:
        leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f)

def draw_text_centered(screen, text, font, y, color=(255,255,255)):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    screen.blit(rendered, rect)

def main_menu(screen, font):
    selected = 0
    options = ["Play", "Leaderboard", "Exit"]
    while True:
        screen.fill((10, 10, 30))
        draw_text_centered(screen, "=== MENIU PRINCIPAL ===", font, 100)

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            draw_text_centered(screen, option, font, 200 + i * 50, color)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == K_RETURN:
                    return options[selected]

def game_over_menu(screen, font):
    selected = 0
    options = ["Play again!", "Leaderboard", "Main Menu"]
    while True:
        screen.fill((0, 0, 0))
        draw_text_centered(screen, "=== SFÂRȘIT JOC ===", font, 100)
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            draw_text_centered(screen, option, font, 200 + i * 50, color)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == K_RETURN:
                    return options[selected]

def show_leaderboard(screen, font):
    leaderboard = load_leaderboard()
    screen.fill((20, 20, 20))
    draw_text_centered(screen, "=== CLASAMENT ===", font, 60)
    if not leaderboard:
        draw_text_centered(screen, "Fără scoruri salvate!", font, HEIGHT//2)
    else:
        for i, entry in enumerate(leaderboard):
            text = f"{i+1}. {entry['name']} - {entry['score']}"
            draw_text_centered(screen, text, font, 120 + i * 40)
    draw_text_centered(screen, "Apasă Enter pentru a reveni", font, HEIGHT - 40)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN and event.key == K_RETURN:
                return

def get_player_name(screen, font):
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN and name.strip():
                    return name
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and event.unicode.isprintable():
                    name += event.unicode

        screen.fill((30, 30, 30))
        prompt = font.render("Nume jucător:", True, (255, 255, 255))
        txt = font.render(name, True, (255, 255, 255))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 70))
        input_box.w = max(200, txt.get_width() + 10)
        screen.blit(txt, (input_box.x + 5, input_box.y + 10))
        pygame.draw.rect(screen, pygame.Color('dodgerblue2'), input_box, 2)
        pygame.display.flip()

def countdown(screen, font):
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        draw_text_centered(screen, f"Începe în {i}...", font, HEIGHT//2)
        pygame.display.flip()
        pygame.time.delay(1000)

def run_game(screen, font, assets, player_name):
    import math
    clock = pygame.time.Clock()
    shoot_sound = assets['shoot']
    miss_sound = assets['miss']
    background_img = pygame.transform.scale(assets['player'], (WIDTH, int(HEIGHT * 0.8)))
    heart_img = pygame.transform.scale(assets['heart'], (30, 30))
    compass_img = pygame.transform.scale(assets['compass'], (30, 30))
    crosshair_img = pygame.transform.scale(assets['crosshair'], (40, 40))
    pygame.mouse.set_visible(False)

    panel_main = pygame.Rect(0, 0, WIDTH, int(HEIGHT * 0.8))
    panel_bottom = pygame.Rect(0, int(HEIGHT * 0.8), WIDTH, int(HEIGHT * 0.2))

    enemies = []
    hearts = []
    spawn_timer = 0
    score = 0
    level = 1
    lives = 4
    level_time = 60
    start_ticks = pygame.time.get_ticks()
    time_bonus = 0
    score_flash_timer = 0

    MAX_TARGETS_ON_SCREEN = 5
    HEART_DROP_CHANCE = 0.1

    while True:
        dt = clock.tick(FPS)
        screen.fill((0, 0, 0))
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, level_time + time_bonus - seconds_passed)

        if time_left <= 0 or lives <= 0:
            save_to_leaderboard(player_name, score)
            return

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                hit = False
                for enemy in enemies[:]:
                    if enemy['rect'].collidepoint(event.pos):
                        shoot_sound.play()
                        score += enemy['base_value'] * level
                        time_bonus += 3
                        enemies.remove(enemy)
                        hit = True
                        score_flash_timer = 10
                        break
                if not hit:
                    for heart in hearts[:]:
                        if heart['rect'].collidepoint(event.pos):
                            shoot_sound.play()
                            lives = min(lives + 1, 5)
                            hearts.remove(heart)
                            hit = True
                            break
                if not hit:
                    miss_sound.play()
                    lives -= 1

        if score >= level * 100:
            level += 1

        ENEMY_SPEED = 1 + 0.1 * level
        SPAWN_TIME_CURRENT = max(15, 30 - level * 2)

        spawn_timer += 1
        if spawn_timer >= SPAWN_TIME_CURRENT and len(enemies) < MAX_TARGETS_ON_SCREEN:
            spawn_timer = 0

            is_rare = random.random() < 0.15
            size = 60 if is_rare else 50
            img = assets['target_5'] if is_rare else assets['target_1']
            image = pygame.transform.smoothscale(img, (size, size))
            x = random.randint(0, panel_main.width - size)
            rect = pygame.Rect(x, -size, size, size)
            enemies.append({'rect': rect, 'image': image, 'base_value': 5 if is_rare else 1})

            if lives == 1 and random.random() < HEART_DROP_CHANCE:
                heart_image = pygame.transform.smoothscale(assets['heart'], (40, 40))
                hx = random.randint(0, panel_main.width - 40)
                hearts.append({'rect': pygame.Rect(hx, -40, 40, 40), 'image': heart_image})

        for enemy in enemies[:]:
            enemy['rect'].y += ENEMY_SPEED
            if enemy['rect'].top > panel_main.height:
                enemies.remove(enemy)
                lives -= 1

        for heart in hearts[:]:
            heart['rect'].y += ENEMY_SPEED
            if heart['rect'].top > panel_main.height:
                hearts.remove(heart)

        screen.blit(background_img, panel_main.topleft)
        for enemy in enemies:
            screen.blit(enemy['image'], enemy['rect'])
        for heart in hearts:
            screen.blit(heart['image'], heart['rect'])


        pygame.draw.rect(screen, (50, 50, 50), panel_bottom)
        screen.blit(font.render(f"Nume: {player_name}", True, (255, 255, 255)), (20, panel_bottom.y + 5))


        score_color = (255, 255, 255)
        if score_flash_timer > 0:
            score_color = (255, 255, 0)
            score_flash_timer -= 1
        score_text = font.render(f"Puncte: {score}", True, score_color)
        screen.blit(score_text, (20, panel_bottom.y + 35))

        screen.blit(font.render(f"Nivel: {level}", True, (255, 255, 255)), (250, panel_bottom.y + 5))

        
        if lives == 1:
            pulse_scale = 1.2 + 0.2 * abs(math.sin(pygame.time.get_ticks() / 300))
            pulsing_heart = pygame.transform.smoothscale(assets['heart'], (int(30 * pulse_scale), int(30 * pulse_scale)))
            heart_rect = pulsing_heart.get_rect()
            heart_rect.topleft = (250, panel_bottom.y + 35 - (heart_rect.height - 30) // 2)
            screen.blit(pulsing_heart, heart_rect)
        else:
            screen.blit(heart_img, (250, panel_bottom.y + 35))

        screen.blit(font.render(f"x {lives}", True, (255, 255, 255)), (285, panel_bottom.y + 38))
        screen.blit(compass_img, (450, panel_bottom.y + 30))
        screen.blit(font.render(f"{time_left}s", True, (255, 255, 255)), (485, panel_bottom.y + 33))

        mx, my = pygame.mouse.get_pos()
        screen.blit(crosshair_img, crosshair_img.get_rect(center=(mx, my)))

        pygame.display.flip()



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rapid Fire")
    font = pygame.font.SysFont(None, 36)
    assets = load_assets()

    while True:
        choice = main_menu(screen, font)
        if choice == "Exit":
            break
        elif choice == "Leaderboard":
            show_leaderboard(screen, font)
        elif choice == "Play":
            player_name = get_player_name(screen, font)
            countdown(screen, font)
            run_game(screen, font, assets, player_name)
            while True:
                post_game_choice = game_over_menu(screen, font)
                if post_game_choice == "Play again!":
                    countdown(screen, font)
                    run_game(screen, font, assets, player_name)
                elif post_game_choice == "Leaderboard":
                    show_leaderboard(screen, font)
                else:
                    break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
