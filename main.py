import csv
import os

NOMBRE_ARCHIVO = "paises.csv"

# 1. MANEJO DE ARCHIVOS CSV

def cargar_paises_desde_csv(ruta_archivo):
    """Carga los datos del archivo CSV en una lista de diccionarios."""
    paises = []
    if not os.path.exists(ruta_archivo):
        print(f"Advertencia: El archivo '{ruta_archivo}' no existe. Se iniciará una lista vacía.")
        return paises

    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    pais = {
                        "nombre": fila["nombre"].strip(),
                        "poblacion": int(fila["poblacion"].strip()),
                        "superficie": int(fila["superficie"].strip()),
                        "continente": fila["continente"].strip()
                    }
                    paises.append(pais)
                except (ValueError, KeyError) as e:
                    print(f"Fila ignorada por formato inválido: {fila} - Error: {e}")
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
    
    return paises


def guardar_paises_en_csv(ruta_archivo, paises):
    """Guarda la lista de diccionarios en el archivo CSV."""
    try:
        with open(ruta_archivo, mode='w', encoding='utf-8', newline='') as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            for pais in paises:
                escritor.writerow(pais)
        print("Datos guardados exitosamente en el archivo CSV.")
    except Exception as e:
        print(f"Error al guardar los datos en el archivo CSV: {e}")

# 2. VALIDACIONES DE ENTRADA

def solicitar_entero_positivo(mensaje):
    """Solicita un número entero estrictamente positivo."""
    while True:
        entrada = input(mensaje).strip()
        if entrada.isdigit() and int(entrada) > 0:
            return int(entrada)
        print("Error: Debe ingresar un entero positivo válido.")


