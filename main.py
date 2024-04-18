import pygame
import time
import random

pygame.font.init()

pygame.display.set_caption('Space Dodge')

pygame.mixer.init()
pygame.mixer.music.load('bg_music.mp3')

# window
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load('bg.jpg'),(WIDTH,HEIGHT))
FONT = pygame.font.SysFont('comicsans',30)

# player
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

# star
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0,0))

    time_text = FONT.render(f'Time: {round(elapsed_time)}s', 1, 'white')

    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, 'red', player)

    for star in stars:
        pygame.draw.rect(WIN, 'white', star)

    pygame.display.update()



def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    # display time
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    # stars
    star_add_increment = 2000
    star_count = 0
    stars = []

    hit = False
    pygame.mixer.music.play()

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time()-start_time
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():

            # Check if quit button is clicked
            if event.type == pygame.QUIT:
                run = False
                pygame.mixer.music.unload()
                break

        # Key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        elif keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
       
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if(hit):
            lost_text = FONT.render('You Lost!', 1, 'white')
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.mixer.music.unload()
            pygame.mixer.music.load('game_over.mp3')
            pygame.mixer.music.play()
            pygame.time.delay(4000)
            pygame.mixer.music.unload()
            break

        draw(player, elapsed_time, stars)


    
    pygame.quit()

if __name__ == '__main__':
    main()