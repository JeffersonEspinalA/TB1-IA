import pygame, sys, random
from tkinter import messagebox, Tk

# definir el tamaño de la ventana
tam = (ancho, altura) = 600, 600
ventana = pygame.display.set_mode(tam)

pygame.init()

# cuantas filas y columnas tendrá el mapa
cols, filas = 15, 15

# matriz en donde se simulara el mapa
matriz = []
# listas en donde se almacenaran los lugares a analizar (openSet) y las lugares que fueron analizadas (closeSet). 
openSet, closeSet = [], []
# lista en donde se almacenaran los lugares que pertenecen al mejor camino
camino = []

# ancho y alto de cada cuadro con resultado entero
an = ancho//cols 
al = altura//filas

# cargar y mostrar el imagenes
casaImagen = pygame.image.load('imagenes/casa.png')
dronImagen = pygame.image.load('imagenes/dron.png')
arbolImagen = pygame.image.load('imagenes/arbol.png')
casaImagen = pygame.transform.scale(casaImagen, (an, al))
dronImagen = pygame.transform.scale(dronImagen, (an, al))
arbolImagen = pygame.transform.scale(arbolImagen, (an, al))
 
def casa(x,y):
    ventana.blit(casaImagen, (x * an, y * al))

def dron(x,y):
    ventana.blit(dronImagen, (x * an, y * al))

def arbol(x,y):
    ventana.blit(arbolImagen, (x * an, y * al))

# clase en donde se especifica las coordenadas, costo y lugar anterior. Ademas, agregar lugares vecinos y definir si es un arbol
class Lugar:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.vecinos = []
        self.anterior = None
        self.pared = False
        if random.randint(0, 100) < 30:
            self.pared = True
        
    def mostrar(self, win, col):
        pygame.draw.rect(win, col, (self.x*an, self.y*al, an-1, al-1))
        if self.pared == True:
            arbol(self.x, self.y)
    
    def agregarVecinos(self, grid):
        if self.x < cols - 1:
            self.vecinos.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.vecinos.append(grid[self.x-1][self.y])
        if self.y < filas - 1:
            self.vecinos.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.vecinos.append(grid[self.x][self.y-1])
      
# funcion heuristica      
def f_heuristica(a, b):
    return (abs(a.x - b.x) + abs(a.y - b.y))

# Agregar los lugares a la matriz que simula el mapa, con sus respectivos vecinos de manera horizontal y vertical
for i in range(cols):
    arr = []
    for j in range(filas):
        arr.append(Lugar(i, j))
    matriz.append(arr)

for i in range(cols):
    for j in range(filas):
        matriz[i][j].agregarVecinos(matriz)

# generamos de forma aleatoria la posicion del punto inicial y punto objetivo
while True:
    pos_i_x = random.randint(0, cols - 1)
    pos_i_y = random.randint(0, filas - 1)
    inicio = matriz[pos_i_x][pos_i_y]
    if inicio.pared == False:
        break

while True:
    pos_f_x = random.randint(0, cols - 1)
    pos_f_y = random.randint(0, filas - 1)
    final = matriz[pos_f_x][pos_f_y]
    if (final.pared == False) and (inicio != final):
        break

#agremos el lugar inicial a la lista de lugares a analizar
openSet.append(inicio)

def main():
    # saber si se llego al punto objetivo
    meta = False
    no_meta = True
    # cuando el usuario presiona "enter", cambia a True y se empieza a usar el algoritmo
    buscar = False
    # lista de coordenadas del camino y asi el dron se pueda dirigir a la casa
    trayecto = []
    while True:
        # accion que hara el usuario
        for accion in pygame.event.get():
            # salir de la aplicación
            if accion.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # iniciar la aplicación presionando "Enter"
            if accion.type == pygame.KEYDOWN:
                if accion.key == pygame.K_RETURN:
                    buscar = True
        # algoritmo A star
        if buscar:
            # si hay lugares para analizar
            if len(openSet) > 0:
                # empezamos analizando al lugar que tengo menor valor f
                ganador = 0
                for i in range(len(openSet)):
                    if openSet[i].f < openSet[ganador].f:
                        ganador = i

                actual = openSet[ganador]
                
                # si se llego al punto objetivo
                if actual == final:
                    # se almacenas los lugares por donde se paso desde el punto inicial
                    aux = actual
                    while aux.anterior:
                        camino.append(aux.anterior)
                        trayecto.append((aux.x, aux.y))
                        aux = aux.anterior 
                    trayecto.append((aux.x, aux.y))
                    if not meta:
                        meta = True
                        print("Done")
                    elif meta:
                        continue
                
                # analizamos el lugar actual
                if meta == False:
                    openSet.remove(actual)
                    closeSet.append(actual)

                    # definimos los valores de los vecinos del lugar actual
                    for vecino in actual.vecinos:
                        # saber si el vecino ya fue analizado o es un arbol, para no analizarlo
                        if vecino in closeSet or vecino.pared:
                            continue
                        tempG = actual.g + 1

                        newPath = False
                        # si se llego a ese lugar anteriormente, pero se encontró una manera mas optima para llegar ahí
                        if vecino in openSet:
                            if tempG < vecino.g:
                                vecino.g = tempG
                                newPath = True
                        # si es la primera vez que se llega a ese lugar
                        else:
                            vecino.g = tempG
                            newPath = True
                            openSet.append(vecino)
                        
                        # definimos el valor h, f y el valor anterior de cada vecino
                        if newPath:
                            vecino.h = f_heuristica(vecino, final)
                            vecino.f = vecino.g + vecino.h
                            vecino.anterior = actual
            # no hay lugares para analizar y no se encontró el camino
            else:
                if no_meta:
                    Tk().wm_withdraw()
                    messagebox.showinfo(":(", "No se encontro el camino")
                    no_meta = False
        
        # colorear los cuadros del mapa
        for i in range(cols):
            for j in range(filas):
                spot = matriz[j][i]
                spot.mostrar(ventana, (52, 229, 88))
                if meta and spot in camino:
                    spot.mostrar(ventana, (25, 120, 255))
                elif spot in closeSet:
                    spot.mostrar(ventana, (0, 255, 255))
                elif spot in openSet:
                    spot.mostrar(ventana, (0, 255, 255))
                try:
                    if spot == final:
                        spot.mostrar(ventana, (52, 229, 88))
                except Exception:
                    pass
        
        # mostrar casa y dron
        casa(pos_f_x, pos_f_y)
        dron(pos_i_x, pos_i_y)

        # movimiento del dron
        for i in range(len(trayecto) - 1, 0, -1):
            d_x, d_y = trayecto[i]
            dron(d_x, d_y)
            if (i > 1):
                pygame.display.update()
                pygame.time.delay(100)
                spot = matriz[d_x][d_y]
                spot.mostrar(ventana, (25, 120, 255))
            
        pygame.display.flip()
    
main()