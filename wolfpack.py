from agentes import Agente
from random import choice,randrange
import pygame
import pygame_gui
from tablero import Tablero
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from time import sleep

DIMENSIONES = (600, 600)
FONDO = (0, 0, 0)
FILAS = 15
COLUMNAS = 15
AGENTES = 2


get_acciones = lambda agente: {
    'izquierda': agente.izquierda,
    'derecha': agente.derecha,
    'arriba': agente.arriba,
    'abajo': agente.abajo,
    'diagonal_arriba_izquierda': agente.diagonal_arriba_izquierda,
    'diagonal_abajo_izquierda': agente.diagonal_abajo_izquierda,
    'diagonal_arriba_derecha': agente.diagonal_arriba_derecha,
    'diagonal_abajo_derecha': agente.diagonal_abajo_derecha,        
}


pygame.init()
screen = pygame.display.set_mode(DIMENSIONES)
pygame.display.set_caption("Wolfpack")
game_over = False
clock = pygame.time.Clock()   
gui_manager = pygame_gui.UIManager(DIMENSIONES) 
# Muestra input para numero de agentes
length = 50
agents_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((((DIMENSIONES[0] - length) // 2) - length*4, length), (length*3, length)), text='Numero de Agentes:', manager=gui_manager)
agents_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(((DIMENSIONES[0] - length*3) // 2, length), (length*2, length)), manager=gui_manager)
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((DIMENSIONES[0] - length*3) // 2, length*2), (length*2, length)), text='Start', manager=gui_manager)
score = 0
score_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((DIMENSIONES[0] // 2.5, 0), (100, 50)), text=f'Score: {score}', manager=gui_manager)
score_label.update(.15)
screen.fill(FONDO)
button_pressed = False
threads_flag = Event()
tablero = Tablero(DIMENSIONES,FILAS,COLUMNAS,screen)
lista_agentes = []
# Crea los agentes
def crear_agentes(n_agentes,tablero,agentes_list,presa):            
    i = 0
    while True:
        x = randrange(0,COLUMNAS)
        y = randrange(0, FILAS)    
        if tablero.tablero_logico[y][x] == 0:            
            tablero.dibujar_agente(x,y,presa)       
            agentes_list.append(Agente(x,y,presa,1))                 
            i += 1
        if i == n_agentes:
            break
# Crea y ejecuta un Thread para cada agente
def worker(agente,tablero_juego):   
    global score, threads_flag       
    while True:
        acciones = get_acciones(agente)
        indice = choice(list(acciones.keys()))
        idx_x,idx_y = acciones[indice]()      
        if (0 <= idx_x[0] < COLUMNAS and 0 <= idx_y[0] < FILAS 
            and tablero_juego.tablero_logico[idx_y[0]][idx_x[0]] == 0):   
            agente.actualizar_indices(idx_x[0],idx_y[0])
            tablero.limpiar_posicion(idx_x[1],idx_y[1])
            tablero.dibujar_agente(idx_x[0],idx_y[0],agente.presa)                   
            if not agente.presa:
                casillas = agente.vision()
                for cordenada in casillas:
                    if (0 <= cordenada[1] < COLUMNAS and 0 <= cordenada[0] < FILAS 
                        and tablero_juego.tablero_logico[cordenada[0]][cordenada[1]] == 3):
                        print("La presa ha sido cazada")                              
                        score += 10                        
                        threads_flag.set()   
                break
            break

# Flujo principal de GUI        
while not game_over and score < 100:            
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            game_over = True
        if evento.type == pygame.USEREVENT and not button_pressed:
            if evento.user_type == pygame_gui.UI_BUTTON_START_PRESS:
                if evento.ui_element == start_button:     
                    agents_input.hide()               
                    agents_label.hide()
                    start_button.hide()                    
                    num_agents = int(agents_input.get_text()) 
                    # Dibuja el tablero en pantalla                    
                    screen.fill(FONDO)
                    tablero.dibujarTablero()                   
                    crear_agentes(num_agents,tablero,lista_agentes,False)
                    crear_agentes(1,tablero,lista_agentes,True)
                    #pool = ThreadPoolExecutor(num_agents)                    
                    button_pressed = True    
    if button_pressed:        
        for agente in lista_agentes:             
            worker(agente,tablero)
            #pool.submit(worker,*(agente,tablero))
            if threads_flag.is_set():
                break
            
    if threads_flag.is_set():                        
        sleep(2)                
        presa_eliminada = lista_agentes.pop()                
        tablero.limpiar_posicion(presa_eliminada.x,presa_eliminada.y)
        tablero.dibujar_ultimo_tablero()                      
        score_label.set_text(f'Score: {score}')                 
        print("Generando nueva presa")
        crear_agentes(1,tablero,lista_agentes,True)
        threads_flag.clear()                
        
    
    gui_manager.process_events(evento)
    gui_manager.update(30)    
    gui_manager.draw_ui(screen)    
    pygame.display.flip()    
    sleep(.15)
    # pygame.time.delay(150)
    clock.tick(60)
pygame.quit()
