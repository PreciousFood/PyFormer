import pygame
from pygame.locals import *
from pygame import Vector2
from typing import Tuple, Dict, Optional, List
import time

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0


pygame.init()


class PlayerHitbox(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, pos: Tuple[int, int], collision_list: List[pygame.mask.Mask], advanced_movement=False):
        super().__init__()
        self.surf = pygame.surface.Surface((width, height))
        self.surf.fill(RED)
        self.rect = self.surf.get_frect(center=pos)
        self.mask = pygame.mask.Mask((width, height), fill=True)

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

        self.collision_list = collision_list


    def update(self, delta: float):
        self.rect.center = pygame.mouse.get_pos()
        # offset is incorrect, mask != screensize
        print(self.collision_list[0].overlap(self.mask, self.rect.topleft))
        # # call functions binded to keys
        # keys = pygame.key.get_pressed()
        # for k, v in self.keybinds.items():
        #     if keys[k]:
        #         v()
        
        # self.process(delta)
        # self.move_and_collide()

    # methods to call or bind to keys
    # could be overidden maybe?
    def up(self):
        self.velocity.y = -self.jump_velocity*delta
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
        self.velocity.y += self.g*delta

    def move_and_collide(self):
        """
        Moves self according to velocity set in update/process.  
        Takes collision into account.
        """
        if self.velocity.length() != 0:
            direction = self.velocity.normalize()
            self.rect.move_ip(self.velocity)
            for mask in self.collision_list:
                while mask.overlap(self.mask, self.rect.topleft):
                    self.rect.move_ip(-direction)

   


    def on_ground(self) -> bool:
        pass



class CollisionMasks:
    """
    A class for creating and using masks from images. The masks are pulled and sorted from the image using color_key.
    If color_key is not given a single mask will be made from all non white pixels.
    color_key has the following format.  
    `color_key = {name: color, ...}`  
    Either `mask_source` or `mask_source_path` must be provided.
    """
    def __init__(self, mask_source: Optional[pygame.surface.Surface]=None, mask_source_path: Optional[str]=None, color_key=None):
        super().__init__()
        if color_key is None:
            color_key = {
                "collision_mask": WHITE
            }

        if mask_source == mask_source_path == None:
            raise ValueError("Either `mask_source` or `mask_source_path` must be provided.")
        elif mask_source_path != None:
            self.mask_source = pygame.image.load(mask_source_path).convert()
        else:
            self.mask_source = mask_source
        
        for name, color in color_key.items():
            self.mask_source.set_colorkey(color)
            mask = pygame.mask.from_surface(self.mask_source).invert()



screen = pygame.display.set_mode(SCREEN_SIZE)

floor_for_testing = pygame.surface.Surface((SCREEN_WIDTH, 20))
floor_for_testing.fill(BLACK)
t_m = pygame.mask.from_surface(floor_for_testing)

box = PlayerHitbox(20, 20, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), [t_m])

clock = pygame.time.Clock()
FPS = 60
delta = 0

run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    box.update(delta)
    
    screen.fill(WHITE)
    screen.blit(box.surf, box.rect)
    screen.blit(floor_for_testing, (0, SCREEN_HEIGHT-20))
    pygame.display.flip()

    # divide by 1000 to convert ms to s
    delta = clock.tick(FPS)/1000

pygame.quit()