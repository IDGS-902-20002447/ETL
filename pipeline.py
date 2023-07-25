import datetime
import subprocess
import logging
import schedule
import time

# Agregamos la configuración básica del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definimos una lista con los diferentes sites uids
extract = ['user', 'pedido', 'detallePedido', 'materia_prima', 'producto', 'compra', 'detalleCompra']
transform = ['Producto_Mas_Vendido_.csv', 'Producto_Menos_Vendido_.csv', 'ValorCalculado_.csv', 'Ventas_mensuales_.csv']
load = ['mayor_vendido_producto', 'menor_vendido_producto', 'valores_calculados', 'ventas_mensuales']


def main():
    _extract()
    _transform()
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


def _transform():
    logger.info('....::: Iniciando el proceso de transformacion:::....')
    # Ejecutamos la etapa de transformacion en la carpeta transform
    subprocess.run(['python', 'main.py'], cwd='./transform')

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
    subprocess.run(['python', 'main.py', transform[0], transform[1], transform[2], transform[3]], cwd='./load')



def run_process():
    main()


# Programar la ejecución cada 1 minuto
schedule.every(1).minutes.do(run_process)

while True:
    schedule.run_pending()
    time.sleep(1)
