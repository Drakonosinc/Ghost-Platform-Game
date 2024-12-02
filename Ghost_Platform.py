import pygame,pygame_gui,random,os
from pygame.locals import *
import numpy as np
class ghost_platform():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Ghost Platform")
        self.config()
        self.running=True
        self.game_over=False
        self.WIDTH =700
        self.HEIGHT=600
        self.screen=pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.manager = pygame_gui.UIManager((self.WIDTH,self.HEIGHT),theme_path=os.path.join(self.config_path,"theme_buttons.json"))
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
        self.active_buttons = []
        self.draw_menus()
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
    def config(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "Config")
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
                    self.sound_health.play()
                case "shield" if not self.state_life[1]:
                    self.state_life[1]=True
                    self.reset_coords(coords)
                    self.sound_shield.play()
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
            self.event_buttons(event)
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
            if self.main==3 and event.key==K_p:self.change_mains(-1,self.GRAY,20)
            elif self.main==-1 and event.key==K_p:self.change_mains(3,self.GRAY)
            if event.key==K_SPACE or event.key==K_w:self.jump()
    def event_buttons(self,event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if self.main==0:self.buttons_main_menu(event)
            if self.main==4:self.buttons_options_menu(event)
    def buttons_main_menu(self,event):
        if event.ui_element == self.play_button:self.change_mains(-1)
        if event.ui_element == self.option_button:self.change_mains(4)
        if event.ui_element == self.exit_button:self.close_game()
    def buttons_options_menu(self,event):
        if event.ui_element == self.visuals_button:self.change_mains(5)
        if event.ui_element == self.sounds_button:self.change_mains(7)
        if event.ui_element == self.keys_button:self.change_mains(6)
        if event.ui_element == self.back_button:self.change_mains(0)
    def press_keys(self):
        if self.main==-1:
            if self.pressed_keys[K_d]:self.object1.x+=5
            if self.pressed_keys[K_a]:self.object1.x-=5
    def draw(self):
        self.screen.fill(self.background)
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
    def draw_menus(self):
        self.main_menu()
        self.game_over_menu()
        self.mode_game_menu()
        self.pausa_menu()
        self.menu_options()
        self.visuals_menu()
        self.keys_menu()
        self.sounds_menu()
    def fade_transition(self,fade_in,color=(0,0,0),limit=255):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.fill(color)
        alpha=0
        while not fade_in and alpha <= limit:
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            self.clock.tick(20)
            alpha += -15 if fade_in else 15
    def change_mains(self,main,color=(0,0,0),limit=255):
        self.fade_transition(False,color,limit)
        self.clear_buttons()
        self.main=main
        self.draw_menus()
    def clear_buttons(self):
        for button in self.active_buttons:button.kill()
        self.active_buttons=[]
    def filt(self,width,height,number,color=(0,0,0),position=(0,0)):
        background=pygame.Surface((width,height),pygame.SRCALPHA)
        background.fill((*color, number))
        self.screen.blit(background,position)
    def main_menu(self):
        if self.main==0:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font3.render("Ghost Platform",True,self.WHITE),(3,10))
            self.play_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 100, 100, 50),text="Play",manager=self.manager)
            self.option_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 150, 100, 50),text='Option',manager=self.manager)
            self.exit_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 200, 100, 50),text='Exit',manager=self.manager)
            self.active_buttons.extend([self.play_button, self.option_button, self.exit_button])
    def game_over_menu(self):
        if self.main==1:self.filt(self.WIDTH,self.HEIGHT,150,self.RED)
    def mode_game_menu(self):
        if self.main==2:self.screen.fill(self.BLACK)
    def pausa_menu(self):
        if self.main==3:
            self.filt(self.WIDTH,self.HEIGHT,150,self.GRAY)
            self.screen.blit(self.font3.render("Pause", True, "White"),(3,10))
    def menu_options(self):
        if self.main==4:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font3.render("Options", True, "White"),(3,10))
            self.visuals_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 100, 100, 50),text="Visuals",manager=self.manager)
            self.sounds_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 150, 100, 50),text='Sounds',manager=self.manager)
            self.keys_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 200, 100, 50),text='Keys',manager=self.manager)
            self.back_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, self.HEIGHT-50, 100, 50),text='Back',manager=self.manager)
            self.active_buttons.extend([self.visuals_button,self.sounds_button,self.keys_button,self.back_button])
    def visuals_menu(self):
        if self.main==5:self.screen.fill(self.BLACK)
    def keys_menu(self):
        if self.main==6:self.screen.fill(self.BLACK)
    def sounds_menu(self):
        if self.main==7:self.screen.fill(self.BLACK)
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