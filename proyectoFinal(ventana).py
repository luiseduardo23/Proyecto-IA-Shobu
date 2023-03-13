from tkinter import *
import tkinter.ttk as TTK
from PIL import Image,ImageTk
import copy
import random
import math

from funcionesAux import *
from Piedra import *
from reglasTableroJuego import *
from Arbol import *
from minimax import *


#Variables Globales: ___________________________________________________

quienInicia=0       #0: Inicia Jugador 1 ; 1: Inicia jugador 2 (P2 o CPU)
modoDeJuego=0       #0: Jugador vs Jugador ; 1: Jugador Vs CPU

#Lista de Piedras:
lpj1=[]              #Tamaño máximo = 16
lpj2=[]              #Tamaño máximo = 16

#Tablas:
t1= [[],[],[],[]]
t2= [[],[],[],[]]
t3= [[],[],[],[]]
t4= [[],[],[],[]]

#Estado del juego:
estado=0
#NOTA: "Jugador" puede ser tanto la cpu como una persona.
    #0: Selección de Piedra negra
    #1: movimiento pasivo jugador con piedras negras
    #2: Selección de Piedra negra
    #3: movimiento agresivo jugador con piedras negras
    #4: Selección de Piedra blanca
    #5: movimiento pasivo jugador con Piedras blanca
    #6: Selección de Piedra blanca
    #7: movimiento agresivo jugador con Piedras blanca

#Ultima Selección de Piedra
ultimaPiedraP= None
ultimaPiedraA= None
#Ultima Tablero usado:
ultimoTableroP= 1
ultimoTableroA= 1
#Dirección y magnitud de ataque en I:
Di=0
#Dirección y magnitud de ataque en J:
Dj=0
#______________________________________________________________________________

turno=1
#Control y verificación de las reglas del juego: (para el caso de jugadores humanos)
def controlyReglas(i, j, numTabla):
    
    global estado, modoDeJuego, lpj1, lpj2, quienInicia, ultimaPiedraP, ultimaPiedraA, ultimoTableroP, ultimoTableroA, Di, Dj,turno
    #print("Estado:", estado)
    if(modoDeJuego==0):
        controlyReglasJ(i, j, numTabla)
    else: 
        if(quienInicia==0):
            controlyReglasJ(i, j, numTabla)
            raiz.update_idletasks()
            if(estado==4):
                mensajeVar.set("___CPU JUGANDO___")
                raiz.update_idletasks()
                crearHilo(aplicarJugadaIA())
        else:
            if(estado>=4): 
                controlyReglasJ(i, j, numTabla)
                raiz.update_idletasks()
                if(estado==0):
                    controlyReglas(0,0,0)
            mensajeVar.set("___CPU JUGANDO___")
            raiz.update_idletasks()
            crearHilo(aplicarJugadaIA())
            
        
    winner = ganador(lpj1, lpj2)
    if(winner==1):
        lpj1 = []
        lpj2 = []
        actualizarPiedrasTablero(P0, P1, vacio, quienInicia, lpj1, lpj2, t1, t2, t3, t4)
        mensajeVar.set("GANA EL JUGADOR 1")
    if(winner==-1):
        lpj1 = []
        lpj2 = []
        actualizarPiedrasTablero(P0, P1, vacio, quienInicia, lpj1, lpj2, t1, t2, t3, t4)
        mensajeVar.set("GANA EL JUGADOR 2")

def aplicarJugadaIA():
    nodoJugada=controlyReglasIA()#devuelve un nodo del arbol
    crearHilo(aplicarJugadaAux(nodoJugada))
    
def aplicarJugadaAux(nodoJugada):
    controlyReglasJ(nodoJugada.ip, nodoJugada.jp,nodoJugada.numTablaP)
    time.sleep(1)
    raiz.update_idletasks()
    controlyReglasJ(nodoJugada.ip+nodoJugada.Di, nodoJugada.jp+nodoJugada.Dj,nodoJugada.numTablaP)
    time.sleep(1)
    raiz.update_idletasks()
    controlyReglasJ(nodoJugada.ia, nodoJugada.ja,nodoJugada.numTablaA)
    mensajeVar.set("")
    time.sleep(1)
    raiz.update_idletasks()
    
