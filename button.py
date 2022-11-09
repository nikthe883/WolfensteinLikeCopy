import pygame as pg


class Button:
    def __init__(self, surface, path, scale, transform_scale_hover, option=False, action_lock=False):
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
        self.saving = saving
        self.value = value
        self.surface = surface
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.mouse_pos = None
        self.slider = pg.image.load('resources/menu/slider/slider.bmp').convert_alpha()
        self.slider_base = pg.image.load('resources/menu/slider/slider_base.bmp').convert_alpha()

        if self.saving:
            self.slider_pos = int(self.value * 2.8 + self.pos_x + self.slider.get_width() * 1.5)
        else:
            self.slider_pos = self.pos_x + self.slider.get_width() * 1.5

        self.min_value = self.pos_x + self.slider.get_width() * 1.5
        self.max_value = self.pos_x + self.slider_base.get_width() - self.slider.get_width() * 2
        self.one_value = (self.max_value - self.min_value) / 100


    def update(self):
        button = pg.mouse.get_pressed()
        if button[0] != 0:
            self.mouse_pos = pg.mouse.get_pos()


    def draw(self):
        self.surface.blit(self.slider_base, (self.pos_x, self.pos_y))
        slider_rect = self.slider.get_rect()
        if self.pos_x + self.slider.get_width() * 1.5 < self.mouse_pos[0] < self.pos_x + self.slider_base.get_width() - self.slider.get_width() * 2 and \
                self.pos_y < self.mouse_pos[1] < self.pos_y + self.slider_base.get_height():

            slider_rect.move_ip(self.mouse_pos[0] , self.pos_y + self.slider.get_height() / 2.5)
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
        return self.pos_x, self.pos_y
