import os
from collections import deque
# =====================================================================
# ENTIDAD BASE ()
# =====================================================================
class Vehiculo: 
    def __init__(self, placa, propietario, tipo):
        self.placa = placa.upper()
        self.propietario = propietario
        self.tipo = tipo.capitalize() # Sedan, Motocicleta, Camion

# =====================================================================
# 1. COLA (FIFO) - Espera de ingreso
# =====================================================================
class ColaEspera:
    def __init__(self):
        self.items = deque()

    def encolar(self, vehiculo):
        self.items.append(vehiculo)

    def desencolar(self):
        return self.items.popleft() if self.items else None
    
    def mostrar(self):
        if not self.items: return "Vacia"
        return " <- ".join([f"[{v.placa}]" for v in self.items])
    
# =====================================================================
# 2. PILA (LIFO) - Historial reciente / Deshacer
# =====================================================================
class PilaHistorial:
    def __init__(self):
        self.historial = []

    def registrar(self, accion, vehiculo, zona=""):
        self.historial.append((accion, vehiculo, zona))

    def desapilar(self):
        return self.historial.pop() if self.historial else None
    
    def mostrar(self):
        if not self.historial: return "Sin acciones recientes."
        return "\n".join([f" | {act.upper()}: {v.placa} en {z}" for act, v, z in reversed(self.historial)])
    

# =====================================================================
# 3. LISTA ENLAZADA - Registro permanente de usuarios
# =====================================================================
class NodoLista:
    def __init__(self, vehiculo):
        self.vehiculo = vehiculo
        self.siguiente = None

class ListaRegistrados:
    def __init__(self):
        self.cabeza = None

    def registrar(self, vehiculo):
        nuevo = NodoLista(vehiculo)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo

    # RECURSIVIDAD en la busqueda de la Lista Enlazada
    def buscar_recursivo(self, nodo, placa):
        if nodo is None: return None
        if nodo.vehiculo.placa == placa.upper(): return nodo.vehiculo
        return self.buscar_recursivo(nodo.siguiente, placa)

    def mostrar(self):
        if not self.cabeza: return "Ninguno"
        res, actual = [], self.cabeza
        while actual:
            res.append(f"[{actual.vehiculo.placa}: {actual.vehiculo.propietario}]")
            actual = actual.siguiente
        return " -> ".join(res) + " -> None"


# =====================================================================
# 4. ARBOL N-ARIO - Clasificacion por Tipo de Vehiculo
# =====================================================================
class NodoArbol:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []
        self.vehiculos = []

    def clasificar(self, tipo, placa):
        if self.nombre.lower() == tipo.lower():
            self.vehiculos.append(placa.upper())
            return True
        for hijo in self.hijos:
            if hijo.clasificar(tipo, placa): return True
        return False

    def remover(self, placa):
        if placa.upper() in self.vehiculos:
            self.vehiculos.remove(placa.upper())
            return True
        for hijo in self.hijos:
            if hijo.remover(placa): return True
        return False

    # RECURSIVIDAD para dibujar las ramas de la jerarquia
    def obtener_diagrama(self, nivel=0):
        espacios = "   " * nivel
        lista_v = f" Ocupantes: {self.vehiculos}" if self.vehiculos else ""
        resultado = f"{espacios}└── {self.nombre}{lista_v}\n"
        for hijo in self.hijos:
            resultado += hijo.obtener_diagrama(nivel + 1)
        return resultado

# =====================================================================
# 5. GRAFO Y 6. RECURSIVIDAD - Conexiones y Busqueda de espacios
# =====================================================================
class GrafoParqueo:
    def __init__(self):
        self.zonas = {}

    def crear_zona(self, nombre, capacidad):
        self.zonas[nombre] = {'conexiones': [], 'capacidad': capacidad, 'ocupados': 0}

    def conectar(self, z1, z2):
        if z1 in self.zonas and z2 in self.zonas:
            self.zonas[z1]['conexiones'].append(z2)
            self.zonas[z2]['conexiones'].append(z1)

    # RECURSIVIDAD + GRAFO: Muestra visual del recorrido paso a paso
    def buscar_espacio_dfs(self, actual, visitados=None, ruta_recorrido=None):
        if visitados is None: visitados = set()
        if ruta_recorrido is not None: ruta_recorrido.append(actual)

        visitados.add(actual)
        info = self.zonas[actual]

        # Si encontramos espacio disponible y no es la zona neutra de Entrada
        if info['ocupados'] < info['capacidad'] and actual != "Entrada":
            info['ocupados'] += 1
            return actual

        # Recorrido recursivo a traves de las aristas del grafo
        for vecina in info['conexiones']:
            if vecina not in visitados:
                zona_libre = self.buscar_espacio_dfs(vecina, visitados, ruta_recorrido)
                if zona_libre: return zona_libre
        return None

    def liberar_espacio(self, zona):
        if zona in self.zonas and self.zonas[zona]['ocupados'] > 0:
            self.zonas[zona]['ocupados'] -= 1
            return True
        return False

    def mostrar(self):
        res = ""
        for zona, datos in self.zonas.items():
            bar = "X" * datos['ocupados'] + "." * (datos['capacidad'] - datos['ocupados'])
            res += f"  [{zona}] [{bar}] ({datos['ocupados']}/{datos['capacidad']}) -> Vias: {datos['conexiones']}\n"
        return res


