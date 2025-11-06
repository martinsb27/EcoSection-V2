import json
from pathlib import Path
from typing import List, Optional
import hashlib
import os
import binascii

from modelos.usuarios import Usuario

BASE = Path(__file__).resolve().parent.parent
DATOS_DIR = BASE / "datos"
USUARIOS_FILE = DATOS_DIR / "usuarios.json"

# --- Helpers de hashing (PBKDF2) ---
def generar_salt(n_bytes: int = 16) -> bytes:
    return os.urandom(n_bytes)

def hash_password(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)

def crear_hash(password: str) -> (str, str): # type: ignore
    salt = generar_salt()
    pwd_hash = hash_password(password, salt)
    return binascii.hexlify(pwd_hash).decode(), binascii.hexlify(salt).decode()

def verificar_password(password: str, pwd_hash_hex: str, salt_hex: str) -> bool:
    salt = binascii.unhexlify(salt_hex.encode())
    pwd_hash = binascii.unhexlify(pwd_hash_hex.encode())
    return hash_password(password, salt) == pwd_hash

# --- I/O ---
def asegurar_datos():
    DATOS_DIR.mkdir(parents=True, exist_ok=True)
    if not USUARIOS_FILE.exists():
        USUARIOS_FILE.write_text("[]", encoding="utf-8")

def cargar_usuarios() -> List[Usuario]:
    asegurar_datos()
    with USUARIOS_FILE.open("r", encoding="utf-8") as f:
        datos = json.load(f)
    return [Usuario.from_dict(d) for d in datos]

def guardar_usuarios(usuarios: List[Usuario]):
    asegurar_datos()
    with USUARIOS_FILE.open("w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in usuarios], f, indent=4)

# --- Operaciones ---
def existe_usuario(username: str) -> bool:
    return any(u.username == username for u in cargar_usuarios())

def crear_usuario(username: str, role: str, password: str) -> bool:
    if existe_usuario(username):
        return False
    pwd_hash_hex, salt_hex = crear_hash(password)
    usuarios = cargar_usuarios()
    usuarios.append(Usuario(username=username, role=role, pwd_hash=pwd_hash_hex, salt=salt_hex))
    guardar_usuarios(usuarios)
    return True

def autenticar(username: str, password: str) -> Optional[Usuario]:
    usuarios = cargar_usuarios()
    for u in usuarios:
        if u.username == username:
            if verificar_password(password, u.pwd_hash, u.salt):
                return u
            return None
    return None

def registrar_usuario_interactivo():
    print("\n--- Registrar nuevo usuario ---")
    username = input("Nombre de usuario: ").strip()
    if not username:
        print("Nombre no válido.")
        return
    if existe_usuario(username):
        print("⚠️ El usuario ya existe.")
        return
    role = input("Rol (admin/empleado): ").strip().lower()
    if role not in ("admin", "empleado"):
        print("Rol inválido.")
        return
    password = input("Contraseña: ").strip()
    password2 = input("Confirmar contraseña: ").strip()
    if password != password2:
        print("Las contraseñas no coinciden.")
        return
    crear_usuario(username, role, password)
    print("✅ Usuario creado correctamente.")

def listar_usuarios():
    usuarios = cargar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    print("\nUsuarios registrados:")
    for u in usuarios:
        print(f"- {u.username} ({u.role})")

