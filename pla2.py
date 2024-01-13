from asyncio import shield
import pygame,random
# ignore the Spanish-English mixes, sometimes I forget to write only in one
pygame.init()
screen_width = 700
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ghost Platform")
clock = pygame.time.Clock()
FPS = 60
pausa_valor,valor1 = 0, 0
running = True
blanco = (255, 255, 255)
negro = (0, 0, 0)
gris = (127, 127, 127)
amarillo= (255,255,0)
verde=(0,255,0)
rojo= (255,0,0)
azul=(0,0,255)
sky_blue=(0,191,255)
low_red=(247, 66, 27)
dorado=(216, 150, 35)
ACELERAR_JUEGO = pygame.USEREVENT + 1
TIEMPO_ACELERACION = 5000 
pygame.time.set_timer(ACELERAR_JUEGO, TIEMPO_ACELERACION)
fuente=pygame.font.Font(None,25)
fuente2=pygame.font.Font(None,50)
espacio=pygame.image.load("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/images/espacio.png")
espacio=pygame.transform.scale(espacio,(700,600))
p=pygame.image.load("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/images/flyghost.png")
p=pygame.transform.scale(p,(35,35))
s=pygame.image.load("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/images/suelo1.png")
s=pygame.transform.scale(s,(100,40))
m=pygame.image.load("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/images/meteorito.png")
m=pygame.transform.scale(m,(50,85))
po=pygame.image.load("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/images/pocion1.png")
po=pygame.transform.scale(po,(35,40))
shi=pygame.image.load("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/images/shield1.png")
shi=pygame.transform.scale(shi,(50,50))
pygame.mixer.init()
s_jump=pygame.mixer.Sound("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/sounds/jump.aiff")
s_meteor=pygame.mixer.Sound("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/sounds/meteor.mp3")
s_health=pygame.mixer.Sound("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/sounds/health.flac")
s_back_fo=pygame.mixer.Sound("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/sounds/back_fo.wav")
s_game_lose=pygame.mixer.Sound("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/sounds/game_lose.flac")
s_shield=pygame.mixer.Sound("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/sounds/shield.wav")
s_jump.set_volume(0.5)
s_game_lose.set_volume(0.4)
background=negro
my_list = []
my_list2 = []
my_list3 = []
my_list4 = []
list_y=[]
list_x=[]

for i in range(-500, 0, 200):list_y.append(i)

for i in range(25, screen_width-50, 115):list_x.append(i)

for _ in range(15):
    x = random.choice(list_x)
    x1=random.choice(list_x)
    y = random.choice(list_y)
    my_list.append([x, y])
my_list2.append([x, y])
my_list3.append([x1, y])
my_list4.append([x1, y])

