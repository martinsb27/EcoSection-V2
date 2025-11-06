import json
from pathlib import Path
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from modelos.tareas import Tarea
from servicios.gestion_usuarios import cargar_usuarios

BASE = Path(__file__).resolve().parent.parent
DATOS_DIR = BASE / "datos"
TAREAS_FILE = DATOS_DIR / "tareas.json"

def asegurar_datos():
    DATOS_DIR.mkdir(parents=True, exist_ok=True)
    if not TAREAS_FILE.exists():
        TAREAS_FILE.write_text("[]", encoding="utf-8")

def cargar_tareas() -> List[Tarea]:
    asegurar_datos()
    with TAREAS_FILE.open("r", encoding="utf-8") as f:
        datos = json.load(f)
    return [Tarea.from_dict(d) for d in datos]

def guardar_tareas(tareas: List[Tarea]):
    asegurar_datos()
    with TAREAS_FILE.open("w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tareas], f, indent=4)

def crear_tarea_interactiva():
    usuarios = cargar_usuarios()
    if not usuarios:
        print("⚠️ No hay usuarios registrados. Pida a un admin crear usuarios.")
        return
    titulo = input("Título de la tarea: ").strip()
    descripcion = input("Descripción: ").strip()
    print("\nUsuarios disponibles:")
    for u in usuarios:
        print(f"- {u.username} ({u.role})")
    asignado_a = input("Asignar a (username): ").strip()
    if not any(u.username == asignado_a for u in usuarios):
        print("Usuario no encontrado.")
        return
    tarea = Tarea(
        id=str(uuid4()),
        titulo=titulo,
        descripcion=descripcion,
        asignado_a=asignado_a,
        completada=False,
        creada_en=datetime.utcnow().isoformat()
    )
    tareas = cargar_tareas()
    tareas.append(tarea)
    guardar_tareas(tareas)
    print("✅ Tarea creada y asignada.")

def listar_tareas_por_usuario(username: str):
    tareas = cargar_tareas()
    tareas_usuario = [t for t in tareas if t.asignado_a == username]
    if not tareas_usuario:
        print(f"No hay tareas para {username}.")
        return
    print(f"\nTareas de {username}:")
    for i, t in enumerate(tareas_usuario, 1):
        estado = "✅ Completada" if t.completada else "⏳ Pendiente"
        print(f"{i}. [{estado}] {t.titulo} - {t.descripcion} (id: {t.id})")

def listar_todas_las_tareas():
    tareas = cargar_tareas()
    if not tareas:
        print("No hay tareas registradas.")
        return
    print("\nTodas las tareas:")
    for t in tareas:
        estado = "✅" if t.completada else "⏳"
        print(f"- {estado} {t.titulo} | Asignado a: {t.asignado_a} | id: {t.id}")

def marcar_tarea_como_completada(username: str):
    tareas = cargar_tareas()
    pendientes = [t for t in tareas if t.asignado_a == username and not t.completada]
    if not pendientes:
        print("No tienes tareas pendientes.")
        return
    print("\nTus tareas pendientes:")
    for i, t in enumerate(pendientes, 1):
        print(f"{i}. {t.titulo} - {t.descripcion} (id: {t.id})")
    try:
        seleccion = int(input("Selecciona el número de tarea a marcar como completa: ").strip())
    except ValueError:
        print("Selección inválida.")
        return
    if not (1 <= seleccion <= len(pendientes)):
        print("Selección fuera de rango.")
        return
    tarea = pendientes[seleccion - 1]
    # actualizar la lista completa
    for t in tareas:
        if t.id == tarea.id:
            t.completada = True
    guardar_tareas(tareas)
    print("✅ Tarea marcada como completada.")

