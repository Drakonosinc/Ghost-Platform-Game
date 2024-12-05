import random
import numpy as np
from Interface import *
class ghost_platform(interface):
    def __init__(self):
        super().__init__(width=700, height=600)
        self.running=True
        self.game_over=False
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.objects()
        self.nuances()
        self.gravity=0.25
        self.down_gravity=0
        self.jumper=-12
        self.isjumper=False
        self.life=100
        self.state_life=[2,False]
        self.floor_fall=False
        self.mode_game={"Training AI":False,"Player":True,"AI":False}
        self.scores=self.reward=0
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
        if self.object1.y>=self.HEIGHT-35 and not self.floor_fall:
            self.object1.y=self.HEIGHT-35
            self.isjumper=True
        elif not self.object1.colliderect(self.object2):
            self.fall()
            if self.object1.y<=-20:
                self.object1.y=-15
                self.down_gravity=self.gravity
            if self.object1.y>=self.HEIGHT+50:self.sounddeath()
    def sounddeath(self,sound=True):
        if sound:
            self.sound_game_lose.play(loops=0)
            self.restart()
            sound=False
        else:sound=True
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
            if self.main==1 and event.key==K_r:self.change_mains(-1,command=self.reset)
    def press_keys(self):
        if self.main==-1:
            if self.pressed_keys[K_d]:self.object1.x+=5
            if self.pressed_keys[K_a]:self.object1.x-=5
    def draw(self):
        self.screen.fill(self.background)
        self.screen.blit(self.player,(self.object1.x-5,self.object1.y-5))
        self.bar_life(),self.shield_draw()
    def jump(self):
        if self.isjumper:
            self.down_gravity=self.jumper
            self.sound_jump.play(loops=0)
            self.isjumper,self.floor_fall=False,True
    def bar_life(self):
        pygame.draw.rect(self.screen,self.BLACK,(50,8,105,20),4)
        pygame.draw.rect(self.screen,self.life_color,(52,11,self.life,15))
        self.life += 1 if self.state_life[0] == 1 else -1 if self.state_life[0] == 0 else 0
        states = {100: (2, self.GREEN),75: (2, self.SKYBLUE),50: (2, self.YELLOW),25: (2, self.RED)}
        if self.life in states:self.state_life[0], self.life_color = states[self.life]
        elif self.life < 0:
            self.restart()
            self.life_color,self.state_life[0] = (self.BLACK,2)
        if self.main==-1:self.screen.blit(self.font6.render("Life",True,self.life_color),(0,9))
    def shield_draw(self):
        if self.state_life[1]:pygame.draw.ellipse(self.screen,self.life_color,(self.object1.x-11,self.object1.y-15,50,50),3)
    def restart(self):
        if self.mode_game["Training AI"]:self.reset()
        if self.mode_game["Player"] or self.mode_game["AI"]:self.change_mains(1,self.RED,150,self.reset)
    def reset(self):
        self.FPS=60
        self.objects()
        self.nuances()
        self.calls_elements()
        self.life=100
        self.state_life=[2,False]
        self.floor_fall=False
        self.scores=self.reward=0
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