# 4LabGenericos

> Implementación de una cola de prioridad genérica (max-heap) aplicada a un sistema de gestión de emergencias hospitalarias.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Typing](https://img.shields.io/badge/typing-Generic%20%7C%20TypeVar-007ACC)
![Stdlib](https://img.shields.io/badge/stdlib-heapq%20%7C%20dataclasses%20%7C%20enum-4B8BBE)
![License](https://img.shields.io/badge/license-Acad%C3%A9mico%20UCAB-lightgrey)

## Overview

Este repositorio contiene el **Laboratorio 4** de la materia *Tópicos Especiales de Programación* (UCAB). El objetivo es demostrar el uso de **genéricos en Python** mediante la implementación desde cero de una `PriorityQueue[T]` capaz de almacenar cualquier tipo de objeto junto con una prioridad numérica, garantizando que el elemento de **mayor prioridad** sea extraído primero.

La estructura interna utiliza `heapq` con inversión de signo para simular un **max-heap**, resolviendo empates de prioridad con un contador monotónico (`itertools.count`) que preserva el orden FIFO entre elementos de igual prioridad.

El caso de estudio modela un **servicio de urgencias hospitalarias**: las tareas clínicas (`TareaMedica`) se encolan mezclando el orden de llegada, pero se procesan estrictamente por gravedad (`Gravedad`: ALTA → MEDIA → BAJA), demostrando que la cola ordena por prioridad y no por orden de inserción.

## Stack Tecnológico

- **Lenguaje core:** Python 3.10+ (probado con Python 3.14)
- **Genéricos y tipado:** `typing.Generic`, `TypeVar`, anotaciones estándar (`from __future__ import annotations`)
- **Estructura de datos:** `heapq` (max-heap simulado), `itertools.count` (desempate estable)
- **Modelado de dominio:** `dataclasses` (`frozen`, `slots`), `enum.IntEnum`
- **Base de datos:** N/A — ejecución en memoria, sin persistencia
- **Testing:** N/A — validación mediante simulación interactiva en consola (`__main__`)

## Requisitos Previos

| Herramienta | Versión recomendada | Notas |
|---|---|---|
| **Python** | ≥ 3.10 | Único runtime requerido |
| **pip / venv** | Opcional | No hay dependencias externas |
| **Docker** | No requerido | — |
| **Node.js** | No requerido | — |

Verifica tu instalación:

```bash
python3 --version
```

## Configuración Local (Quick Start)

Este proyecto no utiliza `package.json`, `Makefile`, `pyproject.toml` ni gestor de dependencias. Es un módulo Python autónomo de la biblioteca estándar.

1. **Clona o accede al directorio del repositorio:**

   ```bash
   cd /Users/victorserrano/UCAB/TOPICOS/LABS/4LabGenericos
   ```

2. **(Opcional) Crea y activa un entorno virtual:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   # .venv\Scripts\activate    # Windows
   ```

3. **Ejecuta la simulación del sistema de urgencias:**

   ```bash
   python3 laboratorio4.py
   ```

4. **Verifica la salida esperada.** Las tareas deben procesarse en orden de prioridad clínica, independientemente del orden de encolado:

   ```
   ALTA  → Intubación por dificultad respiratoria
   MEDIA → Reducción de fractura abierta
   BAJA  → Suministrar medicamento programado
   ```

> **Nota:** No existen pasos de instalación (`pip install`) ni servicios auxiliares (Postgres, Redis, Docker). El script es ejecutable directamente.

## Variables de Entorno

Este proyecto **no define variables de entorno**. No existe archivo `.env`, `.env.example` ni configuración externa.

| Variable | Descripción | Ejemplo |
|---|---|---|
| — | No aplica | — |

Todos los datos de la simulación (pacientes, tareas, prioridades) están codificados en el bloque `if __name__ == "__main__":` de `laboratorio4.py`.

## Estructura del Proyecto

```
4LabGenericos/
├── laboratorio4.py          # Módulo único: cola genérica + dominio hospitalario + simulación
│   ├── QueueEmptyError      # Excepción de dominio para cola vacía
│   ├── PriorityQueue[T]     # Cola de prioridad genérica (max-heap)
│   ├── Gravedad             # Enum de prioridad médica (BAJA, MEDIA, ALTA)
│   ├── Paciente             # Dataclass inmutable del paciente
│   ├── TareaMedica          # Dataclass inmutable de la acción clínica
│   └── __main__             # Entry point: simulación de urgencias en consola
└── README.md                # Documentación del repositorio
```

## Contexto Académico

> **Nota sobre el ecosistema MM4D:** Este repositorio **no forma parte** del ecosistema MM4D (`mm4d-api` / `mm4d-console`). Es un laboratorio académico independiente para la materia *Tópicos Especiales de Programación*.

| Aspecto | Detalle |
|---|---|
| **Tipo de aplicación** | Script CLI / módulo Python ejecutable |
| **Interfaz** | Consola estándar (`stdout`) |
| **API / Swagger** | No aplica — sin servidor HTTP ni endpoints REST |
| **Frontend / SPA** | No aplica — sin cliente web ni `VITE_API_URL` |
| **Modo mock** | No aplica — datos de prueba embebidos en `__main__` |

### Componentes expuestos para reutilización

Si deseas importar la cola genérica en otro módulo:

```python
from laboratorio4 import PriorityQueue, QueueEmptyError, TareaMedica, Paciente, Gravedad

cola: PriorityQueue[TareaMedica] = PriorityQueue()
cola.enqueue(mi_tarea, priority=int(Gravedad.ALTA))
siguiente = cola.dequeue()
```

### Criterios de evaluación cubiertos

- Genéricos con `TypeVar` y `Generic[T]`
- Encapsulamiento (`self._queue`, atributos privados)
- Excepción personalizada (`QueueEmptyError`)
- Docstrings estilo Google en clases y métodos
- Simulación demostrativa con `peek()`, `size()` y procesamiento por prioridad
# 4Lab-Genericos
