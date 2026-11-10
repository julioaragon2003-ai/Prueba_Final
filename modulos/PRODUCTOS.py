
import streamlit as st
from config.conexion import obtener_conexion


def mostrar_productos():
    st.title("Productos")
    st.write(
        "Consulta de productos registrados "
        "en el módulo de Ventas."
    )

    conexion = obtener_conexion()

    if conexion is None:
        st.error("No se pudo conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
        SELECT Producto, SUM(Cantidad) AS Unidades_Vendidas
        FROM VENTAS
        GROUP BY Producto
        ORDER BY Producto
        """

        cursor.execute(consulta)
        registros = cursor.fetchall()

        if not registros:
            st.info(
                "Todavía no hay productos registrados en Ventas."
            )
        else:
            productos = [
                {
                    "Producto": registro[0],
                    "Unidades vendidas": registro[1]
                }
                for registro in registros
            ]

            total_unidades = sum(
                int(registro[1]) for registro in registros
            )

            columna1, columna2 = st.columns(2)

            columna1.metric(
                "Productos diferentes",
                len(registros)
            )

            columna2.metric(
                "Unidades vendidas",
                total_unidades
            )

            st.subheader("Listado de productos")

            st.dataframe(
                productos,
                use_container_width=True,
                hide_index=True
            )

    except Exception as error:
        st.error(f"Error al consultar productos: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        if conexion.is_connected():
            conexion.close()
