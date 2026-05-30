import datetime
from datetime import datetime, timedelta  # <-- CORRECCIÓN: Para que funcionen las fechas y timedelta
import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Pi+314159265",
    database="fibra_cba_db"
)

cursor = db.cursor()
print("Conectado a MySQL")

# OPCIONES PARA INICIAR LA CONVERSACION CON EL CLIENTE 
sistema_activo = True

while sistema_activo:
    print("\n=========================================")
    print("     BIENVENIDO A FIBRACORD        ")
    print("=========================================")
    print("1. Registrar Alta de Servicio")
    print("2. Modificar Servicio (Cambiar Velocidad)")
    print("3. Dar de Baja Cliente")
    print("4. Salir")
    print("=========================================")
    
    opcion = input("Seleccione una opción (1-4): ")
    
    
# COMANDOS DE OPCION 1
 
    if opcion == "1":
        print("\n--- 📝 FORMULARIO DE ALTA DE SERVICIO ---")
        
        dni = input("DNI del Cliente: ").strip()
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        correo = input("Correo Electrónico: ").strip()
        fecha_nacimiento = input("Fecha de Nacimiento (AAAA-MM-DD): ").strip()
        numero_contacto = input("Número de Contacto/Celular: ").strip()
        
        print("\nPlanes de Velocidad: (1) 100MB - $12500 | (2) 300MB - $16800 | (3) 600MB - $23500 | (4) 1000MB - $31000")
        id_servicio = input("Seleccione el ID del servicio (1-4): ")
        
        print("\n📍 Ingrese el Barrio para verificar disponibilidad del servicio:")
        barrio_ingresado = input("Nombre del Barrio: ").strip().title()
        
        calle = input("Calle: ").strip()
        numero = int(input("Número: "))
        piso_dpto = input("Piso/Dpto (ENTER si es casa): ").strip()
        if piso_dpto == "":
            piso_dpto = None

        cursor.execute("SELECT id_barrio, estado_cobertura FROM cobertura WHERE nombre_barrio = %s", (barrio_ingresado,))
        cobertura_resultado = cursor.fetchone()
        
        if cobertura_resultado is not None and cobertura_resultado[1] == "OK":
            id_barrio = cobertura_resultado[0]
            
            # Lógica de fechas dinámicas (CORREGIDO)
            hoy = datetime.now()
            f1 = hoy + timedelta(days=1)
            f2 = hoy + timedelta(days=2)
            f3 = hoy + timedelta(days=3)
            
            print("\n📅 Seleccione fecha para la visita del técnico:")
            print(f"1. {f1.strftime('%d/%m/%Y')}")
            print(f"2. {f2.strftime('%d/%m/%Y')}")
            print(f"3. {f3.strftime('%d/%m/%Y')}")
            opc_fecha = input("Seleccione opción (1-3): ")
            
            if opc_fecha == "1":
                fecha_visita = f1.strftime('%Y-%m-%d')
            elif opc_fecha == "2":
                fecha_visita = f2.strftime('%Y-%m-%d')
            else:
                fecha_visita = f3.strftime('%Y-%m-%d')
                
            try:
                # 1. Verificamos si el cliente ya existe en la tabla clientes
                query_verificar_cliente = "SELECT dni FROM clientes WHERE dni = %s"
                cursor.execute(query_verificar_cliente, (dni,))
                cliente_existente = cursor.fetchone()

                # 2. Si el cliente NO existe, lo insertamos en la tabla clientes
                
                if cliente_existente is None:
                    query_cli = """INSERT INTO clientes 
                   (dni, nombre, apellido, correo, fecha_nacimiento, numero_contacto) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
                    cursor.execute(query_cli, (dni, nombre, apellido, correo, fecha_nacimiento, numero_contacto))
                
                else:
                    print("\nℹ️ El cliente ya existe en la base de datos. Se asociará una nueva solicitud a su DNI.")

                    # 3. Insertamos siempre una nueva solicitud de servicio
                    query_sol = """INSERT INTO solicitudes 
                (dni_cliente, id_barrio, id_servicio, calle, numero, piso_dpto, tipo_solicitud, fecha_visita) 
                VALUES (%s, %s, %s, %s, %s, %s, 'Alta', %s)"""
                    cursor.execute(query_sol, (dni, id_barrio, id_servicio, calle, numero, piso_dpto, fecha_visita))
                
                # Guardamos los cambios usando la variable real: db (CORREGIDO)
                db.commit()
                
                # Capturamos y mostramos el ID autoincremental de la solicitud
                numero_solicitud = cursor.lastrowid
                db.commit()
                
                print("\n=============================================")
                print("       ✅ ¡ÉXITO! ALTA REGISTRADA             ")
                print("=============================================")
                print(f" NÚMERO DE CLIENTE / SOLICITUD ASIGNADO: {numero_solicitud}")
                print(f"\n FECHA DE VISITA ELEGIDA: {fecha_visita}")
                print("=============================================")
                
            except mysql.connector.Error as err:
                print(f"❌ Error en base de datos: {err}")
        else:
            print("\n❌ Lo sentimos, por el momento no contamos con cobertura en tu barrio o no está registrado.")
        
        # COMANDOS DE OPCION 2
         
    elif opcion == "2":
        print("\n--- 🔄 MODIFICACIÓN DE SERVICIO (CAMBIO DE VELOCIDAD) ---")
        
        dato_busqueda = input("Ingresa tu numero de DNI sin puntos o tu numero de solicitud: ").strip()
        
        # 1. Buscamos todas las coincidencias usando fetchall (Unidad 4)
        query_buscar = """SELECT s.id_solicitud, s.id_servicio, c.nombre, c.apellido, ser.velocidad_mb, s.calle, s.numero, cob.nombre_barrio
                          FROM solicitudes s
                          INNER JOIN clientes c ON s.dni_cliente = c.dni
                          INNER JOIN servicios ser ON s.id_servicio = ser.id_servicio
                          INNER JOIN cobertura cob ON s.id_barrio = cob.id_barrio
                          WHERE s.id_solicitud = %s OR s.dni_cliente = %s"""
        
        cursor.execute(query_buscar, (dato_busqueda, dato_busqueda))
        resultados = cursor.fetchall()  # <-- Trae todas las instalaciones encontradas
        
        if len(resultados) > 0:
            # Saludamos usando los datos del primer registro encontrado (el nombre es el mismo)
            nombre_cliente = resultados[0][2]
            apellido_cliente = resultados[0][3]
            print(f"\n✨ ¡Hola {nombre_cliente} {apellido_cliente}!")
            
            # 2. Si se encontró más de una instalación para ese DNI, hacemos que elija
            if len(resultados) > 1:
                print("Se encontraron múltiples domicilios registrados bajo este DNI. Seleccione cuál desea modificar:")
                # Usamos un bucle for (Unidad 3) para enumerar las direcciones
                for i in range(len(resultados)):
                    sol = resultados[i]
                    print(f"[{i + 1}] Solicitud N° {sol[0]} - Domicilio: {sol[5]} {sol[6]} ({sol[7]}) | Plan: {sol[4]} MB")
                
                indice_elegido = int(input("\nSeleccione el número de opción: ")) - 1
                solicitud_seleccionada = resultados[indice_elegido]
            else:
                # Si tiene una sola, pasa directo
                solicitud_seleccionada = resultados[0]
            
            # Extraemos los datos finales de la solicitud elegida
            id_sol = solicitud_seleccionada[0]
            velocidad_actual = solicitud_seleccionada[4]
            
            print("\n=============================================")
            print(f" 👉 Gestionando Solicitud N° {id_sol}")
            print(f" 👉 Domicilio: {solicitud_seleccionada[5]} {solicitud_seleccionada[6]} ({solicitud_seleccionada[7]})")
            print(f" 👉 Plan actual contratado: {velocidad_actual} MB")
            print("=============================================")
            
            print("\nPlanes de Nueva Velocidad Disponibles:")
            print("1. 100MB - $12500 | 2. 300MB - $16800 | 3. 600MB - $23500 | 4. 1000MB - $31000")
            nuevo_id_servicio = input("Seleccione el ID de la NUEVA velocidad (1-4): ").strip()
            
            try:
                query_update = """UPDATE solicitudes 
                                  SET id_servicio = %s, tipo_solicitud = 'Modificacion' 
                                  WHERE id_solicitud = %s"""
                cursor.execute(query_update, (nuevo_id_servicio, id_sol))
                db.commit()
                print(f"\n✅ ¡ÉXITO! La velocidad del domicilio seleccionado fue actualizada correctamente.")
            except mysql.connector.Error as err:
                print(f"❌ Error al modificar en la base de datos: {err}")
        else:
            print("\n❌ ERROR: No se encontró ninguna solicitud registrada con ese ID o DNI.")


        # COMANDOS DE OPCION 3

    elif opcion == "3":
        print("\n--- 🗑️ PROCESO DE BAJA COMERCIAL DE SERVICIO ---")
        
        dato_busqueda = input("Ingresa tu numero de DNI sin puntos o tu numero de solicitud para empezar con el proceso de baja:").strip()
        
        # 1. Buscamos todas las coincidencias con fetchall
        query_buscar = """SELECT s.id_solicitud, s.id_servicio, c.nombre, c.apellido, ser.velocidad_mb, s.calle, s.numero, cob.nombre_barrio, c.dni
                          FROM solicitudes s
                          INNER JOIN clientes c ON s.dni_cliente = c.dni
                          INNER JOIN servicios ser ON s.id_servicio = ser.id_servicio
                          INNER JOIN cobertura cob ON s.id_barrio = cob.id_barrio
                          WHERE s.id_solicitud = %s OR s.dni_cliente = %s"""
        
        cursor.execute(query_buscar, (dato_busqueda, dato_busqueda))
        resultados = cursor.fetchall()
        
        if len(resultados) > 0:
            nombre_cliente = resultados[0][2]
            apellido_cliente = resultados[0][3]
            dni_cliente = resultados[0][8]
            print(f"\n✨ ¡Hola {nombre_cliente} {apellido_cliente}!")
            
            # 2. Si hay varios domicilios, listamos para que elija cuál dar de baja
            if len(resultados) > 1:
                print("Se encontraron múltiples servicios activos. Seleccione cuál desea DAR DE BAJA:")
                for i in range(len(resultados)):
                    sol = resultados[i]
                    print(f"[{i + 1}] Solicitud N° {sol[0]} - Domicilio: {sol[5]} {sol[6]} ({sol[7]}) | Plan: {sol[4]} MB")
                
                indice_elegido = int(input("\nSeleccione el número de opción: ")) - 1
                solicitud_seleccionada = resultados[indice_elegido]
            else:
                solicitud_seleccionada = resultados[0]
                
            id_sol = solicitud_seleccionada[0]
            domicilio_texto = f"{solicitud_seleccionada[5]} {solicitud_seleccionada[6]} ({solicitud_seleccionada[7]})"
            
            print("\n=============================================")
            print(f" ⚠️ ATENCIÓN: Se procederá a dar de baja la Solicitud N° {id_sol}")
            print(f" Domicilio a eliminar: {domicilio_texto}")
            print("=============================================")
            
            confirmar = input("¿Confirmar la ELIMINACIÓN de este servicio? (S/N): ").strip().upper()
            
            if confirmar == "S":
                try:
                    # Borramos únicamente la solicitud seleccionada (la casa específica)
                    query_delete_sol = "DELETE FROM solicitudes WHERE id_solicitud = %s"
                    cursor.execute(query_delete_sol, (id_sol,))
                    
                    # Condicional inteligente: si era la última solicitud que le quedaba al cliente, 
                    # borramos también sus datos personales para no dejar datos huérfanos.
                    if len(resultados) == 1:
                        query_delete_cli = "DELETE FROM clientes WHERE dni = %s"
                        cursor.execute(query_delete_cli, (dni_cliente,))
                    
                    db.commit()
                    print(f"\n✅ ¡ÉXITO! El servicio en {domicilio_texto} fue dado de baja correctamente.")
                    
                except mysql.connector.Error as err:
                    print(f"❌ Error al procesar la baja: {err}")
            else:
                print("\n❌ Operación cancelada. El servicio sigue activo.")
        else:
            print("\n❌ ERROR: No se encontró ninguna solicitud registrada con ese ID o DNI.")
        
        # COMANDOS DE OPCION 4

    elif opcion == "4":
        print("\nCerrando el sistema... ¡Hasta luego!")
        # Al salir definitivamente del sistema, cerramos los recursos una sola vez
        cursor.close()
        db.close()
        sistema_activo = False
        
    else:
        print("\n⚠️ Opción inválida. Por favor, elija un número del 1 al 4.")
