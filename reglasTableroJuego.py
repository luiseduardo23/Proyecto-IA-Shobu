
#Reglas de Selección:

#esMiFicha?: función que recibe las piedras de los jugadores, una tabla x y el estado
#del juego actual y retorna true si la piedra seleccionada corresponde al
#jugador que juega la jugada actual

def esMiFicha(piedra ,estadoJuego):
    if(estadoJuego==0 or estadoJuego==2):
        if(piedra!= None):
            if(piedra.color==0):
                return True
            return False

    elif(estadoJuego==4 or estadoJuego==6):
        if(piedra!= None):
            if(piedra.color==1):
                return True
            return False
                

#esDeMisTablas_1?: función que recibe el numero de la tabla, quienInicia y el estado de juego
#dependiendo del estado y quien inició la partida con las piedras negras, determina si la tabla de la cual se seleccionó una piedra
#corresponde a las de su lado. Retorna true si la tabla de la piedra seleccionada corresponde a sus tablas y false
#si es lo contrario.
    
def esDeMisTablas_1(numTabla, quienInicia, estadoJuego):
    if(quienInicia==0):
        if(estadoJuego==0):
            if(numTabla==3 or numTabla ==4):
                return True
            else:
                return False
        elif(estadoJuego==4):
            if(numTabla==1 or numTabla ==2):
                return True
            else:
                return False
    elif(quienInicia==1):
        if(estadoJuego==0):
            if(numTabla==1 or numTabla ==2):
                return True
            else:
                return False
        elif(estadoJuego==4):
            if(numTabla==3 or numTabla ==4):
                return True
            else:
                return False

#esDeMisTablas_2?: función que recibe el numero de la tabla en la que se jugó el movimiento pasivo, y el numero de la tabla en
# la que se está jugando el movimiento agresivo. Retorna un booleano si en la tabla de la que se seleccionó la piedra para el movimiento agresivo
# corresponde a una de diferente color que la usada para el movimiento pasivo. NOTA: no se utilizan los colores, para determinarlo, pero si las posiciones
# por defecto.
def esDeMisTablas_2(numTablaJugadaP, numTablaJugadaA):
    posibleTablaA=0
    posibleTablaB=0

    if(numTablaJugadaP==1 or numTablaJugadaP==3):
        posibleTablaA=2
        posibleTablaB=4
    else:
        posibleTablaA=1
        posibleTablaB=3

    if(numTablaJugadaA==posibleTablaA or numTablaJugadaA==posibleTablaB):
        return True
    else:
        return False


#__________________________________________________________________________________________________________________
#Reglas de Movimiento:

#movimientoPasivo: Función que principalmente verifica si el movimiento realizado por el jugador o la
#IA es valido, retorna una lista con el booleano y con la distancia Di y Dj que recorrió desde el punto
#anteriormente seleccionado.

def movimientoPasivo(i1,j1, piedra, lpj1, lpj2):
    if((i1>=0 and i1<4) and (j1>=0 and j1<4)):
        Di= i1-piedra.i
        Dj= j1-piedra.j

        tx = mapearTablaActual(piedra.numTabla, lpj1, lpj2)
            
        if(abs(Di)==2 or abs(Dj)==2):
            return posicionValida(Di, Dj, piedra.i, piedra.j, 2, tx)                     
        elif(abs(Di)==1 or abs(Dj)==1):
            return posicionValida(Di, Dj, piedra.i, piedra.j, 1, tx)
        else:
            return [False,0,0]  
    else:
        return [False,0,0]

def posicionValida(Di, Dj, i0, j0, Magnitud, tx): 
    res= False
    sentidoI=0
    sentidoJ=0
    
    #___________________________________________________________________________
    if((Di==-Magnitud and Dj==-Magnitud) and ((i0+Di>=0 and i0+Di<4) and (j0+Dj>=0 and j0+Dj<4))):
        res = True
        sentidoI=-1
        sentidoJ=-1
    elif((Di==0 and Dj==-Magnitud) and ((i0+Di>=0 and i0+Di<4) and (j0+Dj>=0 and j0+Dj<4))):
        res = True
        sentidoI=0
        sentidoJ=-1
    elif((Di==Magnitud and Dj==-Magnitud) and ((i0+Di>=0 and i0+Di<4) and (j0+Dj>=0 and j0+Dj<4))):
        res = True
        sentidoI=1
        sentidoJ=-1
    elif((Di==Magnitud and Dj==0) and ((i0+Di>=0 and i0+Di<4) and (j0+Dj>=0 and j0+Dj<4))):
        res = True
        sentidoI=1
        sentidoJ=0
    elif((Di==Magnitud and Dj==Magnitud) and ((i0+Di>=0 and i0+Di<4) and (j0+Dj>=0 and j0+Dj<4))):
        res = True
        sentidoI=1
        sentidoJ=1
    elif((Di==0 and Dj==Magnitud) and ((i0+Di>=0 and i0+Di<4) and (j0+Dj>=0 and j0+Dj<4))):
        res = True
        sentidoI=0
        sentidoJ=1
    elif((Di==-Magnitud and Dj==Magnitud) and ((i0+Di>=0 and i0+Di<4) and (j0+Dj>=0 and j0+Dj<4))):
        res = True
        sentidoI=-1
        sentidoJ=1
    elif((Di==-Magnitud and Dj==0) and ((i0+Di>=0 and i0+Di<4) and (j0+Dj>=0 and j0+Dj<4))):
        res = True
        sentidoI=-1
        sentidoJ=0
    else:
        res = False
    #_________________________________________________________________________________

    for x in range(Magnitud,0,-1):
        if(res and tx[i0+(sentidoI*x)][j0+sentidoJ*x]!=-1):
            res= False
            break
        
    return [res, Di, Dj]


