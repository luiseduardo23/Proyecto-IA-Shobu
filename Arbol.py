import copy


class Arbol:
    def __init__(self, padre):
        self.utilidad= 0
        self.ip= 0
        self.jp= 0
        self.ia= 0
        self.ja= 0
        self.Di= 0
        self.Dj= 0
        self.estado=0
        self.lpj1=[]
        self.lpj2=[]
        self.t1= None
        self.t2= None
        self.t3= None
        self.t4= None
        self.hijos = []
        self.padre = padre
        self.seleccion=-1
        self.numTablaA=0
        self.numTablaP=0
        self.profundidad=0

    def heuristica(self, quienInicia):
        p1 = 0
        p2 = 0
        p3 = 0
        p4 = 0
        for casillai in range(0,4):
            for casillaj in range(0,4):
                if(quienInicia==0):
                    if(self.t1[casillai][casillaj]==1):
                        p1+=2
                    if(self.t2[casillai][casillaj]==1):
                        p2+=2
                    if(self.t3[casillai][casillaj]==1):
                        p3+=1
                    if(self.t4[casillai][casillaj]==1):
                        p4+=1
                else:
                    if(self.t1[casillai][casillaj]==0):
                        p1+=2
                    if(self.t2[casillai][casillaj]==0):
                        p2+=2
                    if(self.t3[casillai][casillaj]==0):
                        p3+=1
                    if(self.t4[casillai][casillaj]==0):
                        p4+=1

        matrizH=[[p1, p2],[p3, p4]]

        for casillai in range(0,4):
            for casillaj in range(0,4):
                if(quienInicia==0):
                    if(self.t1[casillai][casillaj]==0):
                        matrizH[0][0] -=1
                    if(self.t2[casillai][casillaj]==0):
                        matrizH[0][0] -=1
                    if(self.t3[casillai][casillaj]==0):
                        matrizH[0][0] -=2
                    if(self.t4[casillai][casillaj]==0):
                        matrizH[0][0] -=2
                else:
                    if(self.t1[casillai][casillaj]==1):
                        matrizH[0][0] -=1
                    if(self.t2[casillai][casillaj]==1):
                        matrizH[0][0] -=1
                    if(self.t3[casillai][casillaj]==1):
                        matrizH[0][0] -=2
                    if(self.t4[casillai][casillaj]==1):
                        matrizH[0][0] -=2
                        
        return matrizH   
                    