def controlyReglasJ(i, j, numTabla):

    global estado, modoDeJuego, lpj1, lpj2, quienInicia, ultimaPiedraP, ultimaPiedraA, ultimoTableroP, ultimoTableroA, Di, Dj
    
    #Verificamos si hay fichas en el tablero, es decir, si se puede jugar.
    if((len(lpj1)!= 0 or len(lpj2)!= 0) ):

        #reseteamos el texto del mensaje.
        mensajeVar.set("...")
        
        #Reglas de Selección:________________________________________________________________________________________________________
        if(estado == 0 or estado == 2 or estado == 4 or estado == 6):

            #buscamos la piedra seleccionada
            piedraSeleccionada= buscarPiedras(lpj1,lpj2,i,j,numTabla)

            #Verificamos si la ficha seleccionada corresponde al jugador actual.
            res= esMiFicha(piedraSeleccionada ,estado)
            
            if(res and (estado == 0 or estado == 4)):
                
                #Verificamos si la tabla de la cual seleccionó la piedra, es de sus tablas
                res= esDeMisTablas_1(numTabla, quienInicia, estado)
                
                if(not(res)):
                    mensajeVar.set("ERROR: La piedra seleccionada\nno corresponde a las de\ntus tableros")
                    
            elif(res and (estado == 2 or estado == 6)):
                #verificamos si la tabla de la cual seleccionó la piedra, es de diferente color a la usada en el movimiento pasivo
                res = esDeMisTablas_2(ultimoTableroP, numTabla)

                if(not(res)):
                    mensajeVar.set("ERROR: La Tabla de la\ncual seleccionó la piedra\n es del mismo color que la\n usada en el mov. pasivo")
            else:
                mensajeVar.set("ERROR: No seleccionaste alguna\npiedra O la piedra que\nseleccionaste no es de las tuyas.")

            #Si res es verdadero, indica que las verificaciones anteriores se cumplieron, por lo tanto se acepta la selección.
            if(res):
                if(estado == 0 or estado == 4):
                    ultimoTableroP= numTabla
                    ultimaPiedraP = piedraSeleccionada
                    enfocarSelección(obtenerTabla(ultimoTableroP), piedraSeleccionada.i, piedraSeleccionada.j)
                else:
                    ultimoTableroA= numTabla
                    ultimaPiedraA = piedraSeleccionada
                    enfocarSelección(obtenerTabla(ultimoTableroA), piedraSeleccionada.i, piedraSeleccionada.j)
                    
                estado+=1
                colorMensajes(estado, ee0, ee2, ee4, ee6)
                
                if(estado == 3 or estado == 7):
                    controlyReglasJ(i, j, numTabla)
                return None
        #_____________________________________________________________________________________________________________________________
        #Reglas de movimiento:
        if(estado == 1 or estado == 3 or estado == 5 or estado == 7):
            
            if(estado== 1 or estado == 5):
                res=True
                #Verificamos si la ultima piedra Pasiva seleccionada, está en la tabla actual del movimiento.
                #________________________________________
                if(ultimoTableroP == numTabla):
                    res= True
                else:
                    res = False
                #_________________________________________

                if(res):
                    #Verificamos si el movimiento es valido.
                    listaRes = movimientoPasivo(i,j, ultimaPiedraP, lpj1, lpj2)

                    res =listaRes[0]
                    Di =listaRes[1]
                    Dj=listaRes[2]

                    if(not(res)):
                        mensajeVar.set("ERROR: La casilla seleccionada\nestá siendo ocupada por otra\npiedra O está fuera del limite\nde alcance.")
                else:
                    mensajeVar.set("ERROR: La tabla en la que\nseleccionaste la casilla\nno es valida para el\nmovimiento a realizar.")

                if(res):
                    ultimaPiedraP.i=i
                    ultimaPiedraP.j=j
                    actualizarPiedrasTablero(P0, P1, vacio, quienInicia, lpj1, lpj2, t1, t2, t3, t4)
                    estado +=1
                    colorMensajes(estado, ee0, ee2, ee4, ee6)
                    return None
                
            if(estado== 3 or estado == 7):

                mensaje=""
                #Verificar si la piedra seleccionada puede hacer el movimiento y si hay alguna piedra que esté empujando.
                listaRes = movimientoAgresivo(Di, Dj, ultimaPiedraA, lpj1, lpj2)
                res = listaRes[0]

                if (res):
                    #Obtenemos las piedras que son movidas (en caso de haber piedras)
                    if (len(listaRes[1])!=0):
                        piedraMovida = buscarPiedras(lpj1,lpj2,listaRes[1][0],listaRes[1][1],ultimoTableroA)
                        res = not(compararColor(ultimaPiedraA, piedraMovida))
                        if(res):
                            #Verificamos hacia donde se mueve:
                            if((listaRes[2]>=0 and listaRes[2]<4) and (listaRes[3]>=0 and listaRes[3]<4)):
                                piedraMovida.i= listaRes[2]
                                piedraMovida.j= listaRes[3]
                            else:
                                eliminarDeLista(lpj1, lpj2, estado, piedraMovida, quienInicia)
                        else:
                            mensaje = "ERROR: No puedes mover\nuna de tus piedras."
                else:
                    mensaje = "ERROR: Una Piedra bloquea\nel ataque o estás en el\nlímite.\nSelecciona otra piedra"

                if(res):
                    ultimaPiedraA.i+=Di
                    ultimaPiedraA.j+=Dj
                    actualizarPiedrasTablero(P0, P1, vacio, quienInicia, lpj1, lpj2, t1, t2, t3, t4)
                    if(estado==7):
                        estado=0
                    else:
                        estado+=1
                    colorMensajes(estado, ee0, ee2, ee4, ee6)
                    return None
                
                else:
                    mensajeVar.set(mensaje)
                    estado -= 1
                    colorMensajes(estado, ee0, ee2, ee4, ee6)
                    actualizarPiedrasTablero(P0, P1, vacio, quienInicia, lpj1, lpj2, t1, t2, t3, t4)
                    return None

