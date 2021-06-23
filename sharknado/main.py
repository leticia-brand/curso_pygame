import pygame
from pygame.locals import (DOUBLEBUF, FULLSCREEN, KEYDOWN, KEYUP, K_LEFT,
                           K_RIGHT, QUIT, K_ESCAPE, K_UP, K_DOWN, K_RCTRL,
                           K_LCTRL, K_KP_ENTER, K_RETURN, K_p, K_c)
from fundo import Fundo
from elementos import ElementoSprite
import math
import random

class Inicio:  # menu
    def __init__(self, size=(1200, 650), fullscreen=False):
        self.elementos = {}
        pygame.init()
        self.tela = pygame.display.set_mode(size, flags=False, depth=16)
        self.fundo = Fundo(image="fundo_menu.png")
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN

        self.screen_size = self.tela.get_size()
        pygame.mouse.set_visible(1)
        pygame.display.set_caption('Sharknado')
        self.run = True

    def desenha_letras(self):
        fonte_titulo = pygame.font.SysFont("arialblack", 75)
        texto_titulo = fonte_titulo.render("MENU", True, (0, 0, 0))
        screen = pygame.display.get_surface()
        screen.blit(texto_titulo, (470, 50))

        imagem = pygame.image.load("imagens/instrucoes4.png")
        screen.blit(imagem, (50, 240))

    def atualiza_menu(self, dt):
        self.fundo.update(dt)
        for v in self.elementos.values():
            v.update(dt)

    def desenha_menu(self):
        self.fundo.draw(self.tela)
        for v in self.elementos.values():
            v.draw(self.tela)

    def main_loop(self):
        clock = pygame.time.Clock()
        dt = 16
        pygame.mixer.music.load("imagens/mar_calmo.wav")
        pygame.mixer.music.play(-1)
        while self.run:
            clock.tick(1000 / dt)
            self.atualiza_menu(dt)
            self.desenha_menu()
            self.desenha_letras()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                    if ((event.key == (K_KP_ENTER))
                            or (event.key == (K_RETURN))):
                        if __name__ == '__main__':
                            J = Jogo()
                            J.loop()

            pygame.display.flip()

class Pause:
    def __init__(self, size=(1200, 650), fullscreen=False):
        self.run = True
            
    def desenha_pause(self):
        fonte1 = pygame.font.SysFont("arialblack", 80)
        texto_pause = fonte1.render("PAUSADO", True, (200, 0, 0))
        screen = pygame.display.get_surface()
        screen.blit(texto_pause, (385, 150))
        
        #retangulo = pygame.draw.rect(screen, (255,255,255), (220, 300, 765, 80))
        
        fonte2 = pygame.font.SysFont("arialblack", 50)
        texto2 = fonte2.render("Pressione C para continuar", True, (0, 0, 0))
        screen.blit(texto2, (230, 300))

    def pause_loop(self):		
            pause = "pausado"
            clock = pygame.time.Clock()
            
            pygame.mixer.music.load("imagens/shark_song2.mp3")
            pygame.mixer.music.pause()
            
            while pause == "pausado":
                clock.tick(1000 / 16)
                self.desenha_pause()
                
                event = pygame.event.poll()
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == (K_c):
                        pygame.mixer.music.load("imagens/shark_song2.mp3")
                        pygame.mixer.music.play(-1)
                        pause = "play"   
                pygame.display.flip()

