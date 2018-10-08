class bep_l:
    raiz = 0
    visitados = []
    cola = []
    posibles_movimientos = 0
    muevete = 0
    arbol = []
    rama = []
    link = {}
    def __init__(self,raiz,posibles_movimientos):
        self.raiz=raiz
        self.rama.append(raiz)
        self.visitados.append(raiz)
        self.posibles_movimientos = posibles_movimientos
        self.revisaryagregar()
       
    
    def revisaryagregar(self):
        seleccion = False
        self.muevete = 0
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
            print('Backtracking')
            print(self.posibles_movimientos)
            if self.cola:
                self.muevete = self.cola.pop()
                while self.muevete in self.visitados and self.cola:
                    self.muevete = self.cola.pop()
                if not(self.cola):
                    print('termine')
                self.arbol.append(self.rama)
                self.rama = self.rama[0:self.rama.index(self.link[self.muevete])+1]
                print(self.muevete)
            else: 
                print('termine')
                self.muevete = 0
        self.visitados.append(self.muevete)
        if seleccion == False:
            self.rama.append(self.muevete)
    def get_movimiento(self):
        return self.muevete

    def mov(self,posibles_movimientos):
        self.posibles_movimientos = posibles_movimientos
        self.revisaryagregar()
        
if __name__ == '__main__':
    import cv2
    from laberinto import laberinto
    Mi_laberinto = laberinto('Laberinto.png')
    Mi_laberinto.set_player(10)#50,10
    busqueda_en_profundidad = bep_l(Mi_laberinto.get_agente(),
                                    Mi_laberinto.get_posiciones_disponibles())
    Mi_laberinto.get_posiciones_disponibles()
    busqueda_en_profundidad.get_movimiento()
    while busqueda_en_profundidad.muevete != 0 and Mi_laberinto.metaalc == False:
        imagen_mostrar = Mi_laberinto.get_imagen_mostrar()
        imagen_recorrida = Mi_laberinto.get_imagen_recorrida()
        cv2.imshow('Laberinto',cv2.resize(imagen_mostrar,(500, 500), interpolation = cv2.INTER_CUBIC))
        cv2.imshow('color',cv2.resize(imagen_recorrida,(500, 500), interpolation = cv2.INTER_CUBIC))
        pulsacion = cv2.waitKey(1)
        if pulsacion == ord('i'):
            break
        Mi_laberinto.set_agente(busqueda_en_profundidad.get_movimiento())
        busqueda_en_profundidad.mov(Mi_laberinto.get_posiciones_disponibles())
    Mi_laberinto.resetimrecorrida()
    for punto in busqueda_en_profundidad.rama:
        imagen_mostrar = Mi_laberinto.get_imagen_mostrar()
        imagen_recorrida = Mi_laberinto.get_imagen_recorrida()
        cv2.imshow('Laberinto',cv2.resize(imagen_mostrar,(500, 500), interpolation = cv2.INTER_CUBIC))
        cv2.imshow('color',cv2.resize(imagen_recorrida,(500, 500), interpolation = cv2.INTER_CUBIC))
        pulsacion = cv2.waitKey(1)
        if pulsacion == ord('i'):
            break
        Mi_laberinto.set_agente(punto) 
    arbol = busqueda_en_profundidad.arbol
        
        
    cv2.destroyAllWindows()    