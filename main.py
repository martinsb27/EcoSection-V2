from servicios.gestion_usuarios import autenticar, registrar_usuario_interactivo, listar_usuarios, cargar_usuarios, crear_usuario
from servicios.gestion_tareas import crear_tarea_interactiva, listar_tareas_por_usuario, marcar_tarea_como_completada, listar_todas_las_tareas
from servicios.gestion_usuarios import cargar_usuarios as cargar_usuarios_func

def menu_admin(usuario):
    while True:
        print(f"\n--- Menú ADMIN ({usuario.username}) ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Crear tarea y asignar")
        print("4. Listar todas las tareas")
        print("5. Cerrar sesión")
        opt = input("Opción: ").strip()
        if opt == "1":
            registrar_usuario_interactivo()
        elif opt == "2":
            listar_usuarios()
        elif opt == "3":
            crear_tarea_interactiva()
        elif opt == "4":
            listar_todas_las_tareas()
        elif opt == "5":
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida.")

def menu_empleado(usuario):
    while True:
        print(f"\n--- Menú EMPLEADO ({usuario.username}) ---")
        print("1. Ver mis tareas")
        print("2. Marcar tarea como completada")
        print("3. Cerrar sesión")
        opt = input("Opción: ").strip()
        if opt == "1":
            listar_tareas_por_usuario(usuario.username)
        elif opt == "2":
            marcar_tarea_como_completada(usuario.username)
        elif opt == "3":
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida.")

def crear_admin_inicial_si_no_hay():
    usuarios = cargar_usuarios_func()
    if not usuarios:
        print("\nNo existen usuarios. Crea un usuario ADMIN inicial.")
        while True:
            username = input("Nombre de admin inicial: ").strip()
            password = input("Contraseña: ").strip()
            password2 = input("Confirmar contraseña: ").strip()
            if not username:
                print("Nombre inválido.")
                continue
            if password != password2:
                print("Contraseñas no coinciden.")
                continue
            creado = crear_usuario(username, "admin", password)
            if creado:
                print("✅ Admin creado. Inicia sesión con sus credenciales.")
                break
            else:
                print("No se pudo crear admin (tal vez ya existe).")

def main():
    print("=== ECOGESTIÓN v2 (Consola) ===")
    crear_admin_inicial_si_no_hay()
    while True:
        print("\n1. Iniciar sesión")
        print("2. Registrar nuevo usuario (solo admin puede crear luego)")
        print("3. Salir")
        opc = input("Seleccione una opción: ").strip()
        if opc == "1":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            user = autenticar(username, password)
            if not user:
                print("Usuario o contraseña incorrectos.")
                continue
            print(f"Bienvenido {user.username} ({user.role})")
            if user.role == "admin":
                menu_admin(user)
            else:
                menu_empleado(user)
        elif opc == "2":
            print("⚠️ Para crear usuarios use la opción de admin tras iniciar sesión. Si no hay admin, cree uno al iniciar.")
        elif opc == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
