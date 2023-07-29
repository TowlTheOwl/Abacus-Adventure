import pygame
from screeninfo import get_monitors
from abacus import Abacus
import numpy as np

def menu(win):
    win.fill((3, 173, 252))

def map(win, map):
    win.blit(map, (0, 0))

def draw_abacus(win, abacus, start_pos, width, height):
    win.fill((65, 132, 52))
    x_interval = width/abacus.width
    bead_height = height/7.5
    bead_pos = np.zeros((7, abacus.width))

    for i in range(abacus.width):
        x = start_pos[0]
        y = start_pos[1]
        for top_interval in range(2):
            if abacus.upper[top_interval, i]:
                pygame.draw.ellipse(win, (200, 200, 200), (x+x_interval*i, y, x_interval, bead_height), 0)
                y += bead_height
                bead_pos[top_interval, i] = y
            else:
                y += bead_height
                bead_pos[top_interval, i] = y
        y += bead_height/2
        for bot_interval in range(5):
            if abacus.lower[bot_interval, i]:
                pygame.draw.ellipse(win, (200, 200, 200), (x+x_interval*i, y, x_interval, bead_height), 0)
                y += bead_height
                bead_pos[bot_interval+2, i] = y
            else:
                y += bead_height
                bead_pos[bot_interval+2, i] = y
    
    return bead_pos, x_interval

def main():
    m = get_monitors()[0]

    user_screen_size = (m.width, m.height)
    # user_screen_size = (1280, 1024)
    desired_size = (1920, 1020)
    scale_factor = (user_screen_size[0]/desired_size[0], user_screen_size[1]/desired_size[1])

    status = "menu"

    clock = pygame.time.Clock()

    # images load
    map_img_raw = pygame.image.load('assets/images/island.jpg')
    map_img = pygame.transform.scale_by(map_img_raw, scale_factor)

    # abacus set up
    abacus_width = 6
    aba = Abacus(abacus_width)
    start_pos = (200*scale_factor[0], 100*scale_factor[1])
    width = 1500*scale_factor[0]
    height = 800*scale_factor[1]

    pygame.init()
    screen = pygame.display.set_mode(user_screen_size)
    pygame.display.set_caption("Abacus Adventure")
    
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            run = False
        if keys[pygame.K_0]:
            status = "menu"
        if keys[pygame.K_1]:
            status = "map"
        if keys[pygame.K_2]:
            status = "abacus"
        
        if status == "menu":
            menu(screen)
        elif status == "map":
            map(screen, map_img)
        elif status == "abacus":
            bead_pos, x_interval = draw_abacus(screen, aba, start_pos, width, height)
            if mouse[0]:
                mouse_pos = pygame.mouse.get_pos()
                if start_pos[0] <= mouse_pos[0] <= (start_pos[0] + width):
                    col = (mouse_pos[0] - start_pos[0])//x_interval
                    col = int(col)
                    for i in range(7):
                        if mouse_pos[1] <= (bead_pos[i, col]):
                            aba.select((i, col))
                            break
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()