# No estoy actualziando self.x y y
class Agente:
    
    def __init__(self,x, y, presa, step):        
        self.presa = presa
        self.step = step 
        self.x = x
        self.y = y               
        
    def izquierda(self):        
        new_x = self.x - self.step                    
        new_y = self.y
        return [new_x,self.x],[new_y,self.y]
        
    def derecha(self):        
        new_x = self.x + self.step        
        new_y = self.y
        return [new_x,self.x],[new_y,self.y]
    
    def arriba(self):        
        new_y = self.y - self.step        
        new_x = self.x
        return [new_x,self.x],[new_y,self.y]
    
    def abajo(self):        
        new_y = self.y + self.step        
        new_x = self.x
        return [new_x,self.x],[new_y,self.y]
    
    def diagonal_arriba_izquierda(self):        
        new_x = self.x - self.step
        new_y = self.y - self.step        
        return [new_x,self.x],[new_y,self.y]
    
    def diagonal_abajo_izquierda(self):        
        new_x = self.x - self.step
        new_y = self.y + self.step        
        return [new_x,self.x],[new_y,self.y]
    
    def diagonal_arriba_derecha(self):        
        new_x = self.x + self.step
        new_y = self.y - self.step        
        return [new_x,self.x],[new_y,self.y]
    
    def diagonal_abajo_derecha(self):        
        new_x = self.x + self.step
        new_y = self.y + self.step                
        return [new_x,self.x],[new_y,self.y]
    
    def vision(self):
        casillas = []        
        for i in range(self.y - self.step, self.y + self.step + 1):
            for j in range(self.x - self.step, self.x + self.step + 1):
                casillas.append([i,j])
        return casillas
    
    def actualizar_indices(self,x,y):
        self.x = x
        self.y = y