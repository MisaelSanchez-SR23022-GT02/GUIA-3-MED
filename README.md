# Sistema de Parqueo

Este programa simula el funcionamiento de un estacionamiento. Permite registrar vehiculos, ponerlos en fila de espera, asignarles un espacio disponible, registrar su salida y deshacer acciones si se comete un error.

Todo esta desarrollado en Python puro, sin librerias externas.

---

## Como funciona

El sistema tiene cinco acciones principales que se manejan desde un menu:

**1. Registrar un vehiculo**
Antes de hacer cualquier cosa, el vehiculo debe estar registrado con su placa, el nombre del dueno y el tipo (Sedan, Motocicleta o Camion). Esto lo guarda en una lista interna.

**2. Ponerlo en la cola de espera**
Una vez registrado, el vehiculo puede unirse a la fila de espera. Los autos se atienden en orden de llegada: el primero en llegar es el primero en entrar.

**3. Procesar la entrada**
El sistema toma el primer vehiculo de la fila y busca automaticamente un espacio libre en el parqueo. Recorre las zonas en orden (Entrada -> Zona A -> Zona B -> Sector VIP) y asigna el primer lugar disponible. Si no hay espacio, el vehiculo vuelve al inicio de la fila.

**4. Registrar la salida**
Cuando un vehiculo se va, se indica su placa y la zona donde estaba. El espacio queda libre para el siguiente.

**5. Deshacer el ultimo movimiento**
Si se cometio un error al procesar una entrada, esta opcion lo revierte: el vehiculo vuelve a la fila y el espacio queda libre de nuevo.

---

## Zonas del parqueo

El parqueo tiene cuatro zonas conectadas en secuencia:

```
Entrada -- Zona A (2 espacios) -- Zona B (2 espacios) -- Sector VIP (1 espacio)
```

La Entrada es solo el punto de acceso y no tiene espacios de estacionamiento.

---

## Ejecucion

```bash
python parqueo.py
```

Al correr el programa, se muestra el estado actual del sistema en cada paso: la lista de vehiculos registrados, la cola de espera, las zonas ocupadas y la clasificacion por tipo de vehiculo.

---

## Requisitos

Python 3.6 o superior. No necesita instalar nada adicional.
