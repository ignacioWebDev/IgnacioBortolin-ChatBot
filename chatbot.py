import streamlit as st
from groq import Groq

# Configuración de la página
st.set_page_config(page_title="Mi chat de IA", page_icon="🐼", layout="centered")

# Título de la aplicación
st.title("Mi primera aplicación con Streamlit")

# Entrada de texto para nombre
nombre = st.text_input("¿Cuál es tu nombre?")

# Botón para saludar
if st.button("Saludar"):
    st.write(f"¡Hola, {nombre}! gracias por venir a Talento Tech")

# Barra lateral
st.sidebar.title("Título de mi barra lateral")
st.sidebar.write("Texto en mi barra lateral.")

# Modelos
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

# Configuración de la página
def configurar_pagina():
    st.title("Mi chat de IA")
    st.sidebar.title("Configuración de la IA")
    elegirModelo = st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
    return elegirModelo

# Inicializar cliente Groq con clave secreta
def crear_usuario_groq():
    try:
        clave_secreta = st.secrets["CLAVE_API"]
        return Groq(api_key=clave_secreta)
    except Exception as e:
        st.error("Error al inicializar el cliente de Groq")
        return None

# Configurar el modelo y obtener respuesta del asistente
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model= modelo,
        messages = [{"role": "user", "content": mensajeDeEntrada}],
        stream = True
    )

# Inicializar el estado de la aplicación
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content":contenido, "avatar":avatar})
    
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])
            
def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat:
        mostrar_historial()

# Configurar la página y el modelo
# modelo = configurar_pagina()
# clienteUsuario = crear_usuario_groq()
# inicializar_estado()
# area_chat()

# Entrada de mensaje del usuario
# mensaje = st.chat_input("Escribí tu mensaje:")

# if mensaje:
#     actualizar_historial("user", mensaje, "🤖")
#     chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
#     actualizar_historial("assistant", chat_completo, "🤖")
#     st.rerun()

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    mensaje = st.chat_input("Escribí tu mensaje: ")
    area_chat()
    if mensaje:
        actualizar_historial("user", mensaje, "🧑‍💻")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa,"🤖")
                st.rerun()

if __name__ == "__main__":
    main()