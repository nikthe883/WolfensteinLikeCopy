import pygame as pg


class Button:
    def __init__(self, surface, path, scale, transform_scale_hover, option=False, action_lock=False):
        """Button clas takes as parameter the surface on which it is drawn, path to image, scale of the image,
        transform scale when hover. You can make the scale and the transform_scale_hover the same if you don't want
        to have hover effect.
        Optional parameters: option  - If True when mouse click image takes the transform_scale scale
        action_lock - Locks the button to return True"""
        self.surface = surface
        self.action_lock = action_lock
        self.transform_scale_hover = transform_scale_hover
        self.option = option
        self.scale = scale
        self.image_load = pg.image.load(path).convert_alpha()
        self.width = self.image_load.get_width()
        self.height = self.image_load.get_height()
        self.image = pg.transform.scale(self.image_load, (int(self.width * self.scale), int(self.height * self.scale)))
        self.rect = self.image.get_rect()
        self.clicked = False

    def draw(self, x, y):
        """Drawing function of the button. Placing the rect on the coordinates.
        Takes as arguments x and y which are the positions"""
        pos = pg.mouse.get_pos()
        self.rect.topleft = (x, y)

        if self.rect.collidepoint(pos):
            self.image = pg.transform.scale(self.image_load, (int(self.width * self.transform_scale_hover), int(self.height * self.transform_scale_hover)))
            self.surface.blit(self.image, (self.rect.x, self.rect.y))
        elif not self.option:
            self.image = pg.transform.scale(self.image_load, (int(self.width * self.scale), int(self.height * self.scale)))
            self.surface.blit(self.image, (self.rect.x, self.rect.y))

        if self.option:
            self.image = pg.transform.scale(self.image_load, (int(self.width * self.transform_scale_hover), int(self.height * self.transform_scale_hover)))
            self.surface.blit(self.image, (self.rect.x, self.rect.y))

    def action(self):
        """Function that returns True if button is clicked. If action_lock - it always return true"""

        action = False

        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.action_lock:
            return False
        return action

    @property
    def get_size(self):
        return self.width, self.height


class Slider:

    def __init__(self, surface, pos_x, pos_y, saving=False, value=None):
        """Slider class. Take as parameters the surface, pos_x and pos_y on the screen
        Optional parameters: saving - this when you save the game the slider to return to the same possition
        value - again used for saving the slider - the value is taken from the saved settings."""
        self.saving = saving
        self.value = value
        self.surface = surface
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.mouse_pos = None
        self.slider = pg.image.load('resources/menu/slider/slider.bmp').convert_alpha()
        self.slider_base = pg.image.load('resources/menu/slider/slider_base.bmp').convert_alpha()
        # If saving is True we are calculating the position of the slider based on the value that is given.
        if self.saving:
            self.slider_pos = int(self.value * 2.8 + self.pos_x + self.slider.get_width() * 1.5)
        else:
            self.slider_pos = self.pos_x + self.slider.get_width() * 1.5

        self.min_value = self.pos_x + self.slider.get_width() * 1.5
        self.max_value = self.pos_x + self.slider_base.get_width() - self.slider.get_width() * 2
        self.one_value = (self.max_value - self.min_value) / 100

    def update(self):
        """Update function for the slider to check the mouse position"""
        button = pg.mouse.get_pressed()
        if button[0] != 0:
            self.mouse_pos = pg.mouse.get_pos()

    def draw(self):
        """Drawing function of the slicer"""
        self.surface.blit(self.slider_base, (self.pos_x, self.pos_y))
        slider_rect = self.slider.get_rect()
        if self.pos_x + self.slider.get_width() * 1.5 < self.mouse_pos[0] < self.pos_x + self.slider_base.get_width() - self.slider.get_width() * 2 and \
                self.pos_y < self.mouse_pos[1] < self.pos_y + self.slider_base.get_height():

            slider_rect.move_ip(self.mouse_pos[0], self.pos_y + self.slider.get_height() / 2.5)
            self.surface.blit(self.slider, slider_rect)
            self.slider_pos = slider_rect.x

        else:
            self.surface.blit(self.slider, (self.slider_pos, self.pos_y + self.slider.get_height() // 2.5))

    @property
    def get_slider_value(self):
        """Calculates the slide bar position in percentage"""
        number = int((self.slider_pos - self.min_value) // self.one_value)
        return number if number > 0 else 0

    @property
    def get_position(self):
        """Returns the possition of the slider"""
        return self.pos_x, self.pos_y
