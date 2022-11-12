from sprite_object import *


class Shotgun(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        """
                Init method of class

                :param game: game instance
                :type game: self
                :param path: path to images
                :type path: str
                :param scale: scale of images
                :type scale: float
                :param animation_time: animation time
                :type animation_time: int
                """
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = SHOTGUN_DAMAGE

    def animate_shot(self):
        """
        Animation function

        :return: None
        :rtype: None
        """

        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        """
        Drawing function

        :return: None
        :rtype: None
        """

        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        """
        Updating function

        :return: None
        :rtype: None
        """
        self.check_animation_time()
        self.animate_shot()

# The other classes are basically the same

class Chainsaw(AnimatedSprite):
    """
    Class Chainsaw

    """
    def __init__(self, game, path='resources/sprites/weapon/chainsaw/0.png', scale=3, animation_time=90):
        """
                Init method of class

                :param game: game instance
                :type game: self
                :param path: path to images
                :type path: str
                :param scale: scale of images
                :type scale: float
                :param animation_time: animation time
                :type animation_time: int
                """
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.vroom_vroom = False
        self.num_images = len(self.images)
        self.first_image = self.images[0]
        self.frame_counter = 0
        self.damage = CHAINSAW_DAMAGE
        self.fuel_consumption = 1

    def animate_vruum_vruum(self):
        """
        Animation function

        :return: None
        :rtype: None
        """

        if self.vroom_vroom:
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.frame_counter = 0

    def draw(self):
        """
        Drawing function

        :return: None
        :rtype: None
        """

        if self.vroom_vroom:
            self.game.screen.blit(self.images[0], self.weapon_pos)
        else:
            self.game.screen.blit(self.first_image, self.weapon_pos)

    def update(self):
        """
        Updating function

        :return: None
        :rtype: None
        """
        self.check_animation_time()
        self.animate_vruum_vruum()


class Minigun(AnimatedSprite):
    """
    Class Minigun

    """
    def __init__(self, game, path='resources/sprites/weapon/minigun/0.png', scale=3, animation_time=90):
        """
        Init method of class

        :param game: game instance
        :type game: self
        :param path: path to images
        :type path: str
        :param scale: scale of images
        :type scale: float
        :param animation_time: animation time
        :type animation_time: int
        """

        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.minigun_shoot = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = MINIGUN_DAMAGE
        self.ammo = 1
        self.idle = deque(self.get_images('resources/sprites/weapon/minigun/minigun_no_ammo'))
        self.idle = deque(
            [pg.transform.smoothscale(img, (self.idle[0].get_width() * scale, self.idle[0].get_height() * scale))
             for img in self.idle])
        self.first_image = self.idle[0]
        self.weapon_pos_no_ammo = (HALF_WIDTH - self.first_image.get_width() // 2, HEIGHT - self.first_image.get_height())

    def animate_minigun(self):
        """
        Animation function

        :return: None
        :rtype: None
        """

        if self.minigun_shoot:
            if self.game.player.minigun_ammo > 0:
                if self.animation_trigger:
                    self.images.rotate(-1)
                    self.image = self.images[0]
                    self.frame_counter += 1
                    if self.frame_counter == self.num_images:
                        self.frame_counter = 0

    def draw(self):
        """
        Drawing function

        :return: None
        :rtype: None
        """

        if self.minigun_shoot:
            self.game.screen.blit(self.images[0], self.weapon_pos)
        else:
            self.game.screen.blit(self.first_image, self.weapon_pos_no_ammo)

    def update(self):
        """
        Updating function

        :return: None
        :rtype: None
        """

        self.check_animation_time()
        self.animate_minigun()

    def get_images(self, path):
        """
        Function to get the images when minigun is not firing or out of ammo

        :param path: path to images
        :type path: str
        :return: images list
        :rtype: list
        """

        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
