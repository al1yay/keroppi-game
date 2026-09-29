import pygame
import asyncio
import io
import random
import sys
from urllib.request import urlopen

# 1. Initialize Pygame
async def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Sprite URL Loader")
    clock = pygame.time.Clock()

    # 2. Your image URL (Make sure it ends in .png, .jpg, etc.)
    # Note: The website hosting the image must allow cross-origin (CORS) requests.
    # 3. Fetch image using urllib instead of requests

    pygame.mixer.init()

    pygame.mixer.music.load("assets/keroppisong.ogg")
    jump_sound = pygame.mixer.Sound("assets/keroppijump.wav")
    kirby_sound = pygame.mixer.Sound("assets/kirby.wav")
    keroppi_change = pygame.mixer.Sound("assets/keroppi_change.wav")

    # Set the volume (value from 0.0 to 1.0)
    pygame.mixer.music.set_volume(0.5)
    jump_sound.set_volume(0.8)
    kirby_sound.set_volume(0.8)
    keroppi_change.set_volume(0.8)
    # Play the music (-1 means it will loop infinitely)
    pygame.mixer.music.play(-1)


    bg_image = pygame.image.load ("assets/keroppibackground.jpg").convert()
    bg_image = pygame.transform.scale(bg_image, (1200, 400))
    sprite_surface = pygame.image.load("assets/keroppi.png").convert_alpha()
    kirby_surface = pygame.image.load("assets/kirby.png").convert_alpha() 

    gravity = 2
    score = 0

    PLATFORM = (255, 255, 255)

    # Game Loop
    running = True
    sprite_surface = pygame.transform.scale_by(sprite_surface, (0.2))
    kirby_surface = pygame.transform.scale_by(kirby_surface, (0.03))
    sprite_x, sprite_y = 100, 0
    ground = 400 - sprite_surface.get_height() + 5
    on_ground = False
    sprite_dy = 0

    kirby_list = []


    hitbox_list = []

    for k in kirby_list:
        kirby_rect = pygame.Rect(k[0]+10, k[1]+10, 25, 25)

        hitbox_list.append(kirby_rect)

    platform_list = []

    platform_list.append(pygame.Rect(30, 350, 180, 35))
    platform_list.append(pygame.Rect(170, 225, 180, 35))
    platform_list.append(pygame.Rect(400, 100, 180, 35))
    platform_list.append(pygame.Rect(400, 350, 180, 35))

    for i in range(10):
        cx = random.randint(0+kirby_surface.get_height(), 600-kirby_surface.get_height())
        cy = random.randint(0+kirby_surface.get_height(), 400-kirby_surface.get_height())

        kirby_list.append([cx, cy])

    hitbox_list = []

    for k in kirby_list:
            
        kirby_rect = pygame.Rect(k[0]+6, k[1]+6, 35, 35)

        hitbox_list.append(kirby_rect)

    for i in range(10):
        for p in platform_list:
            while hitbox_list[i].colliderect(p):
                cx = random.randint(0+kirby_surface.get_height(), 600-kirby_surface.get_height())
                cy = random.randint(0+kirby_surface.get_height(), 400-kirby_surface.get_height())
                kirby_list[i] = ([cx, cy])
                hitbox_list[i] = pygame.Rect(kirby_list[i][0]+10, kirby_list[i][1]+10, 25, 25)



    player_rect = pygame.Rect(
        (sprite_x),
        (sprite_y),
        60,
        90
    )

    score_font = pygame.font.SysFont(None, 40) 

    def display_score(x, y):
        score_text = score_font.render("Kirby Count: " + str(score), True, PLATFORM)
        
        # 4. Draw the score text surface onto the screen at (x, y) coordinates
        screen.blit(score_text, (x, y))

    tinted = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # Clear screen with a background color
        screen.blit(bg_image, (0, 0))

        # pygame.draw.rect(screen, PLATFORM, player_rect)
    
        # Draw your sprite onto the screen
        screen.blit(sprite_surface, (sprite_x, sprite_y))

        # for a in hitbox_list:
            # pygame.draw.rect(screen, PLATFORM, a)

        for k in kirby_list:
            screen.blit(kirby_surface, (k[0], k[1]))

        for p in platform_list:
            pygame.draw.rect(screen, PLATFORM, p)

        display_score(10, 10)

        # keys
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            sprite_x -= 3

        if keys[pygame.K_RIGHT]:
            sprite_x += 3
        

        if keys[pygame.K_UP] and on_ground:
            jump_sound.play()
            sprite_dy = -23
            on_ground = False
        
        # gravity or movement
        sprite_dy += gravity
        sprite_y += sprite_dy

        player_rect.x = sprite_x+17
        player_rect.y = sprite_y+10

        for i in range(len(hitbox_list) - 1, -1, -1):

            if player_rect.colliderect(hitbox_list[i]):
                kirby_sound.play()
                hitbox_list.remove(hitbox_list[i])
                kirby_list.remove(kirby_list[i])
                score += 1

        on_ground = False

        for p in platform_list:

            if player_rect.colliderect(p) and on_ground:
                if sprite_x > p.x-90:
                    sprite_x = p.x-90
                elif sprite_x > p.x+180:
                    sprite_x = p.x+180
            if player_rect.colliderect(p) and sprite_dy > 0:
                    player_rect.bottom = p.top
                    sprite_y = player_rect.y - 10
                    sprite_dy = 0
                    on_ground = True
            else:
                ground = 400 - sprite_surface.get_height() + 5

        if sprite_y >= ground:
            sprite_y = ground
            sprite_dy = 0
            on_ground = True

        if not kirby_list:
            for i in range(10):
                cx = random.randint(20, 550)
                cy = random.randint(20, 350)
                kirby_list.append([cx, cy])
                hitbox_list.append(pygame.Rect(cx + 10, cy + 10, 25, 25))

        if score >= 50 and not tinted:
            keroppi_change.play()
            tinted = True
            # Apply a pink tint to the sprite_surface
            pink_surface = pygame.Surface(sprite_surface.get_size(), pygame.SRCALPHA)
            pink_surface.fill((255, 105, 180))  # Hot pink RGB value

            sprite_surface.blit(pink_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)




        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0) # 3. VERY IMPORTANT: Yield control to the browser

    pygame.quit()

    sys.exit()

asyncio.run(main())
