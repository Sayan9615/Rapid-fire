import pygame
import os

ASSETS = {}

def load_assets():
    folder = os.path.dirname(__file__)
    ASSETS['player'] = pygame.image.load(os.path.join(folder, 'player.png')).convert_alpha()
    ASSETS['shoot'] = pygame.mixer.Sound(os.path.join(folder, 'shoot.wav'))
    ASSETS['miss'] = pygame.mixer.Sound(os.path.join(folder, 'miss.wav'))
    ASSETS['crosshair'] = pygame.image.load(os.path.join(folder, 'target.png')).convert_alpha()
    ASSETS['heart'] = pygame.image.load(os.path.join(folder, 'heart.png')).convert_alpha()
    ASSETS['compass'] = pygame.image.load(os.path.join(folder, 'time.png')).convert_alpha()
    ASSETS['target_1'] = pygame.image.load(os.path.join(folder, '1point.png')).convert_alpha()
    ASSETS['target_5'] = pygame.image.load(os.path.join(folder, '5points.png')).convert_alpha()
    return ASSETS
