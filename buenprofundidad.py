class bep_l:
    raiz = 0
    visitados = []
    cola = []
    posibles_movimientos = 0
    muevete = 0
    arbol = []
    rama = []
    link = {}
    backtracking = False
    backtrackingList = []
    color = [255,0,0]
    muevetet = 0

    
    def __init__(self,raiz,posibles_movimientos):
        self.raiz=raiz
        self.rama.append(raiz)
        self.visitados.append(raiz)
        self.posibles_movimientos = posibles_movimientos
        self.revisaryagregar()
       
    
    def revisaryagregar(self):
        seleccion = False
        self.muevete = 0
        #if self.backtrackingList:
        #    self.backtracking = False
        if self.backtracking == False:
            for movimiento in self.posibles_movimientos:
                if movimiento != 0:
                    if seleccion == False and movimiento not in self.visitados:
                        self.muevete = movimiento
                        self.rama.append(self.muevete)
                        seleccion = True
                    else:
                        if movimiento not in self.visitados and movimiento not in self.cola:
                            self.cola.append(movimiento)
                            self.link[movimiento] = self.rama[-2]            
        if self.muevete == 0:
            if self.backtracking == False:
                print('Backtracking')
                self.backtracking = True
                print(self.posibles_movimientos)
                self.arbol.append(self.rama)
                if self.cola:
                    self.muevetet = self.cola.pop()
                    while self.muevetet in self.visitados and self.cola:
                        self.muevetet = self.cola.pop()
                if self.rama.index(self.link[self.muevetet])==0:
                    inc = 0
                else:
                    inc = -1
                self.backtrackingList  = self.rama[self.rama.index(self.link[self.muevetet])+inc:]
                self.rama = self.rama[0:self.rama.index(self.link[self.muevetet])+1]
                self.color = [50,180,180]

                if self.backtrackingList:
                    self.muevete = self.backtrackingList.pop()
                    if not(self.backtrackingList):
                        self.backtracking = False
                        self.color = [255,0,0]

            else:
                if self.backtrackingList:
                    self.muevete = self.backtrackingList.pop()
                    if not(self.backtrackingList):
                        self.backtracking = False
                        self.color = [255,0,0]
                        self.muevete = self.muevetet
                        self.rama.append(self.muevete)
                        self.visitados.append(self.muevete)
                if not(self.cola):
                    print('termine')
        if self.backtracking == False:
            self.visitados.append(self.muevete)
            
                


            
            
            
            
    def get_movimiento(self):
        return self.muevete

    def mov(self,posibles_movimientos):
        self.posibles_movimientos = posibles_movimientos
        self.revisaryagregar()
        
if __name__ == '__main__':
    import cv2
    from laberinto import laberinto
    import os
    import errno
    frame_width = 700
    frame_height = 700
    Mi_laberinto = laberinto('Laberinto3.png')
    Mi_laberinto.set_player(50)#50,10
    busqueda_en_profundidad = bep_l(Mi_laberinto.get_agente(),
                                    Mi_laberinto.get_posiciones_disponibles())
    path = os.getcwd()
    try:
        os.mkdir('BENP')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            os.rmdir('BENP')
            os.mkdir('BENP')
            pass
        
    os.chdir('BENP')
    laberinto_outasdc1 = cv2.VideoWriter('laberinto_outasdc1.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (frame_width,frame_height))
    recorrido_outasdc1 = cv2.VideoWriter('recorrido_outasdc1.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (frame_width,frame_height))

    while busqueda_en_profundidad.muevete != 0 and Mi_laberinto.metaalc == False:
        Mi_laberinto.colores = busqueda_en_profundidad.color
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
        Mi_laberinto.set_agente(busqueda_en_profundidad.get_movimiento())
        busqueda_en_profundidad.mov(Mi_laberinto.get_posiciones_disponibles())
    
    
    laberinto_outasdc2 = cv2.VideoWriter('laberinto_outasdc2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (frame_width,frame_height))
    recorrido_outasdc2 = cv2.VideoWriter('recorrido_outasdc2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (frame_width,frame_height))  
    Mi_laberinto.resetimrecorrida()
    for punto in busqueda_en_profundidad.rama:
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
    cv2.destroyAllWindows()    