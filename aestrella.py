# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 23:34:36 2018

@author: delga
"""

import numpy as np
import copy
class aest:
    raiz = 0
    posibles_movimientos = 0
    muevete = 0 
    colamovimientos = [] 
    visitados = []
    nodo = 0
    rama = []
    puntos_meta = [] 
    arbol =[]
    backtrackingList = []
    ruta = []
    backtracking = False
    color = [255,0,0]
    nodos_abiertos = {}
    costo_ruta = 0
    indice_rama = 0
    nodo_backtracking = 0
    costo_backtracking = 0
    costo_backtracking_ruta = 0
    indice_rama_backtracking = 0
    destino_backtracking = 0
    costo = 0
    asenso = False
    
    def __init__(self,nodo,puntos_meta):
        self.puntos_meta = puntos_meta
        self.raiz = nodo
        self.nodo = nodo
        self.rama.append(self.nodo)
        self.visitados.append(nodo)
        self.muevete = nodo
        
    def mov(self,posibles_movimientos,nodo):
        movimientos = []
        for movimiento in posibles_movimientos:
            if movimiento != 0:
                if movimiento not in self.rama and movimiento not in self.visitados:
                    movimientos.append(movimiento)

        self.evalua(movimientos,nodo)
        if self.muevete not in self.visitados:
            self.visitados.append(self.muevete)
        print('me movi a: ', self.muevete)
        #print(movimientos)
        #print(self.nodos_abiertos)

    def evalua(self,movimientos,nodo):
        if self.backtracking == False:
            d = []
            d1L = []
            d2L = []
            costo_ruta = self.costo_ruta
            ####### Revisa el costo de los nodos abiertos en la rama selecciona el menor  
            for movimiento in movimientos:
                d1,d2 = self.distancia(movimiento)
                d.append(costo_ruta+d1+d2)
                d1L.append(d1)
                d2L.append(d2)
            if(d != []):
                indice = np.argmin(d)
                if type(movimientos)==list:
                    movimientot = movimientos.pop(indice)
                    d1 = d1L.pop(indice)
                    d2 = d2L.pop(indice)
                # añade el resto a una lista de nodos abiertos
                print(movimientot)
                for indice, movimiento in enumerate(movimientos):
                    if movimiento not in self.nodos_abiertos and movimiento not in self.visitados:
                        self.nodos_abiertos[movimiento] = (costo_ruta+d1L[indice]+d2L[indice],d1L[indice],d2L[indice],costo_ruta,self.indice_rama,nodo,copy.deepcopy(self.rama))
                    else:
                        if movimiento not in self.visitados:
                            if costo_ruta+d1L[indice]+d2L[indice]<self.nodos_abiertos[movimiento][0]:
                                self.nodos_abiertos[movimiento] = (costo_ruta+d1L[indice]+d2L[indice],d1L[indice],d2L[indice],costo_ruta,self.indice_rama,nodo,copy.deepcopy(self.rama))
                self.rcostoenna(costo_ruta+d1+d2,movimientot,d2,nodo,d1,costo_ruta)
            else:
                costo = -1
                for movimiento in self.nodos_abiertos:
                    if costo == -1:
                        costo = self.nodos_abiertos[movimiento][0]
                        key = movimiento
                        
                    elif self.nodos_abiertos[movimiento][0]<costo:
                        costo = self.nodos_abiertos[movimiento][0]
                        key = movimiento
                self.costo_ruta = self.nodos_abiertos[key][3]+self.nodos_abiertos[key][2]
                self.rama = self.nodos_abiertos[key][6]
                del(self.nodos_abiertos[key])
                self.muevete = key
            self.rama.append(self.muevete)
    def rcostoenna(self,costo,movimiento_v,costo_mov,nodo,d1,costo_ruta):
        key = 0
        if self.backtracking == False:
            print('entre')
            for movimiento in self.nodos_abiertos:
                if self.nodos_abiertos[movimiento][0]<costo:
                   if key ==0:
                       tem = (costo,d1,costo_mov,costo_ruta,self.indice_rama,nodo,copy.deepcopy(self.rama))
                   costo = self.nodos_abiertos[movimiento][0]
                   key = movimiento
            if key != 0:
                self.nodos_abiertos[movimiento_v] = tem
                self.rama = self.nodos_abiertos[key][6]
                self.muevete = key
                self.costo_ruta = self.nodos_abiertos[key][3]+self.nodos_abiertos[key][2]
                self.backtracking = False
                print('backtracking')
                del(self.nodos_abiertos[key])
            else:
                print('entre')
                self.muevete = movimiento_v
                self.costo_ruta += costo_mov
                self.color = [255,0,0]
    
    def distancia(self,nodo):
        x,y = nodo
        d = -1
        d2 = -1
        for punto in self.puntos_meta:
            x1,y1 = punto
            tem = abs(x-x1)+abs(y-y1)
            tem2 = (abs(abs(x-x1)-abs(y-y1))/50)
            if d == -1:
                d2= tem2
                d =  tem
            elif d > tem:
                d = tem
                d2 = tem2
        return d,d2

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
    acenso_de_colina = aest(Mi_laberinto.get_agente(),
                                    Mi_laberinto.puntosmeta)

    path = os.getcwd()
    try:
        os.mkdir('AEST')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            os.rmdir('AEST')
            os.mkdir('AEST')
            pass
        
    os.chdir('AEST')
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
    for punto in  acenso_de_colina.rama:
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
        
    laberinto_outasdc2.release()
    recorrido_outasdc2.release()     
    laberinto_outasdc1.release()
    recorrido_outasdc1.release()   
     
    cv2.destroyAllWindows() 
    os.chdir(path)