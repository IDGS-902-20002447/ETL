import argparse
from datetime import datetime
import logging

import pandas as pd
from base import Base, engine, Session
from structure import ClientesMasPedido, ExistenceMateriaPrima, ExistenceProduct, TopSellingProduct, BottomSellingProduct, CalculatedValues, MonthlySales

# Agregamos la configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(filename1, filename2, filename3, filename4,filename5,filename6,filename7):
    # Generamos el esquema de la BD
    Base.metadata.create_all(engine)

    # Iniciamos la sesión
    session = Session()
    logger.info('....::: Eliminacion de datos en la BD:::....')


    logger.info('....::: Cargando datos en la BD:::....')

    # Cargar los datos desde los archivos CSV
    df_top_selling = pd.read_csv(filename1, encoding='utf-8')
    df_bottom_selling = pd.read_csv(filename2, encoding='utf-8')
    df_calculated_values = pd.read_csv(filename3, encoding='utf-8')
    df_calculated_values.columns = df_calculated_values.columns.str.strip()
    df_monthly_sales = pd.read_csv(filename4, encoding='utf-8')
    df_top_clientes = pd.read_csv(filename5, encoding='utf-8')
    df_materia_existente = pd.read_csv(filename6, encoding='utf-8')
    df_producto_existentes = pd.read_csv(filename7, encoding='utf-8')

    # Cargar los datos en las tablas correspondientes
    for _, row in df_top_selling.iterrows():
        top_selling_product = TopSellingProduct(row['idProducto'], row['nombre'], row['cantidad'], row['costo'], row['total_obtenido'],row['fecha'])
       
        try:
            session.add(top_selling_product)
            session.commit()
        except Exception as e:
            session.rollback()  # Deshacer la transacción en caso de excepción
            logger.error(f"Error al insertar registro: {e}")

    for _, row in df_bottom_selling.iterrows():
        bottom_selling_product = BottomSellingProduct(row['idProducto'], row['nombre'], row['cantidad'], row['costo'], row['total_obtenido'],row['fecha'])
        session.add(bottom_selling_product)

    for _, row in df_calculated_values.iterrows():
       
        calculated_values = CalculatedValues(row['Beneficio Bruto'], row['Valor de compra promedio'], row['Total de usuarios'], row['Valor de venta promedio'],row['fecha'])
        session.add(calculated_values)

    for _, row in df_monthly_sales.iterrows():
        year = int(row['year'])
        month = int(row['month'])
        nombre = str(row['nombre'])
        total_vendido = int(row['total_vendido'])
        monthly_sales = MonthlySales(year=year, month=month,nombre=nombre ,total_vendido=total_vendido)

        session.add(monthly_sales)

    for _, row in df_top_clientes.iterrows():
        top_selling_clientes = ClientesMasPedido(row['numPedidos'], row['name'], row['telefono'], row['email'],row['fecha'])
        session.add(top_selling_clientes)

    for _, row in df_materia_existente.iterrows():
        matera_prima_exitente = ExistenceMateriaPrima( row['nombre'], row['cantidad'], row['unidad_medida'], row['costo'],row['fecha'])
        session.add(matera_prima_exitente)

    for _, row in df_producto_existentes.iterrows():
        producto_exitente = ExistenceProduct(row['nombre'], row['costo'], row['tipo_producto'], row['stock'],row['fecha'])
        session.add(producto_exitente)

    # Guardar los cambios en la base de datos
    session.commit()
    logger.info('Los datos se han cargado correctamente en la base de datos.')

    # Cerrar la sesión de la base de datos
    session.close()

def truncate_tables(session):
    try:
        # Eliminar los datos de las tablas existentes
        with session.begin():
            for table in reversed(Base.metadata.sorted_tables):
                session.execute(table.delete())
        logger.info('Registros eliminados en las tablas existentes')
    except Exception as e:
        logger.error(f'Error al eliminar registros de las tablas: {e}')

if __name__ == '__main__':
    # Creamos el parser de argumentos
    parser = argparse.ArgumentParser()

    # Creamos argumentos obligatorios para los cuatro archivos
    parser.add_argument('filename1', help='El archivo del top de productos más vendidos', type=str)
    parser.add_argument('filename2', help='El archivo del top de productos menos vendidos', type=str)
    parser.add_argument('filename3', help='El archivo de los valores calculados', type=str)
    parser.add_argument('filename4', help='El archivo de las ventas mensuales', type=str)
    parser.add_argument('filename5', help='El archivo del top de productos más vendidos', type=str)
    parser.add_argument('filename6', help='El archivo del top de productos menos vendidos', type=str)
    parser.add_argument('filename7', help='El archivo de los valores calculados', type=str)


    args = parser.parse_args()

    main(args.filename1, args.filename2, args.filename3, args.filename4, args.filename5, args.filename6, args.filename7)
