import streamlit as st
from groq import Groq

# Configuración de la página
st.set_page_config(page_title="Mi chat de IA", page_icon="6️⃣", layout="centered")

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

# Función para configurar la página
def configurar_pagina():
    st.title("Mi chat de IA")
    st.sidebar.title("Configuración de la IA")
    elegirModelo = st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
    return elegirModelo

# Función para crear el cliente de Groq
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

# Inicializa el estado para evitar errores
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# Llamar a inicializar_estado al principio
inicializar_estado()

# Función para actualizar el historial de mensajes
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

# Función para configurar el modelo Groq
def configurar_modelo(cliente, modelo, mensaje):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensaje}],
        stream=True
    )

# Función para mostrar el historial de chat
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

# Área de chat
def area_chat():
    contenedorDelChat = st.container()
    with contenedorDelChat:
        mostrar_historial()

# Generar la respuesta del modelo en flujo
def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

# Función principal
def main(): 
    modelo = configurar_pagina()  # Selección del modelo
    cliente = crear_usuario_groq()  # Crear el cliente Groq

    mensaje = st.chat_input("Escribí tu mensaje:")  # Entrada de chat
    area_chat()  # Mostrar historial del chat

    if mensaje:  # Si hay un mensaje, procesarlo
        actualizar_historial("user", mensaje, "🧑‍💻")  # Guardar mensaje del usuario
        chat_completo = configurar_modelo(cliente, modelo, mensaje)  # Obtener respuesta del modelo

        if chat_completo:
            with st.chat_message("assistant", avatar="🤖"):
                # Mostrar respuesta del modelo en tiempo real
                respuesta_completa = st.empty()
                for respuesta in generar_respuesta(chat_completo):
                    respuesta_completa.markdown(respuesta)  # Mostrar contenido generado
                actualizar_historial("assistant", respuesta_completa, "🤖")  # Guardar respuesta del asistente

if __name__ == "__main__":
    main()
    

    
    
    
    
    
    
    
    
    
  
   