from sqlalchemy import Column, Integer, Float, String,DateTime
from base import Base

class TopSellingProduct(Base):
    __tablename__ = 'mayor_vendido_producto'

    id= Column(Integer, primary_key=True)
    idProducto = Column(Integer)
    nombre = Column(String)
    cantidad = Column(Integer)
    costo = Column(Float)
    total_obtenido = Column(Float)
    fecha=Column(Integer)

    def __init__(self,idProducto, nombre, cantidad, costo, total_obtenido,fecha):
        self.idProducto=idProducto
        self.nombre = nombre
        self.cantidad = cantidad
        self.costo = costo
        self.total_obtenido = total_obtenido
        self.fecha=fecha

class BottomSellingProduct(Base):
    __tablename__ = 'menor_vendido_producto'

    id= Column(Integer, primary_key=True)
    idProducto = Column(Integer)
    nombre = Column(String)
    cantidad = Column(Integer)
    costo = Column(Float)
    total_obtenido = Column(Float)
    fecha=Column(Integer)

    def __init__(self, idProducto,nombre, cantidad, costo, total_obtenido,fecha):
        self.idProducto=idProducto
        self.nombre = nombre
        self.cantidad = cantidad
        self.costo = costo
        self.total_obtenido = total_obtenido
        self.fecha=fecha


class CalculatedValues(Base):
    __tablename__ = 'valores_calculados'

    id = Column(Integer, primary_key=True)
    gross_profit = Column(Float)
    average_purchase_value = Column(Float)
    total_users = Column(Integer)
    average_order_value = Column(Integer)
    fecha=Column(Integer)

    def __init__(self, gross_profit, average_purchase_value, total_users, average_order_value,fecha):
        self.gross_profit = gross_profit
        self.average_purchase_value = average_purchase_value
        self.total_users = total_users
        self.average_order_value = average_order_value
        self.fecha=fecha

class MonthlySales(Base):
    __tablename__ = 'ventas_mensuales'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    nombre=Column(String)
    total_vendido= Column(Integer)

    def __init__(self,year, month, nombre,total_vendido):
        self.year = year
        self.month = month
        self.nombre = nombre
        self.total_vendido = total_vendido


class ExistenceMateriaPrima(Base):
    __tablename__ = 'materia_prima_existencia'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    cantidad = Column(Integer)
    unidad_medida = Column(String)
    costo=Column(Float)
    fecha = Column(Integer)
    

    def __init__(self,nombre, cantidad, unidad_medida, costo,fecha):
        self.nombre = nombre
        self.cantidad = cantidad
        self.costo = costo
        self.unidad_medida = unidad_medida
        self.fecha = fecha

class ExistenceProduct(Base):
    __tablename__ = 'producto_existencia'

    id = Column(Integer, primary_key=True)
    nombre= Column(String)
    costo = Column(Integer)
    tipo_producto= Column(String)
    stock = Column(Integer)
    fecha = Column(Integer)

    
    def __init__(self, nombre,costo,tipo_producto,stock,fecha):
        self.nombre = nombre
        self.costo = costo
        self.tipo_producto = tipo_producto
        self.stock = stock
        self.fecha = fecha
    
class ClientesMasPedido(Base):
    __tablename__ = 'clientes_mayores_pedidos'

    id = Column(Integer, primary_key=True) 
    numPedidos = Column(Integer)
    name = Column(String)
    telefono = Column(Integer)
    email = Column(String)
    fecha=Column(Integer)
    

    def __init__(self,numPedidos,name,telefono,email,fecha):
        self.numPedidos=numPedidos
        self.name = name
        self.telefono = telefono
        self.email = email
        self.fecha = fecha