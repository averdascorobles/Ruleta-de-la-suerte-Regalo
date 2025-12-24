import streamlit as st
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="¡Sorpresa para Mamá y Tata!",
    page_icon="🎁",
    layout="centered"
)

# --- ESTILOS CSS PERSONALIZADOS ---
# Esto hace que las letras se vean bonitas, como en el panel de la tele
st.markdown("""
    <style>
    .letter-box {
        display: inline-block;
        width: 40px;
        height: 50px;
        margin: 5px;
        background-color: #ffffff;
        color: #000000;
        text-align: center;
        font-size: 24px;
        line-height: 50px;
        font-weight: bold;
        border-radius: 5px;
        border: 2px solid #333;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .space-box {
        display: inline-block;
        width: 20px;
        height: 50px;
        margin: 5px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DEL JUEGO ---
# ¡AQUÍ PUEDES CAMBIAR LA FRASE! (Usa mayúsculas)
SECRET_PHRASE = "NOS VAMOS AL CAMINITO DEL REY"
HINT = "Es una aventura en las alturas... cerca de Málaga."

# Inicializar variables de estado (memoria del juego)
if 'guessed_letters' not in st.session_state:
    st.session_state.guessed_letters = set()
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# --- FUNCIONES ---
def display_word(phrase, guessed):
    html_content = "<div>"
    for char in phrase:
        if char == " ":
            html_content += '<div class="space-box"></div>'
        elif char in guessed:
            html_content += f'<div class="letter-box" style="background-color: #4CAF50; color: white;">{char}</div>'
        else:
            html_content += '<div class="letter-box">_</div>'
    html_content += "</div>"
    return html_content

def check_win(phrase, guessed):
    # Quitamos los espacios para comprobar
    phrase_no_spaces = phrase.replace(" ", "")
    return all(char in guessed for char in phrase_no_spaces)

# --- INTERFAZ PRINCIPAL ---

st.title("🎉 ¡El Juego del Regalo Misterioso! 🎉")
st.write("Hola **Mamá y Tata**. Para descubrir vuestro regalo, tenéis que adivinar la frase oculta panel a panel.")

# Mostrar el panel
st.markdown("### El Panel:")
st.markdown(display_word(SECRET_PHRASE, st.session_state.guessed_letters), unsafe_allow_html=True)
st.write("") # Espacio

# Mostrar pista si quieren
with st.expander("¿Necesitáis una pista?"):
    st.info(HINT)

# --- TECLADO PARA JUGAR ---
if not st.session_state.game_over:
    st.write("Selecciona una letra:")
    
    # Alfabeto español
    alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    
    # Crear columnas para los botones (7 columnas)
    cols = st.columns(7)
    
    for index, letter in enumerate(alphabet):
        # Deshabilitar botón si ya se ha usado
        disabled = letter in st.session_state.guessed_letters
        
        if cols[index % 7].button(letter, key=letter, disabled=disabled):
            st.session_state.guessed_letters.add(letter)
            st.rerun()

    # Botón para resolver (arriesgarse)
    st.write("---")
    guess_phrase = st.text_input("¿Ya sabéis lo que es? Escribidlo aquí (opcional):").upper()
    if guess_phrase:
        if guess_phrase == SECRET_PHRASE:
            # Añadir todas las letras para mostrar el panel completo
            for char in SECRET_PHRASE:
                if char != " ":
                    st.session_state.guessed_letters.add(char)
            st.rerun()
        else:
            st.error("¡Casi! Pero esa no es la frase exacta.")

# --- LÓGICA DE VICTORIA ---
if check_win(SECRET_PHRASE, st.session_state.guessed_letters):
    st.session_state.game_over = True
    
    st.markdown("---")
    st.balloons() # Lanza globos
    time.sleep(1)
    st.title("🎊 ¡FELICIDADES! 🎊")
    st.success(f"¡El regalo es: **{SECRET_PHRASE}**!")
    
    # Imagen del lugar (Url pública de Wikimedia)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Caminito_del_Rey.jpg/800px-Caminito_del_Rey.jpg", 
             caption="Preparaos para las alturas y las vistas increíbles.")
    
    st.write("📅 **Fecha:** (Diles la fecha aquí o en persona)")
    st.write("🎒 **Preparad:** Ropa cómoda y muchas ganas.")
    
    if st.button("Jugar otra vez"):
        st.session_state.guessed_letters = set()
        st.session_state.game_over = False
        st.rerun()
