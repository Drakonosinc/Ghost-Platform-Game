import pygame,pygame_gui,random,os
from pygame.locals import *
import numpy as np
class ghost_platform():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Ghost Platform")
        self.running=True
        self.game_over=False
        self.WIDTH =700
        self.HEIGHT=600
        self.screen=pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.manager = pygame_gui.UIManager((self.WIDTH,self.HEIGHT))
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.define_colors()
        self.load_images()
        self.load_fonts()
        self.load_sounds()
        self.objects()
        self.nuances()
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys
        self.gravity=0.25
        self.down_gravity=0
        self.jumper=-11
        self.isjumper=False
        self.reward=0
        self.life=100
        self.state_life=[2,False]
    def define_colors(self):
        self.GRAY=(127,127,127)
        self.WHITE=(255,255,255)
        self.BLACK=(0,0,0)
        self.GREEN=(0,255,0)
        self.BLUE=(0,0,255)
        self.SKYBLUE=(135,206,235)
        self.YELLOW=(255,255,0)
        self.RED=(255,0,0)
        self.GOLDEN=(255,199,51)
        self.background=self.GRAY
        self.life_color=self.GREEN
    def load_images(self):
        self.image_path=os.path.join(os.path.dirname(__file__), "images")
        self.space=pygame.image.load(os.path.join(self.image_path,"espacio.png"))
        self.space=pygame.transform.scale(self.space,(700,400))
        self.player=pygame.image.load(os.path.join(self.image_path,"flyghost.png")).convert_alpha()
        self.player=pygame.transform.scale(self.player,(35,35))
        self.floor=pygame.image.load(os.path.join(self.image_path,"suelo1.png")).convert_alpha()
        self.floor=pygame.transform.scale(self.floor,(100,40))
        self.meteorite=pygame.image.load(os.path.join(self.image_path,"meteorito.png")).convert_alpha()
        self.meteorite=pygame.transform.scale(self.meteorite,(50,85))
        self.potion=pygame.image.load(os.path.join(self.image_path,"pocion1.png")).convert_alpha()
        self.potion=pygame.transform.scale(self.potion,(35,40))
        self.shield=pygame.image.load(os.path.join(self.image_path,"shield1.png")).convert_alpha()
        self.shield=pygame.transform.scale(self.shield,(50,50))
    def load_fonts(self):
        self.font_path=os.path.join(os.path.dirname(__file__), "fonts")
        self.font=pygame.font.Font(None,25)
        self.font1=pygame.font.SysFont("times new roman", 80)
        self.font2=pygame.font.Font(None,35)
        self.font2_5=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),30)
        self.font3=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),60)
        self.font3_5=pygame.font.Font(os.path.join(self.font_path,"8bitOperatorPlusSC-Bold.ttf"),30)
        self.font4=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),75)
        self.font5=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),20)
        self.font6=pygame.font.Font(os.path.join(self.font_path,"ka1.ttf"),16)
    def load_sounds(self):
        pygame.mixer.init()
        self.sound_path=os.path.join(os.path.dirname(__file__), "sounds")
        self.sound_jump=pygame.mixer.Sound(os.path.join(self.sound_path,"jump.aiff"))
        self.sound_meteorite=pygame.mixer.Sound(os.path.join(self.sound_path,"meteor.mp3"))
        self.sound_health=pygame.mixer.Sound(os.path.join(self.sound_path,"health.flac"))
        self.sound_background=pygame.mixer.Sound(os.path.join(self.sound_path,"back_fo.wav"))
        self.sound_game_lose=pygame.mixer.Sound(os.path.join(self.sound_path,"game_lose.flac"))
        self.sound_shield=pygame.mixer.Sound(os.path.join(self.sound_path,"shield.wav"))
        self.sound_exit=pygame.mixer.Sound(os.path.join(self.sound_path,"exitbutton.wav"))
    def objects(self):
        self.object1=Rect(350, self.HEIGHT-35,25,25)
        self.object2=None
        self.object3=None
        self.object4=None
        self.object5=None
    def generate_nuances(self):
        return np.column_stack((np.random.choice(np.arange(25, self.WIDTH-50, 115), 15),np.random.choice(np.arange(-500, 0, 200), 15))).tolist()
    def nuances(self):self.matrix=[self.generate_nuances(),self.generate_nuances()]
    def elements(self,matrix,speed_fall,object_name,width,height,type_object,image=None,restx=0,resty=0):
        for coords in matrix:
            coords[1]+=speed_fall
            rect=Rect(coords[0],coords[1],width,height)
            if coords[1]>=self.HEIGHT:self.reset_coords(coords)
            self.collision(rect,type_object,coords)
            setattr(self, object_name, rect)
            self.screen.blit(image,(coords[0]-restx,coords[1]-resty))
            # pygame.draw.rect(self.screen,self.BLACK,rect)
    def collision(self,objects,type_object,coords):
        if self.object1.colliderect(objects):
            match type_object:
                case "platform":
                    self.object1.y=objects.y-25
                    self.down_gravity=0
                    self.isjumper=True
                case "meteorite":
                    if not self.state_life[1]:
                        self.reset_coords(coords)
                        self.state_life[0]=0
                        self.sound_meteorite.play()
                    else:
                        self.state_life[1]=False
                        self.reset_coords(coords)
                        self.sound_meteorite.play()
                case "potion" if self.life<100:
                    self.state_life[0]=1
                    self.reset_coords(coords)
                case "shield" if not self.state_life[1]:
                    self.state_life[1]=True
                    self.reset_coords(coords)
    def reset_coords(self,coords):
        coords[1]=random.choice(np.arange(-500, 0, 200))
        coords[0]=random.choice(np.arange(25, self.WIDTH-50, 115))
    def calls_elements(self):
        self.elements(self.matrix[0],3,"object2",100,25,"platform",self.floor,0,10)
        self.elements([self.matrix[1][0]],6,"object3",50,35,"meteorite",self.meteorite,0,45)
        self.elements([self.matrix[1][1]],2,"object4",35,25,"potion",self.potion,0,10)
        self.elements([self.matrix[1][2]],4,"object5",45,25,"shield",self.shield,5,10)
    def events(self):
        if not self.isjumper:self.fall()
        if self.object1.y>=self.HEIGHT-35:
            self.object1.y=self.HEIGHT-35
            self.isjumper=True
        elif not self.object1.colliderect(self.object2):
            self.fall()
            if self.object1.y<=-20:
                self.object1.y=-15
                self.down_gravity=self.gravity
    def fall(self):
        self.down_gravity+=self.gravity
        self.object1.y+=self.down_gravity
    def handle_keys(self):
        for event in pygame.event.get():
            self.manager.process_events(event)
            self.event_quit(event)
            self.event_keydown(event)
        self.pressed_keys=pygame.key.get_pressed()
        self.pressed_mouse=pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.press_keys()
    def event_quit(self,event):
        if event.type==QUIT:self.close_game()
    def close_game(self):
        self.sound_exit.play(loops=0)
        self.game_over=True
    def event_keydown(self,event):
        if event.type==KEYDOWN:
            if self.main==3 and event.key==K_p:self.main=-1
            elif self.main==-1 and event.key==K_p:self.main=3
            if event.key==K_SPACE or event.key==K_w:self.jump()
    def press_keys(self):
        if self.main==-1:
            if self.pressed_keys[K_d]:self.object1.x+=5
            if self.pressed_keys[K_a]:self.object1.x-=5
    def draw(self):
        self.screen.fill(self.background)
        # pygame.draw.rect(self.screen, self.GREEN, self.object1)
        self.screen.blit(self.player,(self.object1.x-5,self.object1.y-5))
        self.bar_life()
        self.shield_draw()
    def jump(self):
        if self.isjumper:
            self.down_gravity=self.jumper
            self.sound_jump.play(loops=0)
            self.isjumper=False
    def bar_life(self):
        pygame.draw.rect(self.screen,self.BLACK,(50,8,105,20),4)
        pygame.draw.rect(self.screen,self.life_color,(52,11,self.life,15))
        self.life += 1 if self.state_life[0] == 1 else -1 if self.state_life[0] == 0 else 0
        states = {100: (2, self.GREEN),75: (2, self.SKYBLUE),50: (2, self.YELLOW),25: (2, self.RED)}
        if self.life in states:self.state_life[0], self.life_color = states[self.life]
        elif self.life < 0:self.main,self.life_color,self.state_life[0] = (1,self.BLACK,2)
        self.screen.blit(self.font6.render("Life",True,self.life_color),(0,9))
    def shield_draw(self):
        if self.state_life[1]:pygame.draw.ellipse(self.screen,self.life_color,(self.object1.x-11,self.object1.y-15,50,50),3)
    def main_menu(self):
        if self.main==0:pass
    def game_over_menu(self):
        if self.main==1:pass
    def mode_game_menu(self):
        if self.main==2:pass
    def pausa_menu(self):
        if self.main==3:pass
    def menu_options(self):
        if self.main==4:pass
    def visuals_menu(self):
        if self.main==5:pass
    def keys_menu(self):
        if self.main==6:pass
    def sounds_menu(self):
        if self.main==7:pass
    def run_with_model(self):
        self.running=True
        score=0
        while self.running and self.game_over==False:
            self.handle_keys()
            if self.main==-1:
                self.draw()
                self.events()
                self.calls_elements()
            self.time_delta = self.clock.tick(self.FPS)/1000.0
            self.manager.update(self.time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()
        return score

if __name__ == "__main__":
    game=ghost_platform()
    game.run_with_model()