#Movimiento Agresivo:___________________________________________________________________________________________
def movimientoAgresivo(Di, Dj, piedra, lpj1, lpj2):
    if(((piedra.i+Di)>=0 and (piedra.i+Di)<4) and ((piedra.j+Dj)>=0 and (piedra.j+Dj)<4)):
        
        tx = mapearTablaActual(piedra.numTabla, lpj1, lpj2)
        if(abs(Di)==2 or abs(Dj)==2):
            return posicionValidaMoviendoPiedra(Di, Dj, piedra.i, piedra.j, 2, tx)
        else:
            return posicionValidaMoviendoPiedra(Di, Dj, piedra.i, piedra.j, 1, tx)
    else:
        return [False, [], 0, 0]

def posicionValidaMoviendoPiedra(Di, Dj, i0, j0, Magnitud, tx):
    ProxCasillaI =0  #Estas variables almacenarán cual será la casilla en la qué
    ProxCasillaJ =0  #Se moverá la piedra a mover (en caso de que exista)
    sentidoI=0
    sentidoJ=0
    listaPos =[]

    #___________________________________________________________________________
    if(Di==-Magnitud and Dj==-Magnitud):
        ProxCasillaI= i0 + (Di-1)
        ProxCasillaJ= j0 + (Dj-1)
        sentidoI=-1
        sentidoJ=-1
    elif(Di==0 and Dj==-Magnitud):
        ProxCasillaI= i0 + (Di)
        ProxCasillaJ= j0 + (Dj-1)
        sentidoI=0
        sentidoJ=-1
    elif(Di==Magnitud and Dj==-Magnitud):
        ProxCasillaI= i0 + (Di+1)
        ProxCasillaJ= j0 + (Dj-1)
        sentidoI=1
        sentidoJ=-1
    elif(Di==Magnitud and Dj==0):
        ProxCasillaI= i0 + (Di+1)
        ProxCasillaJ= j0 + (Dj)
        sentidoI=1
        sentidoJ=0
    elif(Di==Magnitud and Dj==Magnitud):
        ProxCasillaI= i0 + (Di+1)
        ProxCasillaJ= j0 + (Dj+1)
        sentidoI=1
        sentidoJ=1
    elif(Di==0 and Dj==Magnitud):
        ProxCasillaI= i0 + (Di)
        ProxCasillaJ= j0 + (Dj+1)
        sentidoI=0
        sentidoJ=1
    elif(Di==-Magnitud and Dj==Magnitud):
        ProxCasillaI= i0 + (Di-1)
        ProxCasillaJ= j0 + (Dj+1)
        sentidoI=-1
        sentidoJ=1
    elif(Di==-Magnitud and Dj==0):
        ProxCasillaI= i0 + (Di-1)
        ProxCasillaJ= j0 + (Dj)
        sentidoI=-1
        sentidoJ=0
        #_________________________________________________________________________________

    for x in range(Magnitud,0,-1):
        if(tx[i0+(sentidoI*x)][j0+(sentidoJ*x)]!=-1):
            listaPos.append(i0+(sentidoI*x))
            listaPos.append(j0+(sentidoJ*x))
                
    if(len(listaPos)>2 and len(listaPos)==Magnitud*2):
        return [False, [], 0, 0]
    elif((ProxCasillaI>=0 and ProxCasillaI<4) and (ProxCasillaJ>=0 and ProxCasillaJ<4)):
        if(tx[ProxCasillaI][ProxCasillaJ]!=-1 and len(listaPos)>=2):
            return [False, [], 0, 0]
        else:
            return [True, listaPos, ProxCasillaI, ProxCasillaJ]
    else:
        return [True, listaPos, ProxCasillaI, ProxCasillaJ]

#______________________________________________________________________________________________________________

def mapearTablaActual(numTabla, lpj1, lpj2):
    tx = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]

    for x in lpj1:
        if(x.numTabla==numTabla):
            if(x.color==0):
                tx[x.i][x.j] = 0
            else:
                tx[x.i][x.j] = 1

    for y in lpj2:
        if(y.numTabla==numTabla):
            if(y.color==0):
                tx[y.i][y.j] = 0
            else:
                tx[y.i][y.j] = 1
    return tx
#___________________________________________________________________________________________________________
def ganador(lpj1, lpj2):
    T1 = 0
    T2 = 0
    T3 = 0
    T4 = 0
    for piedra in lpj2:
        if(piedra.numTabla == 1):
            T1 += 1
        if(piedra.numTabla == 2):
            T2 += 1
        if(piedra.numTabla == 3):
            T3 += 1
        if(piedra.numTabla == 4):
            T4 += 1
    if(T1 == 0 or T2 == 0 or T3 == 0 or T4 == 0):
        return 1

    for piedra in lpj1:
        if(piedra.numTabla == 1):
            T1 += 1
        if(piedra.numTabla == 2):
            T2 += 1
        if(piedra.numTabla == 3):
            T3 += 1
        if(piedra.numTabla == 4):
            T4 += 1
    if(T1 == 0 or T2 == 0 or T3 == 0 or T4 == 0):
        return -1
    else: 
        return 0
