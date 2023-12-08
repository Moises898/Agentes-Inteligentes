import pygame
from random import randrange

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (20, 80, 240)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)

class Tablero:
    
    def __init__(self,dimensiones,filas,columnas,screen):
        """
            Inicializa los valores por defecto para la ventana y dibujar el tablero
        """
        self.dimensiones = dimensiones
        self.filas = filas
        self.columnas = columnas      
        self.tablero_logico = [[0] * self.columnas for _ in range(self.filas)]        
        self.medida = max(dimensiones)  // max(self.columnas,self.filas)        
        self.screen = screen
        self.obstaculos = []        
        
    
    def dibujarTablero(self):
        """
        Funcion que dibuja el tablero
        screen: 		referencia del lienzo donde dibujar
        medida: 		tamaño de los rectangulos		
        actual: 		rectangulo actual 
        obstaculos:     numero de obstaculos a generar
        """     	        
        obstaculos = int((self.filas * self.columnas) / 3)        
        for _ in range(0,obstaculos):
            x = randrange(0, self.columnas) 
            y = randrange(0, self.filas) 
            xobs = x * self.medida
            yobs = y * self.medida 
            self.tablero_logico[y][x] = 1
            self.obstaculos.append([yobs,xobs])
            pygame.draw.rect(self.screen,AZUL,[xobs,yobs,self.medida,self.medida])            
    
    def dibujar_ultimo_tablero(self):        
        cordenadas_agentes = list()
        for i in range(self.columnas):
            for j in range(self.filas):
                if self.tablero_logico[j][i] == 3:
                    cordenadas_agentes.append([j,i,True])
                elif self.tablero_logico[j][i] == 2:
                    cordenadas_agentes.append([j,i,False])
        self.screen.fill(NEGRO)
        for cordenada in self.obstaculos:
            pygame.draw.rect(self.screen,AZUL,[cordenada[1],cordenada[0],self.medida,self.medida])            
        for agente in cordenadas_agentes:
            self.dibujar_agente(agente[1],agente[0],agente[2])
            
    def dibujar_agente(self,x,y,presa):
        """
            presa -> True -->   3
            presa -> False ->   2
            huecos --------->   0
            obstaculo ------>   1
        """        
        self.tablero_logico[y][x] = 3 if presa else 2
        x = x * self.medida
        y = y * self.medida 
        pygame.draw.rect(self.screen,ROJO if presa else AMARILLO,[x,y,self.medida,self.medida])    
        pygame.display.flip()            
    
    def limpiar_posicion(self,x,y):        
        self.tablero_logico[y][x] = 0                   
        x = x * self.medida
        y = y * self.medida        
        pygame.draw.rect(self.screen,NEGRO,[x,y,self.medida,self.medida])  
        pygame.display.flip()      
        
        