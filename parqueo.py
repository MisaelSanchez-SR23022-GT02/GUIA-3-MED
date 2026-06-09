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
