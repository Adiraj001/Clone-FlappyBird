import pygame as pg

class Bird(pg.sprite.Sprite):
    def __init__(self, scale_factor: float):
        super().__init__()
        self.img_list = [pg.transform.scale(pg.image.load("assets/birdup.png").convert_alpha(),
                                            (int(34 * scale_factor), int(24 * scale_factor))),
                         pg.transform.scale(pg.image.load("assets/birddown.png").convert_alpha(),
                                            (int(34 * scale_factor), int(24 * scale_factor)))]
        self.image_index = 0
        self.image = self.img_list[self.image_index]
        self.rect = self.image.get_rect(center=(100, 200))
        self.y_velocity = 0
        self.gravity = 10
        self.flap_speed = 250
        self.anim_count = 0
    
    def update(self, dt):
        self.animate()
        self.apply_gravity(dt)
        
        if self.rect.y <= 0:
            self.rect.y = 0
            self.flap_speed = 0
        elif self.rect.y > 0 and self.flap_speed == 0:
            self.flap_speed = 250
            
    def apply_gravity(self, dt):
        self.y_velocity += self.gravity * dt
        self.rect.y += self.y_velocity
        
    def fly(self, dt):
        self.y_velocity = -self.flap_speed * dt
    
    def animate(self):
        if self.anim_count == 5:
            self.image = self.img_list[self.image_index]
            self.image_index = 1 if self.image_index == 0 else 0
            self.anim_count = 0
        
        self.anim_count += 1