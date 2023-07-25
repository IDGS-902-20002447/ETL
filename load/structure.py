from sqlalchemy import Column, Integer, Float, String
from base import Base

class TopSellingProduct(Base):
    __tablename__ = 'mayor_vendido_producto'

    idProducto = Column(Integer, primary_key=True)
    nombre = Column(String)
    cantidad = Column(Integer)
    costo = Column(Float)
    total_obtenido = Column(Float)

    def __init__(self,idProducto, nombre, cantidad, costo, total_obtenido):
        self.idProducto=idProducto
        self.nombre = nombre
        self.cantidad = cantidad
        self.costo = costo
        self.total_obtenido = total_obtenido

class BottomSellingProduct(Base):
    __tablename__ = 'menor_vendido_producto'

    idProducto = Column(Integer, primary_key=True)
    nombre = Column(String)
    cantidad = Column(Integer)
    costo = Column(Float)
    total_obtenido = Column(Float)

    def __init__(self, idProducto,nombre, cantidad, costo, total_obtenido):
        self.idProducto=idProducto
        self.nombre = nombre
        self.cantidad = cantidad
        self.costo = costo
        self.total_obtenido = total_obtenido


class CalculatedValues(Base):
    __tablename__ = 'valores_calculados'

    id = Column(Integer, primary_key=True)
    gross_profit = Column(Float)
    average_purchase_value = Column(Float)
    total_users = Column(Integer)
    new_users_weekly = Column(Integer)

    def __init__(self, gross_profit, average_purchase_value, total_users, new_users_weekly):
        self.gross_profit = gross_profit
        self.average_purchase_value = average_purchase_value
        self.total_users = total_users
        self.new_users_weekly = new_users_weekly

class MonthlySales(Base):
    __tablename__ = 'ventas_mensuales'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    total_sales = Column(Integer)

    def __init__(self,year, month, total_sales):
        self.year = year
        self.month = month
        self.total_sales = total_sales




    
