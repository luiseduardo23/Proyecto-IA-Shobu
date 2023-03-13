class Piedra:
    def __init__(self, i, j, numTabla, color):
        self.i = i #Fila en la que se encuentra el elemento
        self.j = j #Columna en la que se encuentra el elemento
        self.numTabla = numTabla
        self.color = color #el color es un valor númerico que indica el color de la piedra, donde 0
                           #indica que la piedra es negra y 1 que la piedra es blanca.

    def set_i(self,i):
        self.i=i

    def set_j(self,j):
        self.j=j
