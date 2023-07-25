import csv
import argparse
import pyodbc
from common import config

def fetch_data(table_name):
    # Obtener la configuración desde el archivo config.yaml
    db_config = config()

    # Establecer la conexión con la base de datos
    connection_string = db_config['database']['connection']
    connection = pyodbc.connect(connection_string)

    # Obtener la consulta y los encabezados de la tabla
    query = db_config['database']['tablas'][table_name]['query']
    headers = db_config['database']['tablas'][table_name]['headers']

    # Ejecutar la consulta SQL para obtener los datos
    cursor = connection.cursor()
    cursor.execute(query)

    # Obtener los datos de la consulta
    data = cursor.fetchall()

    # Cerrar la conexión con la base de datos
    connection.close()

    return headers, data

def save_to_csv(data, headers, table_name):
    # Generar el nombre del archivo CSV usando el nombre de la tabla
    filename = f"{table_name}.csv"

    # Abrir el archivo CSV en modo escritura
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Escribir los encabezados en el archivo CSV
        writer.writerow(headers)

        # Escribir los datos en el archivo CSV
        writer.writerows(data)

    print(f"Los datos se han guardado correctamente en '{filename}'.")

if __name__ == '__main__':
    # Crear un parser de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument('table_name', help='Nombre de la tabla')

    # Obtener el argumento proporcionado por el usuario
    args = parser.parse_args()
    table_name = args.table_name

    # Obtener los datos de la tabla especificada
    headers, data = fetch_data(table_name)

    # Guardar los datos en el archivo CSV con el nombre de la tabla
    save_to_csv(data, headers, table_name)
