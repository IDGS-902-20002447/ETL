import argparse
import datetime
import logging
import pandas as pd

# Importamos la librería logging para mostrar mensajes al usuario
import logging

# Obtenemos una referencia al logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Definimos la función principal
def main(month):
    # Leer los archivos CSV y cargar los datos en DataFrames
    df_detallePedido = pd.read_csv('detallePedido.csv')
    df_pedido=pd.read_csv('pedido.csv')
    df_compra = pd.read_csv('compra.csv')
    df_detalleCompra = pd.read_csv('detalleCompra.csv')
    df_producto = pd.read_csv('producto.csv')
    df_producto_existentes=pd.read_csv('producto_existente.csv')
    df_materia_prima = pd.read_csv('materia_prima.csv', header=0)
    df_user = pd.read_csv('user.csv', header=0)
    
    # Convertir la columna 'confirmed_at' a tipo datetime
    df_user['confirmed_at'] = pd.to_datetime(df_user['confirmed_at'])
     # Agrega una columna de fecha con el primer día del mes actual
    current_date = datetime.datetime.now()
    first_day_of_month = current_date.replace(day=1,month=month)
    
    df_producto_existentes['fecha'] = first_day_of_month
    df_materia_prima['fecha'] = first_day_of_month

    df_pedido['fecha'] = pd.to_datetime(df_pedido['fecha'])
    df_pedidos_filtered = df_pedido[df_pedido['fecha'].dt.month == month]
    

    print("**************************************Productos*********************")
    print(df_producto_existentes)
    print(df_materia_prima)
    print(df_pedidos_filtered)


    # Realizar las transformaciones y análisis de datos
    top_selling_products = get_top_selling_products(df_detalleCompra, df_producto, 5,first_day_of_month)
    bottom_selling_products = get_bottom_selling_products(df_detalleCompra, df_producto, 5,first_day_of_month)
    total_users = get_user_statistics(df_user)
    average_order_value=calculate_average_order_value(df_detallePedido)
    product_sales_by_month = get_product_sales_by_month(df_detallePedido, df_pedido, df_producto)
    top_clients = get_top_clients(df_pedidos_filtered, df_user, num_clients=5)



    # Realizar las transformaciones y análisis de datos utilizando los DataFrames filtrados
    gross_profit = calculate_gross_profit(df_detalleCompra, df_detallePedido)
    average_purchase_value = calculate_average_purchase_value(df_detalleCompra, df_producto)

    # Imprimir los resultados
    print("Beneficio Bruto:", gross_profit)
    print("Valor de compra promedio:", average_purchase_value)
    
    print("Valor de venta promedio",average_order_value)
    print("Top 5 productos más vendidos:")
    print(top_selling_products)
    print("Top 5 productos menos vendidos:")
    print(bottom_selling_products)
  
    print("Ventas mensuales por producto:")
    print(product_sales_by_month)
    print("Total de usuarios:", total_users)
   
    print("-----------------------------------------------------")
    print(top_clients)
    
    # Crear un DataFrame con los resultados
    Valor_Calculado = pd.DataFrame({
        'Beneficio Bruto': [gross_profit],
        'Valor de compra promedio': [average_purchase_value],
        'Total de usuarios': [total_users],
        'Valor de venta promedio':[average_order_value],
        'fecha':[first_day_of_month]
    })
    # Crear DataFrame para los productos menos vendidos
    Producto_Mas_Vendido = pd.DataFrame(
      top_selling_products, columns=['idProducto', 'nombre', 'cantidad', 'costo', 'total_obtenido','fecha'
                                     ])
    

    Producto_Menos_Vendido = pd.DataFrame(
        bottom_selling_products, columns=['idProducto', 'nombre', 'cantidad', 'costo', 'total_obtenido','fecha'])

    Ventas_mensuales = pd.DataFrame(
        product_sales_by_month, columns=['year','month', 'nombre','total_vendido']
    )

    Clientes_Mas_Pedido=pd.DataFrame(
        top_clients, columns=['numPedidos', 'name', 'telefono', 'email','fecha']
    )
 

    Productos_Existente=pd.DataFrame(
        df_producto_existentes
    )

    Materia_prima_Existente=pd.DataFrame(
        df_materia_prima
    )

   

    # Obtener la fecha actual para utilizarla en el nombre del archivo CSV
    current_date = datetime.datetime.now().strftime("")

    # Guardar el DataFrame en un archivo CSV
  
    Valor_Calculado.to_csv(f'ValorCalculado_{current_date}.csv', index=False)

    Producto_Menos_Vendido.to_csv(f'Producto_Menos_Vendido_{current_date}.csv', index=False)

    Producto_Mas_Vendido.to_csv(f'Producto_Mas_Vendido_{current_date}.csv', index=False)

    Ventas_mensuales.to_csv(f'Ventas_mensuales_{current_date}.csv', index=False)

    Clientes_Mas_Pedido.to_csv(f'Clientes_Mas_Pedido_{current_date}.csv', index=False)

    Productos_Existente.to_csv(f'Productos_Existente_{current_date}.csv', index=False)

    Materia_prima_Existente.to_csv(f'Materia_prima_Existente_{current_date}.csv', index=False)

    print("Los archivos CSV se han generado exitosamente.")


