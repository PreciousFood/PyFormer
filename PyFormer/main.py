import pygame
from pygame.locals import *
from pygame import Vector2
from typing import Tuple

from pygame.sprite import _Group


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0


pygame.init()



class PlayerHitbox(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, pos: Tuple[int, int], hard_collision_list: list, soft_collision_list=None, advanced_movement=False):
        super().__init__()
        self.surf = pygame.surface.Surface((width, height))
        self.surf.fill(RED)
        self.rect = self.surf.get_frect(center=pos)

        self.keybinds = {
            K_UP: self.up,
            K_DOWN: self.down,
            K_LEFT: self.left,
            K_RIGHT: self.right
        }

        self.g = 10 # gravity
        self.max_velocity = 100
        self.jump_velocity = 20
        self.velocity = Vector2()

        self.advanced_movement = advanced_movement


        self.hard_collision_list = hard_collision_list  # hard_collision_list: walls, floor, platform, ect.
        self.soft_collision_list = soft_collision_list if soft_collision_list is not None else [] # soft_collision_list: coins, collectables, enemies

    def update(self, delta: float):
        # call functions binded to keys
        keys = pygame.key.get_pressed()
        for k, v in self.keybinds:
            if keys[k]:
                v()
        
        self.process(delta)

    # methods to call or bind to keys
    # could be overidden maybe?
    def up(self):
        self.velocity.y = -self.jump_velocity
    def down(self):
        pass
    def left(self):
        pass
    def right(self):
        pass
    def process(self, delta: float):
        """
        Called every frame/every time update() is called. Default use is to handle gravity and friction
        """
        self.velocity.y += self.g

    def move_and_collide(self):
        pass
        

    def on_ground(self) -> bool:
        pass



class HardObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    


screen = pygame.display.set_mode(SCREEN_SIZE)

box = PlayerHitbox(20, 20, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), [])


run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    
    screen.fill(WHITE)
    screen.blit(box.surf, box.rect)
    pygame.display.flip()


pygame.quit()