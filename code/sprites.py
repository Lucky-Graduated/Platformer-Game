from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos,groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)

        # movement and collisions
        self.speed = 400
        self.direction = pygame.math.Vector2()
        self.collision_sprites = collision_sprites
        self.gravity = 50
        self.is_onfloor = False
    
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        if keys[pygame.K_w] and self.is_onfloor:
            self.direction.y = -20

    def move(self, dt):
        # horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # vertical
        self.is_onfloor = False
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collision('vertical')
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction =='horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction =='vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def check_floor(self):
        bottom_rect = pygame.FRect((0, 0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
        self.is_onfloor = True if bottom_rect.collidelist([sprite.rect for sprite in self.collision_sprites]) >= 0 else False
    
    def update(self, dt):
        self.check_floor()
        self.input()
        self.move(dt)