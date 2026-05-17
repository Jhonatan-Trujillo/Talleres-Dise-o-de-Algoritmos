class Cliente:
    def __init__(self, nombre: str, latitud: float, longitud: float, peso_kg: float, volumen: tuple[float, float, float], origen: str, destino: str):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.peso_kg = peso_kg
        self.volumen = volumen
        self.origen = origen
        self.destino = destino

    def __repr__(self):
        return f"Cliente({self.nombre}, lat={self.latitud}, lon={self.longitud})"

    def volumen_total(self) -> float:
        x, y, z = self.volumen  # unpacking de la tupla
        return x * y * z