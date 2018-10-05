# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 18:46:20 2018

@author: delga
"""
from skimage import io
from math import ceil
import numpy as np

class laberinto():
    imagen = 0
    estados_validos = []
    filas = 0
    columnas = 0
    canales = 0
    numero_de_estados = 0
    agente = []
    imagen_recorrida = 0
    colores = [255,0,0]
    imagen_mostrar = 0
    tamaño_agente = 5
    estados_disponibles = [0,0,0,0]  #derecha, arriba, izquierda, abajo
    
    def __init__(self,ruta,colores = [255,0,0]):
        self.imagen = io.imread(ruta)
        self.filas,self.columnas,self.canales = self.imagen.shape
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.imagen[i,j,0]>10:
                    self.estados_validos.append((i,j))
        self.numero_de_estados = len(self.estados_validos)
        self.imagen_mostrar = np.copy(self.imagen)
        self.imagen_recorrida = np.copy(self.imagen)
        self.colores = colores
        
    def set_player(self,semilla):
        np.random.seed(semilla)
        posicion = ceil(self.numero_de_estados*np.random.random())
        x,y = self.estados_validos[posicion]
        agente_establecido = False
        while agente_establecido == False:
            Agente_M = self.imagen[x:x+self.tamaño_agente,y:y+self.tamaño_agente,0]
            espacion_disponible = np.sum(Agente_M>10)
            if espacion_disponible==self.tamaño_agente**2:
                self.agente=(x,y)
                agente_establecido = True
            else:
                posicion = ceil(self.numero_de_estados*np.random.random())
                x,y = self.estados_validos[posicion]
        self.dibuja_agente()
        self.acciones_validas()        

    def acciones_validas(self):
        #######################derecha, arriba, izquierda, abajo
        ######################izquierdaiii
        x,y = self.agente
        if y-1 > self.tamaño_agente:
            Agente_M = self.imagen[x:x+self.tamaño_agente,y-1:y-1+self.tamaño_agente,0]
            espacion_disponible = np.sum(Agente_M>10)
            if espacion_disponible==self.tamaño_agente**2:
                self.estados_disponibles[2] = 1
            else:
                self.estados_disponibles[2] = 0
        else:
            self.estados_disponibles[2] = 0
        ################# Arriba
        if x-1 > self.tamaño_agente:
            Agente_M = self.imagen[x-1:x-1+self.tamaño_agente,y:y+self.tamaño_agente,0]
            espacion_disponible = np.sum(Agente_M>10)
            if espacion_disponible==self.tamaño_agente**2:
                self.estados_disponibles[1] = 1
            else:
                self.estados_disponibles[1] = 0
        else:
            self.estados_disponibles[1] = 0
        ################# derecha
        if y+1 < self.imagen.shape[1]-self.tamaño_agente:
            Agente_M = self.imagen[x:x+self.tamaño_agente,y+1:y+1+self.tamaño_agente,0]
            espacion_disponible = np.sum(Agente_M>10)
            if espacion_disponible==self.tamaño_agente**2:
                self.estados_disponibles[0] = 1
            else:
                self.estados_disponibles[0] = 0
        else:
            self.estados_disponibles[0] = 0
        ################# Abajo
        if x+1 < self.imagen.shape[0]-self.tamaño_agente:
            Agente_M = self.imagen[x+1:x+1+self.tamaño_agente,y:y+self.tamaño_agente,0]
            espacion_disponible = np.sum(Agente_M>10)
            if espacion_disponible==self.tamaño_agente**2:
                self.estados_disponibles[3] = 1
            else:
                self.estados_disponibles[3] = 0
        else:
            self.estados_disponibles[3] = 0
    
    def dibuja_agente(self):
        x,y = self.agente
        self.imagen_mostrar = np.copy(self.imagen)
        self.imagen_mostrar[x:x+self.tamaño_agente,y:y+self.tamaño_agente,0] = self.colores[0]
        self.imagen_mostrar[x:x+self.tamaño_agente,y:y+self.tamaño_agente,1] = self.colores[1]
        self.imagen_mostrar[x:x+self.tamaño_agente,y:y+self.tamaño_agente,2] = self.colores[2]
        
        self.imagen_recorrida[x:x+self.tamaño_agente,y:y+self.tamaño_agente,0] = self.colores[1]
        self.imagen_recorrida[x:x+self.tamaño_agente,y:y+self.tamaño_agente,1] = self.colores[0]
        self.imagen_recorrida[x:x+self.tamaño_agente,y:y+self.tamaño_agente,2] = self.colores[2]
    
    def mov_iz(self):
        if self.estados_disponibles[2] == 1:
            x,y = self.agente
            y=y-1
            self.agente = (x,y)
            self.dibuja_agente()
            self.acciones_validas()
        else:
            print('Tope pared')
        
    def mov_arr(self):
        if self.estados_disponibles[1] == 1:
            x,y = self.agente
            x=x-1
            self.agente = (x,y)
            self.dibuja_agente()
            self.acciones_validas()
        else:
            print('Tope pared')
            
    def mov_der(self):
        if self.estados_disponibles[0] == 1:
            x,y = self.agente
            y=y+1
            self.agente = (x,y)
            self.dibuja_agente()
            self.acciones_validas()
        else:
            print('Tope pared')          
            
    def mov_ab(self):
        if self.estados_disponibles[3] == 1:
            x,y = self.agente
            x=x+1
            self.agente = (x,y)
            self.dibuja_agente()
            self.acciones_validas()
        else:
            print('Tope pared')    


    def set_posicion(self,posicion):
        self.agente = posicion

    def get_estados_validos(self):
        return self.estados_validos
    
    def get_imagen(self):
        return self.imagen
    
    def get_imagen_mostrar(self):
        return self.imagen_mostrar
    
    def get_imagen_recorrida(self):
        return self.imagen_recorrida
    
    def get_acciones_validas(self):
        return self.estados_disponibles

    def get_agente(self):
        return self.agente
         
if __name__ == '__main__':
    import cv2
    Mi_laberinto = laberinto('Laberinto.png')
    estados = Mi_laberinto.get_estados_validos()
    Mi_laberinto.set_player(8)
    while True:
        imagen_mostrar = Mi_laberinto.get_imagen_mostrar()
        imagen_recorrida = Mi_laberinto.get_imagen_recorrida()
        cv2.imshow('Laberinto',imagen_mostrar)
        cv2.imshow('color',imagen_recorrida)
        pulsacion = cv2.waitKey(0)
        if pulsacion == ord('i'):
            break
        elif pulsacion == ord('a'):
            Mi_laberinto.mov_iz()
            
        elif pulsacion == ord('w'):
            Mi_laberinto.mov_arr()        

        elif pulsacion == ord('d'):
            Mi_laberinto.mov_der()             
            
        elif pulsacion == ord('s'):
            Mi_laberinto.mov_ab()              
    cv2.destroyAllWindows()    
                     
                