#TOP 5 clientes
def get_top_clients(df_pedidos, df_user, num_clients=5):
    # Calcula el total de pedidos por cliente
    pedidos_por_cliente = df_pedidos['iduser'].value_counts().reset_index()
    pedidos_por_cliente.columns = ['iduser', 'numPedidos']
    # Ordena los clientes por el total de pedidos en orden descendente
    pedidos_por_cliente = pedidos_por_cliente.sort_values(by='numPedidos', ascending=False)
    # Obtén los ID de los 5 clientes con más pedidos
    top_clientes_ids = pedidos_por_cliente.head(num_clients)['iduser']
    # Filtra los datos del DataFrame de usuarios para obtener solo los 5 clientes principales
    top_clientes = df_user[df_user['id'].isin(top_clientes_ids)]
    # Combina los DataFrames utilizando la columna 'iduser' como clave de combinación
    result = df_pedidos.merge(top_clientes, left_on='iduser', right_on='id')
    # Agrega la columna 'numPedidos' al DataFrame resultante
    result = result.merge(pedidos_por_cliente, left_on='iduser', right_on='iduser')
    # Agrupa por las columnas y suma los valores en 'numPedidos'
    result_grouped = result.groupby(['iduser', 'fecha', 'direccion', 'folio', 'estatus', 'name', 'email', 'telefono'])['numPedidos'].sum().reset_index()
    result_grouped = result_grouped.drop_duplicates(subset=['iduser'])

    return result_grouped


# Beneficio Bruto
def calculate_gross_profit(df_detalleCompra, df_detallePedido):
    costo_total = df_detalleCompra['cantidad'] * df_detalleCompra['precio']
    
    ingreso_total = df_detallePedido['cantidad'] * df_detallePedido['costoTotal']
    
    beneficio_bruto = round (ingreso_total.sum() - costo_total.sum())
    print(ingreso_total)
    print(costo_total)
    print(beneficio_bruto)
    return beneficio_bruto

# Valor de compra promedio
def calculate_average_purchase_value(df_detalleCompra, df_producto):
    # Merge para obtener los precios de los productos
    print(df_detalleCompra)
    print(df_producto)
    df_merged = pd.merge(df_detalleCompra, df_producto, left_on='idProducto', right_on='id')
    
    print(df_merged)
    # Cálculo del valor total de compra
    df_merged['valor_total'] = df_merged['cantidad'] * df_merged['precio']
    
    # Cálculo del valor promedio de compra
    average_purchase_value =round (df_merged['valor_total'].sum() / df_detalleCompra['idCompra'].nunique(),2)
    
    print("Listo 2")
    return average_purchase_value

# Función para calcular el valor promedio del pedido
def calculate_average_order_value(df_detallePedido):
    # Calcular el valor promedio del pedido
    average_order_value = df_detallePedido['costoTotal'].mean()

    return round(average_order_value, 2)

# Obtener los 5 productos más vendidos
def get_top_selling_products(df_detalleCompra, df_producto, num_products,first_day_of_month):
    df_merged = pd.merge(df_detalleCompra, df_producto, left_on='idProducto', right_on='id')
    df_grouped = df_merged.groupby('idProducto').agg({'idProducto':'first','cantidad': 'sum', 'nombre': 'first', 'costo': 'first'})
    df_grouped['total_obtenido'] = df_grouped['cantidad'] * df_grouped['costo']
    df_sorted = df_grouped.sort_values('cantidad', ascending=False).head(num_products)
    df_sorted['fecha'] = first_day_of_month
    return df_sorted[['idProducto','nombre', 'cantidad', 'costo', 'total_obtenido','fecha']]

# Obtener los 5 productos menos vendidos
def get_bottom_selling_products(df_detalleCompra, df_producto, num_products,first_day_of_month):
    df_merged = pd.merge(df_detalleCompra, df_producto, left_on='idProducto', right_on='id')
    df_grouped = df_merged.groupby('idProducto').agg({'idProducto': 'first', 'cantidad': 'sum', 'nombre': 'first', 'costo': 'first'})
    df_grouped['total_obtenido'] = df_grouped['cantidad'] * df_grouped['costo']
    df_sorted = df_grouped.sort_values('cantidad').head(num_products)
    df_sorted['fecha'] = first_day_of_month
    return df_sorted[['idProducto', 'nombre', 'cantidad', 'costo', 'total_obtenido','fecha']]


def get_product_sales_by_month(df_detallePedido, df_pedido, df_producto):
      # Merge para obtener los nombres de los productos en df_detallePedido
    df_merged = pd.merge(df_detallePedido, df_producto, left_on='idProducto', right_on='id', how='left')
    # Merge para obtener la fecha en df_detallePedido
    df_merged = pd.merge(df_merged, df_pedido[['id', 'fecha']], left_on='idPedido', right_on='id', how='left', suffixes=('_detalle', '_pedido'))
    # Convertir la columna 'fecha' a tipo datetime
    df_merged['fecha'] = pd.to_datetime(df_merged['fecha'])
    # Agregar columnas para el año y el mes
    df_merged['year'] = df_merged['fecha'].dt.year
    df_merged['month'] = df_merged['fecha'].dt.month
    # Agrupar por año, mes y producto, y sumar las cantidades vendidas
    df_grouped = df_merged.groupby(['year', 'month', 'nombre'])['cantidad'].sum().reset_index()
    # Renombrar la columna 'cantidad' a 'total_vendido'
    df_grouped.rename(columns={'cantidad': 'total_vendido'}, inplace=True)
    return df_grouped[['year', 'month', 'nombre', 'total_vendido']]


# Número de usuarios y nuevos usuarios semanales
def get_user_statistics(df_user):
    total_users = df_user.shape[0]
    df_user['confirmed_at'] = pd.to_datetime(df_user['confirmed_at'])
   
    return total_users

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ETL Process for Monthly Data Analysis')
    parser.add_argument('month', type=int, help='Month number for analysis')
    args = parser.parse_args()
    main(args.month)

