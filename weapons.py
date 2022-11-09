from sprite_object import *

class Shotgun(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animate_shot(self):
        """"Shooting animation for shotgun if it is animated
        you can not shoot"""
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
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()

class Chainsaw(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/chainsaw/0.png', scale=3, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.vroom_vroom = False
        self.num_images = len(self.images)
        self.first_image = self.images[0]
        self.frame_counter = 0
        self.damage = 10
        self.fuel_consumption = 1

    def animate_vruum_vruum(self):
        if self.vroom_vroom:
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.frame_counter = 0


    def draw(self):
        if self.vroom_vroom:
            self.game.screen.blit(self.images[0], self.weapon_pos)
        else:
            self.game.screen.blit(self.first_image, self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_vruum_vruum()


class Minigun(AnimatedSprite):

    def __init__(self, game, path='resources/sprites/weapon/minigun/0.png', scale=3, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.minigun_shoot = False
        self.num_images = len(self.images)

        self.frame_counter = 0
        self.damage = 10
        self.ammo = 1
        self.idle = deque(self.get_images('resources/sprites/weapon/minigun/minigun_no_ammo'))
        self.idle = deque(
            [pg.transform.smoothscale(img, (self.idle[0].get_width() * scale, self.idle[0].get_height() * scale))
             for img in self.idle])
        self.first_image = self.idle[0]
        self.weapon_pos_no_ammo = (HALF_WIDTH - self.first_image.get_width() // 2, HEIGHT - self.first_image.get_height())

    def animate_minigun(self):
        if self.minigun_shoot:
            if self.game.player.minigun_ammo > 0:
                if self.animation_trigger:
                    self.images.rotate(-1)
                    self.image = self.images[0]
                    self.frame_counter += 1
                    if self.frame_counter == self.num_images:
                        self.frame_counter = 0


    def draw(self):
        if self.minigun_shoot:
            self.game.screen.blit(self.images[0], self.weapon_pos)
        else:
            self.game.screen.blit(self.first_image, self.weapon_pos_no_ammo)

    def update(self):
        self.check_animation_time()
        self.animate_minigun()


    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
