import pygame
import random
from pygame.locals import *
from pygame import mixer


pygame.init()

# Screen setup
SCREEN = pygame.display.set_mode((640, 480))
CLOCK = pygame.time.Clock()

pygame.display.set_caption("Winter Holidays")
mixer.init()
mixer.music.load('C:/Users/tsver/Downloads/song2.mp3')
mixer.music.set_volume(0.1)  #MUSCIS
mixer.music.play(-1)

# Background setup
background = pygame.image.load("C:/Users/tsver/Downloads/cleanbackground1.png"
"").convert_alpha()
background = pygame.transform.scale(background, (640, 480))
dark_overlay = pygame.Surface((640, 480))  # Same size as the screen
dark_overlay.set_alpha(50)  # Adjust transparency (0 is fully transparent, 255 is fully opaque)
dark_overlay.fill((0, 0, 0))  # Black color
 
# Load sound effects
catch_sound = pygame.mixer.Sound("C:/Users/tsver/Downloads/shine.mp3")  # Replace with your sound file path
catch_sound.set_volume(0.1)
hazard_sound = pygame.mixer.Sound("C:/Users/tsver/Downloads/damagesound.mp3")  # Replace with your hazard sound file path
hazard_sound.set_volume(0.1)
game_over_music = pygame.mixer.Sound("C:/Users/tsver/Downloads/gameover.mp3")  # Game over music file
game_over_music.set_volume(0.1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:/Users/tsver/Downloads/penguin3.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (640 // 2, 480 - 60)
        self.speed = 3
        self.lives = 3  # Starting with 3 lives
        self.direction = "right"  # Initial direction

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 640: 
            self.rect.x += self.speed

        # Move left
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            if self.direction != "left":
                self.image = pygame.transform.flip(self.image, True, False)  # Flip horizontally
                self.direction = "left"

        # Move right
        if keys[pygame.K_RIGHT] and self.rect.right < 640:
            self.rect.x += self.speed
            if self.direction != "right":
                self.image = pygame.transform.flip(self.image, True, False)  # Flip horizontally
                self.direction = "right"





class Present(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:/Users/tsver/Downloads/present2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Adjusting present size to be smaller than the player
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 640 - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 480:
            self.kill()

class Hazard(pygame.sprite.Sprite):  # New class for hazard objects
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:/Users/tsver/Downloads/rock2.png").convert_alpha()  # Use a hazard image
        self.image = pygame.transform.scale(self.image, (70, 40))  # Adjust size
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 640 - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 480:
            self.kill()

def main():
    running = True
    presents = pygame.sprite.Group()
    hazards = pygame.sprite.Group()  # New group for hazard objects
    all_sprites = pygame.sprite.Group()  # Group for all sprites
    player = Player()
    all_sprites.add(player)
    score = 0
    lives = 3  # Number of lives
    SPAWN_PRESENT = pygame.USEREVENT + 1
    SPAWN_HAZARD = pygame.USEREVENT + 2  # New event for spawning hazards
    pygame.time.set_timer(SPAWN_PRESENT, 2000)  # Spawn a present every 2 seconds
    pygame.time.set_timer(SPAWN_HAZARD, 3000)  # Spawn a hazard every 3 seconds


     # Load heart images for lives display
    heart_image = pygame.image.load("C:/Users/tsver/Downloads/heart2.png").convert_alpha()
    heart_image = pygame.transform.scale(heart_image, (35, 35))  # Adjust size

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_PRESENT:
                present = Present()
                presents.add(present)
                all_sprites.add(present)
            elif event.type == SPAWN_HAZARD:  # Spawn hazards at regular intervals
                hazard = Hazard()
                hazards.add(hazard)
                all_sprites.add(hazard)

        # Update player and presents
        player.update()
        presents.update()
        hazards.update()

        # Check for collisions with presents
        collided_presents = pygame.sprite.spritecollide(player, presents, True)
        score += len(collided_presents)
        if collided_presents:
            mixer.Sound.play(catch_sound)  # Play catch sound when present is collected

        # Check for collisions with hazards
        collided_hazards = pygame.sprite.spritecollide(player, hazards, True)
        if collided_hazards:
            player.lives -= 1
            mixer.Sound.play(hazard_sound)
            if player.lives <= 0:
                running = False  # End the game if no lives are left

        # Drawing
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(dark_overlay, (0, 0))
        all_sprites.draw(SCREEN)

        # Display score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        SCREEN.blit(score_text, (10, 10))
        #lives_text = font.render(f"Lives: {player.lives}", True, (255, 0, 0))
        #SCREEN.blit(lives_text, (10, 40))

        if player.lives <= 0:
            mixer.music.stop()
            mixer.Sound.play(game_over_music)  # Play game over music
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            SCREEN.blit(game_over_text, (240, 240))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds before exiting
            running = False

        # Display lives as heart images
        for i in range(player.lives):
            SCREEN.blit(heart_image, (10 + i * 40, 40))  # Display hearts spaced apart


        pygame.display.flip()
        CLOCK.tick(60)

    pygame.quit()

main()
