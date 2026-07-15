# viaje_chile_peru.py
# Script para calcular distancia, tiempo y narrativa de un viaje entre Chile y Perú
import math

# Base de datos de ciudades con sus coordenadas (Latitud, Longitud)
ciudades_chile = {
    "santiago": {"nombre": "Santiago", "lat": -33.4489, "lon": -70.6693},
    "valparaiso": {"nombre": "Valparaíso", "lat": -33.0472, "lon": -71.6127},
    "concepcion": {"nombre": "Concepción", "lat": -36.8201, "lon": -73.0444},
    "antofagasta": {"nombre": "Antofagasta", "lat": -23.6509, "lon": -70.3975},
    "arica": {"nombre": "Arica", "lat": -18.4783, "lon": -70.3126}
}

ciudades_peru = {
    "lima": {"nombre": "Lima", "lat": -12.0464, "lon": -77.0428},
    "arequipa": {"nombre": "Arequipa", "lat": -16.4090, "lon": -71.5375},
    "cusco": {"nombre": "Cusco", "lat": -13.5319, "lon": -71.9675},
    "tacna": {"nombre": "Tacna", "lat": -18.0117, "lon": -70.2536},
    "trujillo": {"nombre": "Trujillo", "lat": -8.1160, "lon": -79.0300}
}

# Medios de transporte y sus velocidades promedio estimadas (km/h)
transportes = {
    "1": {"nombre": "Auto", "velocidad": 100, "descripcion": "conduciendo por carreteras interurbanas disfrutando del paisaje"},
    "2": {"nombre": "Autobús", "velocidad": 80, "descripcion": "viajando cómodamente en bus de larga distancia de forma económica"},
    "3": {"nombre": "Avión", "velocidad": 800, "descripcion": "volando de manera veloz sobre las cordilleras sudamericanas"}
}

def calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula la distancia en kilómetros usando la fórmula de Haversine."""
    R = 6371.0 # Radio de la Tierra en km
    
    # Conversión a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    km = R * c
    millas = km * 0.621371
    return km, millas

def obtener_ciudad(pais, diccionario):
    """Solicita una ciudad al usuario y valida que exista en la base de datos."""
    print(f"\nCiudades disponibles en {pais}:")
    for key, info in diccionario.items():
        print(f" - {info['nombre']}")
        
    while True:
        entrada = input(f"Ingrese la Ciudad de {pais} (o escriba 's' para salir): ").strip().lower()
        if entrada == 's':
            return 's'
        if entrada in diccionario:
            return diccionario[entrada]
        print("Ciudad no encontrada. Por favor, intente nuevamente.")

# --- Bucle principal del programa ---
while True:
    print("\n=============================================")
    print("      PLANIFICADOR DE VIAJE CHILE - PERÚ     ")
    print("=============================================")
    print("Escriba 's' en cualquier momento para salir.")
    
    # 1. Solicitar Ciudad de Origen (Chile)
    origen = obtener_ciudad("Chile", ciudades_chile)
    if origen == 's':
        break
        
    # 2. Solicitar Ciudad de Destino (Perú)
    destino = obtener_ciudad("Perú", ciudades_peru)
    if destino == 's':
        break

    # 3. Seleccionar Medio de Transporte
    print("\nSeleccione su medio de transporte:")
    for opcion, datos in transportes.items():
        print(f"[{opcion}] {datos['nombre']} (Velocidad prom: {datos['velocidad']} km/h)")
    
    transporte_seleccionado = None
    while True:
        opcion = input("Ingrese el número del transporte (o 's' para salir): ").strip()
        if opcion.lower() == 's':
            transporte_seleccionado = 's'
            break
        if opcion in transportes:
            transporte_seleccionado = transportes[opcion]
            break
        print("Opción inválida. Intente de nuevo.")
        
    if transporte_seleccionado == 's':
        break

    # 4. Cálculos de Distancia y Duración
    km, millas = calcular_distancia(origen["lat"], origen["lon"], destino["lat"], destino["lon"])
    
    # Tiempo de viaje en horas decimales y formateo a Horas/Minutos
    horas_totales = km / transporte_seleccionado["velocidad"]
    horas_enteras = int(horas_totales)
    minutos_restantes = int((horas_totales - horas_enteras) * 60)

    # 5. Mostrar Resultados del Viaje
    print("\n---------------- Resumen del Viaje ----------------")
    print(f"Ruta: {origen['nombre']} (Chile) ➔ {destino['nombre']} (Perú)")
    print(f"Distancia en Kilómetros: {km:.2f} km")
    print(f"Distancia en Millas: {millas:.2f} mi")
    print(f"Duración estimada del viaje: {horas_enteras} horas y {minutos_restantes} minutos")
    print(f"Medio de transporte: {transporte_seleccionado['nombre']}")
    print("---------------------------------------------------")
    
    # 6. Narrativa del Viaje
    print("\nNarrativa del viaje:")
    print(f"Comenzarás tu aventura saliendo desde la hermosa ciudad de {origen['nombre']}, Chile.")
    print(f"Te desplazarás en {transporte_seleccionado['nombre'].lower()}, {transporte_seleccionado['descripcion']}.")
    print(f"Tras cruzar la frontera y recorrer una distancia aproximada de {km:.1f} km ({millas:.1f} millas),")
    print(f"llegarás finalmente a tu destino en la histórica ciudad de {destino['nombre']}, Perú.")
    print(f"El trayecto completo te tomará cerca de {horas_enteras} horas con {minutos_restantes} minutos.")
    print("===================================================\n")
    
    # Preguntar si desea planificar otro viaje o salir
    continuar = input("¿Desea planificar otro viaje? (Presione Enter para continuar o 's' para salir): ").strip().lower()
    if continuar == 's':
        break

print("\n¡Gracias por usar el Planificador de Viajes! ¡Buen viaje!")
