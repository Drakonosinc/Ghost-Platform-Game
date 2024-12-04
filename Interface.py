import pygame_gui
from Load_elements import *
class interface(load_elements):
    def __init__(self,width=0, height=0):
        self.WIDTH = width
        self.HEIGHT = height
        super().__init__("Ghost Platform",self.WIDTH,self.HEIGHT)
        self.manager = pygame_gui.UIManager((self.WIDTH,self.HEIGHT),theme_path=os.path.join(self.config_path,"theme_buttons.json"))
        self.main=0 #-1=game, 0=menu, 1=game over, 2=game menu, 3=pausa, 4=options, 5=visuals, 6=menu keys
        self.active_buttons = []
        self.draw_menus()
    def draw_menus(self):
        self.main_menu()
        self.game_over_menu()
        self.mode_game_menu()
        self.pausa_menu()
        self.menu_options()
        self.visuals_menu()
        self.keys_menu()
        self.sounds_menu()
    def event_buttons(self,event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if self.main!=-1:self.buttons_repetitive(event)
            if self.main==0:self.buttons_main_menu(event)
            if self.main==4:self.buttons_options_menu(event)
    def buttons_repetitive(self,event):
        if self.main!=0 and event.ui_element == self.back_button:self.change_mains(0)
        if self.main!=2 and event.ui_element == self.option_button:self.change_mains(4)
        if (self.main!=2 and self.main!=4) and event.ui_element == self.exit_button:self.close_game()
        if (self.main!=0 and self.main!=4) and event.ui_element == self.reset_button:self.change_mains(-1,command=self.reset)
    def buttons_main_menu(self,event):
        if event.ui_element == self.play_button:self.change_mains(2)
    def buttons_options_menu(self,event):
        if event.ui_element == self.visuals_button:self.change_mains(5)
        if event.ui_element == self.sounds_button:self.change_mains(7)
        if event.ui_element == self.keys_button:self.change_mains(6)
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
    def change_mains(self,main,color=(0,0,0),limit=255,command=None):
        self.fade_transition(False,color,limit)
        self.clear_buttons()
        self.main=main
        self.draw_menus()
        if command!=None:command()
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
        if self.main==1:
            self.filt(self.WIDTH,self.HEIGHT,150,self.RED)
            self.screen.blit(self.font4.render("Game Over", True, self.BLACK),(3,10))
            self.reset_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 100, 150, 50),text="Press R to Restart",manager=self.manager)
            self.back_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 150, 150, 50),text='Exit The Menu',manager=self.manager)
            self.exit_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 200, 150, 50),text='Exit The Game',manager=self.manager)
            self.active_buttons.extend([self.reset_button, self.back_button, self.exit_button])
    def mode_game_menu(self):
        if self.main==2:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.font3.render("Mode Game", True, "orange"),(3,10))
            self.reset_button=pygame_gui.elements.UIButton(relative_rect=Rect(self.WIDTH-110, self.HEIGHT-50, 100, 50),text='Continue',manager=self.manager)
            self.back_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, self.HEIGHT-50, 100, 50),text='Back',manager=self.manager)
            self.active_buttons.extend([self.reset_button,self.back_button])
    def pausa_menu(self):
        if self.main==3:
            self.filt(self.WIDTH,self.HEIGHT,150,self.GRAY)
            self.screen.blit(self.font3.render("Pause", True, "White"),(3,10))
            self.reset_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 100, 100, 50),text="Reset",manager=self.manager)
            self.option_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 150, 100, 50),text='Option',manager=self.manager)
            self.back_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 200, 100, 50),text='Menu',manager=self.manager)
            self.exit_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, 250, 100, 50),text='Exit',manager=self.manager)
            self.active_buttons.extend([self.reset_button, self.option_button, self.back_button,self.exit_button])
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
        if self.main==5:
            self.screen.fill(self.BLACK)
            self.option_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, self.HEIGHT-50, 100, 50),text='Back',manager=self.manager)
            self.active_buttons.extend([self.option_button])
    def keys_menu(self):
        if self.main==6:
            self.screen.fill(self.BLACK)
            self.option_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, self.HEIGHT-50, 100, 50),text='Back',manager=self.manager)
            self.active_buttons.extend([self.option_button])
    def sounds_menu(self):
        if self.main==7:
            self.screen.fill(self.BLACK)
            self.option_button=pygame_gui.elements.UIButton(relative_rect=Rect(10, self.HEIGHT-50, 100, 50),text='Back',manager=self.manager)
            self.active_buttons.extend([self.option_button])