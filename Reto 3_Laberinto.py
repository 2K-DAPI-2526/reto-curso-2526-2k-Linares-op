import pygame
import random
import sys

pygame.init()

TAM_CELDA = 30
FILAS = 21
COLUMNAS = 31
MARGEN_SUPERIOR = 60

ANCHO = COLUMNAS * TAM_CELDA
ALTO = FILAS * TAM_CELDA + MARGEN_SUPERIOR

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego del Laberinto")

reloj = pygame.time.Clock()

fuente_grande = pygame.font.SysFont("arial", 60)
fuente = pygame.font.SysFont("arial", 30)

BLANCO = (240,240,240)
NEGRO = (30,30,30)
ROJO = (231,76,60)
AZUL = (52,152,219)
GRIS = (210,210,210)

def crear_laberinto():

    laberinto = [["X" for _ in range(COLUMNAS)] for _ in range(FILAS)]
    direcciones = [(2,0),(-2,0),(0,2),(0,-2)]

    pila = [(1,1)]
    laberinto[1][1] = " "

    while pila:

        x,y = pila[-1]
        vecinos = []

        for dx,dy in direcciones:

            nx = x + dx
            ny = y + dy

            if 1 <= nx < FILAS-1 and 1 <= ny < COLUMNAS-1:
                if laberinto[nx][ny] == "X":
                    vecinos.append((nx,ny,dx,dy))

        if vecinos:

            nx,ny,dx,dy = random.choice(vecinos)

            laberinto[x + dx//2][y + dy//2] = " "
            laberinto[nx][ny] = " "

            pila.append((nx,ny))

        else:
            pila.pop()

    return laberinto


def iniciar_nivel():

    global laberinto, jugador_x, jugador_y, gano, tiempo_inicio

    laberinto = crear_laberinto()

    inicio = (1,1)
    salida = (FILAS-2,COLUMNAS-2)

    laberinto[inicio[0]][inicio[1]] = "E"
    laberinto[salida[0]][salida[1]] = "S"

    jugador_x, jugador_y = inicio
    gano = False

    tiempo_inicio = pygame.time.get_ticks()

    return salida


salida = iniciar_nivel()

retardo_movimiento = 120
ultimo_movimiento = pygame.time.get_ticks()

boton_siguiente = pygame.Rect(ANCHO//2 - 120, ALTO//2 + 40, 240, 50)
boton_salir = pygame.Rect(ANCHO//2 - 120, ALTO//2 + 110, 240, 50)

def dibujar_laberinto():

    for i in range(FILAS):
        for j in range(COLUMNAS):

            rect = pygame.Rect(j*TAM_CELDA, i*TAM_CELDA + MARGEN_SUPERIOR, TAM_CELDA, TAM_CELDA)

            if laberinto[i][j] == "X":
                pygame.draw.rect(pantalla,NEGRO,rect)
            else:
                pygame.draw.rect(pantalla,BLANCO,rect)

            if (i,j) == salida:
                pygame.draw.rect(pantalla,ROJO,rect)

    pygame.draw.rect(pantalla,AZUL,(jugador_y*TAM_CELDA, jugador_x*TAM_CELDA + MARGEN_SUPERIOR, TAM_CELDA, TAM_CELDA))


def dibujar_tiempo():

    if gano:
        tiempo = tiempo_final
    else:
        tiempo = pygame.time.get_ticks() - tiempo_inicio

    segundos = tiempo // 1000
    minutos = segundos // 60
    segundos = segundos % 60

    texto = fuente.render(f"Tiempo: {minutos:02}:{segundos:02}", True, (0,0,0))

    pantalla.blit(texto,(20,15))


def dibujar_barra_superior():
    pygame.draw.rect(pantalla, GRIS, (0,0,ANCHO,MARGEN_SUPERIOR))


def ventana_victoria():

    capa = pygame.Surface((ANCHO,ALTO))
    capa.set_alpha(200)
    capa.fill((180,180,180))
    pantalla.blit(capa,(0,0))

    texto = fuente_grande.render("¡GANASTE!",True,(0,0,0))
    pantalla.blit(texto,(ANCHO//2 - texto.get_width()//2, ALTO//2 - 160))

    texto_tiempo = fuente.render(f"Tiempo: {tiempo_victoria}",True,(0,0,0))
    pantalla.blit(texto_tiempo,(ANCHO//2 - texto_tiempo.get_width()//2, ALTO//2 - 80))

    pygame.draw.rect(pantalla,GRIS,boton_siguiente)
    pygame.draw.rect(pantalla,GRIS,boton_salir)

    t1 = fuente.render("Siguiente nivel",True,(0,0,0))
    t2 = fuente.render("Salir",True,(0,0,0))

    pantalla.blit(t1,(boton_siguiente.x + 40, boton_siguiente.y + 10))
    pantalla.blit(t2,(boton_salir.x + 90, boton_salir.y + 10))



ejecutando = True
tiempo_victoria = ""
tiempo_final = 0

while ejecutando:

    reloj.tick(60)

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if gano and evento.type == pygame.MOUSEBUTTONDOWN:

            if boton_siguiente.collidepoint(evento.pos):
                salida = iniciar_nivel()

            if boton_salir.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()

    teclas = pygame.key.get_pressed()
    tiempo_actual = pygame.time.get_ticks()

    if not gano and tiempo_actual - ultimo_movimiento > retardo_movimiento:

        nx,ny = jugador_x,jugador_y

        if teclas[pygame.K_UP]:
            nx -= 1

        elif teclas[pygame.K_DOWN]:
            nx += 1

        elif teclas[pygame.K_LEFT]:
            ny -= 1

        elif teclas[pygame.K_RIGHT]:
            ny += 1

        if 0 <= nx < FILAS and 0 <= ny < COLUMNAS:
            if laberinto[nx][ny] != "X":
                jugador_x,jugador_y = nx,ny

        if (jugador_x,jugador_y) == salida:

            gano = True
            tiempo_final = pygame.time.get_ticks() - tiempo_inicio

            segundos = tiempo_final // 1000
            minutos = segundos // 60
            segundos = segundos % 60

            tiempo_victoria = f"{minutos:02}:{segundos:02}"

        ultimo_movimiento = tiempo_actual

    pantalla.fill(BLANCO)

    dibujar_barra_superior()
    dibujar_laberinto()
    dibujar_tiempo()

    if gano:
        ventana_victoria()

    pygame.display.update()
