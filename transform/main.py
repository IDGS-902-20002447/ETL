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
def main():
    # Leer los archivos CSV y cargar los datos en DataFrames
    df_user = pd.read_csv('user.csv')
    df_detallePedido = pd.read_csv('detallePedido.csv')
    df_compra = pd.read_csv('compra.csv')
    df_detalleCompra = pd.read_csv('detalleCompra.csv')
    df_producto = pd.read_csv('producto.csv')
    df_materia_prima = pd.read_csv('materia_prima.csv', header=0)
    print(df_materia_prima)


    # Realizar las transformaciones y análisis de datos
    gross_profit = calculate_gross_profit(df_detalleCompra, df_detallePedido)
    average_purchase_value = calculate_average_purchase_value(df_detalleCompra, df_producto)
    top_selling_products = get_top_selling_products(df_detalleCompra, df_producto, 5)
    bottom_selling_products = get_bottom_selling_products(df_detalleCompra, df_producto, 5)
    monthly_sales = get_monthly_sales(df_compra)
    total_users, new_users_weekly = get_user_statistics(df_user)

    # Imprimir los resultados
    print("Beneficio Bruto:", gross_profit)
    print("Valor de compra promedio:", average_purchase_value)
    print("Top 5 productos más vendidos:")
    print(top_selling_products)
    print("Top 5 productos menos vendidos:")
    print(bottom_selling_products)
    print("Ventas mensuales:")
    print(monthly_sales)
    print("Total de usuarios:", total_users)
    print("Nuevos usuarios semanales:")
    print(new_users_weekly)
    # Crear un DataFrame con los resultados
    Valor_Calculado = pd.DataFrame({
        'Beneficio Bruto': [gross_profit],
        'Valor de compra promedio': [average_purchase_value],
        'Total de usuarios': [total_users],
        'Nuevos usuarios semanales': [new_users_weekly],
    })
    # Crear DataFrame para los productos menos vendidos
    
    Producto_Mas_Vendido = pd.DataFrame(
      top_selling_products, columns=['idProducto', 'nombre', 'cantidad', 'costo', 'total_obtenido'])

    Producto_Menos_Vendido = pd.DataFrame(
        bottom_selling_products, columns=['idProducto', 'nombre', 'cantidad', 'costo', 'total_obtenido'])

    Ventas_mensuales = pd.DataFrame(
        monthly_sales, columns=['year','month', 'total_sales']
    )

    # Obtener la fecha actual para utilizarla en el nombre del archivo CSV
    current_date = datetime.datetime.now().strftime("")

    # Guardar el DataFrame en un archivo CSV
  
    Valor_Calculado.to_csv(f'ValorCalculado_{current_date}.csv', index=False)
    Producto_Menos_Vendido.to_csv(f'Producto_Menos_Vendido_{current_date}.csv', index=False)

    Producto_Mas_Vendido.to_csv(f'Producto_Mas_Vendido_{current_date}.csv', index=False)
    Ventas_mensuales.to_csv(f'Ventas_mensuales_{current_date}.csv', index=False)

    print("Los archivos CSV se han generado exitosamente.")




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



# Obtener los 5 productos más vendidos
def get_top_selling_products(df_detalleCompra, df_producto, num_products):
    df_merged = pd.merge(df_detalleCompra, df_producto, left_on='idProducto', right_on='id')
    df_grouped = df_merged.groupby('idProducto').agg({'idProducto':'first','cantidad': 'sum', 'nombre': 'first', 'costo': 'first'})
    df_grouped['total_obtenido'] = df_grouped['cantidad'] * df_grouped['costo']
    df_sorted = df_grouped.sort_values('cantidad', ascending=False).head(num_products)
    return df_sorted[['idProducto','nombre', 'cantidad', 'costo', 'total_obtenido']]

# Obtener los 5 productos menos vendidos
def get_bottom_selling_products(df_detalleCompra, df_producto, num_products):
    df_merged = pd.merge(df_detalleCompra, df_producto, left_on='idProducto', right_on='id')
    df_grouped = df_merged.groupby('idProducto').agg({'idProducto': 'first', 'cantidad': 'sum', 'nombre': 'first', 'costo': 'first'})
    df_grouped['total_obtenido'] = df_grouped['cantidad'] * df_grouped['costo']
    df_sorted = df_grouped.sort_values('cantidad').head(num_products)
    return df_sorted[['idProducto', 'nombre', 'cantidad', 'costo', 'total_obtenido']]




# Número de ventas mensuales
def get_monthly_sales(df_compra):
    df_compra['fecha'] = pd.to_datetime(df_compra['fecha'])
    df_compra['year'] = df_compra['fecha'].dt.year 
    
     # Agregar columna "year"
    df_compra['month'] = df_compra['fecha'].dt.month
    df_grouped = df_compra.groupby(['year', 'month']).size().reset_index(name='total_sales')
    print(df_grouped )
    return df_grouped


# Número de usuarios y nuevos usuarios semanales
def get_user_statistics(df_user):
    current_week = datetime.datetime.now().isocalendar()[1]
    total_users = df_user.shape[0]
    df_user['confirmed_at'] = pd.to_datetime(df_user['confirmed_at'])
    df_user['week'] = df_user['confirmed_at'].dt.week
    new_users_weekly = df_user[df_user['week'] == current_week].shape[0]
    return total_users, new_users_weekly

if __name__ == '__main__':
    main()
