# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 23:27:33 2018

@author: delga
"""
import numpy as np
class asdc:
    raiz = 0
    posibles_movimientos = 0
    muevete = 0 
    colamovimientos = [] 
    visitados = {}
    nodo = 0
    rama = []
    puntos_meta = [] 
    arbol =[]
    backtrackingList = []
    ruta = []
    backtracking = False
    color = [255,0,0]
    def __init__(self,nodo,puntos_meta):
        self.puntos_meta = puntos_meta
        self.raiz = nodo
        self.nodo = nodo
        self.rama.append(self.nodo)
        self.visitados[nodo] = []
        self.muevete = nodo
        
    def mov(self,posibles_movimientos,nodo):
        movimientos = []
        self.muevete = 0
        for movimiento in posibles_movimientos:
            if movimiento != 0:
                if movimiento not in self.rama  and movimiento not in self.visitados[nodo]:
                    movimientos.append(movimiento)
        if movimientos:

            if self.backtracking == True:
                self.rama.append(nodo)
                self.muevete = nodo
            else:
                rnodos = self.visitados[nodo]
                self.muevete = self.evalua(movimientos)
                rnodos.append(self.muevete)
                self.visitados[nodo] = rnodos
                self.rama.append(self.muevete)
                if self.muevete not in self.visitados:
                    self.visitados[self.muevete] = [nodo]
            self.backtracking = False
            self.color = [255,0,0]
        else:
            if not(self.backtracking): #backtrackin
                self.ruta = self.rama
                self.arbol.append(self.rama)
                self.backtracking = True                      
            if self.rama:
                movback = self.rama.pop()
                self.muevete = movback
                self.color = [50,180,180]
            else:
                print('Termine')
    
    def evalua(self,movimientos):
        d = []
        for movimiento in movimientos:
            d.append(self.distancia(movimiento))
        d = np.array(d)
        return movimientos[np.argmin(d)]
    
    def distancia(self,nodo):
        x,y = nodo
        d = -1
        for punto in self.puntos_meta:
            x1,y1 = punto
            tem = abs(x-x1)+abs(y-y1)
            if d == -1:
                d =  tem
            elif d > tem:
                d = tem
        return d

    def get_movimiento(self):
        return self.muevete

if __name__ == '__main__':
    import cv2
    from laberinto import laberinto
    import os
    import errno
    frame_width = 700
    frame_height = 700
    Mi_laberinto = laberinto('Laberinto3.png')
    Mi_laberinto.set_player(50)#50,10
    acenso_de_colina = asdc(Mi_laberinto.get_agente(),
                                    Mi_laberinto.puntosmeta)

    path = os.getcwd()
    try:
        os.mkdir('ASCDR')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            os.rmdir('ASCDR')
            os.mkdir('ASCDR')
            pass
        
    os.chdir('ASCDR')
    laberinto_outasdc1 = cv2.VideoWriter('laberinto_outasdc1.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (frame_width,frame_height))
    recorrido_outasdc1 = cv2.VideoWriter('recorrido_outasdc1.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (frame_width,frame_height))
  
    while acenso_de_colina.muevete != 0 and Mi_laberinto.metaalc == False:
        Mi_laberinto.colores = acenso_de_colina.color
        imagen_mostrar = Mi_laberinto.get_imagen_mostrar()
        imagen_recorrida = Mi_laberinto.get_imagen_recorrida()
        laberinto = cv2.resize(imagen_mostrar,(frame_width, frame_height), interpolation = cv2.INTER_CUBIC)
        recorrido = cv2.resize(imagen_recorrida,(frame_width, frame_height), interpolation = cv2.INTER_CUBIC)
        cv2.imshow('Laberinto',laberinto)
        cv2.imshow('color',recorrido)
        laberinto_outasdc1.write(laberinto)
        recorrido_outasdc1.write(recorrido)
        pulsacion = cv2.waitKey(1)
        if pulsacion == ord('i'):
            break
        Mi_laberinto.set_agente(acenso_de_colina.get_movimiento())
        acenso_de_colina.mov(Mi_laberinto.get_posiciones_disponibles(),Mi_laberinto.get_agente())

    
    laberinto_outasdc2 = cv2.VideoWriter('laberinto_outasdc2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (frame_width,frame_height))
    recorrido_outasdc2 = cv2.VideoWriter('recorrido_outasdc2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (frame_width,frame_height))     
    
    Mi_laberinto.resetimrecorrida()
    for punto in acenso_de_colina.rama:
        imagen_mostrar = Mi_laberinto.get_imagen_mostrar()
        imagen_recorrida = Mi_laberinto.get_imagen_recorrida()
        laberinto = cv2.resize(imagen_mostrar,(frame_width, frame_height), interpolation = cv2.INTER_CUBIC)
        recorrido = cv2.resize(imagen_recorrida,(frame_width, frame_height), interpolation = cv2.INTER_CUBIC)
        cv2.imshow('Laberinto',laberinto)
        cv2.imshow('color',recorrido)
        laberinto_outasdc2.write(laberinto)
        recorrido_outasdc2.write(recorrido)
        pulsacion = cv2.waitKey(1)
        if pulsacion == ord('i'):
            break
        Mi_laberinto.set_agente(punto) 
        
        
    laberinto_outasdc1.release()
    recorrido_outasdc1.release()   
    laberinto_outasdc2.release()
    recorrido_outasdc2.release()       
    cv2.destroyAllWindows() 
    os.chdir(path)

                