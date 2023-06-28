"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem
from node import Node
from random import choice
import random
from time import time


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            # Buscar las acciones que generan el  mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local
            if diff[act] <= 0:

                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end-start
                return

            # Sino, moverse a un nodo con el estado sucesor
            else:

                actual = Node(problem.result(actual.state, act),
                              actual.value + diff[act])
                self.niters += 1


class HillClimbingReset(LocalSearch):
    def solve(self, problem: OptProblem):
        start = time()
        actual = Node(problem.init, problem.obj_val(problem.init))
        n=20
        choise_limit = 2 #elijo un límite de veces para probar con el mismo candidato
        mejor_value=actual.value
        mejor_tour=actual.state
        #creo un for para generar n reinicios
        for i in range(0, n):
            while True:
                acts_old = []
                diff = problem.val_diff(actual.state)
                max_acts = [act for act, val in diff.items() if val ==
                            max(diff.values())]
                act = choice(max_acts)
                ##print(act)
                #registro cuentas veces elegí el mismo act
                if act in acts_old:
                    choise_limit -= 1
                #si excedo el límite de repeticiones de candidato, corto el bucle
                if choise_limit == 0:
                    break              
                acts_old.append(act)
                #como puede ser un máximo local almacena state y value pero no corta el tiempo
                if diff[act] <= 0:
                    if actual.value >= mejor_value:
                        mejor_tour = actual.state
                        mejor_value = actual.value
                    init_copy = problem.init.copy()
                    init_copy.pop()
                    random.shuffle(init_copy)
                    init_copy = init_copy + [init_copy[0]]
                    actual = Node(init_copy, problem.obj_val(init_copy))
                    break
                else:
                    actual = Node(problem.result(actual.state, act),
                                actual.value + diff[act])
                    self.niters += 1
            if choise_limit == 0:
                print("El candidato ya no puede volver a repetirse, exit")
                break 
            self.niters += 1      
        self.value = mejor_value
        self.tour = mejor_tour
        end = time()
        self.time = end-start


class Tabu(LocalSearch):
    def solve(self, problem: OptProblem):
        # Inicio del reloj
        start = time()
        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))
        mejor_value = actual.value
        mejor_tour = actual.state
        #n define el nro de nodos del grafo  
        n=len(actual.state)-1
        #a define el multiplicador de n para definir el nro de iteraciones c
        a=100         
        c=a*n
        #p define en cuánto voy a reducir el tamaño de la lista tabú (len max tabu = a*n/p)
        p=3
        tabu=[]
        while c > 0:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)  #diff es un diccionario
            diff = {vecino: val for vecino, val in diff.items() if problem.result(actual.state, vecino) not in tabu}
            # Buscar las acciones que generan el  mayor incremento de valor obj
            max_acts = [vecino for vecino, val in diff.items() if val ==
                        max(diff.values())]
            # Elegir una accion aleatoria
            vecino = choice(max_acts)
            # Moverse a un nodo con el estado sucesor
            if diff[vecino] > 0 and actual.value + diff[vecino] > mejor_value:
                mejor_value = actual.value + diff[vecino]
                mejor_tour = problem.result(actual.state, vecino)
            #si no retornar si estamos en un optimo local
            else:
                c-=1
            #print(c , ',' , mejor_value , ',' , actual.state)
            tabu.append(actual.state)
            if len(tabu)>(a*n)/p:
                tabu.pop(0)
            actual = Node(problem.result(actual.state, vecino), actual.value + diff[vecino])
            self.niters += 1
        self.tour = mejor_tour
        self.value = mejor_value
        end = time()
        self.time = end-start
        print(len(tabu))
        return
