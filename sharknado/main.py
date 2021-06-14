import pygame
from pygame.locals import (DOUBLEBUF,
                           FULLSCREEN,
                           KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_ESCAPE, K_UP, K_DOWN, K_RCTRL, K_LCTRL,
                           K_KP_ENTER,K_RETURN
                           )
from fundo import Fundo
from elementos import ElementoSprite
import random
import math


class Inicio: # menu
  def __init__(self, size=(1000, 600), fullscreen=False):
        self.elementos = {}
        pygame.init()
        self.tela = pygame.display.set_mode(size, flags=False, depth=16)
        self.fundo = Fundo(image="fundo_menu.png")
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN

        self.screen_size = self.tela.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Sharknado')
        self.run = True
  
  def desenha_letras(self):
      fonte_titulo = pygame.font.SysFont ("arialblack",75)
      texto_titulo = fonte_titulo.render("MENU",True, (0,0,0))
      screen = pygame.display.get_surface()
      screen.blit(texto_titulo,(380,50)) 
      
      imagem = pygame.image.load ("imagens/instrucoes4.png")
      screen.blit(imagem, (100,200))

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
                if event.key == K_RETURN:
                    if __name__ == '__main__':
                        J= Jogo ()
                        J.loop()
                if event.key == (K_KP_ENTER):
                    if __name__ == '__main__':
                        J= Jogo ()
                        J.loop()   
                             
        pygame.display.flip()  

class Jogo:
    def __init__(self, size=(1200, 680), fullscreen=False):
        self.elementos = {}
        pygame.init()
        self.tela = pygame.display.set_mode(size)
        self.fundo = Fundo()
        self.jogador = None
        self.interval = 0
        self.nivel = 1
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN

        self.screen_size = self.tela.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Sharknado')
        self.run = True

    def manutenção(self):
        r = random.randint(0, 100)
        x = random.randint(1, self.screen_size[0])
        if r > (40 * len(self.elementos["virii"])):
            enemy = Virus([0, 0])
            size = enemy.get_size()
            enemy.set_pos([x, 0])
            self.elementos["virii"].add(enemy)

    def muda_nivel(self):
        xp = self.jogador.get_pontos()
        if xp > 10 and self.nivel == 1:
			    self.fundo = Fundo("mar2.png")
			    self.nivel = 2
			    self.jogador.set_lives(self.jogador.get_lives() + 3)
		    elif xp > 20 and self.nivel == 2:
			    self.fundo = Fundo("mar3.png")
			    self.nivel = 3
			    self.jogador.set_lives(self.jogador.get_lives() + 3)
		    elif xp > 30 and self.nivel == 3:
			    self.fundo = Fundo("mar4.png")
			    self.nivel = 4
			    self.jogador.set_lives(self.jogador.get_lives() + 3)
		    elif xp > 40 and self.nivel == 4:
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
                    action(o)
            return hitted

        elif isinstance(elemento, pygame.sprite.Sprite):
            if pygame.sprite.spritecollide(elemento, list, 1):
                action()
            return elemento.morto

    def ação_elemento(self):
        self.verifica_impactos(self.jogador, self.elementos["tiros_inimigo"],
                               self.jogador.alvejado)
        if self.jogador.morto:
            self.run = False
            return

        # Verifica se o personagem trombou em algum inimigo
        self.verifica_impactos(self.jogador, self.elementos["virii"],
                               self.jogador.colisão)
        if self.jogador.morto:
            self.run = False
            return
        # Verifica se o personagem atingiu algum alvo.
        hitted = self.verifica_impactos(self.elementos["tiros"],
                                        self.elementos["virii"],
                                        Virus.alvejado)

        # Aumenta a pontos baseado no número de acertos:
        self.jogador.set_pontos(self.jogador.get_pontos() + len(hitted))

    def trata_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False

        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                self.run = False
            elif key == K_UP:
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
                if key in (K_LCTRL, K_RCTRL):
                    self.interval = 0
                    self.jogador.atira(self.elementos["tiros"])
       
        if event.type == pygame.KEYUP:
            key = event.key
            if key == K_UP or key == K_DOWN or key == K_RIGHT or key == K_LEFT:
                self.jogador.stop()

    def loop(self):
        clock = pygame.time.Clock()
        dt = 16
        self.elementos['virii'] = pygame.sprite.RenderPlain(Virus([120, 50]))
        self.jogador = Jogador ([self.screen_size[0]/2, 400], 5)
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        self.elementos['tiros'] = pygame.sprite.RenderPlain()
        self.elementos['tiros_inimigo'] = pygame.sprite.RenderPlain()
        #self.musica()
        while self.run:
            clock.tick(1000 / dt)

            self.trata_eventos()
            self.ação_elemento()
            self.manutenção()
            self.interval += 1
            
            # Atualiza Elementos
            self.atualiza_elementos(dt)
            self.muda_nivel()

            # Desenhe no back buffer
            self.desenha_elementos()
            self.desenha_vidas()
            self.desenha_pontos()
            self.desenha_nivel()
            pygame.display.flip()

    def desenha_vidas(self):
      fonte = pygame.font.SysFont ("arialblack",24)
      texto = fonte.render(f"Vidas: {self.jogador.lives}", True, (255,0,0))
      screen = pygame.display.get_surface()
      screen.blit(texto,(30, int(self.screen_size[1] * 0.02)))

    def desenha_pontos(self):
      fonte = pygame.font.SysFont ("arialblack",24)
      texto = fonte.render(f"Pontos: {self.jogador.pontos}", True, (255,0,0))
      screen = pygame.display.get_surface()
      screen.blit(texto,(30, int(self.screen_size[1] * 0.07)))

    def desenha_nivel(self):
      fonte = pygame.font.SysFont ("arialblack",24)
      texto = fonte.render(f"Nível: {self.nivel}", True, (255,0,0))
      screen = pygame.display.get_surface()
      screen.blit(texto,(30, int(self.screen_size[1] * 0.12)))

