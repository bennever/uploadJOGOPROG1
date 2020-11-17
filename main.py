import pyxel
import math
import time
import random

LARGURA_TELA = 255
ALTURA_TELA = 120
COR_FUNDO = 0
BOLA_TAMANHO = 2
BOLA_VELOCIDADE = 2
BARRA_TAMANHO = 8


class Vec2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Vec2_norm:
    def __init__(self,x,y):
        self.magnitude = math.sqrt(x*x + y*y)

        self.x = x / self.magnitude * BOLA_VELOCIDADE
        self.y = y / self.magnitude * BOLA_VELOCIDADE

class Bola:
    def __init__(self,px,py,vx,vy):
        self.position = Vec2(px,py)
        self.velocidade = Vec2_norm(vx,vy)

    def update(self):
        self.position.x += self.velocidade.x
        self.position.y += self.velocidade.y

        if self.position.y >= ALTURA_TELA - BOLA_TAMANHO:
            self.velocidade.y = -self.velocidade.y

        if self.position.y <= BOLA_TAMANHO:
            self.velocidade.y = -self.velocidade.y

class HitBox:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1 # coordenada x do canto superior esquerdo
        self.y1 = y1 # coordenada y do canto superior esquerdo
        self.x2 = x2 # coordenada x do canto inferior direito
        self.y2 = y2 # coordenada y do canto inferior direito

class Barra:
    color = 10

    def __init__(self,px,py):
        self.position = Vec2(px,py)
        self.velocidade = 0
        self.hitbox = HitBox(
            self.position.x - BARRA_TAMANHO / 4, # coordenada x superior esquerda
            self.position.y - BARRA_TAMANHO, # coordenada y superior esquerda
            self.position.x + BARRA_TAMANHO / 4, # coordenada x inferior direita
            self.position.y + BARRA_TAMANHO,  # coordenada y inferior direita
        )

    def update(self):
        self.position.y += self.velocidade

        self.hitbox = HitBox(
            self.position.x - BARRA_TAMANHO / 4,
            self.position.y - BARRA_TAMANHO,
            self.position.x + BARRA_TAMANHO / 4,
            self.position.y + BARRA_TAMANHO
        )

        if self.position.y < BARRA_TAMANHO:
            self.position.y = BARRA_TAMANHO
            self.velocidade = 0

        if self.position.y >= ALTURA_TELA - BARRA_TAMANHO:
            self.position.y = ALTURA_TELA - BARRA_TAMANHO
            self.velocidade = 0

        if pyxel.btnp(pyxel.KEY_W):
            self.velocidade = -2

        if pyxel.btnp(pyxel.KEY_S):
            self.velocidade = 2

class App:
    def __init__(self):
        pyxel.init(LARGURA_TELA, ALTURA_TELA)
        self.bola = Bola(20, 20, 2, 2)
        self.barras = [Barra(2,10), Barra(LARGURA_TELA - 2,10)]
        self.score = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.bola.update()

        for barra in self.barras:
            barra.update()
            
            if (barra.hitbox.x1 < self.bola.position.x < barra.hitbox.x2
            and barra.hitbox.y1 < self.bola.position.y < barra.hitbox.y2):
                self.bola.velocidade.x = -self.bola.velocidade.x
                self.score += 1
                print(self.score)
               
        if (self.bola.position.x < 0 or
            self.bola.position.x > LARGURA_TELA):
            pyxel.quit()

    def draw(self):
        pyxel.cls(COR_FUNDO)

        pyxel.text(
            LARGURA_TELA / 2,
            ALTURA_TELA / 12,
            str(self.score),
            10)

        pyxel.circ(self.bola.position.x, self.bola.position.y, BOLA_TAMANHO, 10)

        for barra in self.barras:
            pyxel.rect(
                barra.hitbox.x1,
                barra.hitbox.y1,
                barra.hitbox.x2,
                barra.hitbox.y2,
                barra.color
            )

App()
