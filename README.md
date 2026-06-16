<div align="center">

# 🏥 4LabGenericos

**Cola de prioridad genérica en Python · Caso de urgencias hospitalarias**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Typing](https://img.shields.io/badge/Generics-TypeVar%20%7C%20Generic-007ACC?style=for-the-badge)
![Stdlib](https://img.shields.io/badge/Dependencias-0%20externas-4B8BBE?style=for-the-badge)
![UCAB](https://img.shields.io/badge/UCAB-T%C3%B3picos%20Especiales-E31937?style=for-the-badge)

<br/>

![heapq](https://img.shields.io/badge/heapq-max--heap-306998)
![dataclasses](https://img.shields.io/badge/dataclasses-frozen%20%7C%20slots-FF6F00)
![enum](https://img.shields.io/badge/enum-IntEnum-009688)
![CLI](https://img.shields.io/badge/interfaz-CLI%20consola-607D8B)

</div>

---

## 🎯 ¿Qué hace este proyecto?

Este repositorio implementa una **`PriorityQueue[T]`** genérica en Python puro y la aplica a un **servicio de urgencias hospitalarias**. Las tareas clínicas llegan en cualquier orden, pero el sistema las procesa **siempre por gravedad médica**, no por orden de llegada.

```mermaid
flowchart LR
    subgraph Llegada["📥 Orden de llegada"]
        A1["1️⃣ BAJA<br/>Medicamento"]
        A2["2️⃣ ALTA<br/>Intubación"]
        A3["3️⃣ MEDIA<br/>Fractura"]
    end

    subgraph Cola["⚡ PriorityQueue[T]"]
        PQ["Max-Heap<br/>heapq + desempate FIFO"]
    end

    subgraph Salida["📤 Orden de atención"]
        B1["🔴 ALTA → Intubación"]
        B2["🟡 MEDIA → Fractura"]
        B3["🟢 BAJA → Medicamento"]
    end

    A1 & A2 & A3 --> PQ --> B1 --> B2 --> B3

    style B1 fill:#ffcdd2,stroke:#c62828
    style B2 fill:#fff9c4,stroke:#f9a825
    style B3 fill:#c8e6c9,stroke:#2e7d32
```

| Pregunta | Respuesta |
|:--|:--|
| **¿Qué es?** | Laboratorio 4 — *Tópicos Especiales de Programación* (UCAB) |
| **¿Qué problema resuelve?** | Ordenar tareas por prioridad clínica, independiente del orden de encolado |
| **¿Cómo?** | Max-heap genérico con `heapq` + modelo de dominio hospitalario |
| **¿Dependencias?** | Ninguna — solo biblioteca estándar de Python |

---

## 🧠 Idea central en 30 segundos

```
  ORDEN DE LLEGADA          COLA DE PRIORIDAD           ORDEN REAL DE ATENCIÓN
  ─────────────────         ─────────────────           ─────────────────────

  ① BAJA  ──┐                                          🔴 ALTA  (prioridad 3)
  ② ALTA  ──┼──►  [ heap interno ]  ──dequeue()──►     🟡 MEDIA (prioridad 2)
  ③ MEDIA ──┘                                          🟢 BAJA  (prioridad 1)

        ❌ No es FIFO                    ✅ Es "el más grave primero"
```

> 💡 **Insight clave:** `heapq` en Python implementa un *min-heap*. Multiplicamos la prioridad por `-1` para simular un **max-heap** sin reescribir el algoritmo.

---

## 🏗️ Arquitectura del módulo

El proyecto es un **monolito de un solo archivo** organizado en tres capas bien separadas:

```mermaid
flowchart TB
    subgraph Capa1["🔧 Capa de Infraestructura"]
        PQ["PriorityQueue[T]<br/>enqueue · dequeue · peek · size"]
        ERR["QueueEmptyError"]
    end

    subgraph Capa2["🩺 Capa de Dominio Clínico"]
        G["Gravedad<br/>BAJA=1 · MEDIA=2 · ALTA=3"]
        P["Paciente<br/>id · nombre · edad · diagnóstico"]
        T["TareaMedica<br/>descripción · paciente · gravedad"]
    end

    subgraph Capa3["🖥️ Capa de Presentación"]
        MAIN["__main__<br/>Simulación CLI en consola"]
    end

    MAIN --> PQ
    MAIN --> T
    T --> P
    T --> G
    PQ -.-> ERR

    style Capa1 fill:#e3f2fd,stroke:#1565c0
    style Capa2 fill:#fce4ec,stroke:#c2185b
    style Capa3 fill:#f3e5f5,stroke:#7b1fa2
```

### Diagrama de clases

```mermaid
classDiagram
    class PriorityQueue~T~ {
        -list _queue
        -counter _counter
        +enqueue(item, priority)
        +dequeue() T
        +peek() T
        +is_empty() bool
        +size() int
    }

    class QueueEmptyError {
        <<Exception>>
    }

    class Gravedad {
        <<IntEnum>>
        BAJA = 1
        MEDIA = 2
        ALTA = 3
    }

    class Paciente {
        <<dataclass frozen>>
        +str id_paciente
        +str nombre
        +int edad
        +str diagnostico
    }

    class TareaMedica {
        <<dataclass frozen>>
        +str descripcion
        +Paciente paciente
        +Gravedad gravedad
    }

    PriorityQueue --> QueueEmptyError : lanza
    TareaMedica --> Paciente : contiene
    TareaMedica --> Gravedad : usa
    PriorityQueue ..> TareaMedica : T = TareaMedica
```

---

## ⚙️ Cómo funciona el Max-Heap

Cada entrada en la cola es una tupla de tres elementos:

```
┌─────────────────────────────────────────────────────────────┐
│  entry = ( -prioridad ,  contador ,  item )                 │
│             ▲               ▲          ▲                     │
│             │               │          └── Tu objeto T       │
│             │               └── Desempate FIFO (itertools)   │
│             └── Signo invertido → max-heap con heapq         │
└─────────────────────────────────────────────────────────────┘
```

### Visualización del heap durante la simulación

Después de encolar las 3 tareas (BAJA → ALTA → MEDIA), el heap interno queda así:

```
                    ┌─────────────────┐
                    │  (-3, 1, ALTA)  │  ◄── raíz: mayor prioridad
                    └────────┬────────┘
              ┌──────────────┴──────────────┐
     ┌────────┴────────┐         ┌─────────┴─────────┐
     │ (-2, 2, MEDIA)  │         │  (-1, 0, BAJA)   │
     └─────────────────┘         └───────────────────┘

     peek()  →  Tarea ALTA  (intubación)
     dequeue →  extrae ALTA, reordena heap
     dequeue →  extrae MEDIA
     dequeue →  extrae BAJA
```

### Flujo de operaciones

```mermaid
sequenceDiagram
    actor Usuario
    participant Main as __main__
    participant Cola as PriorityQueue[T]
    participant Heap as heapq

    Usuario->>Main: python3 laboratorio4.py
    Main->>Cola: enqueue(tarea_baja, priority=1)
    Cola->>Heap: heappush(-1, counter, item)
    Main->>Cola: enqueue(tarea_alta, priority=3)
    Cola->>Heap: heappush(-3, counter, item)
    Main->>Cola: enqueue(tarea_media, priority=2)
    Cola->>Heap: heappush(-2, counter, item)

    Main->>Cola: peek()
    Cola-->>Main: tarea_alta 🔴

    loop mientras no esté vacía
        Main->>Cola: dequeue()
        Cola->>Heap: heappop()
        Cola-->>Main: tarea por prioridad
    end
```

---

## 🚦 Niveles de prioridad clínica

| Nivel | Valor | Badge | Ejemplo en la simulación |
|:-----:|:-----:|:-----:|:--|
| 🔴 **ALTA** | `3` | ![ALTA](https://img.shields.io/badge/Gravedad-ALTA-red) | Intubación por dificultad respiratoria |
| 🟡 **MEDIA** | `2` | ![MEDIA](https://img.shields.io/badge/Gravedad-MEDIA-yellow) | Reducción de fractura abierta |
| 🟢 **BAJA** | `1` | ![BAJA](https://img.shields.io/badge/Gravedad-BAJA-green) | Suministrar medicamento programado |

---

## 🚀 Quick Start

```mermaid
flowchart LR
    S1["1️⃣ Clonar repo"] --> S2["2️⃣ cd al directorio"]
    S2 --> S3["3️⃣ python3 laboratorio4.py"]
    S3 --> S4["4️⃣ Ver salida en consola"]

    style S3 fill:#c8e6c9,stroke:#2e7d32
```

**Paso 1 — Clona o entra al directorio**

```bash
git clone <url-del-repo>
cd 4LabGenericos
```

**Paso 2 — (Opcional) Entorno virtual**

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
```

**Paso 3 — Ejecuta la simulación**

```bash
python3 laboratorio4.py
```

**Paso 4 — Salida esperada**

```
========================================================================
============ SISTEMA DE GESTION DE EMERGENCIAS HOSPITALARIAS ===========
========================================================================

[Ingreso de tareas en orden de llegada (mezclado)]
 + Encolada: Tarea: Suministrar medicamento...  | Prioridad: BAJA
 + Encolada: Tarea: Intubacion...              | Prioridad: ALTA
 + Encolada: Tarea: Reduccion de fractura...   | Prioridad: MEDIA

[Procesamiento por prioridad medica]
 > Ejecutando: ... Intubacion ...              | Prioridad: ALTA   🔴
 > Ejecutando: ... Reduccion de fractura ...   | Prioridad: MEDIA  🟡
 > Ejecutando: ... Suministrar medicamento ... | Prioridad: BAJA   🟢
```

> ✅ **Sin `pip install`**, sin Docker, sin `.env`. Solo Python 3.10+.

---

## 📁 Estructura del proyecto

```
4LabGenericos/
│
├── 📄 laboratorio4.py          ← Módulo único (todo vive aquí)
│   │
│   ├── 🔴 QueueEmptyError      Excepción personalizada
│   ├── 🔵 PriorityQueue[T]     Cola genérica (max-heap)
│   ├── 🟠 Gravedad             Enum de prioridad médica
│   ├── 🟢 Paciente             Dataclass inmutable
│   ├── 🟣 TareaMedica          Dataclass de acción clínica
│   └── ▶️  __main__             Entry point CLI
│
└── 📖 README.md
```

---

## 🛠️ Stack tecnológico

<table>
<tr>
  <td align="center"><br/><strong>🐍 Python 3.10+</strong><br/><sub>Lenguaje core</sub><br/><br/></td>
  <td align="center"><br/><strong>🔤 TypeVar + Generic</strong><br/><sub>Genéricos</sub><br/><br/></td>
  <td align="center"><br/><strong>📊 heapq</strong><br/><sub>Max-heap simulado</sub><br/><br/></td>
  <td align="center"><br/><strong>📦 dataclasses</strong><br/><sub>frozen + slots</sub><br/><br/></td>
  <td align="center"><br/><strong>🏷️ enum.IntEnum</strong><br/><sub>Prioridades tipadas</sub><br/><br/></td>
</tr>
<tr>
  <td align="center" colspan="5">
    <br/>
    <img src="https://img.shields.io/badge/PostgreSQL-No%20requerido-lightgrey?style=flat-square" />
    <img src="https://img.shields.io/badge/Docker-No%20requerido-lightgrey?style=flat-square" />
    <img src="https://img.shields.io/badge/API%20REST-No%20aplica-lightgrey?style=flat-square" />
    <img src="https://img.shields.io/badge/Frontend-No%20aplica-lightgrey?style=flat-square" />
    <br/><br/>
  </td>
</tr>
</table>

### Requisitos previos

| Herramienta | Versión | ¿Obligatorio? |
|:--|:--|:--:|
| Python | ≥ 3.10 | ✅ Sí |
| pip / venv | Cualquiera | ⚪ Opcional |
| Docker | — | ❌ No |
| Node.js | — | ❌ No |

```bash
python3 --version   # debe mostrar 3.10 o superior
```

---

## 🔌 Reutilizar la cola en otro módulo

```python
from laboratorio4 import PriorityQueue, QueueEmptyError, TareaMedica, Paciente, Gravedad

cola: PriorityQueue[TareaMedica] = PriorityQueue()

paciente = Paciente("P-004", "María López", 28, "Crisis asmática")
tarea = TareaMedica("Nebulización urgente", paciente, Gravedad.ALTA)

cola.enqueue(tarea, priority=int(Gravedad.ALTA))
print(cola.peek())       # muestra sin extraer
siguiente = cola.dequeue() # extrae la de mayor prioridad
```

---

## ✅ Criterios de evaluación cubiertos

```mermaid
mindmap
  root((Laboratorio 4))
    Genéricos
      TypeVar T
      Generic T
      PriorityQueue T
    OOP
      Encapsulamiento
      Dataclasses inmutables
      Excepción personalizada
    Estructuras
      Max-heap con heapq
      Desempate FIFO
    Documentación
      Docstrings Google
      Simulación CLI
```

| Criterio | Implementación |
|:--|:--|
| Genéricos | `TypeVar("T")` + `class PriorityQueue(Generic[T])` |
| Encapsulamiento | `self._queue`, `self._counter` privados |
| Excepción propia | `QueueEmptyError` en `dequeue()` y `peek()` |
| Docstrings | Estilo Google en todas las clases y métodos |
| Demostración | `peek()`, `size()`, loop de procesamiento por prioridad |

---

## 🎓 Contexto académico

> **Nota:** Este repositorio **no forma parte** del ecosistema MM4D (`mm4d-api` / `mm4d-console`). Es un laboratorio independiente de *Tópicos Especiales de Programación* — UCAB.

| Aspecto | Detalle |
|:--|:--|
| Tipo | Script CLI / módulo Python ejecutable |
| Interfaz | Consola estándar (`stdout`) |
| Persistencia | En memoria — sin base de datos |
| Variables de entorno | No aplica — datos embebidos en `__main__` |
| Licencia | Académica UCAB |

---

<div align="center">

**Laboratorio 4 · Genéricos en Python · UCAB 2026**

<br/>

![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Zero Dependencies](https://img.shields.io/badge/Zero-Dependencies-success?style=flat-square)
![Status](https://img.shields.io/badge/Status-Laboratorio%20completo-brightgreen?style=flat-square)

</div>
