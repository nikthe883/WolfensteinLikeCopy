import pygame as pg


class Button:
    """
    Button class

    Class that makes easy placement of buttons on the screen. Build specifically for the menu.
    """
    def __init__(self, surface, path, scale, transform_scale_hover, option=False, action_lock=False):
        """
        Init function of Button class

        :param surface: Pygame surface object
        :type surface: object
        :param path: Path to the image
        :type path: str
        :param scale: Scale of the image
        :type scale: float
        :param transform_scale_hover: Hover scale of image
        :type transform_scale_hover: float
        :param option: If this is and option button
        :type option: bool
        :param action_lock: To lock the return to True
        :type action_lock: bool
        """

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
        """
        Drawing function of the button.

        Placing the rect on the coordinates.
        Takes as arguments x and y which are the positions

        :param x: x position on the scree
        :type x: float
        :param y: y position on the screen
        :type y: float
        :return: None
        :rtype: None
        """
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
        """
        Action function of class button

        It that returns True if button is clicked. If action_lock - it always return true

        :return: True or False
        :rtype: bool
        """

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
    """
    Slider class

    Slider class that makes easy placing the sliders on the menu.
    """

    def __init__(self, surface, pos_x, pos_y, saving=False, value=None):
        """
        Function init of slider class

        :param surface: Pygame surface object
        :type surface: object
        :param pos_x: x position on the screen
        :type pos_x: float
        :param pos_y: y position on the screen
        :type pos_y: float
        :param saving: Optional parameter for loading the slider position
        :type saving: bool
        :param value: Optional parameter for loading. Takes the loaded value
        :type value: float
        """

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
        """
        Update function for the slider to check the mouse position

        :return: None
        :rtype: None
        """

        button = pg.mouse.get_pressed()
        if button[0] != 0:
            self.mouse_pos = pg.mouse.get_pos()

    def draw(self):
        """
        Drawing function of the slider

        :return: None
        :rtype: None
        """

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
        """
        Property method of class Slider for getting the value of the slider.

        Calculates the sliders value. If the number is negative returns 0.
        Used to determine the option value eg : mouse sensitivity, volume, screen resolution.

        :return: number - slide position on the screen
        :rtype: int
        """

        number = int((self.slider_pos - self.min_value) // self.one_value)
        return number if number > 0 else 0

    @property
    def get_position(self):
        """
        Property method of class slider for getting the position of the slider

        :return: x and y position of slider
        :rtype: tuple
        """
        return self.pos_x, self.pos_y
