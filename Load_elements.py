import pygame,os
from pygame.locals import *

class load_elements():
    def __init__(self,title,width=0, height=0):
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((width, height))
        self.config()
        self.define_colors()
        self.load_images()
        self.load_fonts()
        self.load_sounds()
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