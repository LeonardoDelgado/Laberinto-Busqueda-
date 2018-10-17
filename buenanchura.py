# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 14:03:04 2018

@author: delga
"""

class beal:
    raiz = 0
    posibles_movimientos = 0
    muevete = 0 
    colamovimientos = [] 
    visitados = []
    movimietos_disponibles = False
    cola = []
    ruta_actual = []
    nodo = 0
    tamaño = 0
    def __init__(self,raiz,posibles_movimientos,tamaño):
        self.raiz = raiz
        self.tamaño = tamaño
        self.cola.append(raiz)
        self.posibles_movimientos = posibles_movimientos
        self.revisaryagregar()
        
        
    def revisaryagregar(self):
        self.muevete = 0
        if self.cola:
            self.ruta_actual = self.cola.pop(0)
            if type(self.ruta_actual)==type([]):
                self.nodo = self.ruta_actual[-1]
            else:
                self.nodo = self.ruta_actual
                self.ruta_actual = [self.ruta_actual]
            self.marcarnodosvisitados(self.nodo)
            for movimiento in self.posibles_movimientos:
                if movimiento != 0:
                    a = self.movnotinvisitados(movimiento)
                    if not(a):
                        self.marcarnodosvisitados(movimiento)
                        self.cola.append(self.ruta_actual+[movimiento])
            
            if type(self.cola[0])==type([]):
                self.muevete = self.cola[0][-1]
            else:
                self.muevete = self.cola[0]
                
        
    def mov(self,posibles_movimientos):
        self.posibles_movimientos = posibles_movimientos
        self.revisaryagregar()
        
    def get_movimiento(self):
        return self.muevete
    
    def marcarnodosvisitados(self, nodo):
        x,y = nodo
        for x1 in range(x,x+self.tamaño):
            for y1  in range(y,y+self.tamaño):
                if (x1,y1) not in self.visitados:
                    self.visitados.append((x1,y1))
                
    def movnotinvisitados(self,movimiento):
        x,y = movimiento
        visitado = True 
        for x1 in range(x,x+self.tamaño):
            for y1  in range(y,y+self.tamaño):
                if (x1,y1) not in self.visitados:
                    visitado = False
                    return visitado
        return visitado                    
    
if __name__ == '__main__':
    import cv2
    from laberinto import laberinto
    Mi_laberinto = laberinto('Laberinto3.png')
    Mi_laberinto.set_player(10)#50,10
    busqueda_en_anchura = beal(Mi_laberinto.get_agente(),
                                    Mi_laberinto.get_posiciones_disponibles(),
                                    tamaño = Mi_laberinto.tamaño_agente)
    Mi_laberinto.set_agente(busqueda_en_anchura.get_movimiento())
    while busqueda_en_anchura.muevete != 0:
        busqueda_en_anchura.mov(Mi_laberinto.get_posiciones_disponibles())
        Mi_laberinto.set_agente(busqueda_en_anchura.get_movimiento())
        if Mi_laberinto.metaalc == True:
            break
        imagen_mostrar = Mi_laberinto.get_imagen_mostrar()
        imagen_recorrida = Mi_laberinto.get_imagen_recorrida()
        cv2.imshow('Laberinto',cv2.resize(imagen_mostrar,(600, 600), interpolation = cv2.INTER_CUBIC))
        cv2.imshow('color',cv2.resize(imagen_recorrida,(600, 600), interpolation = cv2.INTER_CUBIC))
        pulsacion = cv2.waitKey(1)
        if pulsacion == ord('i'):
            break

    Mi_laberinto.resetimrecorrida()
    for punto in busqueda_en_anchura.cola[0]:
        imagen_mostrar = Mi_laberinto.get_imagen_mostrar()
        imagen_recorrida = Mi_laberinto.get_imagen_recorrida()
        cv2.imshow('Laberinto',cv2.resize(imagen_mostrar,(600, 600), interpolation = cv2.INTER_CUBIC))
        cv2.imshow('color',cv2.resize(imagen_recorrida,(600, 600), interpolation = cv2.INTER_CUBIC))
        pulsacion = cv2.waitKey(1)
        if pulsacion == ord('i'):
            break
        Mi_laberinto.set_agente(punto) 

        
        
    cv2.destroyAllWindows()       