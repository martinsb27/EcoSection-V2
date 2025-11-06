from dataclasses import dataclass
from typing import Dict

@dataclass
class Usuario:
    username: str
    role: str  # 'admin' or 'empleado'
    pwd_hash: str  # hex
    salt: str      # hex

    def to_dict(self) -> Dict:
        return {
            "username": self.username,
            "role": self.role,
            "pwd_hash": self.pwd_hash,
            "salt": self.salt
        }

    @staticmethod
    def from_dict(d: Dict) -> "Usuario":
        return Usuario(
            username=d["username"],
            role=d["role"],
            pwd_hash=d["pwd_hash"],
            salt=d["salt"]
        )

