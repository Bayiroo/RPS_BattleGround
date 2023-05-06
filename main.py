import pygame as mygame
from sys import exit

import pygame.transform

import main
from Button import Button
from Entity import Entity
from SlideBar import SlideBar

mygame.init()

# Game Valuables
screenWidht, screenHeight = 1920, 1080
screen_size = [screenWidht, screenHeight]
thick_rate = 60
item_amount = 5
object_speed = 1
object_size = (35, 35)
menu_object_size = (100, 100)
chase_speed_multiplier = 1
escape_speed_multiplier = 1
game_phase = "start"

# Game Window
gameWindow = mygame.display.set_mode((screenWidht, screenHeight))
mygame.display.set_caption("RPS Battle Simulation")
clock = mygame.time.Clock()

# SURFACES
background_surface = mygame.Surface((screenWidht, screenHeight))
background_surface.fill(color="grey")

rock_surface = mygame.image.load("graphics/the rock original.gif")
rock_surface = pygame.transform.scale(rock_surface, menu_object_size)

paper_surface = mygame.image.load("graphics/paper no backgorund.png")
paper_surface = pygame.transform.scale(paper_surface, menu_object_size)

scissor_surface = mygame.image.load("graphics/scissor no backgorund.png")
scissor_surface = pygame.transform.scale(scissor_surface, menu_object_size)

endgame_background_surface = mygame.Surface((screenWidht, screenHeight))
endgame_background_surface.fill(color="purple")

game_notice_text = ""
game_notice_font = mygame.font.Font("Foonts\DejaVuSerif-BoldItalic.ttf", 25)

start_button_text = "START SIMULATION"
exit_button_text = "EXIT"
reset_bar_button_text = "Reset"
button_font = mygame.font.Font("Foonts\DejaVuSerif-BoldItalic.ttf", 25)

# Create instances
rock_group = mygame.sprite.Group()
paper_group = mygame.sprite.Group()
scissor_group = mygame.sprite.Group()

# Buttons
start_button = Button(x=screenWidht / 2, y=screenHeight / 10 * 7
                      , text_input=start_button_text
                      , base_color='blue'
                      , hovering_color='red'
                      , background_color='white'
                      , screen_surface=gameWindow)
exit_button = Button(x=screenWidht / 2, y=screenHeight / 10 * 8
                     , text_input=exit_button_text
                     , base_color='red'
                     , hovering_color='black'
                     , background_color='white'
                     , screen_surface=gameWindow)

reset_bar_button = Button(x=screenWidht / 10 * 9, y=screenHeight / 10 * 4
                          , text_input=reset_bar_button_text
                          , base_color='red'
                          , hovering_color='black'
                          , background_color='white'
                          , screen_surface=gameWindow)

chase_speed_multiplier_bar = SlideBar(screenWidht / 10 * 9, screenHeight / 10 * 1
                                      , 'Chase Speed'
                                      , 'green'
                                      , 'white'
                                      , screen_size
                                      , gameWindow)

escape_speed_multiplier_bar = SlideBar(screenWidht / 10 * 9, screenHeight / 10 * 3
                                       , 'Escape Speed'
                                       , 'red'
                                       , 'white'
                                       , screen_size
                                       , gameWindow)


def check_collision(sprite, target_group):
    return mygame.sprite.spritecollide(sprite, target_group, True)


def set_game_properties():
    for i in range(item_amount):
        rock_group.add(Entity('Rock', screenWidht, screenHeight, object_size, 1))
        paper_group.add(Entity('Paper', screenWidht, screenHeight, object_size, 1))
        scissor_group.add(Entity('Scissor', screenWidht, screenHeight, object_size, 1))


# game phases

def game_phase_end():
    global game_notice_image
    gameWindow.blit(endgame_background_surface, (0, 0))
    game_notice_image = game_notice_font.render(game_notice_text, 0, "red")
    game_notice_rect = game_notice_image.get_rect(center=(screenWidht / 2, screenHeight / 10 * 5))

    chase_speed_multiplier_bar.update()
    escape_speed_multiplier_bar.update()

    start_button.update()
    reset_bar_button.update()
    exit_button.update()

    if start_button.isclicked():
        set_game_properties()
        main.game_phase = "running"

    if exit_button.isclicked():
        mygame.quit()
        exit()

    gameWindow.blit(game_notice_image, game_notice_rect)
    # gameWindow.blit(start_game, (screenWidht / 3, screenHeight / 4 * 3))


def game_phase_start():
    gameWindow.blit(background_surface, (0, 0))
    chase_speed_multiplier_bar.update()
    escape_speed_multiplier_bar.update()
    start_button.update()
    reset_bar_button.update()
    exit_button.update()

    if start_button.isclicked():
        set_game_properties()
        main.game_phase = "running"

    if exit_button.isclicked():
        mygame.quit()
        exit()

    gameWindow.blit(rock_surface, (screenWidht / 6 * 2, screenHeight / 4 * 2))
    gameWindow.blit(paper_surface, (screenWidht / 6 * 3, screenHeight / 4 * 2))
    gameWindow.blit(scissor_surface, (screenWidht / 6 * 4, screenHeight / 4 * 2))


