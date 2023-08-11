import datetime
import subprocess
import logging
import argparse


# Agregamos la configuración básica del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definimos una lista con los diferentes sites uids
extract = ['user', 'pedido', 'detallePedido', 'materia_prima', 'producto', 'compra', 'detalleCompra','producto_existente']
transform = ['Producto_Mas_Vendido_.csv', 'Producto_Menos_Vendido_.csv', 'ValorCalculado_.csv', 'Ventas_mensuales_.csv','Clientes_Mas_Pedido_.csv','Materia_prima_Existente_.csv','Productos_Existente_.csv']
load = ['mayor_vendido_producto', 'menor_vendido_producto', 'valores_calculados', 'ventas_mensuales','clientes_mayores_pedidos','materia_prima_existencia','producto_existencia']


def main(month):
    _extract()
    _transform(month)
    _load()
    logger.info('....:::: Proceso ETL Finalizado ::::.....')


# Funcion encargada de invocar el proceso de extraccion el proceso de extraccion
def _extract():
    logger.info('....::: Iniciando el proceso de extraccion:::....')

    # Iteramos por cada uno de los nombres de la extraccion que tenemos en la configuracion
    for new_site_uid in extract:
        # Ejecutamos la etapa de extraccion en la carpeta extract
        subprocess.run(['python', 'main.py', new_site_uid], cwd='./extract')

        # Movemos el archivo .csv a la carpeta transform
        subprocess.run(['move', r'extract\*.csv', r'transform'], shell=True)


def _transform(month):
    logger.info('....::: Iniciando el proceso de transformacion:::....')
    # Ejecutamos la etapa de transformacion en la carpeta transform
    subprocess.run(['python', 'main.py', str(month)], cwd='./transform')

    # Iteramos por cada uno de los newsites que tenemos en la configuracion
    for new_site_uid in extract:

        dirty_data_filename = '{}.csv'.format(new_site_uid)

        # Eliminando el archivo .csv sucio
        subprocess.run(['del', dirty_data_filename], shell=True, cwd='./transform')

    # Movemos el archivo .csv limpio a la carpeta load.
    subprocess.run(['move', r'transform\*.csv', r'load'], shell=True)


def _load():
    logger.info('....::: Iniciando el proceso de Carga:::....')

    now = datetime.datetime.now().strftime('%Y%m%d')
    # Ejecutamos la etapa de carga en la carpeta load
    subprocess.run(['python', 'main.py', transform[0], transform[1], transform[2], transform[3], transform[4], transform[5], transform[6]], cwd='./load')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ETL Process for Monthly Data Analysis')
    parser.add_argument('month', type=int, help='Month number for analysis')
    args = parser.parse_args()
    main(args.month)

