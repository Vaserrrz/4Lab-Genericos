"""Laboratorio 4: Cola de Prioridad Genérica con caso hospitalario.

Este módulo implementa una cola de prioridad genérica (max-heap) y la aplica
a una simulación de gestión de emergencias médicas.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
import heapq
from itertools import count
from typing import Generic, TypeVar

T = TypeVar("T")


class QueueEmptyError(Exception):
    """Excepción lanzada cuando se intenta extraer de una cola vacía."""


class PriorityQueue(Generic[T]):
    """Implementa una cola de prioridad genérica basada en max-heap.

    Esta estructura permite almacenar elementos de cualquier tipo junto con una
    prioridad numérica, garantizando que el elemento con mayor prioridad sea el
    primero en salir.
    """

    def __init__(self) -> None:
        """Inicializa una cola de prioridad vacía."""
        self._queue: list[tuple[int, int, T]] = []
        self._counter = count()

    def enqueue(self, item: T, priority: int) -> None:
        """Inserta un elemento en la cola con su prioridad asociada.

        Args:
            item: Elemento de tipo genérico que se desea insertar.
            priority: Valor entero de prioridad. Un valor mayor implica
                prioridad más alta.

        Raises:
            TypeError: Si `priority` no es un entero.
        """
        if not isinstance(priority, int):
            raise TypeError("La prioridad debe ser un entero.")

        # Se multiplica por -1 para simular un max-heap usando heapq.
        entry = (-priority, next(self._counter), item)
        heapq.heappush(self._queue, entry)

    def dequeue(self) -> T:
        """Extrae y retorna el elemento con mayor prioridad.

        Returns:
            El elemento de mayor prioridad almacenado en la cola.

        Raises:
            QueueEmptyError: Si la cola no contiene elementos.
        """
        if self.is_empty():
            raise QueueEmptyError("No se puede hacer dequeue: la cola está vacía.")

        _, _, item = heapq.heappop(self._queue)
        return item

    def peek(self) -> T:
        """Retorna el elemento de mayor prioridad sin extraerlo.

        Returns:
            El elemento con prioridad más alta.

        Raises:
            QueueEmptyError: Si la cola no contiene elementos.
        """
        if self.is_empty():
            raise QueueEmptyError("No se puede hacer peek: la cola está vacía.")

        _, _, item = self._queue[0]
        return item

    def is_empty(self) -> bool:
        """Indica si la cola está vacía.

        Returns:
            `True` si no hay elementos en la cola; en caso contrario, `False`.
        """
        return len(self._queue) == 0

    def size(self) -> int:
        """Obtiene el número total de elementos almacenados.

        Returns:
            Cantidad de elementos en la cola.
        """
        return len(self._queue)

    def __len__(self) -> int:
        """Retorna la cantidad de elementos usando `len(cola)`.

        Returns:
            Número de elementos en la cola.
        """
        return len(self._queue)


class Gravedad(IntEnum):
    """Define niveles de prioridad médica para tareas de urgencias."""

    BAJA = 1
    MEDIA = 2
    ALTA = 3


@dataclass(frozen=True, slots=True)
class Paciente:
    """Representa la información clínica básica de un paciente.

    Attributes:
        id_paciente: Identificador único del paciente.
        nombre: Nombre completo del paciente.
        edad: Edad del paciente en años.
        diagnostico: Diagnóstico médico principal.
    """

    id_paciente: str
    nombre: str
    edad: int
    diagnostico: str


@dataclass(frozen=True, slots=True)
class TareaMedica:
    """Modela una acción médica priorizable asociada a un paciente.

    Attributes:
        descripcion: Descripción de la tarea clínica.
        paciente: Paciente relacionado con la tarea.
        gravedad: Nivel de prioridad médica de la tarea.
    """

    descripcion: str
    paciente: Paciente
    gravedad: Gravedad

    def __str__(self) -> str:
        """Retorna una representación amigable de la tarea para consola.

        Returns:
            Cadena con datos esenciales de la tarea médica.
        """
        return (
            f"Tarea: {self.descripcion} | "
            f"Paciente: {self.paciente.nombre} ({self.paciente.id_paciente}) | "
            f"Prioridad: {self.gravedad.name}"
        )


if __name__ == "__main__":
    print("=" * 72)
    print(" SISTEMA DE GESTION DE EMERGENCIAS HOSPITALARIAS ".center(72, "="))
    print("=" * 72)

    cola_tareas: PriorityQueue[TareaMedica] = PriorityQueue()

    paciente_1 = Paciente(
        id_paciente="P-001",
        nombre="Carlos Mendoza",
        edad=67,
        diagnostico="Insuficiencia respiratoria aguda",
    )
    paciente_2 = Paciente(
        id_paciente="P-002",
        nombre="Ana Fuentes",
        edad=45,
        diagnostico="Tratamiento farmacologico programado",
    )
    paciente_3 = Paciente(
        id_paciente="P-003",
        nombre="Luis Herrera",
        edad=31,
        diagnostico="Fractura abierta de tibia",
    )

    tarea_alta = TareaMedica(
        descripcion="Intubacion por dificultad respiratoria",
        paciente=paciente_1,
        gravedad=Gravedad.ALTA,
    )
    tarea_baja = TareaMedica(
        descripcion="Suministrar medicamento programado",
        paciente=paciente_2,
        gravedad=Gravedad.BAJA,
    )
    tarea_media = TareaMedica(
        descripcion="Reduccion de fractura abierta",
        paciente=paciente_3,
        gravedad=Gravedad.MEDIA,
    )

    print("\n[Ingreso de tareas en orden de llegada (mezclado)]")
    cola_tareas.enqueue(tarea_baja, priority=int(tarea_baja.gravedad))
    print(f" + Encolada: {tarea_baja}")

    cola_tareas.enqueue(tarea_alta, priority=int(tarea_alta.gravedad))
    print(f" + Encolada: {tarea_alta}")

    cola_tareas.enqueue(tarea_media, priority=int(tarea_media.gravedad))
    print(f" + Encolada: {tarea_media}")

    print("\n" + "-" * 72)
    print(f"Tareas pendientes (size): {cola_tareas.size()}")
    print(f"Proxima tarea a ejecutar (peek): {cola_tareas.peek()}")
    print("-" * 72)

    print("\n[Procesamiento por prioridad medica]")
    while not cola_tareas.is_empty():
        tarea_actual = cola_tareas.dequeue()
        print(f" > Ejecutando: {tarea_actual}")
        print(f"   Tareas restantes: {cola_tareas.size()}")

    print("\n" + "=" * 72)
    print(" Todas las tareas de urgencias fueron procesadas ".center(72, "="))
    print("=" * 72)