class Jogo:
    def __init__(self, size=(1200, 650), fullscreen=False):
        self.elementos = {}
        self.arraias = []
        self.espadas = []
        self.polvos = []
        self.tubarao = []
        pygame.init()
        self.tela = pygame.display.set_mode(size)
        self.fundo = Fundo("mar.png")
        self.jogador = None
        self.interval = 0
        self.nivel = 1
        self.contador = 0
        self.spaw_espada = 1
        self.spaw_polvo = 1
        self.spaw_Tubarao = 1
        self.mover = True
        self.barra = -1
        self.tubarao_live = 150
        self.tubarao_existe = False
        self.spaw_pos_mini_tubarao = 0
        self.spaw_espada_tubarao_run = False
        self.spaw_espada_tubarao = 0
        self.test = 0
        self.repetir_mini_tubarao = False
        self.lista_modo = 0
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN

        self.screen_size = self.tela.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption("Sharknado")
        self.run = True

    def set_pos(self, tiro):
        self.elementos["tiros_inimigo"].add(tiro)

    def manutenção(self, pos):
        
        if self.nivel<5:
        
            #Arraia
            
            r = random.randint(0, 100)
            x = random.randint(1, self.screen_size[0])
            if r > (10 * (6 - self.nivel) * len(self.arraias)):
                enemy = Arraia([0, 0], speed = [0, 1 + self.nivel])
                enemy.set_pos([x, 0])
                self.elementos["fish"].add(enemy)
                self.arraias.append(enemy)
                        
                #Espada
                      
            if (self.contador == self.spaw_espada):
                self.spaw_espada = self.contador + 30*(5-self.nivel)*(random.randint(1, 3) + 5)
                if self.nivel > 1:
                    if random.randint(1, 2) == 1:
                        enemy = Espada([-50, pos[1]], speed = (2, 0), new_angle = 90, tempo_inicial = self.contador)
                        enemy.set_pos([-50, pos[1]])
                    else:
                        enemy = Espada([self.screen_size[0] + 50, pos[1]], speed = (-2, 0), new_angle = -90, tempo_inicial = self.contador)
                        enemy.set_pos([self.screen_size[0] + 50, pos[1]])
                    self.elementos["fish"].add(enemy)
                    self.espadas.append(enemy)            
            
                
                #Polvo
                
            if self.contador == self.spaw_polvo:
                self.spaw_polvo = self.contador + 20*(5-self.nivel)*(random.randint(5, 10) + 5)
                if self.nivel > 2:
                    if len(self.polvos) < 1:
                        r = random.randint(1, 2)
                        if r == 1:
                            enemy = Polvo([-50, -50], lives=4, speed = (2, 2), tempo_inicial = self.contador)
                            enemy.set_pos([-50, -50])
                        elif r == 2:
                            enemy = Polvo([self.screen_size[0] + 50, -50], speed = (-2, 2), tempo_inicial = self.contador)
                            enemy.set_pos([self.screen_size[0] + 50, -50])
                            
                        self.elementos["fish"].add(enemy)
                        self.polvos.append(enemy)
                        
            
                        
        for n in self.espadas:
            n.parar(self.contador)
            n.correr(self.contador, self.nivel)
            if self.nivel==5:
                s = n.get_speed()
                n.set_speed([-2*s[0], s[1]])
            
        for n in self.polvos:
            n.parar(self.contador)
            tiro = n.tinta(self.contador, pos, self.nivel)
            if tiro and self.nivel<5:
                self.elementos["tiros_inimigo"].add(tiro)  
            if self.nivel==5:
                n.set_speed([0, -3])
                  
        # Tubarao
        
        if self.nivel == 5:
            Modo = self.barra
            if self.tubarao_existe == False:
                self.spaw_Tubarao = self.contador
                self.tubarao_existe = True
                
            if self.tubarao_existe:
                    
                if self.contador == self.spaw_Tubarao:
                    boss = Tubarao([0, 0], speed=(0, 1), tempo_inicial = self.contador)
                    boss.set_pos([self.screen_size[0]/2, -400])
                    self.elementos["Shark"].add(boss)
                    self.tubarao.append(boss)
                    self.mover = False                        
                    
                if len(self.tubarao) > 0:
                    boss = self.tubarao[0]
                    
                if Modo == -1:
                        Modo = boss.parar(self.contador)
                        self.jogador.set_speed([0, 1])

                elif Modo == 0:
                    Modo = boss.iniciar(self.contador)
                    if Modo == 1:
                        boss.tempo_inicial = self.contador
                        
                elif Modo > 0:
                    self.mover = True
                    self.tubarao_live = boss.get_lives() + 1
                    mod = int(4 - (self.tubarao_live/50))
        
                    if Modo == 1:
                        boss.set_speed([0, 0])
                        lista_modo = [3, 4, 5]
                        i = 1
                        while i<mod:
                            lista_modo.append(random.randint(3, 5))
                            i += 1
                        
                        iniciar = boss.parar(self.contador + 100)
                        
                        self.lista_modo = lista_modo
                        
                        if iniciar==0:
                            boss.set_speed([0, -1])
                            Modo = 2
                            boss.tempo_inicial = self.contador
                            
                        
                    elif Modo == 2:
                        
                        parar = boss.parar(self.contador)
                        if parar == 0:
                            ID = random.randint(1, len(self.lista_modo))
                            Modo = self.lista_modo[ID-1]
                            del self.lista_modo[ID-1]                
                        else:
                            Modo = 2
                            
                    elif Modo == 3:
                        seguir = boss.seguir(pos, self.contador,  self.screen_size)
                        
                        if seguir:
                            boss.perseguir = False
                            if len(self.lista_modo)>0:
                                ID = random.randint(1, len(self.lista_modo))
                                Modo = self.lista_modo[ID-1]
                                del self.lista_modo[ID-1]
                            else:
                                boss.set_pos([self.screen_size[0]/2, -400])
                                boss.set_speed([0, 1])
                                old_angle = boss.get_angle()
                                boss.tempo_inicial = self.contador
                                boss.rotate(old_angle, 0)
                                Modo = 6
                        
                    elif Modo == 4:
                        arrancar = boss.arrancada(pos, self.contador, self.screen_size)
                        
                        if arrancar:
                            boss.repetir_arrancada = False
                            if len(self.lista_modo)>0:
                                ID = random.randint(1, len(self.lista_modo))
                                Modo = self.lista_modo[ID-1]
                                del self.lista_modo[ID-1]
                            else:
                                boss.set_pos([self.screen_size[0]/2, -400])
                                boss.set_speed([0, 1])
                                old_angle = boss.get_angle()
                                boss.tempo_inicial = self.contador
                                boss.rotate(old_angle, 0)
                                Modo = 6
                        
                    elif Modo == 5:
                        
                        if self.repetir_mini_tubarao == False:
                            self.repetir_mini_tubarao_num = mod + 2
                            self.repetir_mini_tubarao = True
                        
                        if self.repetir_mini_tubarao_num > 0:
                            
                            boss.set_pos([self.screen_size[0]/2, -400])
                            
                            if self.spaw_espada_tubarao_run == False:
                                self.spaw_espada_tubarao = self.contador
                                self.spaw_espada_tubarao_run = True
                                
                            if (self.contador - self.spaw_espada_tubarao)%25 == 0:
                                c = int(self.screen_size[0]/(2*mod))
                                if self.spaw_pos_mini_tubarao < self.screen_size[0]:
                                                                                    
                                    enemy = Tubarao_mini([0, 0], speed = (0, 10), new_angle = 0)
                                    enemy.set_pos([self.spaw_pos_mini_tubarao, -50])
                                    self.elementos["fish"].add(enemy)
                                    self.tubarao.append(enemy)
                                    
                                    self.spaw_pos_mini_tubarao += c
                                    
                                else:
                                    self.spaw_pos_mini_tubarao = c*random.randint(-3, 3)/3
                                    self.repetir_mini_tubarao_num -= 1
                            mini_tubarao = False
                        else:
                            mini_tubarao = True
                                        
                        if mini_tubarao:
                            self.repetir_mini_tubarao = False
                            self.spaw_espada_tubarao_run = False
                            if len(self.lista_modo)>0:
                                ID = random.randint(1, len(self.lista_modo))
                                Modo = self.lista_modo[ID-1]
                                del self.lista_modo[ID-1]
                            else:
                                boss.set_pos([self.screen_size[0]/2, -400])
                                boss.set_speed([0, 1])
                                old_angle = boss.get_angle()
                                boss.tempo_inicial = self.contador
                                boss.rotate(old_angle, 0)
                                Modo = 6
                                
                    elif Modo == 6:
                        parar = boss.parar(self.contador)
                        if parar == 0:
                            Modo = 1
                            boss.tempo_inicial = self.contador
                        else:
                            Modo = 6

                self.barra = Modo

                    
                    
        #Jogador
        
        self.jogador.fantasma(self.contador)

                    

    def muda_nivel(self):
        xp = self.jogador.get_pontos()
        if xp > 25 and self.nivel == 1:
            self.fundo = Fundo("mar2.png")
            self.nivel = 2
            self.jogador.set_lives(self.jogador.get_lives() + 3)
        elif xp > 125 and self.nivel == 2:
            self.fundo = Fundo("mar3.png")
            self.nivel = 3
            self.jogador.set_lives(self.jogador.get_lives() + 3)
        elif xp > 300 and self.nivel == 3:
            self.fundo = Fundo("mar4.png")
            self.nivel = 4
            self.jogador.set_lives(self.jogador.get_lives() + 3)
        elif xp > 500 and self.nivel == 4:
            self.fundo = Fundo("mar5.png")
            self.nivel = 5
            self.jogador.set_lives(self.jogador.get_lives() + 6)

    def atualiza_elementos(self, dt):
        self.fundo.update(dt)
        for v in self.elementos.values():
            v.update(dt)

    def desenha_elementos(self):
        self.fundo.draw(self.tela)
        for v in self.elementos.values():
            v.draw(self.tela)

    def verifica_impactos(self, elemento, list, action):
        
        if isinstance(elemento, pygame.sprite.RenderPlain):
            hitted = pygame.sprite.groupcollide(elemento, list, 1, 0)
            for v in hitted.values():
                for o in v:
                    action(o, self.contador)
            return hitted
        elif elemento.hit_box:
            if isinstance(elemento, pygame.sprite.Sprite):
                if pygame.sprite.spritecollide(elemento, list, 1):
                    action(self.contador)
                return elemento.morto
            
    def verifica_impactos_boss(self, elemento, list, action):
        if elemento.hit_box:
            if isinstance(elemento, pygame.sprite.Sprite):
                if pygame.sprite.spritecollide(elemento, list, 0):
                    action(self.contador)
                return elemento.morto

    def ação_elemento(self):
        self.verifica_impactos(self.jogador, self.elementos["tiros_inimigo"],
                               self.jogador.alvejado)
        if self.jogador.morto:
            self.jogador.set_lives = 0
            self.desenha_vidas()
            morto = "status"
            while morto =="status":
                
                fonte1 = pygame.font.SysFont("arialblack", 80)
                texto_pause = fonte1.render("GAME OVER", True, (200, 0, 0))
                screen = pygame.display.get_surface()
                screen.blit(texto_pause, (335.5, 50))
        
        
                fonte2 = pygame.font.SysFont("arialblack", 50)
                texto2 = fonte2.render("Pressione Enter para retornar ao menu", True, (0, 0, 0))
                screen.blit(texto2, (74, 500))
                imagem = pygame.image.load("imagens/game_over.png")
                screen.blit(imagem, (289, 230))
                
                pygame.display.flip()
            
                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                    self.run = False 
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == K_KP_ENTER or key == K_RETURN:
                            self.run = False
                            morto = "menu"
                            


        # Verifica se o personagem trombou em algum inimigo
        self.verifica_impactos(self.jogador, self.elementos["fish"],
                               self.jogador.colisão)
        if self.jogador.morto:
            morto = "status"
            self.jogador.set_lives = 0
            self.desenha_vidas()
            while morto =="status":
                
                fonte1 = pygame.font.SysFont("arialblack", 80)
                texto_over = fonte1.render("GAME OVER", True, (200, 0, 0))
                screen = pygame.display.get_surface()
                screen.blit(texto_over, (335.5, 50))
        
        
                fonte2 = pygame.font.SysFont("arialblack", 50)
                texto2 = fonte2.render("Pressione Enter para retornar ao menu", True, (0, 0, 0))
                screen.blit(texto2, (74, 500))
                imagem = pygame.image.load("imagens/game_over.png")
                screen.blit(imagem, (289, 230))
                
                pygame.display.flip()
            
                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                    self.run = False 
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == K_KP_ENTER or key == K_RETURN:
                            self.run = False
                            morto = "menu"
        
        # Verifica se o personagem atingiu algum alvo.
        hitted = self.verifica_impactos(self.elementos["tiros"],
                                        self.elementos["fish"],
                                        Arraia.alvejado)
        

        # Aumenta a pontos baseado no número de acertos:
        
        acerta_boss = self.verifica_impactos(self.elementos["tiros"],
                                        self.elementos["Shark"],
                                        Tubarao.alvejado)
        
        self.verifica_impactos_boss(self.jogador, self.elementos["Shark"],
                                                    self.jogador.colisão)
        
        # Aumenta a pontos baseado no número de acertos:
        self.jogador.set_pontos(self.jogador.get_pontos() + len(hitted) + 4*len(acerta_boss))

    def trata_eventos(self, move):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False               

        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                pygame.mixer.music.load("imagens/shark_song2.mp3")
                pygame.mixer.music.play(0)
                self.run = False
            elif move:
                if key == K_UP:
                    self.jogador.accel_top()
                elif key == K_DOWN:
                    self.jogador.accel_bottom()
                elif key == K_RIGHT:
                    self.jogador.accel_right()
                elif key == K_LEFT:
                    self.jogador.accel_left()

        if self.interval > 30:
            if event.type == pygame.KEYUP:
                key = event.key
                if move:
                    if key in (K_LCTRL, K_RCTRL):
                        self.interval = 0
                        self.jogador.atira(self.elementos["tiros"])
                        # arpao_som = pygame.mixer.Sound("imagens/arpao_sound.wav")
                        
                        if self.nivel <= 3:
                            arpao_som = pygame.mixer.Sound("imagens/arpao_sound.wav")
                        else:
                            arpao_som = pygame.mixer.Sound("imagens/som_canhao.wav")
                        arpao_som.play()                    
                    
                if key == (K_p):
                    if __name__ == '__main__':
                        P = Pause()
                        dp = 0
                        while True:
                            self.atualiza_elementos(dp)
                            P.pause_loop()
                            break              

        if event.type == pygame.KEYUP:
            key = event.key
            if key == K_UP or key == K_DOWN or key == K_RIGHT or key == K_LEFT:
                self.jogador.stop()

    def remover_elementos(self):
        for n in self.arraias:
            if str(n) == "<Arraia Sprite(in 0 groups)>":
                self.arraias.remove(n)
                
        for n in self.espadas:
            if str(n) == "<Espada Sprite(in 0 groups)>":
                self.espadas.remove(n)
                
        for n in self.polvos:
            if str(n) == "<Polvo Sprite(in 0 groups)>":
                self.polvos.remove(n)
                
    def loop(self):
        clock = pygame.time.Clock()
        dt = 16
        self.elementos['fish'] = pygame.sprite.RenderPlain()
        self.elementos['Shark'] = pygame.sprite.RenderPlain()
        self.jogador = Jogador([self.screen_size[0]/2, 400], 5)
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        self.elementos['tiros'] = pygame.sprite.RenderPlain()
        self.elementos['tiros_inimigo'] = pygame.sprite.RenderPlain(())
        self.musica()
        
        while self.run:
            clock.tick(1000 / dt)
            
            self.remover_elementos()
            self.muda_nivel()
            self.trata_eventos(self.mover)
            self.ação_elemento()
            
            pos = self.jogador.get_pos()
            
            self.interval += 1
            self.contador += 1            
            
            self.manutenção(pos)
            

                                
            # Atualiza Elementos
            self.atualiza_elementos(dt)
            
            # Desenhe no back buffer
            self.desenha_elementos()
            self.desenha_vidas()
            self.desenha_pontos()
            self.desenha_nivel()
            if self.tubarao_live <= 1:
                self.desenha_vitoria()
            
            if self.barra > 0:    
                self.desenha_barra(self.tubarao_live)
            pygame.display.flip()

    def desenha_vidas(self):
        fonte = pygame.font.SysFont("arialblack", 24)
        texto = fonte.render(f"Vidas: {self.jogador.lives}", True, (255, 0, 0))
        screen = pygame.display.get_surface()
        screen.blit(texto, (30, int(self.screen_size[1] * 0.02)))

    def desenha_pontos(self):
        fonte = pygame.font.SysFont("arialblack", 24)
        texto = fonte.render(f"Pontos: {self.jogador.pontos}", True, (255, 0, 0))
        screen = pygame.display.get_surface()
        screen.blit(texto, (30, int(self.screen_size[1] * 0.07)))

    def desenha_nivel(self):
        fonte = pygame.font.SysFont("arialblack", 24)
        texto = fonte.render(f"Nível: {self.nivel}", True, (255, 0, 0))
        screen = pygame.display.get_surface()
        screen.blit(texto, (30, int(self.screen_size[1] * 0.12)))
    
    def desenha_vitoria(self):
            ganhou = "status"
            while ganhou =="status":
                
                fonte1 = pygame.font.SysFont("arialblack", 80)
                texto_over = fonte1.render("PARABÉNS", True, (200, 0, 0))
                screen = pygame.display.get_surface()
                screen.blit(texto_over, (335.5, 50))
        
        
                fonte2 = pygame.font.SysFont("arialblack", 50)
                texto2 = fonte2.render("Pressione Enter para retornar ao menu", True, (0, 0, 0))
                screen.blit(texto2, (74, 500))
                imagem = pygame.image.load("imagens/vitoria.png")
                screen.blit(imagem, (289, 230))
                
                pygame.display.flip()
            
                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                    self.run = False 
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == K_KP_ENTER or key == K_RETURN:
                            self.run = False
                            ganhou = "menu"
                
        
    def desenha_barra(self, lives):
      screen = pygame.display.get_surface()
      size = self.screen_size
      
      
      bar_max_size = size[0]*0.75
      bar_pos = [size[0]*0.125, size[1]*0.9]
      bar_size = bar_max_size*lives/150
      R = int(200 * (200 - lives) / (50 + lives))
      if R>200:
          R = 200
      G = int(200 * (50 + lives) / (200 - lives))
      if G>200:
          G = 200
        
      pygame.draw.rect(screen, (0,0,0), (bar_pos[0], bar_pos[1], bar_max_size, 30))
      pygame.draw.rect(screen, (R, G, 50), (bar_pos[0], bar_pos[1], bar_size, 30))

    def musica(self):
        pygame.mixer.music.load("imagens/shark_song2.mp3")
        pygame.mixer.music.play(-1)


