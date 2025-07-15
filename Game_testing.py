import pygame
import math
from Y13_game_map import start_pos, level1, level2, level3
level = level1
pygame.init()  # initialisation of pygame
WIDTH = 720
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # create the game screen to play on
pygame.display.set_caption("Menu")
main_font = pygame.font.SysFont("cambria", 47)
button_image = pygame.image.load('images/button.png')
working = True
menu = True
top_score = [9999, 9999, 9999]


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

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            if self.function == 0:
                global working
                working = False
                pygame.quit()
                exit()
            else:
                global menu, level, vehicle, run, go
                if self.function in (1, 2, 11):  # functions that cause a level to begin
                    menu = False
                if self.function == 1:  # level1
                    level = level1
                    vehicle = 0
                elif self.function == 2:  # level2
                    level = level2
                    vehicle = 0
                elif self.function == 11:  # level3
                    level = level3
                    vehicle = 0
                elif self.function == 3:  # change to man
                    change_vehicle(center_x, center_y, vehicle, 0)
                elif self.function == 4:  # change to bike
                    change_vehicle(center_x, center_y, vehicle, 1)
                elif self.function == 5:  # change to car
                    change_vehicle(center_x, center_y, vehicle, 2)
                elif self.function == 6:  # menu
                    run = False
                    menu = True
                    menu_screen.run()
                elif self.function == 7:
                    go = True

    def change_colour(self, position):  # changes the colour of the button when hovering over
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "white")