#    def musica(self):
#      pygame.mixer.music.load("imagens/shark_song.mp3")
#      pygame.mixer.music.load("imagens/shark_song2.mp3")
#      pygame.mixer.music.play(-1)

class Nave (ElementoSprite):
    def __init__(self, position, lives=0, speed=[0, 0], image=None, new_size=[40, 100],new_angle=None):
        self.acceleration = [5, 5]
        if not image:
            image = "barco.png"
        super().__init__(image, position, speed, new_size,new_angle)
        self.set_lives(lives)

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives

    def colisão(self):
        if self.get_lives() <= 0:
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)

    def atira(self, lista_de_tiros, image=None):
        s = list(self.get_speed())
        s[1] *= 2
        Tiro(self.get_pos(), s, image, lista_de_tiros)

    def alvejado(self):
        if self.get_lives() < 1:
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)

    @property
    def morto(self):
        return self.get_lives() == 0

    def accel_top(self):
        speed = self.get_speed()
        self.set_speed((speed[0], - self.acceleration[1]))
        old_angle = self.get_angle()
        if old_angle != 360:    
            self.rotate(old_angle, 360)

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
        if old_angle != -90:    
            self.rotate(old_angle, -90)
    
    def stop(self):
        self.set_speed((0, 0))


class Virus(Nave):
    def __init__(self, position, lives=1, speed=None, image=None, size=(100, 100),new_angle=None):
        if not image:
            image = "tubarao.png"
        super().__init__(position, lives, speed, image, size)


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

    def __init__(self, position, lives=10, image=None, new_size=[65, 150], new_angle=None):
        if not image:
            image = "barco.png"
        super().__init__(position, lives, [0, 0], image, new_size,new_angle)
        self.pontos = 0

    def update(self, dt):
        move_speed = (self.speed[0] * dt / 16,
                      self.speed[1] * dt / 16)
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
        return (self.rect.center[0], self.rect.top)

    def get_pontos(self):
        return self.pontos

    def set_pontos(self, pontos):
        self.pontos = pontos

    def atira(self, lista_de_tiros, image=None):
        l = 1
        if self.pontos > 10: l = 3
        if self.pontos > 50: l = 5

        p = self.get_pos()
        angle = self.get_angle()
        speeds = self.get_fire_speed(l, angle)
        for s in speeds:
            Tiro(p, s, image, lista_de_tiros,[15,100],angle)

    def get_fire_speed(self, shots,direction):
        speeds=[]

        if shots <= 0:
            return speeds

        if shots == 1:
            speeds += [(- 0 * math.cos(math.radians(direction)) + (-7) * math.sin(math.radians(direction)), 0 * math.sin(math.radians(direction)) + (-7) * math.cos(math.radians(direction)))]

        if shots > 1 and shots <= 3:
            speeds += [(- 0 * math.cos(math.radians(direction)) + (-7) * math.sin(math.radians(direction)), 0 * math.sin(math.radians(direction)) + (-7) * math.cos(math.radians(direction)))]
            speeds += [(- 0 * math.cos(math.radians(direction - 30)) + (-7) * math.sin(math.radians(direction - 30)), 0 * math.sin(math.radians(direction - 30)) + (-7) * math.cos(math.radians(direction - 30)))]
            speeds += [(- 0 * math.cos(math.radians(direction + 30)) + (-7) * math.sin(math.radians(direction + 30)), 0 * math.sin(math.radians(direction + 30)) + (-7) * math.cos(math.radians(direction + 30)))]

        if shots > 3 and shots <= 5:
            speeds += [(- 0 * math.cos(math.radians(direction)) + (-7) * math.sin(math.radians(direction)), 0 * math.sin(math.radians(direction)) + (-7) * math.cos(math.radians(direction)))]
            speeds += [(- 0 * math.cos(math.radians(direction - 30)) + (-7) * math.sin(math.radians(direction - 30)), 0 * math.sin(math.radians(direction - 30)) + (-7) * math.cos(math.radians(direction - 30)))]
            speeds += [(- 0 * math.cos(math.radians(direction + 30)) + (-7) * math.sin(math.radians(direction + 30)), 0 * math.sin(math.radians(direction + 30)) + (-7) * math.cos(math.radians(direction + 30)))]
            speeds += [(- 0 * math.cos(math.radians(direction - 60)) + (-7) * math.sin(math.radians(direction - 60)), 0 * math.sin(math.radians(direction - 60)) + (-7) * math.cos(math.radians(direction - 60)))]
            speeds += [(- 0 * math.cos(math.radians(direction + 60)) + (-7) * math.sin(math.radians(direction + 60)), 0 * math.sin(math.radians(direction + 60)) + (-7) * math.cos(math.radians(direction + 60)))]

        return speeds


class Tiro(ElementoSprite):
    def __init__(self, position, speed=None, image=None, list=None, new_size=[15,100], new_angle=None):
        if not image:
            image = "arpao.png"
        super().__init__(image, position, speed, new_size, new_angle)
        if list is not None:
            self.add(list)


if __name__ == '__main__':
    I= Inicio ()
    I.main_loop()
pygame.quit()