class Nave(ElementoSprite):
    def __init__(self,
                 position,
                 lives=0,
                 speed=[0, 0],
                 image=None,
                 new_size=[40, 100],
                 new_angle=None):
        self.acceleration = [5, 5]
        if not image:
            image = "barco.png"
        super().__init__(image, position, speed, new_size, new_angle)
        self.set_lives(lives)

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives

    def colisão(self, tempo):
        if self.get_lives() < 1:
            self.kill()
            del self
        else:
            self.set_lives(self.get_lives() - 1)
        self.hit_box = False
        self.tempo_fantasma = tempo
        
    def fantasma(self, tempo):
        if self.hit_box == False:
            if (tempo - self.tempo_fantasma) < 100:
                    
                if (tempo - self.tempo_fantasma)% 5 == 0:
                    if (int((tempo - self.tempo_fantasma)/10))% 2 == 0:
                        self.opacidade(0)
                    else:
                        self.opacidade(255)
            else:
                self.opacidade(255)
                self.hit_box = True

    def atira(self, lista_de_tiros, image=None):
        s = list(self.get_speed())
        s[1] *= 2
        if self.nivel<=3:
            Tiro(self.get_pos(), s, image, lista_de_tiros)
        elif self.nivel == 4:
            Rede(self.get_pos(), s, image, lista_de_tiros)
        elif self.nivel == 5:
            Canhao(self.get_pos(), s, image, lista_de_tiros)

    def alvejado(self, tempo):
        if self.get_lives() < 1:
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)
        self.hit_box = False
        self.tempo_fantasma = tempo

    @property
    def morto(self):
        return self.get_lives() == 0
    
    def accel_top(self):
        speed = self.get_speed()
        self.set_speed((speed[0], -self.acceleration[1]))
        old_angle = self.get_angle()
        if old_angle != 0:    
            self.rotate(old_angle, 0)

    def accel_bottom(self):
        speed = self.get_speed()
        self.set_speed((speed[0], self.acceleration[1]))
        old_angle = self.get_angle()
        if old_angle != 180:    
            self.rotate(old_angle, 180)

    def accel_left(self):
        speed = self.get_speed()
        self.set_speed((-self.acceleration[0], speed[1]))
        old_angle = self.get_angle()
        if old_angle != 90:    
            self.rotate(old_angle, 90)

    def accel_right(self):
        speed = self.get_speed()
        self.set_speed((self.acceleration[0], speed[1]))
        old_angle = self.get_angle()
        if old_angle != 270:    
            self.rotate(old_angle, 270)
    
    def stop(self):
        self.set_speed((0, 0))