class Personaje:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.rect1 = pygame.Rect(0, 0, 50, 10)
        self.rect2 = pygame.Rect(0, 0, 0, 0)
        self.rect3 = pygame.Rect(0, 0, 50, 10)
        self.rect4 = pygame.Rect(0, 0, 50, 10)
        self.velocidad_y = 0
        self.saltando = False
        self.salto_inicial = -15
        self.gravedad = 0.25
        self.mover_x = 0
        self.pausa = False
        self.flor=False
        self.game_over=False
        self.reset=False
        self.puntaje=0
        self.vida=100
        self.vida_dec=False
        self.vida_aci=False
        self.color=verde
        self.inter=True
        self.color_p=sky_blue
        self.color_p1=dorado
        self.color_fp=negro
        self.color_p2=sky_blue
        self.color_p3=dorado
        self.color_fp1=negro
        self.shield=False
        self.max_score=0
        self.s_v=True
        self.damage_me=False
    def actualizar(self):
        if self.pausa==False and self.game_over==False and self.inter==False:
            if not self.saltando:
                self.velocidad_y += self.gravedad
                self.rect.y += self.velocidad_y

            if self.rect.y>=screen_height-35 and self.flor==False:
                self.rect.y = screen_height-35
                self.saltando = True

            elif not self.rect.colliderect(self.rect2):
                self.velocidad_y += self.gravedad
                self.rect.y += self.velocidad_y
                if self.rect.y<=0:
                    self.rect.y = 0
                    self.velocidad_y = 0
                    self.saltando = False
                elif self.rect.y>=screen_height:
                    self.game_over=True
                    self.vida=0
                    self.color=negro
                    s_meteor.play(loops=0)
    def saltar(self):
        if self.saltando and self.pausa==False and self.game_over==False and self.inter==False:
            self.velocidad_y = self.salto_inicial
            s_jump.play(loops=0)
            self.saltando = False
    def mover(self, m):
        if self.pausa==False and self.game_over==False and self.inter==False:
            self.mover_x = m
            self.rect.x += self.mover_x
    def dibujar(self, pantalla):
        if self.game_over==False and self.inter==False:pantalla.blit(p,(self.rect.x,self.rect.y))
    def objetos(self,pantalla):
        if self.inter==False:
            for coords in my_list:
                if self.pausa==False and self.game_over==False:
                    coords[1]+=3
                    self.rect2=pygame.Rect(coords[0],coords[1],100,25)
                    if coords[1]>=screen_height:
                        coords[1]=random.choice(list_y)
                        coords[0]=random.choice(list_x)
                    elif self.rect.colliderect(self.rect2):
                        self.rect.y = self.rect2.y - 25
                        self.velocidad_y = 0
                        self.saltando = True
                        self.flor=True
                        self.puntaje+=1
                pantalla.blit(s,(coords[0],coords[1]))
                if self.reset:
                    coords[1]=random.choice(list_y)
                    coords[0]=random.choice(list_x)
    def acelerar_juego(self,n):
        if self.inter==False:
            global FPS
            FPS += n 
            if FPS>=61:self.flor=True
    def menu_pausar(self,pantalla):
        if self.pausa and self.game_over==False and self.inter==False:
            pygame.draw.rect(pantalla,negro,(screen_width/2-100,screen_height/2-200,200,300),10)
            texto_pausa=fuente.render("PAUSA",True,negro)
            pantalla.blit(texto_pausa,(screen_width/2-30,screen_height/2-180))
    def enemigo_meteorito(self,pantalla):
        if self.inter==False:
            for coords2 in my_list2:
                if self.pausa==False and self.game_over==False:
                    coords2[1]+=6
                    self.rect1=pygame.Rect(coords2[0],coords2[1],60,20)
                    if coords2[1]>=screen_height:
                        coords2[1]=random.choice(list_y)
                        coords2[0]=random.randint(50,650)
                    elif self.rect.colliderect(self.rect1) and self.vida_aci==False:
                        coords2[1]=random.choice(list_y)
                        coords2[0]=random.randint(50,650)
                        s_meteor.play(loops=0)
                        s_health.stop()
                        if self.shield is False:self.vida_dec=True
                        elif self.shield:self.damage_me=True
                pantalla.blit(m,(coords2[0],coords2[1]-50))
                if self.reset:
                    coords2[1]=random.choice(list_y)
                    coords2[0]=random.randint(50,650)
    def shield_fall(self,pantalla):
        if self.inter is False:
            for coords4 in my_list4:
                if self.pausa is False and self.game_over is False:
                    coords4[1]+=4
                    self.rect4=pygame.Rect(coords4[0],coords4[1],60,20)
                    if coords4[1]>=screen_height:
                        coords4[1]=random.choice(list_y)
                        coords4[0]=random.randint(50,650)
                    elif self.rect.colliderect(self.rect4) and self.shield is False:
                        coords4[1]=random.choice(list_y)
                        coords4[0]=random.randint(50,650)
                        self.shield=True
                        s_shield.play(loops=0)
                        s_health.stop()
                pantalla.blit(shi,(coords4[0],coords4[1]-30))
                if self.reset:
                    coords4[1]=random.choice(list_y)
                    coords4[0]=random.randint(50,650)
    def pocion(self,pantalla):
        if self.inter==False:
            for coords3 in my_list3:
                if self.pausa==False and self.game_over==False:
                    coords3[1]+=2
                    self.rect1=pygame.Rect(coords3[0],coords3[1],60,20)
                    if coords3[1]>=screen_height:
                        coords3[1]=random.choice(list_y)
                        coords3[0]=random.randint(50,650)
                    elif self.rect.colliderect(self.rect1) and self.vida<100 and self.vida_dec==False:
                        coords3[1]=random.choice(list_y)
                        coords3[0]=random.randint(50,650)
                        self.vida_aci=True
                        s_health.play(loops=0)
                pantalla.blit(po,(coords3[0],coords3[1]-40))
                if self.reset:
                    coords3[1]=random.choice(list_y)
                    coords3[0]=random.randint(50,650)
    def g_over(self,pantalla):
        if self.game_over and self.inter==False:
            pantalla.fill(gris)
            fuente2=pygame.font.Font(None,50)
            text_game_over=fuente2.render("GAME OVER",True,negro)
            text_reset=fuente.render("Reset Press R",True,negro)
            text_m=fuente.render("Press E for Menu",True,negro)
            pantalla.blit(text_game_over,(screen_width/2-100,screen_width/2-200))
            pantalla.blit(text_reset,(screen_width/2-50,screen_width/2-160))
            pantalla.blit(text_m,(screen_width/2-60,screen_width/2-140))
            self.reset=True
            s_health.stop()
            if self.s_v:
                s_game_lose.play(loops=0)
                self.s_v=False
    def game_reset(self):
        global FPS
        if self.reset and self.inter is False:
            self.rect.x=350
            self.rect.y=screen_height-35
            self.game_over=False
            self.flor=False
            self.reset=False
            FPS=60
            self.puntaje=0
            self.vida=100
            self.pausa=False
            self.vida_dec,self.vida_aci=False,False
            self.color=verde
            self.s_v=True
            self.shield=False
            self.damage_me=False
            s_game_lose.stop()
    def puntaje_j(self,pantalla):
        if self.inter==False:
            text_p=fuente.render(f"Puntaje {self.puntaje}",True,amarillo)
            pantalla.blit(text_p,(10,screen_height-25))
    def vida_p(self,pantalla):
        if self.inter==False:
            pygame.draw.rect(pantalla,negro,(50,8,105,20),4)
            pygame.draw.rect(pantalla,self.color,(52,11,self.vida,15))
            text_vida=fuente.render("Vida",True,self.color)
            if self.pausa==False and self.game_over==False:
                if self.vida_dec:self.vida-=1
                if self.vida_aci:self.vida+=1
                if self.vida==100:
                    self.color=verde
                    self.vida_aci=False
                elif self.vida==75:
                    self.color=sky_blue
                    self.vida_dec,self.vida_aci=False,False
                elif self.vida==50: 
                    self.color=amarillo
                    self.vida_dec,self.vida_aci=False,False
                elif self.vida==25: 
                    self.color=rojo
                    self.vida_dec,self.vida_aci=False,False
                elif self.vida<=0:
                    self.color=negro
                    self.game_over=True
            pantalla.blit(text_vida,(10,10))    
    def fondo(self,pantalla):
            if self.inter==False:pantalla.blit(espacio,(0,0))
    def interfaz(self, pantalla):
        if self.inter:
            pantalla.fill(background)
            s_back_fo.play(loops=-1)
            text = "Press for Play"
            text1 ="Press for Exit"
            text2 ="Ghost Platform"
            text_play = fuente.render(text, True, self.color_p1)
            text_exit = fuente.render(text1, True, self.color_p3)
            text_puntaje = fuente.render(f"Highest Score {self.max_score}", True, dorado)
            text_game = fuente2.render(text2, True, blanco)
            x = screen_width / 2 - 65
            y = screen_height / 2 - 100
            self.rect_inter = pygame.Rect(x - 5, y - 2, 125, 22)
            self.rect_inter1 = pygame.Rect(x - 5, y + 25, 125, 22)
            pygame.draw.rect(pantalla, self.color_fp, self.rect_inter,)
            pygame.draw.rect(pantalla, self.color_fp1, self.rect_inter1,)
            pantalla.blit(text_play, (x, y))
            pantalla.blit(text_exit, (x, y+27))
            pantalla.blit(text_puntaje, (x-7, y-40))
            pantalla.blit(text_game, (x-70, y-80))
            pygame.draw.rect(pantalla, self.color_p, self.rect_inter, 2)
            pygame.draw.rect(pantalla, self.color_p2, self.rect_inter1, 2)
        else:s_back_fo.stop()
    def m_score(self):
        if self.puntaje>=self.max_score:
            self.max_score=self.puntaje
    def guardar_puntajes(self):
        with open("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/score.txt", "w") as archivo:
            archivo.write(str(self.max_score) + "\n")
    def cargar_puntajes(self):
        with open("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/2/final_version/score.txt", "r") as archivo:
            score = archivo.readline()
            self.max_score = int(score)
    def shield_draw(self,pantalla):
        if self.damage_me:
            self.shield=False
            self.damage_me=False
        if self.shield and self.inter is False:pygame.draw.ellipse(pantalla,self.color,(self.rect.x-7,self.rect.y-10,50,50),3)
