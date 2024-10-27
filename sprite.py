import pygame
import sys
import math
import random
from os import listdir
from os.path import isfile, join
from imageConverter import ImageConvert
import tkinter as tk
from tkinter import filedialog

pygame.init()

# Constants and settings
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BG_GREY = (50, 50, 50)
CIRCLE_POSITION = (400, 300)
CIRCLE_RADIUS = 45
MAX_HEARTS = 3

# Game window setup
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image to Top Down Game")

# Initialize user image
userImage = None  # Initially set to None, will be loaded later

# Load background images
bg_img = pygame.image.load('images/bw/bwBackground.jpg')
bgOver_img = pygame.image.load('images/green/treeReplace.png')

# Load heart image
heart_image = pygame.image.load('assets/hearts/heart.png')
heart_image = pygame.transform.scale(heart_image, (90, 90))

# Load candy images
candy_assets = ['assets/candy/candy1.png', 'assets/candy/candy2.png', 
                'assets/candy/candy3.png', 'assets/candy/candy4.png']

# Load player walking animations
walkRight = [pygame.image.load('assets/player/new/walk1.png'),
             pygame.image.load('assets/player/new/walk2.png'),
             pygame.image.load('assets/player/new/walk3.png'),
             pygame.image.load('assets/player/new/walk4.png'),
             pygame.image.load('assets/player/new/walk5.png')]

walkLeft = [pygame.image.load('assets/player/new/walk1.png'),
            pygame.image.load('assets/player/new/walk2.png'),
            pygame.image.load('assets/player/new/walk3.png'),
            pygame.image.load('assets/player/new/walk4.png'),
            pygame.image.load('assets/player/new/walk5.png')]

DEFAULT_IMAGE_SIZE = (50, 50)

# Load and scale idle character image
char = pygame.image.load('assets/player/new/idle.png')
char = pygame.transform.scale(char, DEFAULT_IMAGE_SIZE)