class Arraia(Nave):
    def __init__(self, position, lives=0, speed=None, image=None, size=(60, 60), new_angle=None):
        if not image:
            image = "arraia.png"
        super().__init__(position, lives, speed, image, size, new_angle)
        
        
class Espada(Nave):
    def __init__(self, position, lives=9, speed=None, image=None, size=(50, 150), new_angle=None, tempo_inicial=None):
        
        self.tempo_inicial = tempo_inicial
        self.sentido = speed[0]/abs(speed[0])
        
        if not image:
            image = "espada.png"
        super().__init__(position, lives, speed, image, size, new_angle)
                
    def parar(self, tempo):
        if tempo == self.tempo_inicial + 40:
            self.set_speed((0, 0))
            
    def correr(self, tempo, nivel):
        if tempo == self.tempo_inicial + 80:
            self.set_speed((5*nivel*(self.sentido), 0))
            
            
class Polvo(Nave):
    def __init__(self, position, lives=4, speed=None, image=None, size=(120, 120), new_angle=None, tempo_inicial=None):
        
        self.tempo_inicial = tempo_inicial
        self.sentido = speed[0]/abs(speed[0])
        
        if not image:
            image = "polvo.png"
        super().__init__(position, lives, speed, image, size, new_angle)

        
    def parar(self, tempo):
        if tempo == self.tempo_inicial + 40:
            self.set_speed((0, 0))   
            
    def tinta(self, tempo, pos, nivel):
        if (tempo - self.tempo_inicial) % ((5-nivel) * 100 + 1) == 0: # + 1 p n morrer
            minha_pos = self.get_pos()
            s = [(pos[0] - minha_pos[0]), (pos[1] - minha_pos[1])]
                        
            if s[1]==0:
                if s[0]==0:
                    a = random.randint(0, 180)
                else:
                    a = 90*s[0]/abs(s[0]) + 180
            elif s[1]<0:
                a = math.ceil(math.atan((-1)*s[0]/abs(s[1]))*180/math.pi)
            else:
                a = math.ceil(math.atan(s[0]/abs(s[1]))*180/math.pi) + 180                    
                
            s = [-10 * math.sin(math.radians(a)), -10 * math.cos(math.radians(a))]
            
            shot = Tiro_Inimigo(position=minha_pos, speed=s, new_angle=a)
            return shot
        
