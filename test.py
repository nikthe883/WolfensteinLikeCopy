import sys
import pygame as pg


pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
FONT = pg.font.Font(None, 40)

BG_COLOR = pg.Color('gray12')
GREEN = pg.Color('lightseagreen')


def create_key_list(input_map):
    """A list of surfaces of the action names + assigned keys, rects and the actions."""
    key_list = []
    for y, (action, value) in enumerate(input_map.items()):
        surf = FONT.render('{}: {}'.format(action, pg.key.name(value)), True, GREEN)
        rect = surf.get_rect(topleft=(40, y*40+20))
        key_list.append([surf, rect, action])
    return key_list


def assignment_menu(input_map):
    """Allow the user to change the key assignments in this menu.

    The user can click on an action-key pair to select it and has to press
    a keyboard key to assign it to the action in the `input_map` dict.
    """
    selected_action = None
    key_list = create_key_list(input_map)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if selected_action is not None:
                    # Assign the pygame key to the action in the input_map dict.
                    input_map[selected_action] = event.key
                    selected_action = None
                    # Need to re-render the surfaces.
                    key_list = create_key_list(input_map)
                if event.key == pg.K_ESCAPE:  # Leave the menu.
                    # Return the updated input_map dict to the main function.
                    return input_map
            elif event.type == pg.MOUSEBUTTONDOWN:
                selected_action = None
                for surf, rect, action in key_list:
                    # See if the user clicked on one of the rects.
                    if rect.collidepoint(event.pos):
                        selected_action = action

        screen.fill(BG_COLOR)
        # Blit the action-key table. Draw a rect around the
        # selected action.
        for surf, rect, action in key_list:
            screen.blit(surf, rect)
            if selected_action == action:
                pg.draw.rect(screen, GREEN, rect, 2)

        pg.display.flip()
        clock.tick(30)


def main():
    player = pg.Rect(300, 220, 40, 40)
    # This dict maps actions to the corresponding key scancodes.
    input_map = {'move right': pg.K_d, 'move left': pg.K_a}

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # Enter the key assignment menu.
                    input_map = assignment_menu(input_map)

        pressed_keys = pg.key.get_pressed()
        if pressed_keys[input_map['move right']]:
            player.x += 3
        elif pressed_keys[input_map['move left']]:
            player.x -= 3

        screen.fill(BG_COLOR)
        pg.draw.rect(screen, GREEN, player)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()