# Constants for the player
PLAYER_SIZE = 50
PLAYER_SPEED = 5
PLAYER_INITIAL_POSITION = (100 - PLAYER_SIZE // 2, 300 - PLAYER_SIZE // 2)

# Game variables
score = 0
num_coins = 7
coins = []
game_start = True
game_loading = False  # Added state for loading screen
game_running = False
game_won = False
game_lose = False
time_limit = 30
timer = time_limit

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select an Image", 
                                            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    return file_path

class Player:
    def __init__(self, initial_position, size, speed):
        self.pos = list(initial_position)
        self.angle = 0
        self.size = size
        self.speed = speed
        self.hearts = MAX_HEARTS
        self.is_damaged = False
        self.isJump = False
        self.jumpCount = 10
        self.walkCount = 0

    def move(self, keys):
        if not self.isJump:
            new_pos = self.pos[:]
            if keys[pygame.K_w]:
                new_pos[0] += self.speed * math.sin(math.radians(self.angle))
                new_pos[1] -= self.speed * math.cos(math.radians(self.angle))
            if keys[pygame.K_s]:
                new_pos[0] -= self.speed * math.sin(math.radians(self.angle))
                new_pos[1] += self.speed * math.cos(math.radians(self.angle))
        else:
            if self.jumpCount >= -10:
                new_pos[1] -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 1
            else:
                self.jumpCount = 10
                self.isJump = False
        return new_pos
    
    def rotate(self, direction):
        self.angle += direction
        self.angle %= 360

    def draw(self, window):
        if self.walkCount >= len(walkLeft) * 3:
            self.walkCount = 0
        if keys[pygame.K_a]:
            walkLchar = pygame.transform.scale(walkLeft[self.walkCount // 3], DEFAULT_IMAGE_SIZE)
            rotated_surface = pygame.transform.rotate(walkLchar, -self.angle)
            self.walkCount += 1
        elif keys[pygame.K_d]:
            walkRchar = pygame.transform.scale(walkRight[self.walkCount // 3], DEFAULT_IMAGE_SIZE)
            rotated_surface = pygame.transform.rotate(walkRchar, -self.angle)
            self.walkCount += 1
        else:
            rotated_surface = pygame.transform.rotate(char, -self.angle)
            self.walkCount = 0

        rotated_rect = rotated_surface.get_rect(center=(self.pos[0] + self.size // 2, self.pos[1] + self.size // 2))
        window.blit(rotated_surface, rotated_rect.topleft)

    def reset(self, initial_position):
        self.pos = list(initial_position)
        self.angle = 0
        self.hearts = MAX_HEARTS
        self.is_damaged = False

    def bounce(self):
        self.pos[0] -= self.speed * math.sin(math.radians(self.angle)) * 2
        self.pos[1] += self.speed * math.cos(math.radians(self.angle)) * 2
        self.angle = (self.angle + 180) % 360 
        
def spawn_player():
    max_attempts = 100
    attempt = 0
    while max_attempts > 0:
        x = random.randint(27, WIDTH - 27)
        y = random.randint(27, HEIGHT - 27)
        all_white = True
        ##############################
        for dx in range(-30, 30):
            for dy in range(-30, 30):
                if 0 <= x + dx < bg_img.get_width() and 0 <= y + dy < bg_img.get_height():
                    if bg_img.get_at((x + dx, y + dy))[:3] != WHITE[:3]:
                        all_white = False
                        break
            if not all_white:
                break
        if all_white:
            return (x, y)
        max_attempts -= 1
        attempt += 1
            #####################
            
    return PLAYER_INITIAL_POSITION

def spawn_coins(num_coins):
    for _ in range(num_coins):
        max_attempts = 100
        while max_attempts > 0:
            x = random.randint(27, WIDTH - 27)
            y = random.randint(27, HEIGHT - 27)

            all_white = True
            for dx in range(-30, 30):
                for dy in range(-30, 30):
                    if bg_img.get_at((x + dx, y + dy))[:3] != WHITE[:3]:
                        all_white = False
                        break
                if not all_white:
                    break

            too_close = False
            for _, (existing_x, existing_y) in coins:
                if math.hypot(existing_x - x, existing_y - y) < 20:
                    too_close = True
                    break

            if all_white and not too_close:
                candy_asset = random.choice(candy_assets)
                candy_image = pygame.image.load(candy_asset)
                candy_image = pygame.transform.scale(candy_image, (35, 35))
                coins.append((candy_image, (x, y)))
                break
            
            max_attempts -= 1

def reset_game():
    global score, coins, game_running, game_won, game_lose, timer
    player.pos = list(spawn_player()) 
    player.angle = 0
    player.hearts = MAX_HEARTS
    player.is_damaged = False
    score = 0
    coins.clear()
    spawn_coins(num_coins)
    game_running = True
    game_won = False
    game_lose = False
    timer = time_limit 

def draw_hearts():
    hearts_bg = pygame.Surface((MAX_HEARTS * 44, 40), pygame.SRCALPHA)
    hearts_bg.fill((*BG_GREY, 216))
    window.blit(hearts_bg, (20, 20))
    for i in range(player.hearts):
        window.blit(heart_image, (0 + i * 40, 0))

def draw_score():
    font = pygame.font.Font(None, 36)
    score_surface = font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect(topright=(WIDTH - 30, 30))
    score_bg = pygame.Surface(score_rect.inflate(20, 20).size, pygame.SRCALPHA)
    score_bg.fill((*BG_GREY, 216))
    window.blit(score_bg, score_rect.inflate(20, 20).topleft)
    window.blit(score_surface, score_rect)
    
def draw_timer():
    font = pygame.font.Font(None, 36)
    timer_surface = font.render(f'Time Left: {max(0, int(timer))}', True, WHITE)
    timer_rect = timer_surface.get_rect(topright=(WIDTH - 30, 70))  # Positioned under the score
    timer_bg = pygame.Surface(timer_rect.inflate(20, 20).size, pygame.SRCALPHA)
    timer_bg.fill((*BG_GREY, 216))
    window.blit(timer_bg, timer_rect.inflate(20, 20).topleft)
    window.blit(timer_surface, timer_rect)


def draw_start_screen():
    window.fill(BLACK)
    font = pygame.font.Font('CFHalloween-Regular.ttf', 20)
    win_text = font.render("WELCOME TO PHOTO PHANTOM SCAVANGER HUNT", True, WHITE)
    win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    window.blit(win_text, win_rect)

    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Start", True, WHITE)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 ))
    pygame.draw.rect(window, (255, 169, 71), button_rect.inflate(20, 10), border_radius=10)
    window.blit(button_text, button_rect)

    return button_rect

def draw_loading_screen():
    window.fill(BLACK)
    font = pygame.font.Font(None, 32)
    load_text = font.render("Load an image to continue", True, WHITE)
    load_rect = load_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    window.blit(load_text, load_rect)

    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Load Image", True, WHITE)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 ))
    pygame.draw.rect(window, (255, 169, 71), button_rect.inflate(20, 10), border_radius=10)
    window.blit(button_text, button_rect)

    return button_rect

def draw_win_screen():
    window.fill(BLACK)
    font = pygame.font.Font('CFHalloween-Regular.ttf', 72)
    win_text = font.render("CONGRATS YOU WIN", True, WHITE)
    win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    window.blit(win_text, win_rect)

    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Play Again", True, WHITE)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 ))
    pygame.draw.rect(window, (255, 169, 71), button_rect.inflate(20, 10), border_radius=10)
    window.blit(button_text, button_rect)

    return button_rect

def draw_lose_screen():
    window.fill(BLACK)
    font = pygame.font.Font('CFHalloween-Regular.ttf', 72)
    lose_text = font.render("YOU LOSE", True, WHITE)
    lose_rect = lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    window.blit(lose_text, lose_rect)

    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Play Again", True, WHITE)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 ))
    pygame.draw.rect(window, (255, 169, 71), button_rect.inflate(20, 10), border_radius=10)
    window.blit(button_text, button_rect)

    return button_rect

player = Player(spawn_player(), PLAYER_SIZE, PLAYER_SPEED)

# Spawn initial coins
spawn_coins(num_coins)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_start:  # Check if in start screen
                button_rect = draw_start_screen()
                if button_rect.collidepoint(event.pos):  # Check if the start button is clicked
                    game_start = False  # Change game state to show loading screen
                    game_loading = True  # Now we show the loading screen
            elif game_loading:
                button_rect = draw_loading_screen()
                if button_rect.collidepoint(event.pos):
                    # Open file dialog and load image
                    file_path = open_file_dialog()
                    if file_path:
                        try:
                            userImage = ImageConvert(file_path)  # Use the loaded image path
                            userImage.convert_to_bw_segmentate()  # Assuming this is the method you want to call
                            game_loading = False  # Stop loading
                            game_running = True  # Start the game
                            
                        except Exception as e:
                            print("Error loading image:", e)
            elif game_won or game_lose:
                if draw_win_screen().collidepoint(event.pos) or draw_lose_screen().collidepoint(event.pos):
                    reset_game()
                    timer = time_limit

    keys = pygame.key.get_pressed()

    if game_running:
        timer -= 1 / FPS
        if timer <= 0:
            game_lose = True
        if keys[pygame.K_d]:
            player.rotate(-5)
        if keys[pygame.K_a]:
            player.rotate(5)

        new_pos = player.move(keys)

        player_center_pos = (int(new_pos[0] + player.size // 2), int(new_pos[1] + player.size // 2))
        if bg_img.get_at(player_center_pos)[:3] == (0, 0, 0) and not (CIRCLE_POSITION[0] - CIRCLE_RADIUS < player_center_pos[0] < CIRCLE_POSITION[0] + CIRCLE_RADIUS and 
                                                               CIRCLE_POSITION[1] - CIRCLE_RADIUS < player_center_pos[1] < CIRCLE_POSITION[1] + CIRCLE_RADIUS):
            
            player.bounce()
            if not player.is_damaged:
                player.hearts -= 1
                player.is_damaged = True
                if player.hearts <= 0:
                    game_lose = True
                    
        else:
            player.is_damaged = False
            player.pos = new_pos

        player.pos[0] = max(0, min(player.pos[0], WIDTH - player.size))
        player.pos[1] = max(0, min(player.pos[1], HEIGHT - player.size))

        for candy_image, (x, y) in coins[:]:
            if math.hypot(candy_image.get_rect(center=(x, y)).center[0] - player_center_pos[0],
                           candy_image.get_rect(center=(x, y)).center[1] - player_center_pos[1]) < 30:
                score += 1
                coins.remove((candy_image, (x, y)))
                if score >= num_coins:
                    game_won = True
                    game_running = False

    # Draw everything
    window.blit(bg_img, (0, 0))
    window.blit(bgOver_img, (0, 0))
    
    if not game_running and not (game_won or game_lose):
        window.blit(bgOver_img, (0, 0))

    for candy_image, (x, y) in coins:
        window.blit(candy_image, (x, y))

    player.draw(window)
    draw_hearts()
    draw_score()
    draw_timer()

    if game_won:
        draw_win_screen()

    if game_lose:
        draw_lose_screen()
        
    if game_loading:
        draw_loading_screen()

    if game_start:
        draw_start_screen()

    pygame.display.flip()
    clock.tick(FPS)
