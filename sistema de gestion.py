# ==========================================================
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# Curso: Programación 213023
# ==========================================================

from abc import ABC, abstractmethod
import logging

# ==========================================================
# CONFIGURACIÓN DE LOGS
# ==========================================================

logging.basicConfig(
    filename="eventos.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================================

class ClienteError(Exception):
    pass

class ServicioError(Exception):
    pass

class ReservaError(Exception):
    pass

# ==========================================================
# CLASE ABSTRACTA PERSONA
# ==========================================================

class Persona(ABC):

    def __init__(self, nombre, documento):
        self.nombre = nombre
        self.documento = documento

    @abstractmethod
    def mostrar_datos(self):
        pass

# ==========================================================
# CLASE CLIENTE
# ==========================================================

class Cliente(Persona):

    def __init__(self, nombre, documento, correo):

        super().__init__(nombre, documento)

        if not nombre.strip():
            raise ClienteError("El nombre no puede estar vacío")

        if len(documento) < 5:
            raise ClienteError("Documento inválido")

        if "@" not in correo:
            raise ClienteError("Correo electrónico inválido")

        self.__correo = correo

    def get_correo(self):
        return self.__correo

    def set_correo(self, nuevo_correo):

        if "@" not in nuevo_correo:
            raise ClienteError("Correo inválido")

        self.__correo = nuevo_correo

    def mostrar_datos(self):

        return (
            f"Cliente: {self.nombre} | "
            f"Documento: {self.documento} | "
            f"Correo: {self.__correo}"
        )

# ==========================================================
# CLASE ABSTRACTA SERVICIO
# ==========================================================

class Servicio(ABC):

    def __init__(self, nombre, tarifa_base):

        if tarifa_base <= 0:
            raise ServicioError("La tarifa debe ser positiva")

        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, tiempo):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# ==========================================================
# SERVICIO RESERVA DE SALAS
# ==========================================================

class ReservaSala(Servicio):

    def calcular_costo(self, horas, descuento=0):

        total = self.tarifa_base * horas
        total -= total * descuento

        return total

    def descripcion(self):

        return (
            f"Servicio: Reserva de Sala | "
            f"Tarifa: ${self.tarifa_base}"
        )

# ==========================================================
# SERVICIO ALQUILER DE EQUIPOS
# ==========================================================

class AlquilerEquipo(Servicio):

    def calcular_costo(self, dias, impuesto=0.19):

        subtotal = self.tarifa_base * dias
        total = subtotal + (subtotal * impuesto)

        return total

    def descripcion(self):

        return (
            f"Servicio: Alquiler de Equipos | "
            f"Tarifa: ${self.tarifa_base}"
        )

# ==========================================================
# SERVICIO ASESORÍA ESPECIALIZADA
# ==========================================================

class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, horas, recargo=0):

        total = (self.tarifa_base * horas) + recargo

        return total

    def descripcion(self):

        return (
            f"Servicio: Asesoría Especializada | "
            f"Tarifa: ${self.tarifa_base}"
        )

# ==========================================================
# CLASE RESERVA
# ==========================================================

class Reserva:

    def __init__(self, cliente, servicio, duracion):

        if duracion <= 0:
            raise ReservaError(
                "La duración debe ser mayor que cero"
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):

        self.estado = "Confirmada"

    def cancelar(self):

        self.estado = "Cancelada"

    def procesar(self):

        try:

            costo = self.servicio.calcular_costo(
                self.duracion
            )

            self.confirmar()

            return (
                f"Reserva procesada correctamente.\n"
                f"Cliente: {self.cliente.nombre}\n"
                f"Servicio: {self.servicio.nombre}\n"
                f"Estado: {self.estado}\n"
                f"Total: ${costo}"
            )

        except Exception as e:

            logging.error(
                f"Error procesando reserva: {e}"
            )

            raise ReservaError(
                "No fue posible procesar la reserva"
            ) from e

# ==========================================================
# LISTAS PRINCIPALES
# ==========================================================

clientes = []
servicios = []
reservas = []

# ==========================================================
# REGISTRO DE CLIENTES
# ==========================================================

print("\n========== CLIENTES ==========")

try:

    cliente1 = Cliente(
        "Leorgy Baron",
        "1193133279",
        "leorgy@gmail.com"
    )

    clientes.append(cliente1)

    print(cliente1.mostrar_datos())

except ClienteError as e:

    logging.error(e)
    print(e)

# Cliente inválido

try:

    cliente2 = Cliente(
        "",
        "123",
        "correo"
    )

    clientes.append(cliente2)

except ClienteError as e:

    logging.error(e)
    print(f"Error cliente: {e}")

# ==========================================================
# CREACIÓN DE SERVICIOS
# ==========================================================

print("\n========== SERVICIOS ==========")

try:

    servicio1 = ReservaSala(
        "Sala VIP",
        50000
    )

    servicio2 = AlquilerEquipo(
        "VideoBeam",
        35000
    )

    servicio3 = AsesoriaEspecializada(
        "Asesoría TI",
        80000
    )

    servicios.extend([
        servicio1,
        servicio2,
        servicio3
    ])

    for servicio in servicios:

        print(servicio.descripcion())

except ServicioError as e:

    logging.error(e)
    print(e)

# ==========================================================
# PROCESAMIENTO DE RESERVAS
# ==========================================================

print("\n========== RESERVAS ==========")

try:

    reserva1 = Reserva(
        cliente1,
        servicio1,
        4
    )

    reservas.append(reserva1)

    print(reserva1.procesar())

except ReservaError as e:

    logging.error(e)
    print(e)

# Reserva inválida

try:

    reserva2 = Reserva(
        cliente1,
        servicio2,
        -2
    )

    reservas.append(reserva2)

except ReservaError as e:

    logging.error(e)
    print(f"Error reserva: {e}")

# ==========================================================
# OPERACIONES ADICIONALES
# ==========================================================

print("\n========== OPERACIONES ==========")

operaciones = [
    ("Sala Ejecutiva", 60000),
    ("Sala Reunión", 45000),
    ("Laptop", 30000),
    ("Servidor", 120000)
]

for nombre, tarifa in operaciones:

    try:

        nuevo_servicio = ReservaSala(
            nombre,
            tarifa
        )

        print(
            nuevo_servicio.descripcion()
        )

    except Exception as e:

        logging.error(e)
        print(e)

# ==========================================================
# TRY / EXCEPT / ELSE / FINALLY
# ==========================================================

print("\n========== MANEJO AVANZADO ==========")

try:

    numero = int(
        input(
            "Ingrese un número entero: "
        )
    )

except ValueError:

    print(
        "Debe ingresar un valor numérico válido"
    )

else:

    print(
        f"Número ingresado correctamente: {numero}"
    )

finally:

    print(
        "Proceso finalizado correctamente"
    )

# ==========================================================
# FINAL DEL PROGRAMA
# ==========================================================

print("\nSistema ejecutado correctamente.")