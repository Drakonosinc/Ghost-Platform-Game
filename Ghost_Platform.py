import random
import numpy as np
from Interface import *
import torch
class ghost_platform(interface):
    def __init__(self,model=None):
        super().__init__(width=700, height=600)
        self.model=model
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
        self.mode_game={"Training AI":True,"Player":False,"AI":False}
        self.scores=self.reward=0
        self.last_movement_time = pygame.time.get_ticks()  # Initialize movement timer
    def objects(self):
        self.object1=Rect(350, self.HEIGHT-35,25,25)
        self.object2=Rect(0,0,0,0)
        self.object3=Rect(0,0,0,0)
        self.object4=Rect(0,0,0,0)
        self.object5=Rect(0,0,0,0)
    def generate_nuances(self):
        return np.column_stack((np.random.choice(np.arange(25, self.WIDTH-50, 115), 15),np.random.choice(np.arange(-500, 0, 200), 15))).tolist()
    def nuances(self):self.matrix=[self.generate_nuances(),self.generate_nuances()]
    def elements(self,matrix,speed_fall,object_name,width,height,type_object,image=None,restx=0,resty=0,object_name2=None,object_name3=None,current_elements=None,next_elements1=None,next_elements2=None):
        for coords in matrix:
            coords[1]+=speed_fall
            rect=Rect(coords[0],coords[1],width,height)
            if coords[1]>=self.HEIGHT:self.reset_coords(coords)
            self.collision(rect,type_object,coords)
            self.screen.blit(image,(coords[0]-restx,coords[1]-resty))
        sorted_elements = sorted(matrix, key=lambda t: t[1],reverse=True)
        for i, elements in enumerate(sorted_elements):
            if elements[1] < self.object1.y:
                current_elements = elements
                next_elements1 = sorted_elements[i + 1] if i + 1 < len(sorted_elements) else None
                next_elements2 = sorted_elements[i + 2] if i + 2 < len(sorted_elements) else None
                break
        if current_elements:setattr(self, object_name, Rect(current_elements[0],current_elements[1],width,height))
        # if next_elements1:setattr(self, object_name2, Rect(next_elements1[0],next_elements1[1],width,height))
        # if next_elements2:setattr(self, object_name3, Rect(next_elements2[0],next_elements2[1],width,height))
    def collision(self,objects,type_object,coords):
        if self.object1.colliderect(objects):
            match type_object:
                case "platform":
                    self.object1.y=objects.y-25
                    self.down_gravity=0
                    self.isjumper=True
                    if self.mode_game["Training AI"]:self.reward += 0.2
                case "meteorite":
                    if not self.state_life[1]:
                        self.reset_coords(coords)
                        self.state_life[0]=0
                        self.sound_meteorite.play()
                        if self.mode_game["Training AI"]:self.reward -= 20
                    else:
                        self.state_life[1]=False
                        self.reset_coords(coords)
                        self.sound_meteorite.play()
                        if self.mode_game["Training AI"]:self.reward -= 5
                case "potion" if self.life<100:
                    self.state_life[0]=1
                    self.reset_coords(coords)
                    self.sound_health.play()
                    if self.mode_game["Training AI"]:self.reward += 10
                case "shield" if not self.state_life[1]:
                    self.state_life[1]=True
                    self.reset_coords(coords)
                    self.sound_shield.play()
                    if self.mode_game["Training AI"]:self.reward += 15
    def reset_coords(self,coords):
        coords[1]=random.choice(np.arange(-500, 0, 200))
        coords[0]=random.choice(np.arange(25, self.WIDTH-50, 115))
    def calls_elements(self):
        self.elements(self.matrix[0],3,"object2",100,25,"platform",self.floor,0,10)
        self.elements([self.matrix[1][0]],6,"object3",50,35,"meteorite",self.meteorite,0,45)
        self.elements([self.matrix[1][1]],2,"object4",35,25,"potion",self.potion,0,10)
        self.elements([self.matrix[1][2]],4,"object5",45,25,"shield",self.shield,5,10)
    def events(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_movement_time > 5000:self.floor_fall = True
        if self.object1.x < 0:self.object1.x = 0
        elif self.object1.x > self.WIDTH - 25:self.object1.x = self.WIDTH - 25
        if not self.isjumper:self.fall()
        if self.object1.y>=self.HEIGHT-35 and not self.floor_fall:
            self.object1.y=self.HEIGHT-35
            self.isjumper=True
        elif not self.object1.colliderect(self.object2):
            self.fall()
            if self.object1.y<=-20:
                self.object1.y=-15
                self.down_gravity=self.gravity
            if self.object1.y>=self.HEIGHT+50:
                if self.mode_game["Training AI"]:self.reward -= 30
                self.sounddeath()
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
            self.last_movement_time = pygame.time.get_ticks()  # Update movement timer
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
        self.scores=0
    def get_state(self):
        print(self.object1.x, self.object1.y, self.object2.x, self.object2.y,self.object3.x,self.object3.y,self.object4.x,self.object4.y,self.object5.x,self.object5.y)
        return np.array([self.object1.x, self.object1.y, self.object2.x, self.object2.y,self.object3.x,self.object3.y,self.object4.x,self.object4.y,self.object5.x,self.object5.y])
    def type_mode(self):
        if self.mode_game["Training AI"]:self.actions_AI(self.model)
        if self.mode_game["AI"]:self.actions_AI(self.model_training)
    def actions_AI(self,model):
        state=self.get_state()
        action = model(torch.tensor(state, dtype=torch.float32)).detach().numpy()
        self.AI_actions(action)
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()
    def AI_actions(self, action):
        probabilities = self.softmax(action)
        chosen_action = np.argmax(probabilities)
        # print(f"Probabilidades: {probabilities}, Acción elegida: {chosen_action}")
        if chosen_action == 0:self.object1.x -= 5
        elif chosen_action == 1:self.object1.x += 5
        elif chosen_action == 2 and self.isjumper:self.jump()
    def run_with_model(self):
        self.running = True
        scores = self.reward = 0
        while self.running and self.game_over == False:
            self.handle_keys()
            if self.main == -1:
                if self.mode_game["AI"] or self.mode_game["Training AI"]:self.type_mode()
                self.draw()
                self.events()
                self.calls_elements()
            self.time_delta = self.clock.tick(self.FPS)/1000.0
            self.manager.update(self.time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()
        return scores

if __name__ == "__main__":
    game=ghost_platform()
    game.run_with_model()