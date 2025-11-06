from dataclasses import dataclass
from typing import Dict
from datetime import datetime

@dataclass
class Tarea:
    id: str
    titulo: str
    descripcion: str
    asignado_a: str  # username
    completada: bool
    creada_en: str  # ISO datetime

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "asignado_a": self.asignado_a,
            "completada": self.completada,
            "creada_en": self.creada_en
        }

    @staticmethod
    def from_dict(d: Dict) -> "Tarea":
        return Tarea(
            id=d["id"],
            titulo=d["titulo"],
            descripcion=d["descripcion"],
            asignado_a=d["asignado_a"],
            completada=d.get("completada", False),
            creada_en=d.get("creada_en", datetime.utcnow().isoformat())
        )