def controlyReglasIA():
    global  lpj1, lpj2, quienInicia,estado
    estadoAux= estado
    #Crear nodo padre
    arbolI = Arbol(None)
    jugada(arbolI, estadoAux, lpj1, lpj2, 1) #Aqui termina la construccion del arbol 
    minimax(arbolI,4,-math.inf,math.inf,1)
    NuevaRaiz=arbolI.hijos[arbolI.seleccion]
    return NuevaRaiz

def jugada(padre, estadoAux, l1, l2, profundidad):
    global quienInicia

    posiblesMovimientos=[[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-2,-2],[0,-2],[2,-2],[2,0],[2,2],[0,2],[-2,2],[-2,0]]
    random.shuffle(posiblesMovimientos)
    movimientosSeleccionados=[]
    
    for movimiento in posiblesMovimientos:
        if random.uniform(0.0,1.0)>=0.5:
            movimientosSeleccionados.append(movimiento)
            
    posiblesMovimientos=movimientosSeleccionados
    random.shuffle(l1)
    random.shuffle(l2)
    
    profundidadMaxima=4
    ip= 0
    jp= 0
    ia= 0
    ja= 0
    Di= 0
    Dj= 0
    lpj1Aux= copy.deepcopy(l1)
    lpj2Aux= copy.deepcopy(l2)
    lp=[]#Lista Puntero
    
    if(profundidad<=profundidadMaxima):

        if(profundidad%2 == 0):
            lp=lpj1Aux
        else:
            lp=lpj2Aux            
        for piedraP in lp:
            ip= 0
            jp= 0
            heu= 0
            ia= 0
            ja= 0
            Di= 0
            Dj= 0
            lpj1Aux= copy.deepcopy(l1)
            lpj2Aux= copy.deepcopy(l2)
            estadoC= estadoAux
            #Verificamos si la tabla de la cual seleccionó la piedra, es de sus tablas
            if(esMiFicha(piedraP ,estadoC) and esDeMisTablas_1(piedraP.numTabla, quienInicia, estadoC)):
                ip=piedraP.i
                jp=piedraP.j
                estadoC +=1
                for movimiento in posiblesMovimientos:
                    listaRes= movimientoPasivo(ip+movimiento[0],jp+movimiento[1], piedraP , l1, l2)
                    if(listaRes[0]and (ip+listaRes[1]>=0 and ip+listaRes[1]<4) and (jp+listaRes[2]>=0 and jp+listaRes[2]<4)):
                        Di= listaRes[1]
                        Dj= listaRes[2]
                        piedraP.i= ip+ Di
                        piedraP.j= jp+ Dj
                        estadoC +=1
                        for piedraA in lp:
                            #verificamos si la tabla de la cual seleccionó la piedra, es de diferente color a la usada en el movimiento pasivo
                            if(piedraP != piedraA and esDeMisTablas_2(piedraP.numTabla, piedraA.numTabla)):
                                ia= piedraA.i
                                ja= piedraA.j
                                estadoC +=1
                                listaRes = movimientoAgresivo(Di, Dj, piedraA, lpj1Aux, lpj2Aux)
                                if (listaRes[0] and (ia+Di>=0 and ia+Di<4) and (ja+Dj>=0 and ja+Dj<4)):
                                    res = True
                                    #Obtenemos las piedras que son movidas (en caso de haber piedras)
                                    if (len(listaRes[1])!=0):
                                        piedraMovida = buscarPiedras(lpj1Aux,lpj2Aux,listaRes[1][0],listaRes[1][1],piedraA.numTabla)
                                        res = not(compararColor(piedraA, piedraMovida))
                                        if(res):
                                            #Verificamos hacia donde se mueve:
                                            if((listaRes[2]>=0 and listaRes[2]<4) and (listaRes[3]>=0 and listaRes[3]<4)):
                                                piedraMovida.i= listaRes[2]
                                                piedraMovida.j= listaRes[3]
                                                if(profundidad%2 == 0):
                                                    heu+=-5
                                                else:
                                                    heu+=5
                                            else:
                                                eliminarDeLista(lpj1Aux, lpj2Aux, estadoC, piedraMovida, quienInicia)
                                                if(profundidad%2 == 0):
                                                    heu+=-10
                                                else:
                                                    heu+=10
                                    if(res):
                                        nodo = Arbol(padre)
                                        estadoC+=1
                                        #se verifica si en la jugada actual existe un ganador
                                        winner = ganador(lpj1Aux, lpj2Aux)
                                        if(winner==1):
                                            nodo.utilidad= -math.inf
                                        elif(winner==-1):
                                            nodo.utilidad= math.inf
                                        if(profundidadMaxima==profundidad and winner==0):
                                            nodo.t1 = mapearTablaActual(1, lpj1Aux,lpj2Aux)
                                            nodo.t2 = mapearTablaActual(2, lpj1Aux, lpj2Aux)
                                            nodo.t3 = mapearTablaActual(3, lpj1Aux, lpj2Aux)
                                            nodo.t4 = mapearTablaActual(4, lpj1Aux, lpj2Aux)
                                            matrizUtilidad= nodo.heuristica(quienInicia)
                                            nodo.utilidad=  matrizUtilidad[0][0] + matrizUtilidad[0][1]+ matrizUtilidad[1][0] + matrizUtilidad[1][1] + heu
                                        else:
                                            piedraA.i+=Di
                                            piedraA.j+=Dj
                                            if(estadoC==8):
                                                estadoC=0
                                            #Creamos el nodo:
                                            nodo.ip= ip
                                            nodo.jp= jp
                                            nodo.ia= ia
                                            nodo.ja= ja
                                            nodo.Di= Di
                                            nodo.Dj= Dj
                                            nodo.numTablaA=piedraA.numTabla
                                            nodo.numTablaP=piedraP.numTabla
                                            nodo.estado=estadoC
                                            nodo.lpj1=lpj1Aux
                                            nodo.lpj2=lpj2Aux                    
                                        padre.hijos.append(nodo)
        #sorted(padre.hijos,key=lambda x: x.utilidad,reverse=true)
        for nodos in padre.hijos:
            nodos.profundidad=profundidad
            if(nodos.utilidad==0):
                jugada(nodos, nodos.estado, nodos.lpj1, nodos.lpj2, profundidad+1)