# =====================================================================
# SISTEMA PRINCIPAL INTERACTIVO
# =====================================================================
def inicializar():
    cola, pila, lista, grafo = ColaEspera(), PilaHistorial(), ListaRegistrados(), GrafoParqueo()
    
    # Arbol base
    arbol = NodoArbol("Parqueo_General")
    arbol.hijos.extend([NodoArbol("Sedan"), NodoArbol("Motocicleta"), NodoArbol("Camion")])

    # Grafo base
    grafo.crear_zona("Entrada", capacidad=0)
    grafo.crear_zona("Zona_A", capacidad=2)
    grafo.crear_zona("Zona_B", capacidad=2)
    grafo.crear_zona("Sect_VIP", capacidad=1)
    
    grafo.conectar("Entrada", "Zona_A")
    grafo.conectar("Zona_A", "Zona_B")
    grafo.conectar("Zona_B", "Sect_VIP")

    return cola, pila, lista, arbol, grafo

def ejecutor():
    cola, pila, lista, arbol, grafo = inicializar()

    while True:
        print("\n" + "="*60)
        print(" ESTADO DEL SISTEMA")
        print("="*60)
        print(f"Lista Registrados : {lista.mostrar()}")
        print(f"Cola de espera:     {cola.mostrar()}")
        print(f"\nTipos de autos:\n{arbol.obtener_diagrama()}")
        print(f"Zonas:\n{grafo.mostrar()}")
        print("="*60)
        print(" 1. Registrar Auto\n 2. Poner Auto en Cola de Espera\n 3. Procesar Entrada\n 4. Registrar Salida\n 5. Deshacer Movimiento\n 0. Salir")
        print("="*60)

        opc = input("Opcion: ").strip()
        print("-" * 60)

        if opc == "1":
            placa = input("Placa: ").strip().upper()
            prop = input("Dueño: ").strip()
            tipo = input("Tipo (Sedan/Motocicleta/Camion): ").strip()
            lista.registrar(Vehiculo(placa, prop, tipo))
            print("Vehiculo guardado en la lista enlazada.")

        elif opc == "2":
            placa = input("Placa del auto que llega: ").strip().upper()
            v = lista.buscar_recursivo(lista.cabeza, placa)
            if v:
                cola.encolar(v)
                print(f"El vehiculo de {v.propietario} se unio a la cola de espera.")
            else:
                print("Error: El vehiculo debe estar registrado en la lista primero.")

        elif opc == "3":
            vehiculo = cola.desencolar()
            if not vehiculo:
                print("No hay vehiculos en la cola de espera.")
                continue

            ruta_recorrido = []
            zona_libre = grafo.buscar_espacio_dfs("Entrada", visitados=None, ruta_recorrido=ruta_recorrido)

            # Muestra el camino que tomo la recursividad en el grafo
            print(f"RECORRIDO RECURSIVO: {' -> '.join(ruta_recorrido)}")

            if zona_libre:
                arbol.clasificar(vehiculo.tipo, vehiculo.placa)
                pila.registrar("entrada", vehiculo, zona_libre)
                print(f"¡Asignado con exito a {zona_libre}!")
            else:
                print("No se encontraron espacios. El auto vuelve al inicio de la cola.")
                cola.items.appendleft(vehiculo)

        elif opc == "4":
            placa = input("Placa a retirar: ").strip().upper()
            zona = input("¿De que zona sale?: ").strip()
            if grafo.liberar_espacio(zona):
                arbol.remover(placa)
                print(f"Vehiculo {placa} salio de la {zona}.")
            else:
                print("No se pudo liberar el espacio (Zona vacia o incorrecta).")

        elif opc == "5":
            ultimo = pila.desapilar()
            if ultimo:
                accion, v, zona = ultimo
                if accion == "entrada":
                    grafo.liberar_espacio(zona)
                    arbol.remover(v.placa)
                    cola.items.appendleft(v)
                    print(f"Anulado: {v.placa} removido de {zona} y devuelto a la cola.")
            else:
                print("Nada que deshacer en la Pila.")

        elif opc == "0":
            break

if __name__ == "__main__":
    ejecutor()