personaje = Personaje(350, screen_height-35)
personaje.cargar_puntajes()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        elif event.type == ACELERAR_JUEGO: personaje.acelerar_juego(0.5)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key==pygame.K_UP: personaje.saltar()
            if event.key == pygame.K_d or event.key==pygame.K_RIGHT: valor1 = 6
            if event.key == pygame.K_a or event.key==pygame.K_LEFT: valor1 = -6
            if event.key == pygame.K_r: personaje.game_reset()
            if event.key==pygame.K_e:
                personaje.game_reset()
                personaje.inter=True
            if event.key==pygame.K_p:
                personaje.pausa=True
                pausa_valor+=1
                if pausa_valor%2==0:personaje.pausa=False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a or event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:valor1 = 0
        mouse=pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if personaje.rect_inter.collidepoint(event.pos) and personaje.inter:personaje.inter=False
            if personaje.rect_inter1.collidepoint(event.pos) and personaje.inter:running=False
        if mouse[0]>280 and mouse[0]<400 and mouse[1]>200 and mouse[1]<220 and personaje.inter: personaje.color_p,personaje.color_p1,personaje.color_fp=verde,sky_blue,blanco
        else: personaje.color_p,personaje.color_p1,personaje.color_fp=sky_blue,dorado,negro
        if mouse[0]>280 and mouse[0]<400 and mouse[1]>225 and mouse[1]<245 and personaje.inter: personaje.color_p2,personaje.color_p3,personaje.color_fp1=verde,sky_blue,blanco
        else: personaje.color_p2,personaje.color_p3,personaje.color_fp1=sky_blue,dorado,negro
    personaje.fondo(screen)
    personaje.actualizar()
    personaje.dibujar(screen)
    personaje.mover(valor1)
    personaje.objetos(screen)
    personaje.menu_pausar(screen)
    personaje.enemigo_meteorito(screen)
    personaje.pocion(screen)
    personaje.shield_fall(screen)
    personaje.shield_draw(screen)
    personaje.g_over(screen)
    personaje.puntaje_j(screen)
    personaje.vida_p(screen)
    personaje.interfaz(screen)
    personaje.m_score()
    personaje.guardar_puntajes()
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()