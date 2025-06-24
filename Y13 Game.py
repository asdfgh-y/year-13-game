import pygame
import random
import math
from Y13_game_map import level1

pygame.init()  # initialisation of pygame

# game constants
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # create the game screen to play on
pygame.display.set_caption("Menu")
main_font = pygame.font.SysFont("cambria", 50)
timer = pygame.time.Clock()
fps = 30
level = level1
janno_image = pygame.image.load("janno pog.jpg")
run = False


class Button:
    def __init__(self, image, x_pos, y_pos, text_input, function):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.function = function

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position, function):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            if function == 0:
                pygame.quit()
            elif function == 1:
                global run, screen
                run = True
            pygame.quit()



    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "white")


def main_menu():  # main menu screen
    pygame.display.set_caption("Menu")
    # region buttons
    janno_button_surface = pygame.transform.scale(janno_image, (300, 110))
    janno_button = Button(janno_button_surface, 400, 100, "JANNO!", 1)

    quit_button = Button(janno_button_surface, 400, 500, "QUIT", 0)
    # endregion buttons
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                janno_button.check_for_input(pygame.mouse.get_pos(), 1)
                quit_button.check_for_input(pygame.mouse.get_pos(), 0)
        screen.fill(black)

        janno_button.update()
        janno_button.change_color(pygame.mouse.get_pos())
        quit_button.update()
        quit_button.change_color(pygame.mouse.get_pos())

        pygame.display.update()

# region game


def draw_map():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 * (0.5*num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2:
                pygame.draw.circle(screen, 'white', (j * num2 * (0.5*num2), i * num1 + (0.5 * num1)), 10)


def draw_player():
    player_x = 200
    player_y = 200
    direction = 2
    # 0-RIGHT, 1, LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(janno_image, (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(janno_image, True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(janno_image, 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(janno_image, 270), (player_x, player_y))


main_menu()
pygame.init()
while run:
    timer.tick(fps)
    screen.fill('black')
    draw_map()
    draw_player()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.flip()


# endregion


pygame.quit()
