import pygame
import time
import random
import numpy as np
import os

sourceFileDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(sourceFileDir)
pygame.init()
width = 1920
height = 1080
block_size = 60
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Snek")
pygame.font.init()
color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_snake = (144, 238, 144)
color_fruit = (255, 165, 0)
color_background = (255, 255, 255)
color_border = (59, 71, 48)
clock = pygame.time.Clock()
eating = pygame.mixer.Sound("eating.wav")
eating.set_volume(0.6)
pygame.mixer.music.load("music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

def message(msg, pos, size, color):
    font = pygame.font.SysFont(pygame.font.get_default_font(), size)
    text_surface = font.render(msg, True, color)
    screen.blit(text_surface, text_surface.get_rect(center = pos))

def spawnFruit(snake):
    pos_arr = []
    for i in range(int(width/block_size)-2):
        for j in range(int(height/block_size)-2):
            pos_arr.append([(i+1)*block_size, (j+1)*block_size])
    for element in snake:
        if element in pos_arr:
            pos_arr.remove(element)
    pos = pos_arr[random.randint(0, len(pos_arr)-1)]
    return pos

def gameLoop():
    game_over = False
    game_quit = False
    snake = []
    snake_pos = [width/2, height/2]
    fruit_pos = spawnFruit(snake)
    dir = [0, 1]
    dir_new = [0, 1]
    temp = [0, 1]
    score = 0
    while not game_quit:
        dir = dir_new
        snake.append(snake_pos.copy())
        mouse = pygame.mouse.get_pos()
        
        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_quit = True
                    elif event.key == pygame.K_LEFT:
                        temp = [-1, 0]
                    elif event.key == pygame.K_RIGHT:
                        temp = [1, 0]
                    elif event.key == pygame.K_UP:
                        temp = [0, -1]
                    elif event.key == pygame.K_DOWN:
                        temp = [0, 1]
                    if (temp[0] != dir[0]*(-1) or temp[1] != dir[1]*(-1)) and (temp[0] != dir[0] or temp[1] != dir[1]):
                        dir_new = temp
            snake_pos[0] += dir_new[0]*block_size
            snake_pos[1] += dir_new[1]*block_size
            screen.fill(color_background)
            pygame.draw.rect(screen, color_border, [0, 0, block_size, height])
            pygame.draw.rect(screen, color_border, [0, 0, width, block_size])
            pygame.draw.rect(screen, color_border, [width-block_size, 0, block_size, height])
            pygame.draw.rect(screen, color_border, [0, height-block_size, width, block_size])
            for element in snake:
                pygame.draw.rect(screen, color_snake, [element[0], element[1], block_size, block_size])
            '''
            eyes_arr = []
            if dir == [0, 1]:
                eyes_arr = [[block_size/8, block_size/8], [block_size*5/8, block_size/8], [block_size*5/24, block_size/8], [block_size*5/24, block_size*17/8]]

            elif dir == [0, -1]:
                eyes_arr = [[block_size/8, block_size/8], [block_size*5/8, block_size/8], [block_size*5/24, block_size/8], [block_size*5/24, block_size*17/8]]

            elif dir == [1, 0]:
                eyes_arr = [[block_size/8, block_size/8], [block_size*5/8, block_size/8], [block_size*5/24, block_size/8], [block_size*5/24, block_size*17/8]]

            elif dir == [-1, 0]:
                eyes_arr = [[block_size/8, block_size/8], [block_size*5/8, block_size/8], [block_size*5/24, block_size/8], [block_size*5/24, block_size*17/8]]
            pygame.draw.rect(screen, color_white, [snake_pos[0]+eyes_arr[0][0], snake_pos[1]+eyes_arr[0][1], block_size/4, block_size/4])
            '''
            pygame.draw.rect(screen, color_fruit, [fruit_pos[0], fruit_pos[1], block_size, block_size])
            message(str(score+1), (fruit_pos[0]+block_size/2, fruit_pos[1]+block_size/2), int(block_size), (173, 122, 2))
            pygame.display.update()
            if snake_pos[0] >= width-block_size or snake_pos[0] < block_size or snake_pos[1] >= height-block_size or snake_pos[1] < block_size:
                game_over = True
            for element in snake[:-1]:
                if snake_pos[0] == element[0] and snake_pos[1] == element[1]:
                    game_over = True
                    break
            if game_over:
                message("Snek Is Kil!", (width/2, height/2), block_size, (0, 0, 0))
                message("click anywhere to restart...",(width/2+block_size/5, height/2+40), int(block_size/2), (0, 0, 0))
            if snake_pos[0] == fruit_pos[0] and snake_pos[1] == fruit_pos[1]:
                eating.play()
                score += 1
                fruit_pos = spawnFruit(snake)
            else:
                del(snake[0])
            clock.tick(8)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    if 0 <= mouse[0] <= width and 0 <= mouse[1] <= height:
                        game_over = False
                        snake_pos = [width/2, height/2]
                        snake = []
                        fruit_pos = spawnFruit(snake)
                        dir = [0, 1]
                        score = 0
            pygame.display.update()

gameLoop()
pygame.quit()
quit()
