import pygame
import random

from pygame.sprite import GroupSingle


# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 400
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vertical Scroll Shooter")
icon = pygame.image.load("Icon/icon-ship.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1800)

enemy_shoot_event = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_shoot_event, 2700)

obstacle_change_timer = pygame.USEREVENT + 3
pygame.time.set_timer(obstacle_change_timer, 2500)

# Define colors
WHITE = (255, 255, 255)

# Load images
player_img = pygame.image.load("Player/player.png").convert_alpha()
player_left_img = pygame.image.load("Player/player_left.png").convert_alpha()
player_right_img = pygame.image.load("Player/player_right.png").convert_alpha()
player_healt_img = pygame.image.load("Health/health.png")
enemy_1_img = pygame.image.load("Enemy/enemy.png").convert_alpha()
enemy_2_img = pygame.image.load("Enemy/enemy_2.png").convert_alpha()
enemy_bullet_img = pygame.image.load("Enemy/enemy_bullet.png").convert_alpha()
bullet_img = pygame.image.load("Player/bullet.png").convert_alpha()
background_img = pygame.image.load("All_Background/background.png").convert()
background1_img = pygame.image.load("All_Background/stars-1.png").convert_alpha()
background2_img = pygame.image.load("All_Background/stars-2.png").convert_alpha()

# Load explosion animation frames
explosion_frames = []
for i in range(1, 9):
    frame = pygame.image.load(f"Explosion/explosion-{i}.png").convert_alpha()
    explosion_frames.append(frame)


# Scale the background image
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT * 2))
background1_img = pygame.transform.scale(background1_img, (WIDTH, HEIGHT * 2))
background2_img = pygame.transform.scale(background2_img, (WIDTH, HEIGHT * 2))


# Get image dimensions
player_width, player_height = player_img.get_rect().size
enemy_width, enemy_height = enemy_1_img.get_rect().size
bullet_width, bullet_height = bullet_img.get_rect().size

# Set up the scoreboard
score = 0
font = pygame.font.Font(None, 36)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - player_height - 5)
        self.speed = 5
        self.radius = player_width // 2

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.image = player_left_img
        elif keys[pygame.K_RIGHT] and self.rect.x < WIDTH - player_width:
            self.rect.x += self.speed
            self.image = player_right_img
        else:
            self.image = player_img

class PlayerHealth(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.max_health = 3
        self.current_health = self.max_health
        self.image = pygame.transform.scale_by(player_healt_img.convert_alpha(),1.5)
        
        self.health_bar = pygame.Surface((74, 6))
        self.health_bar.fill((0, 255, 0))
        
        self.rect = self.image.get_rect(center = (50, 580))
        self.health_bar_rect = self.health_bar.get_rect(center = (51, 584))

    def decrease_health(self):
        if self.current_health > 0:
            self.current_health -= 1
            self.health_bar = pygame.Surface((int(self.health_bar.get_width() * self.current_health / self.max_health), 6))
            self.health_bar.fill((0, 255, 0))
        else: game_over == True
    
    def update(self):
        pass
    
    def draw(self, surface):
        surface.blit(self.health_bar, self.health_bar_rect)
        surface.blit(self.image, self.rect)
        


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_1_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - enemy_width)
        self.rect.y = random.randint(-HEIGHT, -enemy_height)
        self.speed = 4
        self.radius = enemy_width // 2

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - enemy_width)
            self.rect.y = random.randint(-HEIGHT, -enemy_height)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.seed = 8
    
    def update(self):
        self.rect.y += self.seed
        if self.rect.y > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frame_index = 0
        self.image = explosion_frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.frame_index += 1
        if self.frame_index >= len(explosion_frames):
            self.kill()
        else:
            self.image = explosion_frames[self.frame_index]


# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Create player instance
player = Player()
all_sprites.add(player)

player_health = PlayerHealth()
all_sprites.add(player_health)

background1_y = 0
background2_y = 0

# Game loop
running = True
game_over = False
enemy_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(bullets) < 3:
                    bullet = Bullet(player.rect.centerx, player.rect.y)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
        if event.type == obstacle_timer or event.type == obstacle_change_timer:
            enemy = Enemy()
            if event.type == obstacle_change_timer:
                enemy.image = enemy_2_img
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemy_count += 1
        if event.type == enemy_shoot_event:
            for enemy in enemies:
                enemy.shoot()


    # Update player pos
    keys = pygame.key.get_pressed()
    player.update(keys)

    # Enemy shoot
    enemy_bullets.update()
    
    # Shows life 
    player_health.update()

    # Move the enemies
    for enemy in enemies:
        enemy.update()

    # Move the bullets
    for bullet in bullets:
        bullet.update()

    # Check for bullet-enemy collisions
    collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for enemy, bullet_list in collisions.items():
        explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
        all_sprites.add(explosion)
        explosions.add(explosion)
        score += 1
    
    explosions.update()
    

    # Check for enemy_bullet-player collisions
    if player_health.current_health > 0:
        collisions1 = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if collisions1:
            player_health.decrease_health()

        # Check for player-enemy collisions
        collisions = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
        if collisions or player.rect.y > HEIGHT:
            player_health.decrease_health()
    else: game_over = True
    
    # Check if the game should end
    if score == 20:
        game_over = True

    if game_over:
        if score >= 15:
            game_result_text = font.render("You Win", True, WHITE)
        else:
            game_result_text = font.render("Game Over", True, WHITE)
        game_result_text_rect = game_result_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(game_result_text, game_result_text_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    # Update background position
    background1_y += 1
    background2_y += 1

    if background1_y >= HEIGHT:
        background1_y = -HEIGHT
    if background2_y >= HEIGHT:
        background2_y = -HEIGHT

    # Draw the scrolling background
    window.blit(background_img, (0, 0))
    window.blit(background1_img, (0, background1_y))
    window.blit(background1_img, (0, background1_y - HEIGHT))   
    window.blit(background2_img, (0, background2_y))
    window.blit(background2_img, (0, background2_y - HEIGHT))


    # Draw all sprites
    all_sprites.draw(window)

    # Draw enemy bullet
    enemy_bullets.draw(window)

    player_health.draw(window)

    # Update and display the scoreboard
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

    # Remove finished explosions
    explosions.remove(*[explosion for explosion in explosions if not explosion.alive()])
    
    # Update the display
    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