def obtenerTabla(numTabla):
    global t1, t2, t3, t4
    if(numTabla == 1):
        return t1
    elif(numTabla== 2):
        return t2
    elif(numTabla== 3):
        return t3
    elif(numTabla== 4):
        return t4

        
#Iniciar: Función que inicializa y crea todos los elementos necesarios para empezar el juego
def iniciar():
    global quienInicia, lpj1, lpj2, t1, t2, t3, t4
    global estado
    quienInicia = combo.current()
    estado = 0
    lpj1=[]
    lpj2=[]

    #Cambiamos el color de los mensajes de estado de la partida:
    colorMensajes(estado, ee0, ee2, ee4, ee6)

    #Funciones de creación y ubicación de piedras
    crearPiedras(lpj1, lpj2, quienInicia, t1, t2, t3, t4)
    actualizarPiedrasTablero(P0, P1, vacio, quienInicia, lpj1, lpj2, t1, t2, t3, t4)

    if(modoDeJuego==1 and quienInicia==1):
        controlyReglas(0,0,0)

#ventana Raiz
raiz = Tk()
raiz.title("Proyecto")
raiz.resizable(0,0)
raiz.geometry("1000x680")

#Imagenes:
P0 = Image.open('P0.png')
P0 = P0.resize((64, 64), Image.ANTIALIAS) # Redimension (Alto, Ancho)
P1 = Image.open('P1.png')
P1 = P1.resize((64, 64), Image.ANTIALIAS) # Redimension (Alto, Ancho)
vacio = Image.open('null.png')
vacio = vacio.resize((64, 64), Image.ANTIALIAS) # Redimension (Alto, Ancho)
cuerda = Image.open('cuerda.png')
cuerda = cuerda.resize((550, 400), Image.ANTIALIAS) # Redimension (Alto, Ancho)