def solicitar_cadena_no_vacia(mensaje):
    """Solicita una cadena de texto no vacía."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print("Error: Este campo no puede estar vacío.")

# 3. FUNCIONALIDADES PRINCIPALES

def agregar_pais(paises):
    """Agrega un nuevo país a la lista evitando duplicados."""
    print("\n--- AGREGAR PAÍS ---")
    nombre = solicitar_cadena_no_vacia("Ingrese nombre del país: ")
    
    for p in paises:
        if p["nombre"].lower() == nombre.lower():
            print(f"Error: El país '{nombre}' ya existe en el registro.")
            return

    poblacion = solicitar_entero_positivo("Ingrese población (número entero): ")
    superficie = solicitar_entero_positivo("Ingrese superficie en km² (número entero): ")
    continente = solicitar_cadena_no_vacia("Ingrese continente: ")

    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    paises.append(nuevo_pais)
    guardar_paises_en_csv(NOMBRE_ARCHIVO, paises)
    print(f"¡País '{nombre}' registrado con éxito!")


def actualizar_pais(paises):
    """Actualiza la población y superficie de un país existente."""
    print("\n--- ACTUALIZAR PAÍS ---")
    nombre_buscado = solicitar_cadena_no_vacia("Ingrese el nombre del país a actualizar: ")
    
    for p in paises:
        if p["nombre"].lower() == nombre_buscado.lower():
            print(f"País encontrado: {p['nombre']} (Población: {p['poblacion']}, Superficie: {p['superficie']} km²)")
            nueva_pob = solicitar_entero_positivo("Ingrese nueva población: ")
            nueva_sup = solicitar_entero_positivo("Ingrese nueva superficie en km²: ")
            
            p["poblacion"] = nueva_pob
            p["superficie"] = nueva_sup
            
            guardar_paises_en_csv(NOMBRE_ARCHIVO, paises)
            print(f"¡Datos de '{p['nombre']}' actualizados correctamente!")
            return
            
    print(f"No se encontró ningún país con el nombre '{nombre_buscado}'.")


def buscar_pais(paises):
    """Busca países por coincidencia parcial o exacta de nombre."""
    print("\n--- BUSCAR PAÍS ---")
    criterio = solicitar_cadena_no_vacia("Ingrese el nombre o parte del nombre a buscar: ").lower()
    coincidencias = [p for p in paises if criterio in p["nombre"].lower()]
    
    if coincidencias:
        print(f"\nResultados encontrados ({len(coincidencias)}):")
        mostrar_lista_paises(coincidencias)
    else:
        print("No se encontraron países que coincidan con la búsqueda.")


def filtrar_paises(paises):
    """Submenú de filtrado de países."""
    print("\n--- FILTRAR PAÍSES ---")
    print("1. Por Continente")
    print("2. Por Rango de Población")
    print("3. Por Rango de Superficie")
    opcion = input("Seleccione una opción: ").strip()

    resultados = []
    if opcion == "1":
        continente = solicitar_cadena_no_vacia("Ingrese el continente a filtrar: ").lower()
        resultados = [p for p in paises if p["continente"].lower() == continente]
    elif opcion == "2":
        min_pob = solicitar_entero_positivo("Ingrese población mínima: ")
        max_pob = solicitar_entero_positivo("Ingrese población máxima: ")
        if min_pob > max_pob:
            print("Error: El valor mínimo no puede ser mayor que el máximo.")
            return
        resultados = [p for p in paises if min_pob <= p["poblacion"] <= max_pob]
    elif opcion == "3":
        min_sup = solicitar_entero_positivo("Ingrese superficie mínima (km²): ")
        max_sup = solicitar_entero_positivo("Ingrese superficie máxima (km²): ")
        if min_sup > max_sup:
            print("Error: El valor mínimo no puede ser mayor que el máximo.")
            return
        resultados = [p for p in paises if min_sup <= p["superficie"] <= max_sup]
    else:
        print("Opción inválida.")
        return

    if resultados:
        mostrar_lista_paises(resultados)
    else:
        print("No se encontraron países que cumplan con los criterios especificados.")


def ordenar_paises(paises):
    """Ordena los países según la clave y el sentido seleccionados."""
    if not paises:
        print("No hay países registrados para ordenar.")
        return

    print("\n--- ORDENAR PAÍSES ---")
    print("1. Por Nombre")
    print("2. Por Población")
    print("3. Por Superficie")
    criterio = input("Seleccione el criterio de ordenamiento: ").strip()

    clave = None
    if criterio == "1":
        clave = "nombre"
    elif criterio == "2":
        clave = "poblacion"
    elif criterio == "3":
        clave = "superficie"
    else:
        print("Criterio inválido.")
        return

    print("1. Ascendente")
    print("2. Descendente")
    sentido = input("Seleccione el sentido: ").strip()
    reverso = (sentido == "2")

    paises_ordenados = sorted(paises, key=lambda x: x[clave], reverse=reverso)
    mostrar_lista_paises(paises_ordenados)


def mostrar_estadisticas(paises):
    """Calcula y muestra las estadísticas generales del dataset."""
    if not paises:
        print("No hay datos suficientes para calcular estadísticas.")
        return

    print("\n--- ESTADÍSTICAS GENERALES ---")
    
    # Mayor y menor población
    pais_max_pob = max(paises, key=lambda x: x["poblacion"])
    pais_min_pob = min(paises, key=lambda x: x["poblacion"])
    
    # Promedios
    total_poblacion = sum(p["poblacion"] for p in paises)
    total_superficie = sum(p["superficie"] for p in paises)
    promedio_poblacion = total_poblacion / len(paises)
    promedio_superficie = total_superficie / len(paises)
    
    # Cantidad de países por continente
    conteo_continentes = {}
    for p in paises:
        c = p["continente"]
        conteo_continentes[c] = conteo_continentes.get(c, 0) + 1

    print(f"• País con mayor población: {pais_max_pob['nombre']} ({pais_max_pob['poblacion']:,} hab.)")
    print(f"• País con menor población: {pais_min_pob['nombre']} ({pais_min_pob['poblacion']:,} hab.)")
    print(f"• Promedio de población: {promedio_poblacion:,.2f} habitantes")
    print(f"• Promedio de superficie: {promedio_superficie:,.2f} km²")
    print("\n• Cantidad de países por continente:")
    for continente, cantidad in conteo_continentes.items():
        print(f"  - {continente}: {cantidad}")


def mostrar_lista_paises(lista_paises):
    """Muestra una tabla legible en consola con los datos de los países."""
    print("\n" + "=" * 70)
    print(f"{'Nombre':<20} | {'Población':<15} | {'Superficie (km²)':<15} | {'Continente':<10}")
    print("=" * 70)
    for p in lista_paises:
        print(f"{p['nombre']:<20} | {p['poblacion']:<15,} | {p['superficie']:<15,} | {p['continente']:<10}")
    print("=" * 70)

# 4. MENÚ PRINCIPAL

def menu_principal():
    paises = cargar_paises_desde_csv(NOMBRE_ARCHIVO)
    
    while True:
        print("\n============================================")
        print(" SISTEMA DE GESTIÓN DE DATOS DE PAÍSES (UTN)")
        print("============================================")
        print("1. Agregar país")
        print("2. Actualizar datos de un país")
        print("3. Buscar país por nombre")
        print("4. Filtrar países")
        print("5. Ordenar países")
        print("6. Ver estadísticas")
        print("7. Mostrar todos los países")
        print("8. Salir")
        
        opcion = input("Seleccione una opción (1-8): ").strip()
        
        if opcion == "1":
            agregar_pais(paises)
        elif opcion == "2":
            actualizar_pais(paises)
        elif opcion == "3":
            buscar_pais(paises)
        elif opcion == "4":
            filtrar_paises(paises)
        elif opcion == "5":
            ordenar_paises(paises)
        elif opcion == "6":
            mostrar_estadisticas(paises)
        elif opcion == "7":
            mostrar_lista_paises(paises)
        elif opcion == "8":
            print("\n¡Gracias por utilizar el sistema! Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    menu_principal()