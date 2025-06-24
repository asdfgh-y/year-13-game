import pygame
import random
import math

pygame.init()  # initialisation of pygame

# game constants
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
WIDTH = 970
HEIGHT = 625
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # create the game screen to play on
pygame.display.set_caption("Menu")
main_font = pygame.font.SysFont("cambria", 36)
building = False


class Button:
    def __init__(self, image, x_pos, y_pos, text_input, function, placement):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.function = function
        self.placement = placement

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position, function):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            global building
            if function == 0:
                pygame.quit()
                print("Quitting game")
                exit()
            elif function == 1:
                melting_floor_game()
                pygame.quit()
            elif function == 2:
                print("Cancel")
                building = False
                print(str(self.placement[0]) + ", " + str(self.placement[1]))
            elif function == 3:
                print("Road")
                building = False
            elif function == 4:
                print("Rail")
            elif function == 5:
                print("Pathway")
            elif function == 6:
                print("Bus")
            elif function == 7:
                print("Destroy")

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "white")


# region maps
# layout of the tiles and starting condition
tiles = [
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
]

y_streets = [
    [10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10],
]

x_streets = [
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
]
# endregion maps


# region Melting floor game
def melting_floor_game():
    # game variables
    global building, tiles, x_streets, y_streets
    mouse_pos = 0
    tile_size = 80
    pygame.display.set_caption("Melting floor game")  # title the window with the already created TITLE variable
    background = black
    font = pygame.font.Font('freesansbold.ttf', 16)

    red_button_button_surface = pygame.image.load("button.png")
    red_button_button_surface = pygame.transform.scale(red_button_button_surface, (170, 60))
    running = True
    while running:
        screen.fill(background)
        if building:
            cancel_button.update()
            build_road_button.update()
            build_train_button.update()
            build_walking_area.update()
            build_bus_lane_road.update()
            build_destroy.update()
            cancel_button.change_color(pygame.mouse.get_pos())
            build_road_button.change_color(pygame.mouse.get_pos())
            build_train_button.change_color(pygame.mouse.get_pos())
            build_walking_area.change_color(pygame.mouse.get_pos())
            build_bus_lane_road.change_color(pygame.mouse.get_pos())
            build_destroy.change_color(pygame.mouse.get_pos())
# region draw_tiles
        for y in range(len(tiles)):  # Loop over column indices
            for x in range(len(tiles[y])):  # Loop over row indices
                pygame.draw.rect(screen, (0, 0, 25 * (tiles[y][x])),
                                 [(tile_size * x + 10), (tile_size * y + 10), (tile_size - 20), (tile_size - 20)])

        for y in range(len(y_streets)):
            for x in range(len(y_streets[y])):
                pygame.draw.rect(screen, ((25 * y_streets[y][x]), 0, 0), [(tile_size * x + 72), (tile_size * y + 15), 16, 50])

        for y in range(len(x_streets)):
            for x in range(len(x_streets[y])):
                pygame.draw.rect(screen, (0, (25 * x_streets[y][x]), 0), [(tile_size * x + 15), (tile_size * y + 72), 50, 16])
# endregion draw_tiles
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if building:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cancel_button.check_for_input(pygame.mouse.get_pos(), 2)
                    build_road_button.check_for_input(pygame.mouse.get_pos(), 3)
                    build_train_button.check_for_input(pygame.mouse.get_pos(), 4)
                    build_walking_area.check_for_input(pygame.mouse.get_pos(), 5)
                    build_bus_lane_road.check_for_input(pygame.mouse.get_pos(), 6)
                    build_destroy.check_for_input(pygame.mouse.get_pos(), 7)

            if not building:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_x = mouse_pos[0]
                    mouse_y = mouse_pos[1]
                    # for y in range(len(tiles)):
                        # if 10 + 80 * y < mouse_y < 70 + 80 * y:
                            # for x in range(len(tiles[y])):
                                # if 10 + 80 * x < mouse_x < 70 + 80 * x:

                                    # print("routing")

                    for y in range(len(y_streets)):
                        if 15 + 80 * y < mouse_y < 65 + 80 * y:
                            for x in range(len(y_streets[y])):
                                if 72 + 80 * x < mouse_x < 88 + 80 * x:
                                    building = True
                                    print("hi")
                                    build_location = (x, y, 1)
                                    cancel_button = Button(red_button_button_surface, 880, 600, "Cancel", 0,
                                                           build_location)
                                    build_road_button = Button(red_button_button_surface, 880, 80, "Road", 3,
                                                               build_location)
                                    build_train_button = Button(red_button_button_surface, 880, 180, "Rail", 4,
                                                                build_location)
                                    build_walking_area = Button(red_button_button_surface, 880, 280, "Pathway", 5,
                                                                build_location)
                                    build_bus_lane_road = Button(red_button_button_surface, 880, 380, "Bus", 6,
                                                                 build_location)
                                    build_destroy = Button(red_button_button_surface, 880, 480, "Destroy", 7,
                                                           build_location)
                    for y in range(len(x_streets)):
                        if 72 + 80 * y < mouse_y < 88 + 80 * y:
                            for x in range(len(x_streets[y])):
                                if 15 + 80 * x < mouse_x < 65 + 80 * x:
                                    building = True
                                    print("bye")
                                    build_type = -1
                                    build_location = (x, y, 0)
                                    cancel_button = Button(red_button_button_surface, 880, 600, "Cancel", 0,
                                                           build_location)
                                    build_road_button = Button(red_button_button_surface, 880, 80, "Road", 3,
                                                               build_location)
                                    build_train_button = Button(red_button_button_surface, 880, 180, "Rail", 4,
                                                                build_location)
                                    build_walking_area = Button(red_button_button_surface, 880, 280, "Pathway", 5,
                                                                build_location)
                                    build_bus_lane_road = Button(red_button_button_surface, 880, 380, "Bus", 6,
                                                                 build_location)
                                    build_destroy = Button(red_button_button_surface, 880, 480, "Destroy", 7,
                                                           build_location)

        mouse_pos_text = font.render('mouse_pos: ' + str(mouse_pos), True, white, black)
        screen.blit(mouse_pos_text, ((WIDTH / 2 - 50), (HEIGHT - 30)))

        pygame.display.flip()


def reset_map():
    global tiles, x_streets, y_streets
    tiles = [
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    ]

    y_streets = [
        [10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10],
    ]

    x_streets = [
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    ]
# endregion


def main_menu():  # main menu screen
    pygame.display.set_caption("Menu")
    # region buttons
    janno_button_surface = pygame.image.load("janno pog.jpg")
    janno_button_surface = pygame.transform.scale(janno_button_surface, (300, 110))
    janno_button = Button(janno_button_surface, 400, 100, "JANNO!", 1, (0, 0, 0))
    quit_button = Button(janno_button_surface, 400, 500, "QUIT", 0, (0, 0, 0))
    # endregion buttons
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                janno_button.check_for_input(pygame.mouse.get_pos(), 1)
                quit_button.check_for_input(pygame.mouse.get_pos(), 0)
        screen.fill(black)
        janno_button.update()
        janno_button.change_color(pygame.mouse.get_pos())
        quit_button.update()
        quit_button.change_color(pygame.mouse.get_pos())

        pygame.display.update()


main_menu()