P0= ImageTk.PhotoImage(P0)
P1 = ImageTk.PhotoImage(P1)
vacio = ImageTk.PhotoImage(vacio)
cuerda = ImageTk.PhotoImage(cuerda)

#Canvas:
canvas = Canvas(width=400, height=300, bg='#B19078')
canvas.pack(expand=YES, fill=BOTH)
canvas.create_rectangle(650, 0, 1000, 700, width=1, fill='#F1E49B')
canvas.create_line(660, 580, 990,580, width=2)
canvas.create_line(660, 440, 990,440, width=2)
canvas.create_line(660, 290, 990,290, width=2)
canvas.create_line(660, 120, 990,120, width=2)
canvas.create_image(50,150, anchor = NW, image = cuerda)

#Etiquetas de presentación:
titulo = Label(text = "SHŌBU",fg="#F1E49B",bg  = '#000000',font = ("Verdana", 32, "bold italic")).place(x=730, y=20)
Label(text = "Escoge un modo:", bg="#F1E49B" ,font = ("Verdana", 14, "bold italic")).place(x=730, y=135)
Label(text = "¿Quién Inicia?", bg="#F1E49B" ,font = ("Verdana", 11, "bold italic")).place(x=690, y=600)
Label(text = "Mensaje:", bg="#F1E49B" ,font = ("Verdana", 14, "bold italic")).place(x=680, y=450)
Label(text = "Estado Del Juego:", bg="#F1E49B" ,font = ("Verdana", 14, "bold italic")).place(x=680, y=300)

#Etiquetas de Estado:
ee0= Label(text = "Movimiento\nPasivo J1", fg="#B2313D", bg="#F1E49B" ,font = ("Verdana", 10, "bold"))
ee0.place(x=720, y=340)
ee2= Label(text = "Movimiento\nAgresivo J1", fg="#B2313D", bg="#F1E49B" ,font = ("Verdana", 10, "bold"))
ee2.place(x=720, y=390)
ee4= Label(text = "Movimiento\nPasivo J2",  fg="#B2313D", bg="#F1E49B" ,font = ("Verdana", 10, "bold"))
ee4.place(x=850, y=340)
ee6= Label(text = "Movimiento\nAgresivo J2", fg="#B2313D", bg="#F1E49B" ,font = ("Verdana", 10, "bold"))
ee6.place(x=850, y=390)

mensajeVar = StringVar()
mensajeVar.set("...")
mensaje= Label(textvariable = mensajeVar, bg="#F1E49B" ,font = ("Verdana", 12, "italic"), justify=LEFT)
mensaje.place(x=690, y=480)

#ComboBox:
combo = TTK.Combobox(state="readonly", values = ["Jugador 1", "Jugador 2"], font = ("Verdana", 11, "italic"), width= 12)
combo.current(0)
combo.place(x=680, y=630)

