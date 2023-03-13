from tkinter import *
from Piedra import *
import time
from threading import *
from PIL import Image,ImageTk


#Crear piedras:
#Función que Crea las piedras que se usarán durante el juego
def crearPiedras(lpj1, lpj2, quienInicia, t1, t2, t3, t4):
    
#Color de piedras:
#0: piedras Negras ; 1: piedras blancas.
    
    if(quienInicia==0):
        for x in range(4):        
            lpj1.append(Piedra(3,x,1, 0))
            lpj1.append(Piedra(3,x,2, 0))
            lpj1.append(Piedra(3,x,3, 0))
            lpj1.append(Piedra(3,x,4, 0))

            lpj2.append(Piedra(0,x,1, 1))
            lpj2.append(Piedra(0,x,2, 1))
            lpj2.append(Piedra(0,x,3, 1))
            lpj2.append(Piedra(0,x,4, 1))
        
    elif(quienInicia==1):
        for x in range(4):
            
            lpj1.append(Piedra(3,x,1, 1))
            lpj1.append(Piedra(3,x,2, 1))
            lpj1.append(Piedra(3,x,3, 1))
            lpj1.append(Piedra(3,x,4, 1))

            lpj2.append(Piedra(0,x,1, 0))
            lpj2.append(Piedra(0,x,2, 0))
            lpj2.append(Piedra(0,x,3, 0))
            lpj2.append(Piedra(0,x,4, 0))
#____________________________________________________________________________
        
#Poner piedras:
#Funcion que recibe dos listas correspondiente a las piedras de los jugadores y 
#Posiciona las piedras en el tablero de juego (ubica las imagenes en los botones correspondientes de las posiciones de las piedras)
        
def actualizarPiedrasTablero(P0, P1, vacio, quienInicia ,l1, l2, t1, t2, t3, t4):

    for x in range(4):
        for y in range(4):
            t1[x][y].config(bg= '#FFEACC')
            t2[x][y].config(bg= '#D6A957')
            t3[x][y].config(bg= '#FFEACC')
            t4[x][y].config(bg= '#D6A957')
            t1[x][y].config(image=vacio)
            t2[x][y].config(image=vacio)
            t3[x][y].config(image=vacio)
            t4[x][y].config(image=vacio)
    tabla = None
    if(quienInicia==0):
        for x in l1:
            if(x.numTabla==1):
                tabla = t1
            elif(x.numTabla== 2):
                tabla =t2
            elif(x.numTabla== 3):
                tabla = t3
            elif(x.numTabla== 4):
                tabla = t4
            tabla[x.i][x.j].config(image=P0)
        for x in l2:
            if(x.numTabla==1):
                tabla = t1
            elif(x.numTabla== 2):
                tabla =t2
            elif(x.numTabla== 3):
                tabla = t3
            elif(x.numTabla== 4):
                tabla = t4
            tabla[x.i][x.j].config(image=P1)
    else:
        for x in l1:
            if(x.numTabla==1):
                tabla = t1
            elif(x.numTabla== 2):
                tabla =t2
            elif(x.numTabla== 3):
                tabla = t3
            elif(x.numTabla== 4):
                tabla = t4
            tabla[x.i][x.j].config(image=P1)
        for x in l2:
            if(x.numTabla==1):
                tabla = t1
            elif(x.numTabla== 2):
                tabla =t2
            elif(x.numTabla== 3):
                tabla = t3
            elif(x.numTabla== 4):
                tabla = t4
            tabla[x.i][x.j].config(image=P0)
#_______________________________________________________________________________
            
#Buscar piedras:
#Función que recibe 2 listas de piedras, una posición  i, una posición j y el numero de la tabla a la cual pertenecen
#y retorna la piedra que está en la tabla especificada y en las posiciones i,j

def buscarPiedras(lpj1,lpj2,i,j,numTabla):
    for x in range(0,len(lpj1)):
        if(lpj1[x].i==i and lpj1[x].j==j and lpj1[x].numTabla== numTabla):
            return lpj1[x]
    for x in range(0,len(lpj2)):
        if(lpj2[x].i==i and lpj2[x].j==j and lpj2[x].numTabla== numTabla):
            return lpj2[x]

#_______________________________________________________________________________
            
#enfocarSelección: Función que recibe 1 tablero, una posición i y una posición j y cambia de color el botón
#seleccionado por un jugador (Usuario / IA).

def enfocarSelección(tx, i, j):
    tx[i][j].config(bg= "#EB7681")

#_______________________________________________________________________________

#Actualizar color de los mensajes de estado:
def colorMensajes(estado, ee0, ee2, ee4, ee6):
    #Rojo "#B2313D"      #Verde "#0D7831"
    
    if(estado==0 ):
        ee0.config(fg="#0D7831")
        ee2.config(fg="#B2313D")
        ee4.config(fg="#B2313D")
        ee6.config(fg="#B2313D")
    elif(estado==2):
        ee2.config(fg="#0D7831")
        ee4.config(fg="#B2313D")
        ee6.config(fg="#B2313D")
        ee0.config(fg="#B2313D")
    elif(estado==4):
        ee4.config(fg="#0D7831")
        ee6.config(fg="#B2313D")
        ee0.config(fg="#B2313D")
        ee2.config(fg="#B2313D")
    elif(estado==6):
        ee6.config(fg="#0D7831")
        ee0.config(fg="#B2313D")
        ee4.config(fg="#B2313D")
        ee2.config(fg="#B2313D")

#_________________________________________________________________________________
#Comparar color de piedras
def compararColor(p1, p2):
    if(p1.color==p2.color):
        return True
    else:
        return False
#_________________________________________________________________________________
#Eliminar piedra de una lista:

def eliminarDeLista(lpj1, lpj2, estado, piedraEliminar, quienInicia):
    if(quienInicia==0):
        if(estado==3):
            for piedra in lpj2:
                if(piedra == piedraEliminar):
                    lpj2.remove(piedraEliminar)
        elif(estado==7):
            for piedra in lpj1:
                if(piedra == piedraEliminar):
                    lpj1.remove(piedraEliminar)
    else:
        if(estado==3):
            for piedra in lpj1:
                if(piedra == piedraEliminar):
                    lpj1.remove(piedraEliminar)
        elif(estado==7):
            for piedra in lpj2:
                if(piedra == piedraEliminar):
                    lpj2.remove(piedraEliminar)
#____________________________________________________________________________________
def escogerModoJuego(m1, m2, modoJuego):
    if(modoJuego==0):
        m1["state"] = "disabled"
        m2["state"] = "normal"
    elif(modoJuego==1):
        m2["state"] = "disabled"
        m1["state"] = "normal"
        
    return modoJuego
#_________________________________________________________________________________
#Crear un hilo para un subproceso:
def crearHilo(f1):
    h= Thread(target = f1)
    h.start()

    