class Tubarao(Nave):
    def __init__(self, position, lives=149, speed=None, image=None, size=[150, 320],
                 new_angle=None, tempo_inicial=None):
        self.tempo_inicial = tempo_inicial
        
        if not image:
            image = "tubarao(boss).png"
        super().__init__(position, lives, speed, image, size, new_angle)
        
        self.update_ = False
        self.correr = False
        self.perseguir = False
        self.repetir_arrancada = False
        
    def update(self, dt):
        move_speed = (self.speed[0] * dt / 16,
                      self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)
            
    def parar(self, tempo):
        if tempo == self.tempo_inicial + 350:
            self.set_speed((0, 0)) 
            return 0
        else:
            return -1
        
    def iniciar(self, tempo):
        if tempo == self.tempo_inicial + 600:
            return 1
        else:
            return 0

    def seguir(self, pos, tempo, screen_size):
        
        mod = int(4 - (self.lives/50))
        minha_pos = self.get_pos()
        
        if self.perseguir == False:
            self.tempo_perseguir = tempo + 100 *(10 + 5*mod)
            self.set_pos([screen_size[0]/2, -159])
            self.perseguir = True
            
        if tempo < self.tempo_perseguir:
                        
            distancia = [(pos[0] - minha_pos[0]), (pos[1] - minha_pos[1])]
                        
            if abs(distancia[0])<abs(distancia[1]):
                if distancia[1]>0:
                    speed = [0, 1*mod]
                    angle = 0
                else:
                    speed = [0, -1*mod]
                    angle = 180
            else:
                if distancia[0]>0:
                    speed = [1*mod, 0]
                    angle = 90
                else:
                    speed = [-1*mod, 0]
                    angle = 270
                    
            old_angle = self.get_angle()
            
            self.rotate(old_angle, angle)
            self.set_speed(speed)
            return False
            
        if (minha_pos[0] > screen_size[0] + 160) or (minha_pos[0] < -160) or (minha_pos[1] > screen_size[1] + 160) or (minha_pos[1] < -160):
            return True
        else:
            return False
            
        
    def arrancada(self, pos, tempo, screen_size):
        
        mod = int(4 - (self.lives/50))
        minha_pos = self.get_pos()
        
        if self.repetir_arrancada == False:
            self.repetir_arrancada_num = 2*mod + 3
            self.repetir_arrancada = True
            
        
        if self.repetir_arrancada_num > 0:

            if self.correr == False:
                
                self.set_speed([0, 0])
                r = random.randint(1, 4)
                self.direction = r
                            
                if r==1:
                    self.set_pos([-160, pos[1]])
                    angle = 90
                    
                elif r== 2:
                    self.set_pos([pos[0], -160])
                    angle = 0
                    
                elif r== 3:
                    self.set_pos([screen_size[0] + 160, pos[1]])
                    angle = 270
                    
                else:
                    self.set_pos([pos[0], screen_size[1] + 160])
                    angle = 180
                    
                self.tempo_correr = tempo + 10 * (6 - mod) * random.randint(3, 4)
                old_angle = self.get_angle()
                self.rotate(old_angle, angle)
                self.correr = True
                
            else:
                r = self.direction
                if r == 1:
                    if tempo == self.tempo_correr:
                        self.set_speed([mod*5, 0])
                    if minha_pos[0] > screen_size[0] + 160:
                        self.repetir_arrancada_num -= 1
                        self.correr = False
    
                elif r == 2:
                    if tempo == self.tempo_correr:
                        self.set_speed([0, mod*5])
                    if minha_pos[1] > screen_size[1] + 160:
                        self.repetir_arrancada_num -= 1
                        self.correr = False
                    
                elif r == 3:
                    if tempo == self.tempo_correr:
                        self.set_speed([-mod*5, 0])
                    if minha_pos[0] < -160:
                        self.repetir_arrancada_num -= 1
                        self.correr = False
                        
                else:
                    if tempo == self.tempo_correr:
                        self.set_speed([0, -mod*5])
                    if minha_pos[1] < -160:
                        self.repetir_arrancada_num -= 1
                        self.correr = False
                
            return False
        
        else:
            return True 
                        
                                
