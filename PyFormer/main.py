import pygame
from pygame.locals import *
from pygame import Vector2
from typing import Tuple, Dict, Optional, List
import time

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

BLACK = pygame.color.Color(0, 0, 0)
WHITE = pygame.color.Color(255, 255, 255)
RED = pygame.color.Color(255, 0, 0)
CLEAR = pygame.color.Color(0, 0, 0, 0)


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





def CollisionAreas_from_image(path: str, color_keys: Optional[Dict[str, pygame.color.Color]]=None, pos: Optional[Tuple[int, int]]=(0, 0)) -> List['CollisionArea']:
    """
    Creats a list of the CollisionArea class.
    Usefull to turn a color coded image into multiple CollisionAreas that share a position.

    NOTE: Transpaarent sectionsof the image will become part of all masks

    Paramaters:
    - path (str): the path to the image to parse into CollisionAreas
    - color_keys (Optional[dict]): A  dictionary pairing names of CollisionAreas to the relevent color in the image specified by `path`.
    Has the format `color_keys = {name: color, ...}`. Default value is `{"collision_area": BLACK}`
    - pos (Optional[Tuple[int, int]]): The position shared by all of the returned CollisionAreas. Default value is `(0, 0)`
    """
    if not color_keys:
        color_keys = {"collision_area": BLACK}

    r = []
    for name, color in color_keys.items():
        surf = pygame.image.load(path).convert()
        surf.set_colorkey(color)
        w, h = surf.get_size()
        mask = pygame.mask.from_surface(surf)
        mask.invert()
        r.append(CollisionArea(name=name, mask=mask, pos=pos, width=w, height=h))
    
    return r


class CollisionArea:
    def __init__(self, name: str, rect: Optional[pygame.rect.Rect|Tuple[int, int]]=None, mask: Optional[pygame.mask.Mask]=None, pos: Optional[Tuple[int, int]]=(0, 0), width: Optional[int]=None, height: Optional[int]=None, debug_color: Optional[pygame.color.Color]=RED) -> None:
        """
        A class for detecting collisions.

        Parameters:
        - name (str): The name of the CollisionArea.
        - rect (Optional[pygame.Rect]): The rectangular area for collision detection.
        - mask (Optional[pygame.mask.Mask]): The mask for collision detection.
        - pos (Optional[Tuple[int, int]]): The position of the CollisionArea (used if `rect` is not provided). 
          Default value is `(0, 0)`.
        - width (Optional[int]): The width of the CollisionArea (used if `rect` is not provided).
        - height (Optional[int]): The height of the CollisionArea (used if `rect` is not provided).
        - debug_color (Optional[pygame.Color]): The color used for debugging purposes.

        Methods:
        - move_by(x: int, y: int) -> None:
            Moves the CollisionArea by the specified amounts along the x and y axes.
            
        - move_to(x: int, y: int) -> None:
            Moves the CollisionArea to the specified coordinates (x, y).

        - collide_with(other_CollisionArea: "CollisionArea", use_mask=True) -> bool:
            Checks if the CollisionArea collides with another CollisionArea.

        - collide_with_several(other_CollisionAreas: List["CollisionArea"], use_mask=True) -> List["CollisionArea.name"]:
            Checks for collisions with multiple CollisionAreas and returns a list of names of collided CollisionAreas.
        """
        if rect == None:
            if width != None and height != None:
                self.rect = pygame.rect.Rect(pos[0], pos[1], width, height)
            else:
                raise ValueError("Requires `width` and `height` or `rect`")
        else:
            self.rect = rect
            
        if mask == None:
            self.mask = pygame.mask.from_surface(pygame.surface.Surface(self.rect.size))
        else:
            self.mask = mask

        self.name = name
        self.debug_surface = self.mask.to_surface(setcolor=debug_color, unsetcolor=CLEAR)

    def move_by(self, x: int, y: int) -> None:
        """
        Moves the CollisionArea by the specified amounts along the x and y axes.

        Parameters:
        - x (int): The amount to move the CollisionArea along the x-axis.
        - y (int): The amount to move the CollisionArea along the y-axis.
        """
        self.rect.move_ip(x, y)

    def move_to(self, x: int, y: int) -> None:
        """
        Moves the CollisionArea to the specified coordinates (x, y).

        Parameters:
        - x (int): The x-coordinate to move the CollisionArea to.
        - y (int): The y-coordinate to move the CollisionArea to.
        """
        move_by_xy = x - self.rect.x, y - self.rect.y
        self.move_by(*move_by_xy)

    def collide_with(self, other_CollisionArea: "CollisionArea", use_mask=True) -> bool:
        """
        Checks if the CollisionArea collides with another CollisionArea.

        Parameters:
        - other_CollisionArea ("CollisionArea"): The other CollisionArea to check for collision.
        - use_mask (bool): If True, uses masks for collision detection. If False, uses rectangular collision.

        Returns:
        - bool: True if there is a collision, False otherwise.
        """
        if self.rect.colliderect(other_CollisionArea.rect):
            if use_mask:
                offset = (
                    other_CollisionArea.rect.x - self.rect.x,
                    other_CollisionArea.rect.y - self.rect.y
                )
                if self.mask.overlap(other_CollisionArea.mask, offset) == None:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False
        

    def collide_with_several(self, other_CollisionAreas: List["CollisionArea"], use_mask=True) -> List["CollisionArea.name"]:
        """
        Checks for collisions with multiple CollisionAreas and returns a list of names of collided CollisionAreas.

        Parameters:
        - other_CollisionAreas (List["CollisionArea"]): The list of other CollisionAreas to check for collision.
        - use_mask (bool): If True, uses masks for collision detection. If False, uses rectangular collision.

        Returns:
        - List["CollisionArea.name"]: A list of names of collided CollisionAreas.
        """
        r = []
        for other in other_CollisionAreas:
            name = other.name
            if self.collide_with(other_CollisionArea=other, use_mask=use_mask):
                r.append(name)
        return r





screen = pygame.display.set_mode(SCREEN_SIZE)

t = CollisionArea("test", width=10, height=10)
t2 = CollisionArea("other test", width=40, height=40)
t3 = CollisionArea("yet another test", width=40, height=40, pos=(100, 100))

t4 = CollisionAreas_from_image("tf.png", pos=(200, 0))[0]

clock = pygame.time.Clock()
FPS = 60
delta = 0

run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    t.move_to(*pygame.mouse.get_pos())


    screen.fill(WHITE)
    screen.blit(t.debug_surface, t.rect)
    screen.blit(t2.debug_surface, t2.rect)
    screen.blit(t3.debug_surface, t3.rect)
    screen.blit(t4.debug_surface, t4.rect)
    print(t.collide_with_several([t, t2, t3, t4], use_mask=True))


    pygame.display.flip()

    # divide by 1000 to convert ms to s
    delta = clock.tick(FPS)/1000

pygame.quit()