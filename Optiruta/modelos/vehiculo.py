class Vehiculo:
    def __init__(self, tipo: str, volumen_max: tuple[float, float, float], peso_max_kg: float, kilometraje: float):
        self.tipo = tipo
        self.volumen_max = volumen_max
        self.peso_max_kg = peso_max_kg
        self.kilometraje = kilometraje

    def __repr__(self):
        return f"Vehiculo(tipo={self.tipo}, peso_max={self.peso_max_kg}kg, km={self.kilometraje})"

    def capacidad_volumen(self) -> float:
        x, y, z = self.volumen_max  # unpacking de la tupla
        return x * y * z