def display_text(text, position, font, color):
    collection = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # finds the width of a " " to add at the end of a word
    x, y = position
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)  # renders the word onto the screen
            word_width, word_height = word_surface.get_size()
            if x + word_width >= (WIDTH // 4 + 240):
                x = position[0]  # resets the line to the left hand side of the text box when at the end of a line
                y += word_height
            screen.blit(word_surface, (x, y))
            x += (word_width + space)
        x = position[0]  # starts the line on the left hand side of the text box
        y += word_height


class Menu:
    def __init__(self, button_image_, top_score_):
        self.button_image = pygame.transform.scale(button_image_, (250, 90))
        self.menu_font = pygame.font.Font('freesansbold.ttf', 16)
        self.title_font = pygame.font.Font('freesansbold.ttf', 50)
        self.office_image = pygame.transform.scale(pygame.image.load("images/office1.png"), (240, 180))
        self.top_score = top_score_
        self.level_1_button = Button(self.button_image, (WIDTH // 5), 100, "Level 1!", 1)
        self.level_2_button = Button(self.button_image, ((WIDTH // 5) * 4), 100, "Level 2!", 2)
        self.level_3_button = Button(self.button_image, ((WIDTH // 5) * 4), 320, "Level 3!", 11)
        self.quit_button = Button(self.button_image, (WIDTH // 2), 550, "QUIT", 0)

    def draw(self):
        screen.fill('black')

        # draw the title
        title1 = self.title_font.render('Work ', True, 'white', 'black')
        title2 = self.title_font.render('Rush!', True, 'white', 'black')
        title1.set_alpha(240)  # make the title partially transparent
        title2.set_alpha(240)
        screen.blit(self.office_image, (WIDTH // 2 - 120, 30))  # draw the office image
        screen.blit(title1, ((WIDTH // 2 - 68), 60))  # draw the title
        screen.blit(title2, ((WIDTH // 2 - 70), 110))
        screen.blit(self.draw_score(0), ((WIDTH // 5 - 70), 170))  # draw the scores
        screen.blit(self.draw_score(1), (((WIDTH // 5) * 4 - 70), 170))
        screen.blit(self.draw_score(2), (((WIDTH // 5) * 4 - 70), 390))
        # display the text that describes how to play
        display_text(
            "Goal:\nWalk to the circled office in the shortest time, you start moving after you "
            "press 'GO'\n\nControls:\nArrow keys control movement\n\nYou can select your vehicle by using the "
            "buttons on-screen.\n\nYou may switch to a bike or car when at home (your start position)\n\n you must be "
            "walking or biking when reaching work and you must park in a parking zone if using a car. Pause using 'e' "
            "or space.",
            ((WIDTH // 4 - 110), 230), self.menu_font, 'white')

        self.level_1_button.change_colour(pygame.mouse.get_pos())
        self.level_1_button.update()
        self.level_2_button.change_colour(pygame.mouse.get_pos())
        self.level_2_button.update()
        self.level_3_button.change_colour(pygame.mouse.get_pos())
        self.level_3_button.update()
        self.quit_button.change_colour(pygame.mouse.get_pos())
        self.quit_button.update()

    def draw_score(self, index):
        if self.top_score[index] < 9999:
            return self.menu_font.render("Best time: " + str(math.floor(self.top_score[index])) + " seconds", True,
                                         'white', 'black')
        else:
            return self.menu_font.render("Best time: None", True, 'white', 'black')

    def run(self):
        pygame.display.set_caption("Menu")
        global menu
        while menu:
            for _event in pygame.event.get():
                if _event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif _event.type == pygame.MOUSEBUTTONDOWN:
                    self.level_1_button.check_for_input(pygame.mouse.get_pos())
                    self.level_2_button.check_for_input(pygame.mouse.get_pos())
                    self.level_3_button.check_for_input(pygame.mouse.get_pos())
                    self.quit_button.check_for_input(pygame.mouse.get_pos())
            self.draw()
            pygame.display.update()


menu_screen = Menu(button_image, top_score)
while working:
    menu_screen.run()
    # region game constants
    pygame.display.set_caption("Game")  # sets the title of the window to 'game'
    score_font = pygame.font.Font('freesansbold.ttf', 16)
    timer = pygame.time.Clock()
    fps = 25
    vehicle = 0  # defaults the vehicle to a man
    direction = 0  # defaults the starting direction to right
    direction_command = 0  # defaults the starting direction command to right
    if level == level2:
        level_number = 2
    elif level == level3:
        level_number = 3
    else:
        level_number = 1
    player_x = (WIDTH // 24) * (start_pos[level_number - 1][0]) - 13
    player_y = ((HEIGHT - 150) // 18) * (start_pos[level_number - 1][1]) - 12
    player_speed = 2
    moves_allowed = [False, False, False, False]  # Right, Left, Up ,Down
    time = 0
    win = False
    go = False
    change_allowed = [False, False, False]
    tile_height = ((HEIGHT - 150) // 18)
    tile_width = (WIDTH // 24)
    man_image = pygame.image.load("images/man.png")
    man_image = pygame.transform.scale(man_image, (49, 49))
    car_image = pygame.image.load("images/car.png")
    car_image = pygame.transform.scale(car_image, (49, 49))
    bike_image = pygame.image.load("images/bike.png")
    bike_image = pygame.transform.scale(bike_image, (49, 49))
    red_game_button_surface = pygame.transform.scale(button_image, (120, 80))
    man_button = Button(red_game_button_surface, (WIDTH // 6 - 50), 500, "man", 3)
    bike_button = Button(red_game_button_surface, (WIDTH // 3 - 50), 500, "bike", 4)
    car_button = Button(red_game_button_surface, (WIDTH // 6 * 3 - 50), 500, "car", 5)
    go_button = Button(red_game_button_surface, (WIDTH // 4 * 3), 500, "GO", 7)
    basic_road_x_image = pygame.image.load("images/basic_road_x.png")
    basic_road_y_image = pygame.image.load("images/basic_road_y.png")
    basic_road_xy_image = pygame.image.load("images/basic_road_xy.png")
    bike_road_x_image = pygame.image.load("images/bike_road_x.png")
    bike_road_y_image = pygame.image.load("images/bike_road_y.png")
    bike_road_xy_image = pygame.image.load("images/bike_road_xy.png")
    office_image = pygame.image.load("images/office1.png")
    house_image = pygame.image.load("images/house.png")
    parking_image = pygame.transform.scale(pygame.image.load("images/parking.png"), (30, 30))
    menu_screen_button_surface = pygame.transform.scale(button_image, (300, 110))
    main_menu_button = Button(menu_screen_button_surface, (WIDTH // 2), 400, "MENU", 6)

    # endregion

    # region game functions
    def draw_map(num1, num2):
        # 1 tile width is currently 30 and height is 25
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == 0:
                    screen.blit(basic_road_x_image, (j * num2, i * num1))
                if level[i][j] == 1:
                    screen.blit(basic_road_y_image, (j * num2, i * num1))
                if level[i][j] == 2:
                    screen.blit(basic_road_xy_image, (j * num2, i * num1))
                if level[i][j] == 3:
                    screen.blit(bike_road_x_image, (j * num2, i * num1))
                if level[i][j] == 4:
                    screen.blit(bike_road_y_image, (j * num2, i * num1))
                if level[i][j] == 5:
                    screen.blit(bike_road_xy_image, (j * num2, i * num1))
                if level[i][j] == 6:
                    screen.blit(parking_image, (j * num2, i * num1))
                if level[i][j] == 7:
                    screen.blit(house_image, (j * num2, i * num1))
                if level[i][j] == 8:
                    screen.blit(office_image, (j * num2, i * num1))
                    pygame.draw.circle(screen, 'red', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 16, 3)
                if level[i][j] == 9:
                    screen.blit(office_image, (j * num2, i * num1))


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


    def check_position(centerx, centery, time_value):  # 1 tile width is currently 30 and height is 25
        global player_speed, win
        turns = [False, False, False, False]
        num1 = (HEIGHT - 150) // 18
        num2 = (WIDTH // 24)
        num3 = 14
        # check collisions based on center x and center y pos of player +- range of error
        allowed_surfaces = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        if vehicle == 0:
            player_speed = 1
        if vehicle == 1:  # bike
            allowed_surfaces = (0, 1, 2, 3, 4, 5, 6, 7, 8)
            if (level[centery // num1][centerx // num2] == 2) and (8 <= (math.floor(time_value) % 10) <= 10):
                player_speed = 0
            elif level[centery // num1][centerx // num2] in (0, 1, 3, 4):
                player_speed = 3
            else:
                player_speed = 2
        if vehicle == 2:  # car
            allowed_surfaces = (0, 1, 2, 3, 4, 5, 6, 7)
            if level[centery // num1][centerx // num2] in (0, 1, 2):
                player_speed = 4
                if (level[centery // num1][centerx // num2] == 2) and (8 <= (math.floor(time_value) % 10) <= 10):
                    player_speed = 0
            else:
                player_speed = 1
                if (level[centery // num1][centerx // num2] == 5) and (8 <= (math.floor(time_value) % 10) <= 10):
                    player_speed = 0
        # checking the player can turn directly behind
        if direction == 0:  # check tile left
            if level[centery // num1][(centerx - num3) // num2] in allowed_surfaces:
                turns[1] = True
        if direction == 1:  # check tile right
            if level[centery // num1][(centerx + num3) // num2] in allowed_surfaces:
                turns[0] = True
        if direction == 2:  # check tile below
            if level[(centery + num3) // num1][(centerx - num3) // num2] in allowed_surfaces:
                turns[3] = True
        if direction == 3:  # check tile above
            if level[(centery - num3) // num1][centerx // num2] in allowed_surfaces:
                turns[2] = True

        if direction == 2 or direction == 3:  # if going up or down
            if 11 <= centerx % num2 <= 19:  # divides position by tile width, give remainder, check player in middle
                if level[(centery + num3) // num1][centerx // num2] in allowed_surfaces:  # checks if down is free tile
                    turns[3] = True  # can turn downward
                if level[(centery - num3) // num1][centerx // num2] in allowed_surfaces:  # checks if up is free tile
                    turns[2] = True  # can turn upward
            if 11 <= centery % num1 <= 19:  # divides position by tile width, give remainder, check player in middle
                if level[centery // num1][(centerx - num2) // num2] in allowed_surfaces:  # checks if left is free tile
                    turns[1] = True  # can turn left
                if level[centery // num1][(centerx + num2) // num2] in allowed_surfaces:  # checks if right is free tile
                    turns[0] = True  # can turn right

        if direction == 0 or direction == 1:  # if going right or left
            if 11 <= centerx % num2 <= 19:  # divides position by tile width, give remainder, check player in middle
                if level[(centery + num1) // num1][centerx // num2] in allowed_surfaces:  # checks if down is free tile
                    turns[3] = True  # can turn downward
                if level[(centery - num1) // num1][centerx // num2] in allowed_surfaces:  # checks if up is free tile
                    turns[2] = True  # can turn upward

            if 11 <= centery % num1 <= 19:  # divides position by tile width, give remainder, check player in middle
                if level[centery // num1][(centerx - num3) // num2] in allowed_surfaces:  # checks if left is free tile
                    turns[1] = True  # can turn left
                if level[centery // num1][(centerx + num3) // num2] in allowed_surfaces:  # checks if right is free tile
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


    def change_vehicle(centerx, centery, current_vehicle, desired_vehicle):
        num1 = (HEIGHT - 150) // 18
        num2 = (WIDTH // 24)
        global vehicle
        if current_vehicle == desired_vehicle:
            vehicle = desired_vehicle
        else:
            if (current_vehicle == 1) and (desired_vehicle == 0):  # change from bike to man anywhere
                vehicle = desired_vehicle
            if level[centery // num1][centerx // num2] == 7:  # change while at home
                vehicle = desired_vehicle
                # change from car ->
            if (current_vehicle == 2) and (level[centery // num1][centerx // num2] == 6) and (desired_vehicle == 0):
                vehicle = desired_vehicle

    def check_change_vehicle(centerx, centery, current_vehicle):
        num1 = (HEIGHT - 150) // 18
        num2 = (WIDTH // 24)
        global change_allowed
        if level[centery // num1][centerx // num2] == 7:  # while at home
            change_allowed = [True, True, True]
        elif current_vehicle == 1:  # change from bike to man anywhere
            change_allowed = [True, True, False]
        elif current_vehicle == 2 and level[centery // num1][centerx // num2] == 6:  # change car to man in parking
            change_allowed = [True, False, True]
        else:
            change_allowed = [False, False, False]
        if current_vehicle == 0:
            change_allowed[0] = True
        if current_vehicle == 2:
            change_allowed[2] = True
        #  endregion

    run = True
    while run:
        timer.tick(fps)
        if go and not win:
            time += (1/25)
        screen.fill((130, 130, 130))
        draw_map(tile_height, tile_width)
        draw_player()
        if win:
            main_menu_button.change_colour(pygame.mouse.get_pos())
            main_menu_button.update()
            if top_score[level_number - 1] <= 9999:
                if top_score[level_number - 1] >= time:
                    top_score[level_number - 1] = time
        center_x = player_x + 24
        center_y = player_y + 24
        check_change_vehicle(center_x, center_y, vehicle)
        if go:
            moves_allowed = check_position(center_x, center_y, time)
            player_x, player_y = move_player(player_x, player_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # make the X in the to right of the game window function properly
                pygame.quit()
                #  change the direction of the player depending on which key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    direction_command = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    direction_command = 1
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    direction_command = 2
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    direction_command = 3
                if event.key == pygame.K_e or event.key == pygame.K_SPACE:  # pause button
                    go = False
                if event.key == pygame.K_ESCAPE:  # return to menu
                    run = False
                    menu = True
                    menu_screen.run()
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
            if event.type == pygame.MOUSEBUTTONDOWN:  # checking whether the player clicked a button
                if change_allowed[0]:
                    man_button.check_for_input(pygame.mouse.get_pos())
                if change_allowed[1]:
                    bike_button.check_for_input(pygame.mouse.get_pos())
                if change_allowed[2]:
                    car_button.check_for_input(pygame.mouse.get_pos())
                go_button.check_for_input(pygame.mouse.get_pos())
                if win:
                    main_menu_button.check_for_input(pygame.mouse.get_pos())

        for n in range(4):  # loops through the 4 allowed directions
            if direction_command == n and moves_allowed[n]:
                direction = n

        if change_allowed[0]:
            man_button.change_colour(pygame.mouse.get_pos())
            man_button.update()
        if change_allowed[1]:
            bike_button.change_colour(pygame.mouse.get_pos())
            bike_button.update()
        if change_allowed[2]:
            car_button.change_colour(pygame.mouse.get_pos())
            car_button.update()
        go_button.change_colour(pygame.mouse.get_pos())
        go_button.update()
        score_text = score_font.render(('Time: ' + str(math.floor(time)) + " seconds"), True, 'white', 'black')
        screen.blit(score_text, ((WIDTH // 2 - 50), (HEIGHT - 30)))  # adds the score text to the game screen

        pygame.display.flip()
    # endregion

pygame.quit()
