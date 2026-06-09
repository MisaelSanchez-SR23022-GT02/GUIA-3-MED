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