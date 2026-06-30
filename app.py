import streamlit as st
import pandas as pd

from api_cliente import obtener_usuarios_api
from database import crear_tabla, guardar_usuarios, consultar_usuarios, eliminar_datos

st.set_page_config(
    page_title="API + SQLite + Streamlit",
    layout="wide"
)

crear_tabla()

st.title("API + SQLite + Streamlit")
st.write("Aplicación que permite obtener datos desde una API, almacenarlos en SQLite y visualizarlos con Streamlit.")

menu = st.sidebar.selectbox(
    "Seleccione una opción",
    [
        "Inicio",
        "Consumir API",
        "Ver base de datos",
        "Buscar usuario",
        "Eliminar datos"
    ]
)

if menu == "Inicio":
    st.header("Panel principal")

    st.write("""
    Esta aplicación simula una arquitectura básica de computación en la nube:

    - API externa como fuente de datos.
    - Streamlit como interfaz web.
    - SQLite como base de datos.
    - GitHub como repositorio.
    - Streamlit Cloud como plataforma de despliegue.
    """)

    st.info("Use el menú lateral para interactuar con la aplicación.")

elif menu == "Consumir API":
    st.header("Consumir API pública")

    st.write("API utilizada:")
    st.code("https://jsonplaceholder.typicode.com/users")

    if st.button("Obtener datos desde API"):
        usuarios = obtener_usuarios_api()

        if usuarios:
            guardar_usuarios(usuarios)
            st.success("Datos obtenidos y guardados correctamente en SQLite.")
            st.json(usuarios[0])
        else:
            st.error("No se pudieron obtener datos desde la API.")

elif menu == "Ver base de datos":
    st.header("Tabla almacenada en SQLite")

    df = consultar_usuarios()

    if df.empty:
        st.warning("La base de datos está vacía. Primero consuma la API.")
    else:
        st.dataframe(df, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total usuarios", len(df))
        col2.metric("Total ciudades", df["ciudad"].nunique())
        col3.metric("Total correos", df["email"].nunique())

elif menu == "Buscar usuario":
    st.header("Buscar usuario en SQLite")

    df = consultar_usuarios()

    if df.empty:
        st.warning("No hay datos guardados.")
    else:
        nombre = st.text_input("Ingrese nombre o usuario a buscar")

        if nombre:
            resultado = df[
                df["nombre"].str.contains(nombre, case=False, na=False) |
                df["usuario"].str.contains(nombre, case=False, na=False)
            ]

            if resultado.empty:
                st.error("No se encontraron coincidencias.")
            else:
                st.success("Resultado encontrado.")
                st.dataframe(resultado, use_container_width=True)

elif menu == "Eliminar datos":
    st.header("Eliminar registros de SQLite")

    st.warning("Esta acción eliminará todos los datos almacenados.")

    if st.button("Eliminar todos los datos"):
        eliminar_datos()
        st.success("Datos eliminados correctamente.")