class Tubarao_mini(Nave):
    def __init__(self, position, lives=9, speed=None, image=None, size=(50, 115), new_angle=None):
        if not image:
            image = "tubarao(boss).png"
        super().__init__(position, lives, speed, image, size, new_angle)   


class Jogador(Nave):
    """
    A classe Player é uma classe derivada da classe GameObject.
       No entanto, o personagem não morre quando passa da borda, este só
    interrompe o seu movimento (vide update()).
       E possui experiência, que o fará mudar de nivel e melhorar seu tiro.
       A função get_pos() só foi redefinida para que os tiros não saissem da
    parte da frente da nave do personagem, por esta estar virada ao contrário
    das outras.
    """

    def __init__(self,
                 position,
                 lives=10,
                 image=None,
                 new_size=[65, 150],
                 new_angle=None):
        if not image:
            image = "barco.png"
        super().__init__(position, lives, [0, 0], image, new_size, new_angle)
        self.pontos = 0
        self.hit_box = True

    def update(self, dt):
        move_speed = (self.speed[0] * dt / 16, self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)

        if (self.rect.right > self.area.right):
            self.rect.right = self.area.right

        elif (self.rect.left < 0):
            self.rect.left = 0

        if (self.rect.bottom > self.area.bottom):
            self.rect.bottom = self.area.bottom

        elif (self.rect.top < 0):
            self.rect.top = 0

    def get_pos(self):
        return (self.rect.center)

    def get_pontos(self):
        return self.pontos

    def set_pontos(self, pontos):
        self.pontos = pontos

    def atira(self, lista_de_tiros, image=None):
        l = 1
        if self.pontos > 125: l = 3
        if self.pontos > 300: l = 5

        angle = self.get_angle()
        if angle == 0:    
            p = (self.rect.center[0], self.rect.top)
        if angle == 180:    
            p = (self.rect.center[0], self.rect.bottom)
        if angle == 90:    
            p = (self.rect.left, (self.rect.top + self.rect.bottom)/2)
        if angle == 270:    
            p = (self.rect.right, (self.rect.top + self.rect.bottom)/2)
            
        speeds = self.get_fire_speed(l, angle)
        for s in speeds:
            
            if s[1]==0:
                if s[0]==0:
                    a = random.randint(0, 180)
                else:
                    a = 90*s[0]/abs(s[0]) + 180
            elif s[1]<0:
                a = math.ceil(math.atan((-1)*s[0]/abs(s[1]))*180/math.pi)
            else:
                a = math.ceil(math.atan(s[0]/abs(s[1]))*180/math.pi) + 180
            
            if self.pontos <= 125:
                Tiro(p, s, image, lista_de_tiros, [15, 100], a)
            elif self.pontos <= 300:
                Rede(p, s, image, lista_de_tiros, [60, 60], a)
            else:
                Canhao(p, s, image, lista_de_tiros, [30, 30], a)
            
            p = self.get_pos()

    def get_fire_speed(self, shots, direction):
        speeds = []

        if shots <= 0:
            return speeds

        if shots == 1:
            speeds += [(-0 * math.cos(math.radians(direction)) +
                        (-7) * math.sin(math.radians(direction)),
                        0 * math.sin(math.radians(direction)) +
                        (-7) * math.cos(math.radians(direction)))]

        if shots > 1 and shots <= 3:
            speeds += [(-0 * math.cos(math.radians(direction)) +
                        (-7) * math.sin(math.radians(direction)),
                        0 * math.sin(math.radians(direction)) +
                        (-7) * math.cos(math.radians(direction)))]
            speeds += [(-0 * math.cos(math.radians(direction - 30)) +
                        (-7) * math.sin(math.radians(direction - 30)),
                        0 * math.sin(math.radians(direction - 30)) +
                        (-7) * math.cos(math.radians(direction - 30)))]
            speeds += [(-0 * math.cos(math.radians(direction + 30)) +
                        (-7) * math.sin(math.radians(direction + 30)),
                        0 * math.sin(math.radians(direction + 30)) +
                        (-7) * math.cos(math.radians(direction + 30)))]

        if shots > 3 and shots <= 5:
            speeds += [(-0 * math.cos(math.radians(direction)) +
                        (-7) * math.sin(math.radians(direction)),
                        0 * math.sin(math.radians(direction)) +
                        (-7) * math.cos(math.radians(direction)))]
            speeds += [(-0 * math.cos(math.radians(direction - 30)) +
                        (-7) * math.sin(math.radians(direction - 30)),
                        0 * math.sin(math.radians(direction - 30)) +
                        (-7) * math.cos(math.radians(direction - 30)))]
            speeds += [(-0 * math.cos(math.radians(direction + 30)) +
                        (-7) * math.sin(math.radians(direction + 30)),
                        0 * math.sin(math.radians(direction + 30)) +
                        (-7) * math.cos(math.radians(direction + 30)))]
            speeds += [(-0 * math.cos(math.radians(direction - 60)) +
                        (-7) * math.sin(math.radians(direction - 60)),
                        0 * math.sin(math.radians(direction - 60)) +
                        (-7) * math.cos(math.radians(direction - 60)))]
            speeds += [(-0 * math.cos(math.radians(direction + 60)) +
                        (-7) * math.sin(math.radians(direction + 60)),
                        0 * math.sin(math.radians(direction + 60)) +
                        (-7) * math.cos(math.radians(direction + 60)))]

        return speeds