#Botones para configuraciones:
m1=None
m2=None
Button(raiz, text = "Iniciar", command = iniciar, fg="#F1E49B", bg  = '#000000', font = ("Verdana", 20, "bold italic")).place(x=850, y =600)
m1 = Button(raiz, text = "Jugador1 Vs. Jugador2", command = lambda: globals().update(modoDeJuego= escogerModoJuego(m1, m2, 0)), fg="#F1E49B", bg  = '#000000', font = ("Verdana", 14, "bold italic"))
m1.place(x=690, y =180)
m2 = Button(raiz, text = "Jugador1 Vs. CPU", command = lambda: globals().update(modoDeJuego= escogerModoJuego(m1, m2, 1)), fg="#F1E49B", bg  = '#000000', font = ("Verdana", 14, "bold italic"))
m2.place(x=720, y =230)
m1["state"] = "disabled"

#Botones para los tableros de juego (Pasar de largo):
#botones- Tabla 1.
t1[0].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(0,0,1)))
t1[0][0].place(x=50, y =50, width = 62.5, height =62.5)
t1[0].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(0,1,1)))
t1[0][1].place(x=112.5, y =50, width = 62.5, height =62.5)
t1[0].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(0,2,1)))
t1[0][2].place(x=175, y =50, width = 62.5, height =62.5)
t1[0].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(0,3,1)))
t1[0][3].place(x=237.5, y =50, width = 62.5, height =62.5)

t1[1].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(1,0,1)))
t1[1][0].place(x=50, y =112.5, width = 62.5, height =62.5)
t1[1].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(1,1,1)))
t1[1][1].place(x=112.5, y =112.5, width = 62.5, height =62.5)
t1[1].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(1,2,1)))
t1[1][2].place(x=175, y =112.5, width = 62.5, height =62.5)
t1[1].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(1,3,1)))
t1[1][3].place(x=237.5, y =112.5, width = 62.5, height =62.5)

t1[2].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(2,0,1)))
t1[2][0].place(x=50, y =175, width = 62.5, height =62.5)
t1[2].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(2,1,1)))
t1[2][1].place(x=112.5, y =175, width = 62.5, height =62.5)
t1[2].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(2,2,1)))
t1[2][2].place(x=175, y =175, width = 62.5, height =62.5)
t1[2].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(2,3,1)))
t1[2][3].place(x=237.5, y =175, width = 62.5, height =62.5)

t1[3].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(3,0,1)))
t1[3][0].place(x=50, y =237.5, width = 62.5, height =62.5)
t1[3].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(3,1,1)))
t1[3][1].place(x=112.5, y =237.5, width = 62.5, height =62.5)
t1[3].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(3,2,1)))
t1[3][2].place(x=175, y =237.5, width = 62.5, height =62.5)
t1[3].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(3,3,1)))
t1[3][3].place(x=237.5, y =237.5, width = 62.5, height =62.5)

#botones- Tabla 2.
t2[0].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(0,0,2)))
t2[0][0].place(x=350, y =50, width = 62.5, height =62.5)
t2[0].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(0,1,2)))
t2[0][1].place(x=412.5, y =50, width = 62.5, height =62.5)
t2[0].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(0,2,2)))
t2[0][2].place(x=475, y =50, width = 62.5, height =62.5)
t2[0].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(0,3,2)))
t2[0][3].place(x=537.5, y =50, width = 62.5, height =62.5)

t2[1].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(1,0,2)))
t2[1][0].place(x=350, y =112.5, width = 62.5, height =62.5)
t2[1].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(1,1,2)))
t2[1][1].place(x=412.5, y =112.5, width = 62.5, height =62.5)
t2[1].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(1,2,2)))
t2[1][2].place(x=475, y =112.5, width = 62.5, height =62.5)
t2[1].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(1,3,2)))
t2[1][3].place(x=537.5, y =112.5, width = 62.5, height =62.5)

t2[2].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(2,0,2)))
t2[2][0].place(x=350, y =175, width = 62.5, height =62.5)
t2[2].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(2,1,2)))
t2[2][1].place(x=412.5, y =175, width = 62.5, height =62.5)
t2[2].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(2,2,2)))
t2[2][2].place(x=475, y =175, width = 62.5, height =62.5)
t2[2].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(2,3,2)))
t2[2][3].place(x=537.5, y =175, width = 62.5, height =62.5)

t2[3].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(3,0,2)))
t2[3][0].place(x=350, y =237.5, width = 62.5, height =62.5)
t2[3].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(3,1,2)))
t2[3][1].place(x=412.5, y =237.5, width = 62.5, height =62.5)
t2[3].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(3,2,2)))
t2[3][2].place(x=475, y =237.5, width = 62.5, height =62.5)
t2[3].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(3,3,2)))
t2[3][3].place(x=537.5, y =237.5, width = 62.5, height =62.5)

