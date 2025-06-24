import pygame
import random
import math
from Y13_game_map import start_pos, level1, level2
level = level2

pygame.init()  # initialisation of pygame
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # create the game screen to play on
pygame.display.set_caption("Menu")
main_font = pygame.font.SysFont("cambria", 50)
button_image = pygame.image.load('button.png')
game = False
menu = True


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
                exit()
            else:
                global game, menu, level, vehicle, run
                if 1 <= function <= 2:
                    menu = False
                game = True
                if function == 1:
                    level = level1
                    vehicle = 0
                elif function == 2:
                    level = level2
                    vehicle = 0
                elif function == 3:
                    vehicle = 0
                elif function == 4:
                    vehicle = 1
                elif function == 5:
                    vehicle = 2
                elif function == 6:
                    run = False
                    game = False
                    menu = True
                    main_menu()

    def change_colour(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "white")


def main_menu():  # main menu screen
    pygame.display.set_caption("Menu")
    # region buttons
    red_menu_button_surface = pygame.transform.scale(button_image, (300, 110))
    level_1_button = Button(red_menu_button_surface, (WIDTH // 3), 100, "Level 1!", 1)
    level_2_button = Button(red_menu_button_surface, ((WIDTH // 3) * 2), 100, "Level 2!", 2)
    quit_button = Button(red_menu_button_surface, (WIDTH // 2), 500, "QUIT", 0)
    # endregion buttons
    while menu:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                exit()
            if events.type == pygame.MOUSEBUTTONDOWN:
                level_1_button.check_for_input(pygame.mouse.get_pos(), 1)
                level_2_button.check_for_input(pygame.mouse.get_pos(), 2)
                quit_button.check_for_input(pygame.mouse.get_pos(), 0)
        screen.fill('black')

        level_1_button.change_colour(pygame.mouse.get_pos())
        level_1_button.update()
        level_2_button.change_colour(pygame.mouse.get_pos())
        level_2_button.update()
        quit_button.change_colour(pygame.mouse.get_pos())
        quit_button.update()

        pygame.display.update()
        

main_menu()
# start again here
if game:
    # region game constants
    pygame.display.set_caption("Game")
    font = pygame.font.Font('freesansbold.ttf', 16)
    timer = pygame.time.Clock()
    fps = 30
    direction = 0
    direction_command = 0
    if level == level2:
        level_number = 2
    else:
        level_number = 1
    player_x = (WIDTH // 30) * (start_pos[level_number - 1][0]) - 13
    player_y = ((HEIGHT - 150) // 32) * start_pos[level_number - 1][1] - 12
    player_speed = 2
    moves_allowed = [False, False, False, False]  # Right, Left, Up ,Down
    time = 0
    win = False
    man_image = pygame.image.load("man.jpg")
    man_image = pygame.transform.scale(man_image, (49, 49))
    car_image = pygame.image.load("car.jpg")
    car_image = pygame.transform.scale(car_image, (49, 49))
    bike_image = pygame.image.load("bike.jpg")
    bike_image = pygame.transform.scale(bike_image, (49, 49))
    red_game_button_surface = pygame.transform.scale(button_image, (150, 80))
    man_button = Button(red_game_button_surface, (WIDTH // 6 - 50), 870, "man", 3)
    bike_button = Button(red_game_button_surface, (WIDTH // 3 - 50), 870, "bike", 4)
    car_button = Button(red_game_button_surface, (WIDTH // 6 * 3 - 50), 870, "car", 5)
    # endregion

# region game functions
    def draw_map():
        num1 = ((HEIGHT - 150) // 32)
        num2 = (WIDTH // 30)
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == 0:
                    pygame.draw.circle(screen, 'green', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
                if level[i][j] == 1:
                    pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 4)
                if level[i][j] == 2:
                    pygame.draw.circle(screen, 'red', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 4)
                if level[i][j] == 3:
                    pygame.draw.circle(screen, 'blue', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 4)
                if level[i][j] == 4:
                    pygame.draw.circle(screen, 'yellow', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 4)
                if level[i][j] == 5:
                    pygame.draw.circle(screen, 'orange', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 4)
                if level[i][j] == 8:
                    pygame.draw.circle(screen, 'red', (j * num2 + (0.5*num2), i * num1 + (0.5 * num1)), 10)


    def draw_player():
        if vehicle == 1:
            player_image = bike_image
        elif vehicle == 2:
            player_image = car_image
        else:
            player_image = man_image
        # 0-RIGHT, 1, LEFT, 2-UP, 3-DOWN
        if direction == 0:
            screen.blit(player_image, (player_x, player_y))
        elif direction == 1:
            screen.blit(pygame.transform.flip(player_image, True, False), (player_x, player_y))
        elif direction == 2:
            screen.blit(pygame.transform.rotate(player_image, 90), (player_x, player_y))
        elif direction == 3:
            screen.blit(pygame.transform.rotate(player_image, 270), (player_x, player_y))


    def check_position(centerx, centery):  # 1 tile width is currently 30 and height is 25
        global player_speed, win
        turns = [False, False, False, False]
        num1 = (HEIGHT - 150) // 32
        num2 = (WIDTH // 30)
        num3 = 15  # eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        # check collisions based on center x and center y pos of player +- range of error
        if vehicle == 0:
            player_speed = 1
        if vehicle == 1:  # bike
            if level[centery // num1][centerx // num2] in (0, 1, 2, 3):
                player_speed = 3
            else:
                player_speed = 2
        if vehicle == 2:  # car
            if level[centery // num1][centerx // num2] == 3:
                player_speed = 4
            else:
                player_speed = 1
        # checking the player can turn directly behind
        if direction == 0:  # check tile left
            if vehicle == 2:
                if 2 <= level[centery // num1][(centerx - num3) // num2] <= 8:
                    turns[1] = True
            else:
                if level[centery // num1][(centerx - num3) // num2] <= 8:
                    turns[1] = True
        if direction == 1:  # check tile right
            if vehicle == 2:
                if 2 <= level[centery // num1][(centerx - num3) // num2] <= 8:
                    turns[0] = True
            else:
                if level[centery // num1][(centerx + num3) // num2] <= 8:
                    turns[0] = True
        if direction == 2:  # check tile below
            if vehicle == 2:
                if 2 <= level[centery // num1][(centerx - num3) // num2] <= 8:
                    turns[3] = True
            else:
                if level[(centery + num3) // num1][(centerx - num3) // num2] <= 8:
                    turns[3] = True
        if direction == 3:  # check tile above
            if vehicle == 2:
                if 2 <= level[centery // num1][(centerx - num3) // num2] <= 8:
                    turns[2] = True
            else:
                if level[(centery - num3) // num1][centerx // num2] <= 8:
                    turns[2] = True

        if direction == 2 or direction == 3:  # if going up or down
            if 12 <= centerx % num2 <= 18:  # divides position by tile width, give remainder, check player in middle
                if vehicle == 2:
                    if 2 <= level[(centery + num3) // num1][centerx // num2] <= 8:  # checks if down is free tile
                        turns[3] = True  # can turn downward
                    if 2 <= level[(centery - num3) // num1][centerx // num2] <= 8:  # checks if up is free tile
                        turns[2] = True  # can turn upward
                else:
                    if level[(centery + num3) // num1][centerx // num2] <= 8:  # checks if down is free tile
                        turns[3] = True  # can turn downward
                    if level[(centery - num3) // num1][centerx // num2] <= 8:  # checks if up is free tile
                        turns[2] = True  # can turn upward

            if 12 <= centery % num1 <= 18:  # divides position by tile width, give remainder, check player in middle
                if vehicle == 2:
                    if 2 <= level[centery // num1][(centerx - num2) // num2] <= 8:  # checks if left is free tile
                        turns[1] = True  # can turn left
                    if 2 <= level[centery // num1][(centerx + num2) // num2] <= 8:  # checks if right is free tile
                        turns[0] = True  # can turn right
                else:
                    if level[centery // num1][(centerx - num2) // num2] <= 8:  # checks if left is free tile
                        turns[1] = True  # can turn left
                    if level[centery // num1][(centerx + num2) // num2] <= 8:  # checks if right is free tile
                        turns[0] = True  # can turn right

        if direction == 0 or direction == 1:  # if going right or left
            if 12 <= centerx % num2 <= 18:  # divides position by tile width, give remainder, check player in middle
                if vehicle == 2:
                    if 2 <= level[(centery + num1) // num1][centerx // num2] <= 8:  # checks if down is free tile
                        turns[3] = True  # can turn downward
                    if 2 <= level[(centery - num1) // num1][centerx // num2] <= 8:  # checks if up is free tile
                        turns[2] = True  # can turn upward
                else:
                    if level[(centery + num1) // num1][centerx // num2] <= 8:  # checks if down is free tile
                        turns[3] = True  # can turn downward
                    if level[(centery - num1) // num1][centerx // num2] <= 8:  # checks if up is free tile
                        turns[2] = True  # can turn upward

            if 12 <= centery % num1 <= 18:  # divides position by tile width, give remainder, check player in middle
                if vehicle == 2:
                    if 2 <= level[centery // num1][(centerx - num3) // num2] <= 8:  # checks if left is free tile
                        turns[1] = True  # can turn left
                    if 2 <= level[centery // num1][(centerx + num3) // num2] <= 8:  # checks if right is free tile
                        turns[0] = True  # can turn right
                else:
                    if level[centery // num1][(centerx - num3) // num2] <= 8:  # checks if left is free tile
                        turns[1] = True  # can turn left
                    if level[centery // num1][(centerx + num3) // num2] <= 8:  # checks if right is free tile
                        turns[0] = True  # can turn right
        if (level[centery // num1][centerx // num2] == 8) or win:
            win = True
            turns = [False, False, False, False]

        return turns


    def move_player(play_x, play_y):
        # 0-RIGHT, 1, LEFT, 2-UP, 3-DOWN
        if direction == 0 and moves_allowed[0]:
            play_x += player_speed
        elif direction == 1 and moves_allowed[1]:
            play_x -= player_speed
        if direction == 2 and moves_allowed[2]:
            play_y -= player_speed
        elif direction == 3 and moves_allowed[3]:
            play_y += player_speed
        return play_x, play_y
#  endregion

    run = True
    while run:
        timer.tick(fps)
        if not win:
            time += 0.1
        screen.fill('black')
        draw_map()
        draw_player()
        if win:
            menu_screen_button_surface = pygame.transform.scale(button_image, (300, 110))
            main_menu_button = Button(menu_screen_button_surface, (WIDTH // 2), 500, "MENU", 0)
            main_menu_button.change_colour(pygame.mouse.get_pos())
            main_menu_button.update()
        center_x = player_x + 24
        center_y = player_y + 24
        pygame.draw.circle(screen, (128, 0, 32), (center_x, center_y), 2)  # for checking the center of player for tests
        moves_allowed = check_position(center_x, center_y)
        player_x, player_y = move_player(player_x, player_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #  change the direction of the player
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    vehicle = 0
                if event.key == pygame.K_2:
                    vehicle = 1
                if event.key == pygame.K_3:
                    vehicle = 2
                if event.key == pygame.K_RIGHT:
                    direction_command = 0
                if event.key == pygame.K_LEFT:
                    direction_command = 1
                if event.key == pygame.K_UP:
                    direction_command = 2
                if event.key == pygame.K_DOWN:
                    direction_command = 3
            if event.type == pygame.KEYUP:
                # keeps the player facing the same way when a key is let go
                if event.key == pygame.K_RIGHT and direction_command == 0:  # checks the player is moving right
                    direction_command = direction
                if event.key == pygame.K_LEFT and direction_command == 1:  # checks the player is moving left
                    direction_command = direction
                if event.key == pygame.K_UP and direction_command == 2:  # checks the player is moving up
                    direction_command = direction
                if event.key == pygame.K_DOWN and direction_command == 3:  # checks the player is moving down
                    direction_command = direction
            if event.type == pygame.MOUSEBUTTONDOWN:
                man_button.check_for_input(pygame.mouse.get_pos(), 3)
                bike_button.check_for_input(pygame.mouse.get_pos(), 4)
                car_button.check_for_input(pygame.mouse.get_pos(), 5)
                if win:
                    main_menu_button.check_for_input(pygame.mouse.get_pos(), 6)

        for i in range(4):  # loops through the 4 allowed directions
            if direction_command == i and moves_allowed[i]:
                direction = i

        man_button.change_colour(pygame.mouse.get_pos())
        man_button.update()
        bike_button.change_colour(pygame.mouse.get_pos())
        bike_button.update()
        car_button.change_colour(pygame.mouse.get_pos())
        car_button.update()
        score_text = font.render(('Score: ' + str(math.floor(100 - time))), True, 'white', 'black')
        screen.blit(score_text, ((WIDTH / 2 - 50), (HEIGHT - 30)))

        pygame.display.flip()

pygame.quit()