class Tiro(ElementoSprite):
    def __init__(self,
                 position,
                 speed=None,
                 image=None,
                 list=None,
                 new_size=[15, 100],
                 new_angle=None):
        if not image:
            image = "arpao.png"
        super().__init__(image, position, speed, new_size, new_angle)
        if list is not None:
            self.add(list)


class Canhao (ElementoSprite):
    def __init__(self,
                 position,
                 speed=None,
                 image=None,
                 list=None,
                 new_size=[30, 30],
                 new_angle=None):
        if not image:
            image = "canhao.png"
        super().__init__(image, position, speed, new_size, new_angle)
        if list is not None:
            self.add(list)
            
class Rede (ElementoSprite):
    def __init__(self,
                 position,
                 speed=None,
                 image=None,
                 list=None,
                 new_size=[60, 60],
                 new_angle=None):
        if not image:
            image = "rede.png"
        super().__init__(image, position, speed, new_size, new_angle)
        if list is not None:
            self.add(list)

class Tiro_Inimigo(ElementoSprite):
    def __init__(self, position, speed=None, image=None,  new_size=[50, 50], new_angle=None):
        if not image:
            image = "tiro.png"
        super().__init__(image, position, speed, new_size, new_angle)

if __name__ == '__main__':
    I = Inicio()
    I.main_loop()
pygame.quit()