#botones- Tabla 3.
t3[0].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(0,0,3)))
t3[0][0].place(x=50, y =400, width = 62.5, height =62.5)
t3[0].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(0,1,3)))
t3[0][1].place(x=112.5, y =400, width = 62.5, height =62.5)
t3[0].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(0,2,3)))
t3[0][2].place(x=175, y =400, width = 62.5, height =62.5)
t3[0].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(0,3,3)))
t3[0][3].place(x=237.5, y =400, width = 62.5, height =62.5)

t3[1].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(1,0,3)))
t3[1][0].place(x=50, y =462.5, width = 62.5, height =62.5)
t3[1].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(1,1,3)))
t3[1][1].place(x=112.5, y =462.5, width = 62.5, height =62.5)
t3[1].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(1,2,3)))
t3[1][2].place(x=175, y =462.5, width = 62.5, height =62.5)
t3[1].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(1,3,3)))
t3[1][3].place(x=237.5, y =462.5, width = 62.5, height =62.5)

t3[2].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(2,0,3)))
t3[2][0].place(x=50, y =525, width = 62.5, height =62.5)
t3[2].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(2,1,3)))
t3[2][1].place(x=112.5, y =525, width = 62.5, height =62.5)
t3[2].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(2,2,3)))
t3[2][2].place(x=175, y =525, width = 62.5, height =62.5)
t3[2].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(2,3,3)))
t3[2][3].place(x=237.5, y =525, width = 62.5, height =62.5)

t3[3].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(3,0,3)))
t3[3][0].place(x=50, y =587.5, width = 62.5, height =62.5)
t3[3].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(3,1,3)))
t3[3][1].place(x=112.5, y =587.5, width = 62.5, height =62.5)
t3[3].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(3,2,3)))
t3[3][2].place(x=175, y =587.5, width = 62.5, height =62.5)
t3[3].append(Button(raiz, bg = '#FFEACC', command = lambda: controlyReglas(3,3,3)))
t3[3][3].place(x=237.5, y =587.5, width = 62.5, height =62.5)

#botones- Tabla 4.
t4[0].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(0,0,4)))
t4[0][0].place(x=350, y =400, width = 62.5, height =62.5)
t4[0].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(0,1,4)))
t4[0][1].place(x=412.5, y =400, width = 62.5, height =62.5)
t4[0].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(0,2,4)))
t4[0][2].place(x=475, y =400, width = 62.5, height =62.5)
t4[0].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(0,3,4)))
t4[0][3].place(x=537.5, y =400, width = 62.5, height =62.5)

t4[1].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(1,0,4)))
t4[1][0].place(x=350, y =462.5, width = 62.5, height =62.5)
t4[1].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(1,1,4)))
t4[1][1].place(x=412.5, y =462.5, width = 62.5, height =62.5)
t4[1].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(1,2,4)))
t4[1][2].place(x=475, y =462.5, width = 62.5, height =62.5)
t4[1].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(1,3,4)))
t4[1][3].place(x=537.5, y =462.5, width = 62.5, height =62.5)

t4[2].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(2,0,4)))
t4[2][0].place(x=350, y =525, width = 62.5, height =62.5)
t4[2].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(2,1,4)))
t4[2][1].place(x=412.5, y =525, width = 62.5, height =62.5)
t4[2].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(2,2,4)))
t4[2][2].place(x=475, y =525, width = 62.5, height =62.5)
t4[2].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(2,3,4)))
t4[2][3].place(x=537.5, y =525, width = 62.5, height =62.5)

t4[3].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(3,0,4)))
t4[3][0].place(x=350, y =587.5, width = 62.5, height =62.5)
t4[3].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(3,1,4)))
t4[3][1].place(x=412.5, y =587.5, width = 62.5, height =62.5)
t4[3].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(3,2,4)))
t4[3][2].place(x=475, y =587.5, width = 62.5, height =62.5)
t4[3].append(Button(raiz, bg = '#D6A957', command = lambda: controlyReglas(3,3,4)))
t4[3][3].place(x=537.5, y =587.5, width = 62.5, height =62.5)
#_______________________________________________________________________________________
raiz.mainloop()
