import pygame as pg
import sys
import time

from bird import Bird
from pipe import Pipe

pg.init()
pg.mixer.init()

class Game:
    def __init__(self):
        self.width = 600
        self.height = 768
        self.scale_factor = 1.5  
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.move_speed = 100  # Initial speed
        self.speed_increment = 20  # Value to change speed
        pg.display.set_caption("Flappy Bird By Adiraj")
        self.is_enter_pressed = False
        self.startmonitoring = False
        self.score = 0

        self.font = pg.font.Font("assets/font.ttf", 30)
        self.score_text = self.font.render("Score: 0", True, (255, 255, 255))
        self.score_rect = self.score_text.get_rect(center=(135, 30))

        self.score_sound = pg.mixer.Sound("assets/sfx/score.wav")
        self.dead_sound = pg.mixer.Sound("assets/sfx/dead.mp3")
        self.flap_sound = pg.mixer.Sound("assets/sfx/flap.mp3")

        self.bird = Bird(self.scale_factor) 
        self.pipe = []  
        self.pipe_timer = 0  
        
        self.load_images()

    def load_images(self):
        self.bg_img = pg.transform.scale(pg.image.load("assets/bg.png").convert(), (self.width, self.height))
        ground_img = pg.image.load("assets/ground.png").convert()
        scaled_width = int(ground_img.get_width() * self.scale_factor)
        scaled_height = int(ground_img.get_height() * self.scale_factor)
        self.ground1_img = pg.transform.scale(ground_img, (scaled_width, scaled_height))
        self.ground2_img = pg.transform.scale(ground_img, (scaled_width, scaled_height))
        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()
        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568  

    def game_loop(self):
        last_time = time.time()
        while True:
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time
            self.pipe_timer += dt  

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.is_enter_pressed = True
                    if event.key == pg.K_SPACE or event.key == pg.K_UP:
                        self.bird.fly(dt)
                        self.flap_sound.play()
                    if event.key == pg.K_p:  # Increase speed
                        self.move_speed += self.speed_increment
                    if event.key == pg.K_o:  # Decrease speed
                        self.move_speed = max(50, self.move_speed - self.speed_increment)  # Prevent speed from becoming too slow

            if self.pipe_timer >= 2.0:  
                self.pipe.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_timer = 0  

            self.update_everything(dt)
            self.check_score()
            self.draw_everything()
            pg.display.update()
            self.clock.tick(60)
    
    def check_score(self):
        """Updates score when the bird successfully passes a pipe."""
        if len(self.pipe) > 0:
            if (self.bird.rect.left > self.pipe[0].rect_down.left and
            self.bird.rect.right < self.pipe[0].rect_down.right and not self.startmonitoring):
                self.startmonitoring = True
            if self.bird.rect.left > self.pipe[0].rect_down.right and self.startmonitoring:
                self.startmonitoring = False
                self.score += 1
                self.score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
                self.score_sound.play()

    def update_everything(self, dt):
        if self.is_enter_pressed:
            self.ground1_rect.x -= self.move_speed * dt
            self.ground2_rect.x -= self.move_speed * dt  
            if self.ground1_rect.right <= 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right <= 0:
                self.ground2_rect.x = self.ground1_rect.right
            self.bird.update(dt)

            for pipe in self.pipe:
                pipe.update(dt)
            self.pipe = [pipe for pipe in self.pipe if pipe.rect_up.right > 0]

            for pipe in self.pipe:
                if self.bird.rect.colliderect(pipe.rect_up) or self.bird.rect.colliderect(pipe.rect_down):
                    self.game_over()

            if self.bird.rect.bottom >= self.ground1_rect.top:
                self.game_over()

    def game_over(self): 
        self.dead_sound.play()

        self.create_restart_button()
        self.win.blit(self.restart_button_bg, self.restart_button_bg_rect)
        self.win.blit(self.restart_button, self.restart_button_rect)
        pg.display.update()
        
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.restart_button_rect.collidepoint(event.pos):
                        self.__init__()  
                        self.game_loop()

    def create_restart_button(self):
        self.restart_button_font = pg.font.Font("assets/font.ttf", 30)
        self.restart_button = self.restart_button_font.render("Restart", True, (0, 0, 0))
        self.restart_button_bg = pg.Surface((self.restart_button.get_width() + 20, self.restart_button.get_height() + 20))
        self.restart_button_bg.fill((255, 255, 255))
        self.restart_button_bg.set_alpha(150)
        self.restart_button_rect = self.restart_button.get_rect(center=(self.width // 2, self.height - 100))
        self.restart_button_bg_rect = self.restart_button_bg.get_rect(center=self.restart_button_rect.center)

    def draw_everything(self):
        self.win.blit(self.bg_img, (0, -165))  
        
        for pipe in self.pipe:
            pipe.drawpipe(self.win)
            
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)
        self.win.blit(self.score_text, self.score_rect)

game = Game()
game.game_loop()