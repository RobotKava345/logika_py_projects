#створи гру "Лабіринт"!
from pygame import *
import random 
init()
font.init()
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.set_volume(0.2)
mixer.music.play(loops=-1)

kick_sound = mixer.Sound('kick.ogg')
kick_sound.set_volume(0.5)
money_sound = mixer.Sound('money.ogg')

FONT = 'PressStart2P-Regular.ttf'

FPS = 60
TILE_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = 20, 15
WIDTH, HEIGHT = TILE_SIZE*MAP_WIDTH, TILE_SIZE*MAP_HEIGHT

#створи вікно гри
window = display.set_mode((WIDTH,HEIGHT))
display.set_caption("Catch_up")
clock = time.Clock()


#задай фон сцени
bg = image.load("StoneFloorTexture.png")
bg = transform.scale(bg, (WIDTH, HEIGHT))
player_img = image.load("hero.png")
wall_img = image.load("wall.png")
enemy_img = image.load("cyborg.png")
treasure_img = image.load("treasure.png")
coin_img = image.load("gold-coin-7023965_1280-removebg-preview.png")
all_labels = sprite.Group()
all_sprites = sprite.Group()
#створи 2 спрайти та розмісти їх на сцені
class BaseSprite(sprite.Sprite):
    def __init__(self,image, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x,y, width, height)
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)
    def draw(self, window):
        window.blit(self.image, self.rect)


class Label(sprite.Sprite):
    def __init__(self,text, x, y, fontsize = 30,color = (255, 255, 255),font_name = FONT):
        super().__init__()
        self.color = color
        self.font = font.Font(FONT, fontsize)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_labels.add(self)

    def set_text(self, new_text, color = (255, 255, 255)):
        self.image = self.font.render(new_text, True, color)



class Player(BaseSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image,True, False)
        self.damage_timer = time.get_ticks()       
        self.speed = 5
        self.hp = 100
        self.coins_counter = 0



    


    def update(self):
        old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -=self.speed
            self.image = self.left_image
        if keys[K_d]:
           self.rect.x +=self.speed
           self.image = self.right_image
        if keys[K_w]:
            self.rect.y -=self.speed
        if keys[K_s]:
            self.rect.y +=self.speed

        coll_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(coll_list)>0:
            self.rect.x, self.rect.y = old_pos

        coll_list = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        if len(coll_list)>0:
            now = time.get_ticks()
            if now - self.damage_timer > 1500:
                self.damage_timer = time.get_ticks()
                self.hp -=10
                hp_label.set_text(f"HP:{self.hp}")
                kick_sound.play()
            
            self.rect.x, self.rect.y = old_pos
            


class Enemy(BaseSprite):
    def __init__(self, image, x, y, width, height, dir_list):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image,True, False)
        self.speed = 2
        self.dir_list = dir_list
        self.dir = random.choice(self.dir_list)
    def update(self):
        old_pos = self.rect.x, self.rect.y
        if self.dir == 'left':
            self.rect.x -=self.speed
            self.image = self.left_image
        elif self.dir == 'right':
           self.rect.x +=self.speed
           self.image = self.right_image
        elif self.dir == 'up':
            self.rect.y -=self.speed
        elif self.dir == 'down':
            self.rect.y +=self.speed
        
        coll_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(coll_list)>0:
            self.rect.x, self.rect.y = old_pos
            self.dir = random.choice(self.dir_list)
        

player1 = Player(player_img,200,300, TILE_SIZE-5, TILE_SIZE-5)
result = Label("", 300, 300, fontsize=60)
restart_text = Label("Press R to restart", 350, 350, fontsize=20 )
all_labels.remove(restart_text)
hp_label = Label(f"HP:{player1.hp}", 10, 10, fontsize=20)
walls = sprite.Group()
enemys = sprite.Group()
def game_start():
    global treasure, run, finish
    for wall in walls:
        wall.kill()
    for e in enemys:
        e.kill()
    
    
    run = True
    finish = False
    player1.hp = 100
    hp_label.set_text(f"HP:{player1.hp}")
    result.set_text('')
    all_labels.remove(restart_text)
    with open("map.txt", "r") as file:
        map = file.readlines()
        x, y = 0,0
        for row in map:
            for symbol in row:
                if symbol=='W':
                    walls.add(BaseSprite(wall_img, x, y, TILE_SIZE, TILE_SIZE))
                
                if symbol == 'P':
                    player1.rect.x = x
                    player1.rect.y = y

                if symbol=='E':
                    enemys.add(Enemy(enemy_img, x, y, TILE_SIZE-5, TILE_SIZE-5, ['left', 'right']))
                if symbol=='H':
                    enemys.add(Enemy(enemy_img, x, y, TILE_SIZE-5, TILE_SIZE-5, ['up', 'down']))
                
                if symbol == 'F':
                    treasure = BaseSprite(treasure_img, x, y, TILE_SIZE, TILE_SIZE)

                #if symbol == 'C':
                    #treasure = BaseSprite(coin_img, x, y, TILE_SIZE, TILE_SIZE)


                x+=TILE_SIZE
            x = 0    
            y+= TILE_SIZE




    
game_start()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_r and finish:
                game_start()


    if player1.hp<=0:
        finish = True
        result.set_text("You lose!")
        result.rect.x = WIDTH/2 - result.image.get_width()/2

        result.rect.y = HEIGHT/2 - result.image.get_height()/2
        all_labels.add(restart_text)
        restart_text.rect.x = WIDTH/2 - result.image.get_width()/2


    if not finish:
        player1.update()

        enemys.update()

    if sprite.collide_mask(player1, treasure):
        finish = True
        result.set_text("You win! ")
        result.rect.x = WIDTH/2 - result.image.get_width()/2
        result.rect.y = HEIGHT/2 - result.image.get_height()/2

    window.blit(bg, (0,0))
    
    all_sprites.draw(window)
    
    all_labels.draw(window)



    display.update()
    clock.tick(FPS)