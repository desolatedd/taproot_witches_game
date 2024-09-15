import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Get the base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define a helper function to construct paths relative to the script
def resource_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)

# Screen dimensions
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Start in windowed mode
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Game title and FPS
pygame.display.set_caption("Taproot Witches Shooter")
clock = pygame.time.Clock()

# Load Images using relative paths
witch_image = pygame.image.load(resource_path('assets/r.png')).convert_alpha()  # Witch image
spell_image = pygame.image.load(resource_path('assets/pngegg.png')).convert_alpha()  # Spell (fireball) image
enemy_image = pygame.image.load(resource_path('assets/bitcoin-cryptocurrency-in-pixel-art-style-illustration-free-png.webp')).convert_alpha()  # Enemy (Eye) image
background_image = pygame.image.load(resource_path('assets/539c483ff16585f1014ce8bff226bc56.png')).convert_alpha()  # Background image
taproot_witches_image = pygame.image.load(resource_path('assets/tap_witch.png')).convert_alpha()  # Taproot Witches text image

# Scale the background to fit the screen size
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Function to display the start screen with multi-line text and background image
def display_start_screen(screen, font):
    # Split the text into lines
    lines = ["Press S to Start.", "Made by CryptoDepressi for Witches :)"]
    
    # Starting position for the first line
    y_offset = screen_height // 2

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Render each line separately
    for i, line in enumerate(lines):
        start_text = font.render(line, True, (255, 255, 255))  # White text
        start_rect = start_text.get_rect(center=(screen_width // 2, y_offset + i * 50))  # Adjust vertical space (50 px)
        screen.blit(start_text, start_rect)

    pygame.display.flip()

    # Wait for the player to press 'S'
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                waiting = False

# Define Player (Witch)
class Witch(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(witch_image, (100, 150))  # Resize if necessary
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = screen_height // 2
        self.speed = 13

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        # Keep witch on the screen
        if self.rect.x < 0: self.rect.x = 0
        if self.rect.x > screen_width - self.rect.width: self.rect.x = screen_width - self.rect.width
        if self.rect.y < 0: self.rect.y = 0
        if self.rect.y > screen_height - self.rect.height: self.rect.y = screen_height - self.rect.height

# Define Spell (Fireball)
class Spell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(spell_image, (40, 40))  # Resize if necessary
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 12

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > screen_width:
            self.kill()

# Define Enemy (Eye)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemy_image, (50, 50))  # Resize if necessary
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        self.speed = 15

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:  # Enemy reached the left side of the screen
            global game_over
            game_over = True
            self.kill()

# Function to display "Game Over" message
def display_game_over(screen, font):
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()

    # Wait for a key press or delay for a few seconds
    pygame.time.wait(3000)  # Wait 3 seconds before quitting

# Main Game Function
def game():
    global game_over
    game_over = False  # Initialize game over status
    witch = Witch()
    spells = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Initialize score
    score = 0

    # Timers for spawning enemies
    enemy_spawn_timer = 50
    enemy_timer = enemy_spawn_timer

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            # Shooting spell
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                spell = Spell(witch.rect.x + 50, witch.rect.y + 50)
                spells.add(spell)

        # Movement controls
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -witch.speed
        if keys[pygame.K_RIGHT]: dx = witch.speed
        if keys[pygame.K_UP]: dy = -witch.speed
        if keys[pygame.K_DOWN]: dy = witch.speed

        witch.move(dx, dy)

        # Spawn enemies
        enemy_timer -= 1
        if enemy_timer <= 0:
            enemy = Enemy()
            enemies.add(enemy)
            enemy_timer = enemy_spawn_timer

        # Update spells and enemies
        spells.update()
        enemies.update()

        # Check for collisions between spells and enemies
        for spell in spells:
            hit_list = pygame.sprite.spritecollide(spell, enemies, True)
            if hit_list:
                spell.kill()
                score += 1

        # Check for collisions between the witch and enemies
        if pygame.sprite.spritecollide(witch, enemies, False):
            game_over = True  # End the game when an enemy collides with the player

        # Draw the background first
        screen.blit(background_image, (0, 0))  # Draw the background at the top-left corner

        # Draw everything else
        screen.blit(witch.image, witch.rect)
        spells.draw(screen)
        enemies.draw(screen)

        # Display the score
        pixel_font = pygame.font.Font(resource_path('assets/PixelifySans-Regular.ttf'), 30)
        score_text = pixel_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(centerx=screen_width // 2, top=10)  # Adjust 'top' as needed for vertical padding

        # Draw the score text on the screen
        screen.blit(score_text, score_rect)

        # Display "Taproot Witches" text below the score
        taproot_font = pygame.font.Font(resource_path('assets/PixelifySans-Regular.ttf'), 60)
        taproot_text = taproot_font.render("Taproot Witches", True, (255, 255, 255))
        taproot_rect = taproot_text.get_rect(centerx=screen_width // 2, top=score_rect.bottom + 10)

        # Draw the text onto the screen
        screen.blit(taproot_text, taproot_rect)

        pygame.display.flip()
        clock.tick(30)

    # End the game and display game over screen
    pixel_font = pygame.font.Font(resource_path('assets/PixelifySans-Regular.ttf'), 50)
    display_game_over(screen, pixel_font)

# Display start screen and wait for player to press 'S' to start the game
pixel_font = pygame.font.Font(resource_path('assets/PixelifySans-Regular.ttf'), 60)
display_start_screen(screen, pixel_font)

# Start the game after 'S' is pressed
game()

pygame.quit()
