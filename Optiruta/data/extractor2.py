import requests
import json
import random
import time

LUGARES_IBAGUE = [
    "Centro Comercial Multicentro Ibagué",
    "Hospital Federico Lleras Acosta Ibagué",
    "Universidad del Tolima Ibagué",
    "Aeropuerto Perales Ibagué",
    "Parque Centenario Ibagué",
    "Centro Comercial Acqua Ibagué",
    "Hospital San Francisco Ibagué",
    "Universidad de Ibagué",
    "Estadio Manuel Murillo Toro Ibagué",
    "Plaza de Bolívar Ibagué",
    "Terminal de Transportes Ibagué",
    "Parque de la Música Ibagué",
    "Centro Comercial La Estación Ibagué",
    "Corporación Universitaria Minuto de Dios Ibagué",
    "Batallón Rooke Ibagué"
]

def buscar_lugar(nombre: str) -> dict | None:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": nombre,
        "format": "json",
        "countrycodes": "co",
        "limit": 1
    }
    headers = {"User-Agent": "OptiroutaPlus/1.0"}
    
    respuesta = requests.get(url, params=params, headers=headers)
    resultados = respuesta.json()
    
    if resultados:
        r = resultados[0]
        return {
            "nombre": nombre,
            "latitud": float(r["lat"]),
            "longitud": float(r["lon"]),
            "peso_kg": round(random.uniform(1.0, 50.0), 2),
            "volumen": [
                round(random.uniform(10.0, 100.0), 1),
                round(random.uniform(10.0, 100.0), 1),
                round(random.uniform(10.0, 100.0), 1)
            ],
            "origen": "Centro de distribución Ibagué",
            "destino": nombre
        }
    return None

def extraer_lugares():
    clientes = []
    
    for nombre in LUGARES_IBAGUE:
        print(f"Buscando: {nombre}...")
        cliente = buscar_lugar(nombre)
        if cliente:
            clientes.append(cliente)
            print(f"  ✓ lat={cliente['latitud']}, lon={cliente['longitud']}")
        else:
            print(f"  ✗ No encontrado")
        time.sleep(1)  # respetar límite de Nominatim
    
    with open("data/clientes.json", "w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, indent=2)
    
    print(f"\nDataset guardado: {len(clientes)} clientes en data/clientes.json")
    return clientes

if __name__ == "__main__":
    extraer_lugares()