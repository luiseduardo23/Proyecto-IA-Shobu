import math


def minimax(posicion,profundidadExploracion,alfa,beta,JugadorMaximiza):

    if profundidadExploracion == 0 or len(posicion.hijos)==0:# si es la profundidad maxima hasta la que se va a explorar, o el maximo de profundidad del arbol(cuando el juego acaba en esa jugada)
        return posicion.utilidad

    if JugadorMaximiza==0:
        EvaluacionMaxima=(-math.inf)
        for hijo in range(len(posicion.hijos)):
            evaluacion= minimax(posicion.hijos[hijo],profundidadExploracion-1,alfa,beta,1)
            comparador=EvaluacionMaxima
            EvaluacionMaxima= max(EvaluacionMaxima,evaluacion)
            if comparador !=EvaluacionMaxima and posicion.hijos[hijo].profundidad==1:
                posicion.seleccion=hijo
            alfa= max(alfa,evaluacion)
            if beta <= alfa:
                break
        return EvaluacionMaxima
    else:
        EvaluacionMinima=math.inf
        for hijo in range(len(posicion.hijos)):
            evaluacion= minimax(posicion.hijos[hijo],profundidadExploracion-1,alfa,beta,0)
            comparador=EvaluacionMinima
            EvaluacionMinima= min(EvaluacionMinima,evaluacion)  
            if comparador !=EvaluacionMinima  and posicion.hijos[hijo].profundidad==1:
                posicion.seleccion=hijo
            beta= min(beta,evaluacion)
            if beta <= alfa:
                break
        return EvaluacionMinima