def game_phase_paused():
    global game_notice_text

    gameWindow.blit(background_surface, (0, 0))
    reset_bar_button.update()
    rock_group.draw(gameWindow)
    paper_group.draw(gameWindow)
    scissor_group.draw(gameWindow)

    game_notice_text = "PAUSED"

    game_notice_image = game_notice_font.render(game_notice_text, 0, "red")
    chase_speed_multiplier_bar.update()
    escape_speed_multiplier_bar.update()
    gameWindow.blit(game_notice_image, (screenWidht / 2, screenHeight / 2))


def game_phase_running():
    global game_notice_text

    gameWindow.blit(background_surface, (0, 0))
    rock_group.draw(gameWindow)
    paper_group.draw(gameWindow)
    scissor_group.draw(gameWindow)
    reset_bar_button.update()
    chase_speed_multiplier = chase_speed_multiplier_bar.update()
    escape_speed_multiplier = escape_speed_multiplier_bar.update()

    if len(rock_group) != 0:
        for i in rock_group:
            i.move(scissor_group, paper_group, chase_speed_multiplier, escape_speed_multiplier)
            for each in check_collision(i, scissor_group):
                pass
                # rock_group.add(Entity('Rock', each.rect.x, each.rect.y, object_size, 0))

    if len(paper_group) != 0:
        for i in paper_group:
            i.move(rock_group, scissor_group, chase_speed_multiplier, escape_speed_multiplier)
            for each in check_collision(i, rock_group):
                pass
                # paper_group.add(Entity('Paper', each.rect.x, each.rect.y, object_size, 0))

    if len(scissor_group) != 0:
        for i in scissor_group:
            i.move(paper_group, rock_group, chase_speed_multiplier, escape_speed_multiplier)
            for each in check_collision(i, paper_group):
                pass
                # scissor_group.add(Entity('Scissor', each.rect.x, each.rect.y, object_size, 0))

    if len(rock_group) == 0 and len(paper_group) == 0:
        main.game_phase = "end"
        game_notice_text = "SCISSOR is the WINNER"
    if len(rock_group) == 0 and len(scissor_group) == 0:
        main.game_phase = "end"
        game_notice_text = "PAPER is the WINNER"
    if len(scissor_group) == 0 and len(paper_group) == 0:
        main.game_phase = "end"
        game_notice_text = "THE ROCK is the WINNER"
    # print(len(rock_group), "---", len(paper_group), "---", len(scissor_group))


def game_phase_running_add_random():
    global game_notice_text
    gameWindow.blit(background_surface, (0, 0))
    rock_group.draw(gameWindow)
    paper_group.draw(gameWindow)
    scissor_group.draw(gameWindow)

    chase_speed_multiplier = chase_speed_multiplier_bar.update()
    escape_speed_multiplier = escape_speed_multiplier_bar.update()

    if len(rock_group) != 0:
        for i in rock_group:
            i.move(scissor_group, paper_group, chase_speed_multiplier, escape_speed_multiplier)
            for each in check_collision(i, scissor_group):
                rock_group.add(Entity('Rock', screenWidht, screenHeight, object_size, 1))

    if len(paper_group) != 0:
        for i in paper_group:
            i.move(rock_group, scissor_group, chase_speed_multiplier, escape_speed_multiplier)
            for each in check_collision(i, rock_group):
                paper_group.add(Entity('Paper', screenWidht, screenHeight, object_size, 1))

    if len(scissor_group) != 0:
        for i in scissor_group:
            i.move(paper_group, rock_group, chase_speed_multiplier, escape_speed_multiplier)
            for each in check_collision(i, paper_group):
                scissor_group.add(Entity('Scissor', screenWidht, screenHeight, object_size, 1))

    if len(rock_group) == 0 and len(paper_group) == 0:
        main.game_phase = "end"
        game_notice_text = "SCISSOR is the WINNER"
    if len(rock_group) == 0 and len(scissor_group) == 0:
        main.game_phase = "end"
        game_notice_text = "PAPER is the WINNER"
    if len(scissor_group) == 0 and len(paper_group) == 0:
        main.game_phase = "end"
        game_notice_text = "THE ROCK is the WINNER"
    print(len(rock_group), "---", len(paper_group), "---", len(scissor_group))


while True:

    for event in mygame.event.get():
        if event.type == mygame.QUIT:
            mygame.quit()
            exit()

        if pygame.mouse.get_pressed()[2]:  # 2 means right mouse button
            if game_phase == "running":
                game_phase = "paused"
            elif game_phase == "paused":
                game_phase = "running"

    if reset_bar_button.isclicked():
        chase_speed_multiplier_bar.reset()
        escape_speed_multiplier_bar.reset()

    if game_phase == "running":

        game_phase_running()

    elif game_phase == "paused":
        game_phase_paused()

    elif game_phase == "start":
        game_phase_start()

    elif game_phase == "end":
        game_phase_end()

    mygame.display.update()
    clock.tick(thick_rate)
